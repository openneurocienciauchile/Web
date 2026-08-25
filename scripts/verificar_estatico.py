#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verificacion estatica del repo, sin compilar Hugo.

No reemplaza `HUGO_ENVIRONMENT=production hugo --minify` (eso lo corre
Claude Code, que si tiene Hugo/npm/go) -- atrapa antes los errores mas
comunes y baratos de revisar: YAML/JSON invalido, front-matter sin
titulo, partials que no existen, bloques {{ if/with/range/block/define }}
sin su {{ end }}, entradas de menu sin contenido, y site.Data/hugo.Data
usado sin su archivo en data/.

Uso:
    pip install PyYAML
    python scripts/verificar_estatico.py
"""
import json
import re
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
errores = []
avisos = []


def error(msg):
    errores.append(msg)
    print(f"  X   {msg}")


def aviso(msg):
    avisos.append(msg)
    print(f"  .   {msg}")


def ok(msg):
    print(f"  OK  {msg}")


IGNORAR = {"node_modules", ".git", "public", ".venv"}


def ignorar(ruta):
    return any(p in IGNORAR for p in ruta.parts)


# 1) YAML / JSON validos --------------------------------------------------
print("\n[1] Sintaxis YAML/JSON")
n = 0
for patron in ("**/*.yaml", "**/*.yml"):
    for ruta in RAIZ.glob(patron):
        if ignorar(ruta):
            continue
        n += 1
        try:
            list(yaml.safe_load_all(ruta.read_text(encoding="utf-8")))
        except yaml.YAMLError as e:
            error(f"YAML invalido: {ruta.relative_to(RAIZ)} -- {e}")
for ruta in RAIZ.glob("data/**/*.json"):
    n += 1
    try:
        json.loads(ruta.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        error(f"JSON invalido: {ruta.relative_to(RAIZ)} -- {e}")
ok(f"{n} archivos YAML/JSON revisados")

# 2) Front-matter con titulo ----------------------------------------------
print("\n[2] Front-matter con \'title\'")
n = 0
for ruta in RAIZ.glob("content/**/*.md"):
    if ignorar(ruta):
        continue
    texto = ruta.read_text(encoding="utf-8", errors="replace")
    if not texto.startswith("---"):
        continue
    partes = texto.split("---", 2)
    if len(partes) < 3:
        continue
    n += 1
    try:
        cab = yaml.safe_load(partes[1]) or {}
    except yaml.YAMLError as e:
        error(f"Front-matter invalido: {ruta.relative_to(RAIZ)} -- {e}")
        continue
    if not str(cab.get("title") or "").strip():
        aviso(f"Sin \'title\': {ruta.relative_to(RAIZ)}")
ok(f"{n} paginas de contenido revisadas")

# 3) Balance de acciones de bloque en plantillas ---------------------------
print("\n[3] Balance de {{ if/with/range/block/define }} vs {{ end }}")
ABREN = re.compile(r"\{\{-?\s*(if|with|range|block|define)\b")
CIERRAN = re.compile(r"\{\{-?\s*end\s*-?\}\}")
n = 0
for ruta in RAIZ.glob("layouts/**/*.html"):
    if ignorar(ruta):
        continue
    n += 1
    texto = ruta.read_text(encoding="utf-8", errors="replace")
    abren = len(ABREN.findall(texto))
    cierran = len(CIERRAN.findall(texto))
    if abren != cierran:
        error(f"Desbalance en {ruta.relative_to(RAIZ)}: {abren} aperturas vs {cierran} \'end\'")
ok(f"{n} plantillas revisadas")

# 4) partials referenciados existen ----------------------------------------
print("\n[4] partials referenciados")
RE_PARTIAL = re.compile(r'partial(?:Cached)?\s+"([^"]+)"')
candidatos_dir = [RAIZ / "layouts" / "_partials", RAIZ / "layouts" / "partials"]
n = 0
for ruta in RAIZ.glob("layouts/**/*.html"):
    if ignorar(ruta):
        continue
    texto = ruta.read_text(encoding="utf-8", errors="replace")
    for nombre in RE_PARTIAL.findall(texto):
        n += 1
        if not any((d / nombre).exists() for d in candidatos_dir):
            error(f"{ruta.relative_to(RAIZ)} referencia partial inexistente: {nombre}")
ok(f"{n} referencias a partial revisadas")

# 5) Entradas de menu con contenido -----------------------------------------
print("\n[5] Entradas de menu con contenido")
menus_path = RAIZ / "config" / "_default" / "menus.yaml"
if menus_path.exists():
    menus = yaml.safe_load(menus_path.read_text(encoding="utf-8")) or {}
    for entrada in menus.get("main") or []:
        url = (entrada.get("url") or "").strip("/")
        if not url:
            continue
        candidatos = [RAIZ / "content" / url / "_index.md", RAIZ / "content" / f"{url}.md"]
        if not any(c.exists() for c in candidatos):
            nombre_menu = entrada.get("name")
            aviso(f"Menu '{nombre_menu}' apunta a '{url}/' sin _index.md/.md correspondiente")
    ok("menu revisado")
else:
    aviso("No se encontro config/_default/menus.yaml")

# 6) site.Data / hugo.Data usados tienen archivo en data/ -------------------
print("\n[6] site.Data / hugo.Data referenciados")
RE_DATA = re.compile(r"(?:site\.Data|hugo\.Data)\.([A-Za-z0-9_]+)")
n = 0
for ruta in RAIZ.glob("layouts/**/*.html"):
    if ignorar(ruta):
        continue
    texto = ruta.read_text(encoding="utf-8", errors="replace")
    for nombre in RE_DATA.findall(texto):
        n += 1
        candidatos = [RAIZ / "data" / f"{nombre}.yaml", RAIZ / "data" / f"{nombre}.yml",
                      RAIZ / "data" / f"{nombre}.json"]
        if not any(c.exists() for c in candidatos):
            error(f"{ruta.relative_to(RAIZ)} usa site.Data/hugo.Data.{nombre} sin data/{nombre}.*")
ok(f"{n} referencias a site.Data/hugo.Data revisadas")

# 7) Rutas absolutas literales en layouts (informativo, hay excepciones ----
#    documentadas en CLAUDE.md regla 6) --------------------------------------
print("\n[7] Rutas absolutas literales en layouts (informativo)")
RE_ABS = re.compile(r'(?:href|src)="(/(?!/)[^"]*)"')
n = 0
for ruta in RAIZ.glob("layouts/**/*.html"):
    if ignorar(ruta):
        continue
    texto = ruta.read_text(encoding="utf-8", errors="replace")
    for m in RE_ABS.finditer(texto):
        n += 1
        aviso(f"{ruta.relative_to(RAIZ)}: ruta absoluta literal {m.group(1)} (revisar si es de las excepciones de la regla 6 de CLAUDE.md)")
print(f"  ({n} halladas)")

print("\n" + "=" * 60)
print(f"RESULTADO: {len(errores)} errores, {len(avisos)} avisos")
sys.exit(1 if errores else 0)
