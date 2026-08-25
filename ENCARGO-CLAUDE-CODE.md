# Encargo para Claude Code — Sincronizacion de publicaciones via ORCID

Generado por el chat de Cowork (modo dual). Todo lo de este encargo se preparo y se
verifico sin red (salvo lo que se indica explicitamente); falta lo que necesita red real,
Hugo, npm o git, que le toca a Claude Code.

Carpeta: la raiz de este repo (`~/Git_Web/Neurociencia` en tu Mac).
Rama de trabajo: `home-etapa3` (no `main` directo).

## 0. Housekeeping antes de empezar

El chat no puede borrar archivos desde su sandbox. Dejo una carpeta `_to_delete/` en la
raiz del repo con un archivo de prueba (`publicaciones_orcid.json.test.json`) que se cayo
ahi por lo mismo. Borrala:

```bash
rm -rf _to_delete/
```

## 1. Que se agrego (ya escrito y verificado sin red)

- `scripts/orcid_sync.py` — sincronizador. Lee el ORCID directamente del front-matter de
  `content/academicos/<slug>/index.md` (acepta URL completa o id pelado, no hace falta
  tocar las 34 fichas), consulta la API publica de ORCID, deduplica, enriquece con
  Crossref, y escribe `data/publicaciones_orcid.json`. Si ORCID o Crossref fallan,
  conserva el JSON anterior y sale en 0 (nunca rompe el build).
- `scripts/test_orcid_sync.py` — 12 aserciones con respuestas simuladas, sin tocar la red.
  **Ya corrido: TODO OK.**
- `scripts/buscar_orcid_academicos.py` — completa los ORCID que faltan (ver seccion 3).
  Necesita red real; no se pudo correr desde el sandbox del chat.
- `scripts/verificar_estatico.py` — chequeo estatico (YAML/JSON validos, front-matter con
  title, balance de `{{ end }}`, partials existentes, menu con contenido, `site.Data`/
  `hugo.Data` con su archivo). **Ya corrido sobre todo el repo: 0 errores, 5 avisos —
  los 5 son preexistentes y no tienen que ver con este cambio** (falta `title` en
  `content/_index.md`; el menu "Eventos" sin `_index.md` explicito, que es un falso
  positivo del checker porque Hugo genera la seccion igual sin ese archivo; y 3 rutas
  `/uploads/favicon-*` literales en `custom.html`, que son las excepciones documentadas
  en la regla 6 de CLAUDE.md). Puedes volver a correrlo cuando quieras:
  `python scripts/verificar_estatico.py`
- `data/orcid_opciones.yaml` — opciones del sincronizador (ano minimo, Crossref, tipos
  aceptados). El ORCID de cada persona NO esta aqui: sigue viviendo solo en el
  front-matter de su ficha, para no tener dos fuentes de verdad.
- `data/publicaciones_orcid.json` — semilla vacia (`publicaciones: []`), para que el
  build no falle antes de la primera corrida real.
- `.github/workflows/orcid.yml` — cron diario (08:25 UTC), solo Python (pip install
  requests/PyYAML + `python scripts/orcid_sync.py`), independiente de npm/go. Commitea
  **directo a `main`** si `data/publicaciones_orcid.json` cambio — igual que en
  Neurosistemas, y es lo que corresponde para que el sitio se actualice solo.
- `content/publicaciones/_index.md` + `layouts/publicaciones/list.html` +
  `layouts/_partials/publicacion.html` — listado agregado del Departamento. Fusiona
  `data/publicaciones_orcid.json` con las publicaciones curadas a mano (campo
  `publicaciones` de cada ficha, **solo las que quedaron en formato estructurado
  titulo/revista/ano/link** — si el CMS aplano alguna a texto plano, esa entrada no se
  puede sumar de forma fiable al listado agregado y queda fuera de el, sin romper nada;
  sigue viendose igual en la ficha de la persona). Agrupado por ano, buscador en vivo, y
  un "mostrar mas" por ano cuando supera 25 publicaciones (no es paginacion nativa de
  Hugo — es la decision mas simple para la version 1; si algun ano termina con cientos de
  publicaciones, vale la pena revisarlo).
- `config/_default/menus.yaml` — entrada "Publicaciones" agregada (peso 45, entre Temas y
  Actualidad).
