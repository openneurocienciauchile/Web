#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Boletín de noticias → correo a los suscriptores (Brevo)
Departamento de Neurociencia — Facultad de Medicina, Universidad de Chile.

Qué hace
--------
1. Lee data/boletin.yaml (remitente, lista, textos) y config/_default/hugo.yaml
   (baseURL).
2. Recorre content/blog/*/index.md (y content/blog/*.md): descarta borradores, las noticias con
   `boletin: false` y las anteriores a `enviar_desde`.
3. Pregunta a Brevo qué campañas existen. Cada noticia enviada deja una
   campaña llamada `noticia:<slug>`: si ya existe, no se vuelve a mandar.
   Así el script es idempotente y no necesita guardar estado en el repo.
4. Para cada noticia pendiente: comprueba que su URL ya responda 200 (el
   workflow corre después del despliegue, pero el CDN puede tardar), arma el
   correo (título, fecha, resumen, imagen de portada, botón al enlace), crea
   la campaña y la envía a la lista.

La lista de suscriptores vive en Brevo, nunca en el repo (que es público).
La clave de la API llega por la variable de entorno BREVO_API_KEY.

Uso
---
    python scripts/boletin.py enviar                 # lo que hace el workflow
    python scripts/boletin.py enviar --simular       # muestra, no manda nada
    python scripts/boletin.py enviar --slug Neurofest-2026
    python scripts/boletin.py enviar --slug ... --reenviar   # aunque ya exista
    python scripts/boletin.py prueba --correo tu@correo.cl [--slug ...]
    python scripts/boletin.py vista-previa [--slug ...] [--salida x.html]
    python scripts/boletin.py importar contactos.csv [--simular]
    python scripts/boletin.py enviados               # campañas ya mandadas

Códigos de salida: 0 si no había nada que hacer o faltaba configuración
(no marca el workflow en rojo por eso); 1 si Brevo rechazó un envío.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import html
import os
import re
import sys
import time
import unicodedata
from urllib.parse import quote

try:
    import requests
    import yaml
except ImportError:  # pragma: no cover
    print("Faltan dependencias. Instala con:  pip install requests PyYAML")
    sys.exit(1)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = os.path.join(RAIZ, "data", "boletin.yaml")
HUGO_CFG = os.path.join(RAIZ, "config", "_default", "hugo.yaml")
NOTICIAS = os.path.join(RAIZ, "content", "blog")

BREVO = "https://api.brevo.com/v3"
PREFIJO_CAMPANA = "noticia:"
ETIQUETA = "boletin-noticias"

# Paleta del sitio (ver custom.html). El correo no puede leer el CSS, va fijo.
NAVY = "#0A1533"
AZUL = "#1C4599"
CIAN = "#16C8E6"
TEXTO = "#0C1530"
MUTED = "#5C6781"
LINEA = "#E3E8F2"
MIST = "#F4F7FC"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]


# ---------------------------------------------------------------- utilidades
def log(msg: str) -> None:
    print(msg, flush=True)


def leer_yaml(ruta: str) -> dict:
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def a_fecha(valor) -> dt.date | None:
    """Acepta date, datetime o texto ISO (con o sin hora)."""
    if valor is None or valor == "":
        return None
    if isinstance(valor, dt.datetime):
        return valor.date()
    if isinstance(valor, dt.date):
        return valor
    texto = str(valor).strip()
    try:
        return dt.datetime.fromisoformat(texto.replace("Z", "+00:00")).date()
    except ValueError:
        pass
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", texto)
    if m:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


def fecha_larga(fecha: dt.date | None) -> str:
    if not fecha:
        return ""
    return f"{fecha.day} de {MESES[fecha.month - 1]} de {fecha.year}"


def urlizar(texto: str) -> str:
    """Aproxima el `urlize` de Hugo con removePathAccents: minúsculas, sin
    tildes, espacios → guiones."""
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = texto.strip().lower()
    texto = re.sub(r"\s+", "-", texto)
    return texto


def limpiar_markdown(cuerpo: str) -> str:
    """Primer párrafo del cuerpo, sin marcas: por si la noticia no trae resumen."""
    parrafos = [p.strip() for p in re.split(r"\n\s*\n", cuerpo) if p.strip()]
    parrafos = [p for p in parrafos if not p.startswith("#")]
    if not parrafos:
        return ""
    p = parrafos[0]
    p = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", p)           # imágenes
    p = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", p)        # enlaces → texto
    p = re.sub(r"[*_`>]+", "", p)                          # énfasis, citas
    p = re.sub(r"\s+", " ", p).strip()
    if len(p) > 260:
        p = p[:257].rsplit(" ", 1)[0] + "…"
    return p


def dividir_front_matter(texto: str) -> tuple[dict, str]:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", texto, re.S)
    if not m:
        return {}, texto
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        log(f"  ! front-matter ilegible: {e}")
        fm = {}
    return fm, m.group(2)


# ---------------------------------------------------------------- noticias
class Noticia:
    """Una entrada de content/blog: carpeta con index.md (Pages CMS / Hugo Blox)
    o archivo suelto .md. El slug es el nombre de la carpeta o del archivo."""

    def __init__(self, ruta: str, slug: str, base_url: str):
        self.ruta = ruta
        self.slug = slug
        with open(ruta, encoding="utf-8") as f:
            fm, cuerpo = dividir_front_matter(f.read())
        self.fm = fm
        self.titulo = " ".join(str(fm.get("title") or slug).split())
        self.subtitulo = " ".join(str(fm.get("subtitle") or "").split())
        self.fecha = a_fecha(fm.get("date"))
        self.borrador = bool(fm.get("draft", False))
        # `boletin: false` en el front-matter saca la noticia del correo.
        self.boletin = fm.get("boletin", True) is not False
        resumen = fm.get("summary") or fm.get("resumen") or ""
        self.resumen = " ".join(str(resumen).split()) or limpiar_markdown(cuerpo)
        self.imagen = self._imagen(fm.get("image"), base_url)
        # URL: igual que Hugo. `url` manda; si no, `slug`; si no, la carpeta.
        if fm.get("url"):
            ruta_url = str(fm["url"]).strip("/") + "/"
        else:
            ruta_url = "blog/" + urlizar(str(fm.get("slug") or slug)) + "/"
        self.url = base_url + ruta_url

    def _imagen(self, valor, base_url: str) -> str:
        """`image` puede ser un texto (/uploads/foto.jpg, Pages CMS) o un mapa
        (Hugo Blox: featured.* dentro de la carpeta). Devuelve URL absoluta."""
        if not valor:
            return ""
        if isinstance(valor, dict):
            carpeta = os.path.dirname(self.ruta)
            for nombre in sorted(os.listdir(carpeta)):
                if nombre.lower().startswith("featured."):
                    return base_url + "blog/" + urlizar(self.slug) + "/" + nombre
            return ""
        texto = str(valor).strip()
        if re.match(r"^https?://", texto):
            return texto
        # Espacios y tildes en el nombre del archivo → codificados para el correo.
        return base_url + quote(texto.lstrip("/"), safe="/")

    @property
    def nombre_campana(self) -> str:
        return PREFIJO_CAMPANA + self.slug


def cargar_noticias(base_url: str) -> list[Noticia]:
    out = []
    if not os.path.isdir(NOTICIAS):
        return out
    for nombre in sorted(os.listdir(NOTICIAS)):
        if nombre.startswith("_") or nombre.startswith("."):
            continue
        ruta = os.path.join(NOTICIAS, nombre)
        if os.path.isdir(ruta):
            indice = os.path.join(ruta, "index.md")
            if os.path.exists(indice):
                out.append(Noticia(indice, nombre, base_url))
        elif nombre.endswith(".md"):
            out.append(Noticia(ruta, nombre[:-3], base_url))
    out.sort(key=lambda n: (n.fecha or dt.date.min, n.slug))
    return out


# ---------------------------------------------------------------- correo
def armar_html(n: Noticia, cfg: dict, base_url: str, para_prueba: bool = False) -> str:
    """Correo en tablas con estilos en línea (lo único que entienden todos
    los clientes). Estética del sitio: cabecera navy, acento cian, Sora/IBM
    Plex Sans con fallback a Arial."""
    e = html.escape
    imagen = ""
    if n.imagen:
        imagen = (f'<tr><td style="padding:0 0 22px;">'
                  f'<a href="{e(n.url)}" style="text-decoration:none;">'
                  f'<img src="{e(n.imagen)}" alt="" width="600" '
                  f'style="display:block;width:100%;max-width:600px;height:auto;'
                  f'border-radius:8px;"></a></td></tr>')
    subtitulo = ""
    if n.subtitulo:
        subtitulo = (f'<tr><td style="padding:0 0 14px;font-family:{{cuerpo}};font-size:16px;'
                     f'line-height:1.5;color:{MUTED};">{e(n.subtitulo)}</td></tr>')
    saludo = e(cfg.get("saludo") or "")
    despedida = e(cfg.get("despedida") or "")
    if para_prueba:
        desuscribir = f'<a href="#" style="color:{MUTED};">Darme de baja</a>'
        espejo = ""
    else:
        desuscribir = f'<a href="{{{{ unsubscribe }}}}" style="color:{MUTED};">Darme de baja</a>'
        espejo = f' &nbsp;·&nbsp; <a href="{{{{ mirror }}}}" style="color:{MUTED};">Ver en el navegador</a>'
    cuerpo = "'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif"
    titulo = "Sora, 'Helvetica Neue', Arial, sans-serif"
    rotulo = "'Roboto Condensed', 'Arial Narrow', Arial, sans-serif"
    subtitulo = subtitulo.replace("{cuerpo}", cuerpo)
    dominio = base_url.rstrip("/").replace("https://", "")
    return f"""<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(n.titulo)}</title></head>
<body style="margin:0;padding:0;background:{MIST};">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:{MIST};">
<tr><td align="center" style="padding:28px 12px;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="width:100%;max-width:600px;background:#FFFFFF;border-radius:10px;overflow:hidden;">
  <tr><td style="background:{NAVY};padding:18px 32px;">
    <p style="margin:0;font-family:{rotulo};font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#FFFFFF;">Departamento de Neurociencia</p>
    <p style="margin:4px 0 0;font-family:{rotulo};font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#9FB4E8;">Facultad de Medicina &nbsp;·&nbsp; Universidad de Chile</p>
  </td></tr>
  <tr><td style="height:3px;background:{CIAN};line-height:3px;font-size:0;">&nbsp;</td></tr>
  <tr><td style="padding:24px 32px 0;">
    <p style="margin:0 0 22px;font-family:{cuerpo};font-size:14px;line-height:1.5;color:{MUTED};">{saludo}</p>
  </td></tr>
  <tr><td style="padding:0 32px;">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
      {imagen}
      <tr><td style="padding:0 0 8px;font-family:{rotulo};font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:{AZUL};">Noticia &nbsp;·&nbsp; {e(fecha_larga(n.fecha))}</td></tr>
      <tr><td style="padding:0 0 12px;font-family:{titulo};font-size:24px;line-height:1.25;font-weight:700;color:{TEXTO};"><a href="{e(n.url)}" style="color:{TEXTO};text-decoration:none;">{e(n.titulo)}</a></td></tr>
      {subtitulo}
      <tr><td style="padding:0 0 24px;font-family:{cuerpo};font-size:16px;line-height:1.6;color:{TEXTO};">{e(n.resumen)}</td></tr>
      <tr><td style="padding:0 0 32px;">
        <a href="{e(n.url)}" style="display:inline-block;padding:12px 24px;background:{AZUL};color:#FFFFFF;font-family:{titulo};font-size:15px;font-weight:600;text-decoration:none;border-radius:999px;">Leer la noticia →</a>
      </td></tr>
    </table>
  </td></tr>
  <tr><td style="padding:18px 32px 24px;border-top:1px solid {LINEA};font-family:{cuerpo};font-size:12px;line-height:1.55;color:{MUTED};">
    <p style="margin:0 0 8px;">{despedida}</p>
    <p style="margin:0;"><a href="{e(base_url)}" style="color:{MUTED};">{e(dominio)}</a> &nbsp;·&nbsp; <a href="{e(base_url)}blog/" style="color:{MUTED};">Todas las noticias</a>{espejo} &nbsp;·&nbsp; {desuscribir}</p>
  </td></tr>
</table>
</td></tr></table>
</body></html>"""


# ---------------------------------------------------------------- Brevo
class Brevo:
    def __init__(self, clave: str):
        self.s = requests.Session()
        self.s.headers.update({"api-key": clave, "accept": "application/json",
                               "content-type": "application/json"})

    def _pedir(self, metodo: str, ruta: str, **kw):
        r = self.s.request(metodo, BREVO + ruta, timeout=30, **kw)
        if r.status_code >= 400:
            try:
                detalle = r.json()
            except ValueError:
                detalle = r.text[:300]
            raise RuntimeError(f"Brevo {metodo} {ruta} → {r.status_code}: {detalle}")
        return r

    def campanas(self) -> list[dict]:
        """Todas las campañas de correo, de cualquier estado."""
        out, offset, limite = [], 0, 100
        while True:
            r = self._pedir("GET", "/emailCampaigns",
                            params={"limit": limite, "offset": offset, "sort": "desc"})
            datos = r.json()
            lote = datos.get("campaigns") or []
            out.extend(lote)
            offset += limite
            if len(lote) < limite or offset >= int(datos.get("count") or 0):
                break
        return out

    def crear_campana(self, nombre: str, asunto: str, html_: str, cfg: dict) -> int:
        rem = cfg["remitente"]
        cuerpo = {
            "name": nombre,
            "subject": asunto,
            "sender": {"name": rem["nombre"], "email": rem["correo"]},
            "replyTo": (cfg.get("responder_a") or rem["correo"]),
            "htmlContent": html_,
            "recipients": {"listIds": [int(cfg["lista_id"])]},
            # Sin "tag": Brevo lo rechaza en el plan gratuito con
            # 405 "not allowed to avail tag option" (pasó el 2026-09-07).
            "inlineImageActivation": False,
        }
        r = self._pedir("POST", "/emailCampaigns", json=cuerpo)
        return int(r.json()["id"])

    def enviar_ahora(self, id_campana: int) -> None:
        self._pedir("POST", f"/emailCampaigns/{id_campana}/sendNow")

    def correo_transaccional(self, para: str, asunto: str, html_: str, cfg: dict) -> None:
        rem = cfg["remitente"]
        self._pedir("POST", "/smtp/email", json={
            "sender": {"name": rem["nombre"], "email": rem["correo"]},
            "to": [{"email": para}],
            "subject": asunto,
            "htmlContent": html_,
            "tags": [ETIQUETA, "prueba"],
        })

    def agregar_contacto(self, correo: str, nombre: str, lista_id: int) -> str:
        cuerpo = {"email": correo, "listIds": [lista_id], "updateEnabled": True,
                  "attributes": {}}
        if nombre:
            partes = nombre.split(" ", 1)
            cuerpo["attributes"]["FIRSTNAME"] = partes[0]
            if len(partes) > 1:
                cuerpo["attributes"]["LASTNAME"] = partes[1]
            cuerpo["attributes"]["NOMBRE"] = nombre
        try:
            r = self._pedir("POST", "/contacts", json=cuerpo)
        except RuntimeError as e:
            # Los atributos FIRSTNAME/LASTNAME/NOMBRE pueden no existir en la
            # cuenta: se reintenta sin ellos antes de darse por vencido.
            if "attribute" in str(e).lower():
                cuerpo.pop("attributes", None)
                r = self._pedir("POST", "/contacts", json=cuerpo)
            else:
                raise
        return "creado" if r.status_code == 201 else "actualizado"


# ---------------------------------------------------------------- comprobaciones
def url_viva(url: str, intentos: int = 10, pausa: int = 30) -> bool:
    """Espera a que la URL responda 200 (el CDN de Pages tarda un poco)."""
    for i in range(intentos):
        try:
            r = requests.get(url, timeout=20, allow_redirects=True,
                             headers={"User-Agent": "neurosistemas-boletin/1.0"})
            if r.status_code == 200:
                return True
            log(f"  · {url} → {r.status_code} (intento {i + 1}/{intentos})")
        except requests.RequestException as e:
            log(f"  · {url} → {e.__class__.__name__} (intento {i + 1}/{intentos})")
        if i < intentos - 1:
            time.sleep(pausa)
    return False


def cargar_config() -> tuple[dict, str]:
    cfg = leer_yaml(CFG) if os.path.exists(CFG) else {}
    hugo = leer_yaml(HUGO_CFG) if os.path.exists(HUGO_CFG) else {}
    base = str(hugo.get("baseURL") or "https://www.neurosistemas.cl/")
    if not base.endswith("/"):
        base += "/"
    cfg.setdefault("remitente", {})
    cfg["remitente"].setdefault("nombre", "Laboratorio de Neurosistemas")
    cfg["remitente"].setdefault("correo", "")
    return cfg, base


def elegir(noticias: list[Noticia], slug: str | None) -> list[Noticia]:
    if not slug:
        return noticias
    slug = slug.strip().removesuffix(".md")
    sel = [n for n in noticias if n.slug == slug]
    if not sel:
        log(f"No existe content/noticias/{slug}.md. Disponibles:")
        for n in noticias:
            log(f"  - {n.slug}")
        sys.exit(1)
    return sel


def pendientes(noticias: list[Noticia], cfg: dict, slug: str | None) -> list[Noticia]:
    """Filtra lo que corresponde avisar. Con --slug se salta `enviar_desde`
    (es un pedido explícito), pero nunca borradores ni `boletin: false`."""
    desde = a_fecha(cfg.get("enviar_desde"))
    out = []
    for n in noticias:
        if n.borrador:
            log(f"  – {n.slug}: borrador, se omite")
            continue
        if not n.boletin:
            log(f"  – {n.slug}: boletin: false, se omite")
            continue
        if not slug and desde and (n.fecha is None or n.fecha < desde):
            continue
        out.append(n)
    return out


def asunto_de(n: Noticia, cfg: dict) -> str:
    return (cfg.get("prefijo_asunto") or "") + n.titulo


# ---------------------------------------------------------------- órdenes
def orden_enviar(args) -> int:
    cfg, base = cargar_config()
    clave = os.environ.get("BREVO_API_KEY", "").strip()
    noticias = elegir(cargar_noticias(base), args.slug)
    log(f"Noticias en el repo: {len(noticias)}. enviar_desde = {cfg.get('enviar_desde')}")
    candidatas = pendientes(noticias, cfg, args.slug)
    if not candidatas:
        log("Nada que avisar.")
        return 0

    simular = args.simular or not cfg.get("activo", True)
    if not cfg.get("activo", True):
        log("data/boletin.yaml tiene activo: false → solo simulación.")
    if not simular and not clave:
        log("Sin BREVO_API_KEY en el entorno → solo simulación (no se manda nada).")
        simular = True
    if not simular and not int(cfg.get("lista_id") or 0):
        log("lista_id es 0 en data/boletin.yaml → solo simulación (no se manda nada).")
        simular = True
    if not simular and not cfg["remitente"].get("correo"):
        log("Falta remitente.correo en data/boletin.yaml → solo simulación.")
        simular = True

    ya = set()
    if clave:
        try:
            ya = {c.get("name", "") for c in Brevo(clave).campanas()}
        except RuntimeError as e:
            log(f"No se pudo listar las campañas de Brevo: {e}")
            if not simular:
                return 1

    por_enviar = []
    for n in candidatas:
        if n.nombre_campana in ya and not args.reenviar:
            log(f"  ✓ {n.slug}: ya se avisó (campaña «{n.nombre_campana}»)")
            continue
        por_enviar.append(n)
    if not por_enviar:
        log("Todo estaba avisado. Nada que hacer.")
        return 0

    if not args.slug and len(por_enviar) > 3 and not args.reenviar:
        # Freno de seguridad: si aparecen muchas de golpe (p. ej. se corrió
        # `enviar_desde` hacia atrás), mejor mandarlas a mano una a una.
        log(f"Hay {len(por_enviar)} noticias sin avisar; por seguridad el modo "
            "automático manda como máximo 3 por corrida. Usa --slug para el resto.")
        por_enviar = por_enviar[-3:]

    brevo = Brevo(clave) if (clave and not simular) else None
    fallos = 0
    for n in por_enviar:
        log(f"\n→ {n.slug}")
        log(f"  Asunto : {asunto_de(n, cfg)}")
        log(f"  Fecha  : {n.fecha}   URL: {n.url}")
        log(f"  Resumen: {n.resumen[:120]}{'…' if len(n.resumen) > 120 else ''}")
        if n.imagen:
            log(f"  Imagen : {n.imagen}")
        if simular:
            log("  (simulación: no se envía)")
            continue
        if not args.sin_verificar_url and not url_viva(n.url):
            log("  ✗ La URL no responde 200: no se manda un enlace roto. "
                "Se reintentará en el próximo despliegue.")
            fallos += 1
            continue
        try:
            nombre = n.nombre_campana
            if args.reenviar and nombre in ya:
                nombre = f"{nombre} (reenvío {dt.datetime.now():%Y-%m-%d %H:%M})"
            id_c = brevo.crear_campana(nombre, asunto_de(n, cfg), armar_html(n, cfg, base), cfg)
            brevo.enviar_ahora(id_c)
            log(f"  ✓ Enviada (campaña {id_c} «{nombre}»)")
        except RuntimeError as e:
            log(f"  ✗ {e}")
            fallos += 1
    return 1 if fallos else 0


def orden_prueba(args) -> int:
    cfg, base = cargar_config()
    clave = os.environ.get("BREVO_API_KEY", "").strip()
    if not clave:
        log("Falta BREVO_API_KEY en el entorno.")
        return 1
    noticias = elegir(cargar_noticias(base), args.slug)
    n = noticias[-1]
    asunto = "[PRUEBA] " + asunto_de(n, cfg)
    try:
        Brevo(clave).correo_transaccional(args.correo, asunto, armar_html(n, cfg, base, True), cfg)
    except RuntimeError as e:
        log(f"✗ {e}")
        return 1
    log(f"✓ Correo de prueba con «{n.titulo}» enviado a {args.correo}")
    return 0


def orden_vista_previa(args) -> int:
    cfg, base = cargar_config()
    noticias = elegir(cargar_noticias(base), args.slug)
    n = noticias[-1]
    salida = args.salida or os.path.join(RAIZ, "boletin-vista-previa.html")
    with open(salida, "w", encoding="utf-8") as f:
        f.write(armar_html(n, cfg, base, True))
    log(f"✓ Vista previa de «{n.titulo}» en {salida}")
    return 0


def orden_importar(args) -> int:
    """CSV con columnas `correo` y `nombre` (con o sin encabezado)."""
    cfg, _ = cargar_config()
    lista_id = int(cfg.get("lista_id") or 0)
    clave = os.environ.get("BREVO_API_KEY", "").strip()
    if not lista_id:
        log("lista_id es 0 en data/boletin.yaml: crea la lista en Brevo y anota su ID.")
        return 1
    filas = []
    with open(args.archivo, encoding="utf-8-sig", newline="") as f:
        muestra = f.read(2048)
        f.seek(0)
        sep = ";" if muestra.count(";") > muestra.count(",") else ","
        for fila in csv.reader(f, delimiter=sep):
            if not fila or not fila[0].strip() or fila[0].strip().startswith("#"):
                continue
            correo = fila[0].strip().lower()
            if correo in ("correo", "email", "e-mail"):
                continue
            if "@" not in correo:
                log(f"  – fila ignorada (no es un correo): {fila}")
                continue
            nombre = fila[1].strip() if len(fila) > 1 else ""
            filas.append((correo, nombre))
    if not filas:
        log("El archivo no tiene correos.")
        return 1
    log(f"{len(filas)} contactos para la lista {lista_id}:")
    for correo, nombre in filas:
        log(f"  - {correo}  {nombre}")
    if args.simular:
        log("(simulación: no se agrega nada)")
        return 0
    if not clave:
        log("Falta BREVO_API_KEY en el entorno.")
        return 1
    brevo = Brevo(clave)
    fallos = 0
    for correo, nombre in filas:
        try:
            log(f"  ✓ {correo}: {brevo.agregar_contacto(correo, nombre, lista_id)}")
        except RuntimeError as e:
            log(f"  ✗ {correo}: {e}")
            fallos += 1
        time.sleep(0.15)
    return 1 if fallos else 0


def orden_enviados(args) -> int:
    clave = os.environ.get("BREVO_API_KEY", "").strip()
    if not clave:
        log("Falta BREVO_API_KEY en el entorno.")
        return 1
    try:
        camps = Brevo(clave).campanas()
    except RuntimeError as e:
        log(f"✗ {e}")
        return 1
    mias = [c for c in camps if str(c.get("name", "")).startswith(PREFIJO_CAMPANA)]
    if not mias:
        log("Todavía no hay campañas del boletín.")
        return 0
    for c in mias:
        log(f"  {c.get('id'):>6}  {c.get('status', ''):<10} {c.get('name')}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Boletín de noticias del Laboratorio de Neurosistemas (Brevo).")
    sub = p.add_subparsers(dest="orden")

    e = sub.add_parser("enviar", help="avisar de las noticias nuevas (lo que hace el workflow)")
    e.add_argument("--simular", action="store_true", help="mostrar qué se mandaría, sin mandar")
    e.add_argument("--slug", help="solo esta noticia (nombre del archivo sin .md); ignora enviar_desde")
    e.add_argument("--reenviar", action="store_true", help="mandar aunque ya exista la campaña")
    e.add_argument("--sin-verificar-url", action="store_true", help="no esperar a que la URL responda 200")
    e.set_defaults(fn=orden_enviar)

    t = sub.add_parser("prueba", help="mandar el correo de una noticia a una sola dirección")
    t.add_argument("--correo", required=True)
    t.add_argument("--slug", help="por omisión, la noticia más reciente")
    t.set_defaults(fn=orden_prueba)

    v = sub.add_parser("vista-previa", help="escribir el HTML del correo en un archivo")
    v.add_argument("--slug")
    v.add_argument("--salida")
    v.set_defaults(fn=orden_vista_previa)

    i = sub.add_parser("importar", help="agregar contactos a la lista desde un CSV (correo;nombre)")
    i.add_argument("archivo")
    i.add_argument("--simular", action="store_true")
    i.set_defaults(fn=orden_importar)

    s = sub.add_parser("enviados", help="listar las campañas del boletín ya creadas")
    s.set_defaults(fn=orden_enviados)

    args = p.parse_args()
    if not args.orden:
        args = p.parse_args(["enviar"])
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
