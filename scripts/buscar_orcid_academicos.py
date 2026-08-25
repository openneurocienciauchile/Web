#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Completa el ORCID iD de los academicos que no lo tienen y deja un
informe para revision humana de lo que no se pudo decidir solo.

Dos pasadas:
1. Cruza con ~/Git_Web/Neurosistemas/data/orcid.yaml (varias personas
   estan en ambos sitios) -- gratis, sin tocar la red.
2. Para quienes sigan sin id, busca en la API publica de ORCID acotando a
   afiliacion "Universidad de Chile". Autocompleta SOLO cuando la
   consulta acotada da un unico candidato inequivoco. Todo lo demas queda
   en INFORME-ORCID.md con sus candidatos, para que un humano confirme
   cual es.

Escribe el ORCID directamente en el front-matter de
content/academicos/<slug>/index.md (o HB/HB.md, JS/JS.md), preservando el
resto del archivo linea por linea -- no reescribe el YAML completo, para
no perder comentarios ni el orden de los campos.

Uso:
    pip install requests PyYAML
    python scripts/buscar_orcid_academicos.py               # aplica
    python scripts/buscar_orcid_academicos.py --simular      # solo informa
"""

import argparse
import re
import sys
import time
import unicodedata
from pathlib import Path

import requests
import yaml

RAIZ = Path(__file__).resolve().parent.parent
ACADEMICOS = RAIZ / "content" / "academicos"
INFORME = RAIZ / "INFORME-ORCID.md"
NEUROSISTEMAS_ORCID = Path.home() / "Git_Web" / "Neurosistemas" / "data" / "orcid.yaml"

API = "https://pub.orcid.org/v3.0/expanded-search/"
AFILIACION = "Universidad de Chile"
PAUSA = 0.4
FILAS = 20
RE_ORCID = re.compile(r"(\d{4}-\d{4}-\d{4}-\d{3}[\dX])")
RUIDO = {"dr", "dra", "drs", "prof", "profesor", "profesora", "sr", "sra",
         "ph", "phd", "md", "de", "del", "la", "las", "los", "y", "da", "do"}


def sin_acentos(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def tokens(nombre):
    return [p for p in sin_acentos(nombre).lower().split() if p and p not in RUIDO and len(p) > 1]


def coincide(a, b):
    """Misma persona: comparten nombre de pila y al menos un apellido."""
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb or ta[0] != tb[0]:
        return False
    apa = {t for t in ta[1:] if len(t) > 3}
    apb = {t for t in tb[1:] if len(t) > 3}
    return bool(apa & apb)


# ---------------------------------------------------- fichas de academicos
def fichas():
    """[(ruta, slug, nombre, orcid_actual)] de cada ficha con `title`."""
    salida = []
    rutas = sorted(ACADEMICOS.glob("*/index.md")) + sorted(ACADEMICOS.glob("*/[A-Z][A-Z].md"))
    for ruta in rutas:
        texto = ruta.read_text(encoding="utf-8", errors="replace")
        if not texto.startswith("---"):
            continue
        partes = texto.split("---", 2)
        if len(partes) < 3:
            continue
        try:
            cab = yaml.safe_load(partes[1]) or {}
        except yaml.YAMLError:
            continue
        titulo = str(cab.get("title") or "").strip()
        if not titulo:
            continue
        orcid_crudo = str(cab.get("orcid") or "")
        m = RE_ORCID.search(orcid_crudo)
        salida.append((ruta, ruta.parent.name, titulo, m.group(1) if m else ""))
    return salida


RE_CAMPO_ORCID = re.compile(r"^(\s*)orcid:\s*(.*?)\s*$")
RE_EMAIL = re.compile(r"^(\s*)email:")


def escribir_orcid(ruta: Path, orcid: str, simular: bool) -> bool:
    """Escribe el id en el campo `orcid` del front-matter, linea por linea.

    Mismo formato (URL completa) que las 22 fichas que ya lo traen, para
    no tener que tocar la plantilla que arma el boton ORCID del perfil.
    """
    lineas = ruta.read_text(encoding="utf-8").splitlines(keepends=True)
    marcas = [i for i, l in enumerate(lineas) if l.strip() == "---"]
    if len(marcas) < 2:
        return False
    inicio, fin = marcas[0], marcas[1]
    idx = None
    for i in range(inicio + 1, fin):
        if RE_CAMPO_ORCID.match(lineas[i]):
            idx = i
            break
    linea_nueva = f'orcid: "https://orcid.org/{orcid}"\n'
    if idx is not None:
        lineas[idx] = linea_nueva
    else:
        destino = fin
        for i in range(inicio + 1, fin):
            if RE_EMAIL.match(lineas[i]):
                destino = i + 1
                break
        lineas.insert(destino, linea_nueva)
    if not simular:
        ruta.write_text("".join(lineas), encoding="utf-8")
    return True


# --------------------------------------------------------------- ORCID API
def consultar(sesion, q):
    try:
        r = sesion.get(API, params={"q": q, "rows": FILAS}, timeout=25)
        r.raise_for_status()
        d = r.json()
    except (requests.RequestException, ValueError) as e:
        print(f"    ! error consultando ORCID: {e}")
        return None, []
    time.sleep(PAUSA)
    return d.get("num-found", 0), d.get("expanded-result") or []


def apellido_principal_calza(resultado, apellido):
    perfil = sin_acentos(resultado.get("family-names") or "").lower()
    buscado = sin_acentos(apellido).lower()
    pp = perfil.replace("-", " ").split()
    pb = buscado.replace("-", " ").split()
    return bool(pp and pb and pp[0] == pb[0])


def candidato(r):
    return {
        "orcid": r.get("orcid-id", ""),
        "nombre": " ".join(x for x in (r.get("given-names"), r.get("family-names")) if x),
        "instituciones": r.get("institution-name") or [],
    }


def variantes(texto):
    v = [texto]
    plano = sin_acentos(texto)
    if plano != texto:
        v.append(plano)
    return v


def buscar_persona(sesion, nombre):
    partes = nombre.split()
    pila = partes[0] if partes else nombre
    apellidos = partes[1:] if len(partes) > 1 else [nombre]
    pila_plano = sin_acentos(pila).lower()
    auto = None
    vistos, candidatos = set(), []

    def agregar(res, solo_chilenos=False, solo_misma_pila=False):
        for r in res:
            c = candidato(r)
            if c["orcid"] in vistos:
                continue
            if solo_chilenos and not any("chile" in i.lower() for i in c["instituciones"]):
                continue
            if solo_misma_pila:
                dado = sin_acentos(r.get("given-names") or "").lower()
                if not dado.startswith(pila_plano[:4]):
                    continue
            vistos.add(c["orcid"])
            candidatos.append(c)

    for apellido in apellidos:
        for ap in variantes(apellido):
            for pl in variantes(pila):
                q = f'family-name:{ap} AND given-names:{pl} AND affiliation-org-name:"{AFILIACION}"'
                n, res = consultar(sesion, q)
                if n == 1 and res and auto is None and apellido_principal_calza(res[0], ap):
                    auto = res[0].get("orcid-id")
                agregar(res)
            if auto:
                continue
            _, res2 = consultar(sesion, f'family-name:{ap} AND affiliation-org-name:"{AFILIACION}"')
            agregar(res2, solo_misma_pila=True)
            for pl in variantes(pila):
                n3, res3 = consultar(sesion, f"family-name:{ap} AND given-names:{pl}")
                agregar(res3, solo_chilenos=(n3 or 0) > 3)

    if not auto and not candidatos:
        for ap in variantes(apellidos[0] if apellidos else nombre):
            for pl in variantes(pila):
                _, res = consultar(sesion, f"family-name:{ap} AND given-names:{pl}")
                agregar(res[:5])
            if candidatos:
                break

    return auto, candidatos


MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


def escribir_informe(filas, autocompletados, cruzados, resueltos, total):
    t = time.localtime()
    hoy = f"{t.tm_mday} de {MESES[t.tm_mon - 1]} de {t.tm_year}"
    L = []
    L.append("# Informe de busqueda de ORCID iD -- academicos del Departamento\n")
    L.append(f"Generado por `scripts/buscar_orcid_academicos.py` el {hoy}.\n")
    L.append(
        "\nSe relleno solo lo inequivoco; el resto necesita que confirmes cual es el "
        "perfil correcto y lo apliques por Pages CMS (campo ORCID de la ficha) o pidas "
        "que Claude Code lo aplique.\n"
    )
    L.append(f"\n## Estado actual\n\n{len(resueltos)} de {total} "
              "academicos ya tienen su ORCID iD.\n")

    if cruzados:
        L.append("\n### Rellenados cruzando con Neurosistemas\n")
        L.append("\nMisma persona en ambos sitios; el iD ya estaba confirmado alla.\n\n")
        L.append("| Persona | ORCID iD |\n|---|---|\n")
        for nombre, orcid in cruzados:
            L.append(f"| {nombre} | [{orcid}](https://orcid.org/{orcid}) |\n")

    if autocompletados:
        L.append("\n### Rellenados desde la API de ORCID\n")
        L.append("\nUnico candidato con afiliacion en la Universidad de Chile.\n\n")
        L.append("| Persona | ORCID iD | Afiliaciones declaradas |\n|---|---|---|\n")
        for nombre, orcid, inst in autocompletados:
            L.append(f"| {nombre} | [{orcid}](https://orcid.org/{orcid}) | {inst} |\n")

    L.append("\n## Pendientes de confirmacion\n")
    pendientes = [f for f in filas if not f["auto"]]
    if not pendientes:
        L.append("\nNinguno: todos quedaron resueltos.\n")
    for f in pendientes:
        L.append(f"\n### {f['nombre']}\n\n")
        if not f["candidatos"]:
            L.append("Sin candidatos con afiliacion chilena en la API publica de ORCID. "
                      "Puede que no tenga perfil, este en privado o no declare afiliacion.\n")
            continue
        L.append("| Es? | ORCID iD | Nombre en ORCID | Afiliaciones declaradas |\n")
        L.append("|:---:|---|---|---|\n")
        for c in f["candidatos"]:
            inst = ", ".join(c["instituciones"]) or "--"
            L.append(f"|  | [{c['orcid']}](https://orcid.org/{c['orcid']}) | {c['nombre']} | {inst} |\n")

    INFORME.write_text("".join(L), encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--simular", action="store_true", help="no escribe en las fichas")
    args = ap.parse_args()

    todas = fichas()
    faltan = [(ruta, slug, nombre) for ruta, slug, nombre, orcid in todas if not orcid]
    print(f"Academicos: {len(todas)}. Sin ORCID iD: {len(faltan)}\n")

    cruzados = []
    if NEUROSISTEMAS_ORCID.exists():
        cfg = yaml.safe_load(NEUROSISTEMAS_ORCID.read_text(encoding="utf-8")) or {}
        miembros_ns = [(m.get("nombre", ""), (m.get("orcid") or "").strip())
                       for m in (cfg.get("miembros") or []) if (m.get("orcid") or "").strip()]
        restantes = []
        for ruta, slug, nombre in faltan:
            hallado = next((oid for nom_ns, oid in miembros_ns if coincide(nombre, nom_ns)), None)
            if hallado:
                print(f"  {nombre}: ya esta en Neurosistemas -> {hallado}")
                escribir_orcid(ruta, hallado, args.simular)
                cruzados.append((nombre, hallado))
            else:
                restantes.append((ruta, slug, nombre))
        faltan = restantes
    else:
        print("  (no se encontro Neurosistemas/data/orcid.yaml; se omite el cruce)")

    sesion = requests.Session()
    sesion.headers.update({"Accept": "application/json",
                            "User-Agent": "depto-neurociencia-web/1.0 (https://deptoneuro.med.uchile.cl)"})
    filas, autocompletados = [], []
    for ruta, slug, nombre in faltan:
        print(f"  buscando {nombre}...")
        auto, candidatos = buscar_persona(sesion, nombre)
        filas.append({"nombre": nombre, "auto": auto, "candidatos": candidatos})
        if auto:
            inst = next((", ".join(c["instituciones"]) for c in candidatos if c["orcid"] == auto), "")
            autocompletados.append((nombre, auto, inst))
            escribir_orcid(ruta, auto, args.simular)
            print(f"    -> {auto}")
        else:
            print(f"    -> sin decision automatica ({len(candidatos)} candidatos)")

    resueltos = [(nombre, orcid) for _, _, nombre, orcid in fichas() if orcid]
    escribir_informe(filas, autocompletados, cruzados, resueltos, len(todas))
    print(f"\nInforme escrito en {INFORME.name}")
    print(f"Cruzados con Neurosistemas: {len(cruzados)} . Autocompletados por API: "
          f"{len(autocompletados)} . Pendientes: {len(filas) - len(autocompletados)}")
    if args.simular:
        print("\n(simulacion: no se escribio en ninguna ficha)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