- `layouts/academicos/single.html` — **se reemplazo el bloque "Desde ORCID"**: antes hacia
  un `fetch` en JavaScript en el navegador de cada visitante (lento, no indexable, se
  caia en silencio si ORCID no respondia); ahora es server-side, emparejando por ORCID id
  contra `data/publicaciones_orcid.json` en el build. El resto del archivo (foto, cargo,
  temas, afiliacion, biografia, "Seleccionadas" del CMS, proyectos, autopresentacion) no
  se toco. Revisa el diff igual, es un archivo largo y en produccion.

## 2. Validar

```bash
npm install
HUGO_ENVIRONMENT=production hugo --minify
```

Si algo tira `ERROR`, no sigas: pegame el mensaje completo y lo reviso. Si queda verde,
levanta el preview y mira al menos:
- `/publicaciones/` (nueva)
- 2-3 fichas de `/academicos/<slug>/` — una con ORCID y publicaciones "Desde ORCID"
  vacio (porque `publicaciones_orcid.json` todavia es la semilla vacia en este punto), y
  una con `publicaciones` curadas ("Seleccionadas") para confirmar que ese bloque sigue
  igual.

## 3. Completar los 12 ORCID que faltan

12 de 34 academicos no tienen ORCID: andres-couve, catherine-perez, christ-devia,
gonzalo-farias, gonzalo-olivares, hachi-manzur, manuel-kukuljan, marco-contreras,
maria-hidalgo, nicole-rogers, pablo-henny, rodrigo-nieto.

```bash
pip install requests PyYAML
python scripts/buscar_orcid_academicos.py
```

Esto:
1. Cruza primero con `~/Git_Web/Neurosistemas/data/orcid.yaml` sin tocar la red (ahi ya
   esta el de **christ-devia**, gratis).
2. Para el resto, busca en la API publica de ORCID acotando a afiliacion "Universidad de
   Chile" y **solo** escribe el ORCID en la ficha cuando hay un unico candidato
   inequivoco. Todo lo dudoso queda listado en `INFORME-ORCID.md` (que tambien se genera)
   para que Hayo confirme cual es y lo complete el mismo por Pages CMS, o me lo pases a mi
   para que te arme el bloque de aplicarlo.

**Antes de commitear:** `git diff content/academicos/` y revisa los ORCID que se
auto-rellenaron (aunque el build no se vea afectado, son fichas institucionales — vale la
pena que alguien los mire una vez). Pegame el resultado de la corrida (cuantos se
cruzaron, cuantos se autocompletaron, cuantos quedaron pendientes) y el contenido de
`INFORME-ORCID.md` si quieres que lo revise contigo.

## 4. Primera corrida real del sincronizador

Con los ORCID que haya disponibles en ese momento (no hace falta esperar a tener los 34):

```bash
python scripts/orcid_sync.py
```

Revisa `data/publicaciones_orcid.json` — deberia tener contenido real ahora — y vuelve a
correr el build (`HUGO_ENVIRONMENT=production hugo --minify`) para confirmar que
`/publicaciones/` y las fichas individuales muestran publicaciones reales.

## 5. Permisos de GitHub Actions

Hayo ya activo "Read and write permissions" en Settings → Actions → General del repo
`openneurocienciauchile/Web`. Igual conviene disparar el workflow una vez a mano para
confirmar que efectivamente puede commitear:

Actions → "Sincronizar publicaciones desde ORCID" → Run workflow. Si falla por permisos
pese a lo anterior, avisame.

## 6. Commit y push

Build verde -> commit (puedes dividirlo en 2-3, como prefieras: scripts+workflow+datos;
plantillas+menu; primera corrida real de datos) y push a `main` segun la politica de push
vigente en CLAUDE.md. Verifica con `git log --oneline origin/main..main` que quedo vacio
despues del push (no solo que el commit exista localmente).

## 7. Limitaciones conocidas (documentadas, no bloquean nada)

- El listado agregado (`/publicaciones/`) solo suma publicaciones "Seleccionadas"
  (curadas por CMS) que esten en formato estructurado. Las que el CMS aplano a texto
  libre (como las 15 de la ficha de Jimena Sierralta) siguen viendose en su ficha
  individual, pero no en el agregado del Departamento.
- El resaltado en negrita de autores del Departamento usa una heuristica simple (las dos
  ultimas palabras del nombre de la ficha) — es cosmetico, no afecta que publicacion es de
  quien (eso va por ORCID id).
- `content/publications/` (el sistema nativo de Hugo Blox, en ingles) queda intacto y sin
  usar, tal como estaba — no se toco a proposito. Si en algun momento quieren limpiarlo,
  es una tarea aparte, sin relacion con esto.
