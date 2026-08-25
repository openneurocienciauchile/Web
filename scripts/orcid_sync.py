#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sincronizador de publicaciones ORCID -> data/publicaciones_orcid.json
Departamento de Neurociencia -- Facultad de Medicina, Universidad de Chile.

Adaptado de la implementacion en produccion de ~/Git_Web/Neurosistemas
(scripts/orcid_sync.py). Mismo diseno defensivo: si ORCID o Crossref
fallan, conserva el JSON anterior y termina con codigo 0.

Diferencia principal con el modelo de Neurosistemas: alla "quienes son"
vive en data/orcid.yaml; aca vive en el front-matter de cada
content/academicos/<slug>/index.md (campo `orcid`, el mismo que edita
Pages CMS) -- asi no hay una segunda fuente de verdad que se pueda
desincronizar. El campo puede venir como URL completa
("https://orcid.org/0000-...") o como id pelado: este script acepta
ambos formatos sin necesidad de tocar las fichas.

Uso local:
    pip install requests PyYAML
    python scripts/orcid_sync.py
"""

from __future__ import annotations

import datetime as dt
import glob
import json
import os
import re
import sys
import time
import unicodedata

try:
    import requests
    import yaml
except ImportError:  # pragma: no cover
    print("Faltan dependencias. Instala con:  pip install requests PyYAML")
    sys.exit(1)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACADEMICOS_GLOB = os.path.join(RAIZ, "content", "academicos", "*", "*.md")
OPCIONES = os.path.join(RAIZ, "data", "orcid_opciones.yaml")
SALIDA = os.path.join(RAIZ, "data", "publicaciones_orcid.json")

ORCID_API = "https://pub.orcid.org/v3.0"
CROSSREF_API = "https://api.crossref.org/works"
PAUSA = 0.12  # segundos entre llamadas, para ser buenos ciudadanos

RE_ORCID = re.compile(r"(\d{4}-\d{4}-\d{4}-\d{3}[\dX])")
RUIDO_APELLIDO = {"de", "del", "la", "las", "los", "y", "san", "santa"}


# ---------------------------------------------------------------- utilidades
def normalizar(texto: str) -> str:
    """Minusculas, sin tildes y sin puntuacion: para comparar titulos."""
    if not texto:
        return ""
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = re.sub(r"[^a-z0-9]+", " ", texto.lower())
    return texto.strip()


def limpiar_doi(doi: str) -> str:
    """Deja solo el identificador: 10.xxxx/yyyy."""
    if not doi:
        return ""
    doi = doi.strip().lower()
    doi = re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", doi)
    doi = re.sub(r"^doi:\s*", "", doi)
    return doi.strip().rstrip(".")


def escapar(texto: str) -> str:
    return (texto or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def leer_yaml(ruta: str, por_defecto):
    try:
        with open(ruta, encoding="utf-8") as fh:
            return yaml.safe_load(fh) or por_defecto
    except FileNotFoundError:
        return por_defecto


def sesion_http(correo: str) -> "requests.Session":
    s = requests.Session()
    s.headers.update({
        "Accept": "application/json",
        "User-Agent": f"depto-neurociencia-web/1.0 (https://deptoneuro.med.uchile.cl; mailto:{correo})",
    })
    return s


def pedir(s, url: str, intentos: int = 3, espera: float = 2.0):
    """GET con reintentos. Devuelve dict o None."""
    for n in range(intentos):
        try:
            r = s.get(url, timeout=25)
            if r.status_code == 404:
                return None
            if r.status_code == 429:
                time.sleep(espera * (n + 2))
                continue
            r.raise_for_status()
            return r.json()
        except Exception as e:  # noqa: BLE001
            if n == intentos - 1:
                print(f"   ! no se pudo leer {url}  ({e})")
                return None
            time.sleep(espera * (n + 1))
    return None


# --------------------------------------------------------- fichas academicas
def apellidos_de(nombre: str) -> list[str]:
    """Heuristica: las dos ultimas palabras significativas del nombre.

    Solo se usa para resaltar en negrita al autor del Departamento dentro
    de la lista de autores de cada publicacion (cosmetico). La atribucion
    real de que publicacion es de quien va por ORCID iD, no por este
    nombre.
    """
    partes = [p for p in re.split(r"\s+", nombre.strip()) if p]
    significativas = [p for p in partes if normalizar(p) not in RUIDO_APELLIDO]
    return significativas[-2:] if len(significativas) >= 2 else significativas


def _leer_frontmatter(ruta: str):
    try:
        texto = open(ruta, encoding="utf-8").read()
    except OSError:
        return None
    if not texto.startswith("---"):
        return None
    partes = texto.split("---", 2)
    if len(partes) < 3:
        return None
    try:
        return yaml.safe_load(partes[1]) or {}
    except yaml.YAMLError as e:
        print(f"   ! front-matter invalido en {ruta}: {e}")
        return None


def leer_academicos() -> list[dict]:
    """[{slug, nombre, orcid, apellidos}] de content/academicos/*/index.md.

    Acepta tanto "<slug>/index.md" (la mayoria) como las dos excepciones
    "<slug>/<SLUG>.md" (HB, JS) -- ver CLAUDE.md del repo.
    """
    academicos = []
    for ruta in sorted(glob.glob(ACADEMICOS_GLOB)):
        nombre_archivo = os.path.basename(ruta)
        slug = os.path.basename(os.path.dirname(ruta))
        if nombre_archivo == "_index.md":
            continue
        if not (nombre_archivo == "index.md" or nombre_archivo.lower() == f"{slug.lower()}.md"):
            continue
        cab = _leer_frontmatter(ruta)
        if cab is None or cab.get("draft"):
            continue
        titulo = str(cab.get("title") or "").strip()
        if not titulo:
            continue
        orcid_crudo = str(cab.get("orcid") or "")
        m = RE_ORCID.search(orcid_crudo)
        orcid = m.group(1) if m else ""
        academicos.append({
            "slug": slug,
            "nombre": titulo,
            "orcid": orcid,
            "apellidos": apellidos_de(titulo),
        })
    return academicos


def titulos_curados() -> set[str]:
    """Titulos (normalizados) de las publicaciones curadas a mano por CMS
    (campo `publicaciones` en cada ficha), para no traer de ORCID lo que ya
    esta seleccionado. Si el CMS aplano la lista a texto plano no hay forma
    fiable de extraer el titulo: esas entradas quedan fuera del dedup (en
    el peor caso, una publicacion aparece dos veces -- no rompe nada).
    """
    titulos = set()
    for ruta in sorted(glob.glob(ACADEMICOS_GLOB)):
        if os.path.basename(ruta) == "_index.md":
            continue
        cab = _leer_frontmatter(ruta)
        if cab is None:
            continue
        pubs = cab.get("publicaciones")
        if isinstance(pubs, list):
            for p in pubs:
                if isinstance(p, dict) and p.get("titulo"):
                    titulos.add(normalizar(str(p["titulo"]))[:90])
    return titulos


# ------------------------------------------------------------------- ORCID
def trabajos_de(s, orcid: str) -> list[dict]:
    """Resumenes de trabajos publicos de un perfil ORCID."""
    datos = pedir(s, f"{ORCID_API}/{orcid}/works")
    if not datos:
        return []
    salida = []
    for grupo in datos.get("group", []):
        resumenes = grupo.get("work-summary") or []
        if not resumenes:
            continue
        w = resumenes[0]

        titulo = (((w.get("title") or {}).get("title") or {}).get("value") or "").strip()
        if not titulo:
            continue

        revista = ((w.get("journal-title") or {}) or {}).get("value") or ""
        tipo = (w.get("type") or "").lower()

        anio = None
        fecha = w.get("publication-date") or {}
        if fecha and fecha.get("year"):
            try:
                anio = int(fecha["year"]["value"])
            except (KeyError, TypeError, ValueError):
                anio = None

        doi = ""
        url = ""
        for eid in ((grupo.get("external-ids") or {}).get("external-id") or []):
            clase = (eid.get("external-id-type") or "").lower()
            valor = eid.get("external-id-value") or ""
            if clase == "doi" and not doi:
                doi = limpiar_doi(valor)
            elif clase in ("uri", "handle") and not url:
                url = valor
        if not url:
            url = ((w.get("url") or {}) or {}).get("value") or ""

        salida.append({
            "titulo": titulo,
            "revista": revista.strip(),
            "anio": anio,
            "doi": doi,
            "url": url,
            "tipo": tipo,
        })
    return salida


# ---------------------------------------------------------------- Crossref
def enriquecer(s, doi: str):
    datos = pedir(s, f"{CROSSREF_API}/{doi}")
    if not datos:
        return None
    m = datos.get("message") or {}

    autores = []
    for a in (m.get("author") or [])[:22]:
        apellido = (a.get("family") or "").strip()
        nombre = (a.get("given") or "").strip()
        if not apellido:
            apellido = (a.get("name") or "").strip()
        if not apellido:
            continue
        iniciales = " ".join(p[0].upper() + "." for p in re.split(r"[\s\-]+", nombre) if p)
        autores.append(f"{apellido}, {iniciales}".strip().rstrip(","))
    if len(m.get("author") or []) > 22:
        autores.append("et al.")

    contenedor = (m.get("container-title") or [""])[0]
    volumen = m.get("volume") or ""
    paginas = m.get("page") or ""
    revista = contenedor
    if volumen:
        revista = f"{revista}, {volumen}"
    if paginas:
        revista = f"{revista}, {paginas}"

    anio = None
    for clave in ("published-print", "published-online", "issued", "created"):
        partes = ((m.get(clave) or {}).get("date-parts") or [[None]])[0]
        if partes and partes[0]:
            anio = int(partes[0])
            break

    return {
        "autores": autores,
        "revista": revista.strip(", "),
        "anio": anio,
        "titulo": (m.get("title") or [""])[0],
    }


def resaltar(autores: list[str], apellidos_dept: set[str]) -> str:
    """Pone en negrita a los autores que pertenecen al Departamento."""
    if not autores:
        return ""
    partes = []
    for a in autores:
        apellido = normalizar(a.split(",")[0])
        if apellido and apellido in apellidos_dept:
            partes.append(f"<b>{escapar(a)}</b>")
        else:
            partes.append(escapar(a))
    if len(partes) > 1:
        return ", ".join(partes[:-1]) + " &amp; " + partes[-1]
    return partes[0]


# --------------------------------------------------------------------- main
def main() -> int:
    op = leer_yaml(OPCIONES, {}) or {}
    anio_minimo = int(op.get("anio_minimo") or 0)
    usar_crossref = bool(op.get("usar_crossref", True))
    correo = op.get("correo_contacto") or "webmaster@deptoneuro.med.uchile.cl"
    tipos_ok = {t.lower() for t in (op.get("tipos_aceptados") or [])}

    academicos = leer_academicos()
    con_id = [a for a in academicos if a["orcid"]]
    if not con_id:
        print("Ningun academico tiene ORCID id detectable en su ficha.")
        print("El sitio seguira mostrando solo lo curado a mano por CMS.")
        return 0

    apellidos_dept = set()
    for a in academicos:
        for ap in a["apellidos"]:
            apellidos_dept.add(normalizar(ap))

    titulos_hist = titulos_curados()

    s = sesion_http(correo)
    por_doi: dict = {}
    por_titulo: dict = {}
    fuentes = []

    for a in con_id:
        print(f"-> {a['nombre']}  ({a['orcid']})")
        trabajos = trabajos_de(s, a["orcid"])
        print(f"   {len(trabajos)} trabajos publicos")
        fuentes.append({"nombre": a["nombre"], "orcid": a["orcid"], "trabajos": len(trabajos)})
        time.sleep(PAUSA)

        for t in trabajos:
            if tipos_ok and t["tipo"] and t["tipo"] not in tipos_ok:
                continue
            if t["anio"] and anio_minimo and t["anio"] < anio_minimo:
                continue

            clave_t = normalizar(t["titulo"])
            if any(clave_t and clave_t[:60] in h for h in titulos_hist):
                continue

            doi = t["doi"]
            destino = por_doi if doi else por_titulo
            clave = doi or clave_t
            if not clave:
                continue
            if clave in destino:
                destino[clave].setdefault("miembros", [])
                if a["nombre"] not in destino[clave]["miembros"]:
                    destino[clave]["miembros"].append(a["nombre"])
                continue
            t = dict(t)
            t["miembros"] = [a["nombre"]]
            destino[clave] = t

    entradas = list(por_doi.values()) + list(por_titulo.values())

    # Segunda pasada por titulo: mismo trabajo puede entrar dos veces si el
    # preprint y la version publicada tienen DOI distinto. Se conserva la
    # entrada del anio mas reciente y se juntan los miembros de ambas.
    unicas: dict = {}
    sin_titulo = []
    for e in entradas:
        clave = normalizar(e.get("titulo", ""))[:80]
        if not clave:
            sin_titulo.append(e)
            continue
        previa = unicas.get(clave)
        if previa is None:
            unicas[clave] = e
            continue
        nueva, vieja = ((e, previa) if (e.get("anio") or 0) > (previa.get("anio") or 0)
                        else (previa, e))
        miembros = list(nueva.get("miembros") or [])
        for m in vieja.get("miembros") or []:
            if m not in miembros:
                miembros.append(m)
        nueva = dict(nueva)
        nueva["miembros"] = miembros
        unicas[clave] = nueva
        print(f"   . fusionadas dos versiones de: {nueva['titulo'][:60]}...")

    entradas = list(unicas.values()) + sin_titulo
    print(f"\n{len(entradas)} publicaciones unicas tras deduplicar.")

    if usar_crossref:
        for i, e in enumerate(entradas, 1):
            if not e.get("doi"):
                continue
            extra = enriquecer(s, e["doi"])
            time.sleep(PAUSA)
            if not extra:
                continue
            if extra.get("revista"):
                e["revista"] = extra["revista"]
            if extra.get("anio") and not e.get("anio"):
                e["anio"] = extra["anio"]
            if extra.get("titulo"):
                e["titulo"] = extra["titulo"]
            e["autores"] = resaltar(extra.get("autores") or [], apellidos_dept)
            if i % 20 == 0:
                print(f"   Crossref: {i}/{len(entradas)}")

    salida = []
    for e in entradas:
        if not e.get("anio"):
            continue
        salida.append({
            "anio": int(e["anio"]),
            "titulo": e.get("titulo", "").strip(),
            "autores": e.get("autores", ""),
            "revista": e.get("revista", ""),
            "doi": e.get("doi", ""),
            "url": e.get("url", "") if not e.get("doi") else "",
            "tipo": e.get("tipo", ""),
            "miembros": e.get("miembros", []),
            "fuente": "orcid",
        })
    salida.sort(key=lambda x: (-x["anio"], normalizar(x["titulo"])))

    if not salida:
        print("ORCID no devolvio publicaciones nuevas. Se conserva el JSON anterior.")
        return 0

    documento = {
        "actualizado": dt.date.today().isoformat(),
        "fuentes": fuentes,
        "publicaciones": salida,
    }
    with open(SALIDA, "w", encoding="utf-8") as fh:
        json.dump(documento, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"Escrito {os.path.relpath(SALIDA, RAIZ)} con {len(salida)} publicaciones.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as err:  # noqa: BLE001
        print(f"Error inesperado: {err}")
        print("Se conserva data/publicaciones_orcid.json sin cambios.")
        sys.exit(0)
