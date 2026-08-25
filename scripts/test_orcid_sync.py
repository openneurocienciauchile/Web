# -*- coding: utf-8 -*-
"""Prueba de scripts/orcid_sync.py con respuestas simuladas.

No toca la red ni el contenido real de content/academicos/: reemplaza
leer_academicos() y titulos_curados() por datos ficticios, y escribe el
resultado en un archivo temporal (no en data/publicaciones_orcid.json).

Uso:  python scripts/test_orcid_sync.py
"""
import sys, os, json, tempfile
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, "scripts"))

import orcid_sync  # noqa: E402

# 1) Reemplazar la lectura de academicos por una ficcion de tres personas
ACADEMICOS_FICTICIOS = [
    {"slug": "persona-uno", "nombre": "Ana Uno", "orcid": "0000-0000-0000-0001",
     "apellidos": ["Uno"]},
    {"slug": "persona-dos", "nombre": "Beto Dos", "orcid": "0000-0000-0000-0002",
     "apellidos": ["Dos"]},
    {"slug": "persona-sin-id", "nombre": "Cata Tres", "orcid": "", "apellidos": ["Tres"]},
]
orcid_sync.leer_academicos = lambda: ACADEMICOS_FICTICIOS
orcid_sync.titulos_curados = lambda: {"un articulo ya curado a mano"}

WORKS = {
 "0000-0000-0000-0001": {"group": [
   {"external-ids": {"external-id": [{"external-id-type": "doi", "external-id-value": "https://doi.org/10.1038/S41598-025-99999-9"}]},
    "work-summary": [{"title": {"title": {"value": "Active vision in freely moving observers"}},
                      "journal-title": {"value": "Scientific Reports"},
                      "publication-date": {"year": {"value": "2025"}}, "type": "journal-article"}]},
   # duplicado (mismo DOI, distinta forma) -- debe colapsar con el de Beto
   {"external-ids": {"external-id": [{"external-id-type": "doi", "external-id-value": "10.1016/j.mex.2024.102500"}]},
    "work-summary": [{"title": {"title": {"value": "A shared methods paper"}},
                      "journal-title": {"value": "MethodsX"},
                      "publication-date": {"year": {"value": "2024"}}, "type": "journal-article"}]},
   # ya esta curado a mano en una ficha -> debe descartarse
   {"external-ids": {"external-id": []},
    "work-summary": [{"title": {"title": {"value": "Un articulo ya curado a mano"}},
                      "publication-date": {"year": {"value": "2022"}}, "type": "journal-article"}]},
   # tipo no aceptado -> descartar
   {"external-ids": {"external-id": []},
    "work-summary": [{"title": {"title": {"value": "Una charla"}}, "publication-date": {"year": {"value": "2025"}},
                      "type": "lecture-speech"}]},
   # sin DOI pero valido -> se conserva por titulo
   {"external-ids": {"external-id": []},
    "work-summary": [{"title": {"title": {"value": "Un capitulo sin DOI"}},
                      "journal-title": {"value": "Editorial X"},
                      "publication-date": {"year": {"value": "2025"}}, "type": "book-chapter"}]},
 ]},
 "0000-0000-0000-0002": {"group": [
   {"external-ids": {"external-id": [{"external-id-type": "doi", "external-id-value": "10.1016/J.MEX.2024.102500"}]},
    "work-summary": [{"title": {"title": {"value": "A shared methods paper"}},
                      "journal-title": {"value": "MethodsX"},
                      "publication-date": {"year": {"value": "2024"}}, "type": "journal-article"}]},
 ]},
}
CROSSREF = {
 "10.1038/s41598-025-99999-9": {"message": {
   "author": [{"family": "Dos", "given": "Beto"}, {"family": "Perez", "given": "Ana Maria"},
              {"family": "Uno", "given": "Ana"}],
   "container-title": ["Scientific Reports"], "volume": "15", "page": "1234",
   "issued": {"date-parts": [[2025, 4, 2]]}, "title": ["Active vision in freely moving observers"]}},
 "10.1016/j.mex.2024.102500": {"message": {
   "author": [{"family": "Madariaga", "given": "Samuel"}, {"family": "Babul", "given": "Cecilia"}],
   "container-title": ["MethodsX"], "volume": "12", "page": "102500",
   "issued": {"date-parts": [[2024]]}, "title": ["A shared methods paper"]}},
}

def pedir_falso(s, url, intentos=3, espera=2.0):
    if url.startswith(orcid_sync.ORCID_API):
        return WORKS.get(url.split("/")[-2])
    if url.startswith(orcid_sync.CROSSREF_API):
        return CROSSREF.get(url.split("works/")[-1])
    return None

orcid_sync.pedir = pedir_falso
orcid_sync.PAUSA = 0

salida_tmp = os.path.join(tempfile.gettempdir(), f"orcid_sync_test_{os.getpid()}.json")
orcid_sync.SALIDA = salida_tmp  # fuera del repo: no hay nada que limpiar de vuelta ahi

rc = orcid_sync.main()

print("\n--- JSON generado ---")
doc = json.load(open(salida_tmp, encoding="utf-8"))
print(json.dumps(doc, ensure_ascii=False, indent=2)[:2200])

pubs = doc["publicaciones"]
ok = True
def chk(cond, msg):
    global ok
    print(("  OK  " if cond else "  X   ") + msg); ok = ok and cond

print("\n--- Aserciones ---")
chk(len(pubs) == 3, f"3 publicaciones tras filtrar y deduplicar (obtuve {len(pubs)})")
chk(not any("curado a mano" in p["titulo"].lower() for p in pubs), "descarta lo ya curado a mano en las fichas")
chk(not any("charla" in p["titulo"].lower() for p in pubs), "descarta tipos no aceptados")
compartida = [p for p in pubs if "shared" in p["titulo"].lower()]
chk(len(compartida) == 1, "el DOI compartido aparece una sola vez")
chk(len(compartida[0]["miembros"]) == 2, f"acredita a los 2 academicos ({compartida[0]['miembros']})")
sr = [p for p in pubs if "Active vision" in p["titulo"]][0]
chk("<b>Dos, B.</b>" in sr["autores"] and "<b>Uno, A.</b>" in sr["autores"],
    "resalta en negrita a los academicos del Departamento")
chk("Perez, A. M." in sr["autores"] and "<b>Perez" not in sr["autores"], "no resalta a autores externos")
chk(sr["revista"] == "Scientific Reports, 15, 1234", f"revista con volumen y paginas: {sr['revista']}")
chk(sr["doi"] == "10.1038/s41598-025-99999-9", "DOI normalizado a minusculas y sin prefijo URL")
chk(pubs[0]["anio"] >= pubs[-1]["anio"], "ordenado por ano descendente")
chk(doc["actualizado"] != "", "registra la fecha de actualizacion")

print("\n--- Resiliencia (ORCID caido) ---")
antes = open(salida_tmp, encoding="utf-8").read()
orcid_sync.pedir = lambda *a, **k: None
orcid_sync.main()
despues = open(salida_tmp, encoding="utf-8").read()
chk(antes == despues, "con ORCID caido no borra el JSON existente")

print("\n--- Sin academicos con ORCID ---")
orcid_sync.leer_academicos = lambda: [a for a in ACADEMICOS_FICTICIOS if not a["orcid"]]
rc2 = orcid_sync.main()
chk(rc2 == 0, "sale en 0 cuando nadie tiene ORCID id")

try:
    os.remove(salida_tmp)
except OSError:
    pass
print("\nRESULTADO:", "TODO OK" if ok else "HAY FALLAS")
sys.exit(0 if ok else 1)
