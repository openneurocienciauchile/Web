# CLAUDE.md — Sitio web Departamento de Neurociencia U. de Chile

Contexto y reglas para trabajar en este repositorio con Claude Code.
Propietario: **Hayo Breinbauer** (otoneurólogo, dev Python). Idioma de trabajo: **español**.
Co-editora de contenido: **Francisca Pérez** (psicóloga).

---

## Qué es este repo
Sitio del Departamento de Neurociencia (Facultad de Medicina, U. de Chile), hecho con
**Hugo v0.162.1 extended + tema Hugo Blox + Tailwind v4**, desplegado en **GitHub Pages**.
- En vivo: `https://openneurocienciauchile.github.io/Web/` (servido bajo el path **`/Web/`**).
- Repo: `github.com/openneurocienciauchile/Web`.

## Ramas y despliegue (IMPORTANTE)
- `main` = **producción**. Cada push a `main` dispara el deploy y publica en vivo.
- `home-etapa3` = **rama de trabajo**. Trabaja SIEMPRE aquí.
- **Nunca hagas push a `main` sin autorización explícita de Hayo.** Merge a `main` solo cuando el
  build esté verde y Hayo lo apruebe.
- El repo está dentro de OneDrive → a veces bloquea archivos en operaciones git; si una operación
  falla por archivo bloqueado, reintenta.

## Entorno local de build (IMPORTANTE en Windows)
- Instala las dependencias del front-end con **npm**, NO con pnpm. Con pnpm,
  `@tailwindcss/cli` queda como symlink al store de pnpm y Hugo no puede ejecutar el binario
  de Tailwind v4: el build falla con
  `TAILWINDCSS: failed to transform ".../_entry.css": binary "tailwindcss" is not a Node.js script`
  (bug de Hugo, issue gohugoio/hugo#14852). Con `npm install` la carpeta es real y el build
  queda verde.
- Receta para entorno limpio en Windows:
  `Remove-Item -Recurse -Force node_modules; npm install`
  y luego `$env:HUGO_ENVIRONMENT="production"; hugo --minify`.
- VERIFICADO (2026-06-07): el CI corre en Ubuntu, donde el wrapper `#!/bin/sh` de pnpm SÍ es
  ejecutable, así que el bug #14852 NO afecta el build de Actions — es exclusivo de Windows
  local. El último deploy a `main` quedó verde. No hace falta cambiar el CI a npm; mantener
  pnpm en Actions está OK. (El bug solo obliga a usar npm para el build LOCAL en Windows.)

## Reglas de oro (cúmplelas siempre)
1. **Valida el build antes de commitear.** Corre exactamente lo que corre el CI:
   `HUGO_ENVIRONMENT=production hugo --minify` (en PowerShell: `$env:HUGO_ENVIRONMENT="production"; hugo --minify`).
   Si hay `ERROR`, arrégialo y vuelve a correr hasta que quede verde. No commitees en rojo.
2. **CMS-safe.** Todo lo que un editor deba poder cambiar va por **Pages CMS** (config en `.pages.yml`),
   no hardcodeado en plantillas.
3. **CSS propio en un solo archivo:** `layouts/_partials/hooks/head-end/custom.html`, con clases
   prefijadas `neuro-` / `nuro-`. El tema NO carga `custom.scss`.
4. **Plantillas defensivas.** Cualquier `{{ range }}` sobre un campo editable por el CMS debe tolerar
   que venga como **string** en vez de **lista** (el CMS a veces aplana listas → rompe el build).
   Patrón: usar `reflect.IsSlice` / `reflect.IsMap` y, si es string, `split` por salto de línea.
   Ya aplicado en `afiliacion`; **falta aplicarlo en `publicaciones` y `proyectos`**.
5. **Links internos:** usa `relURL`, `.RelPermalink`, `.Parent.RelPermalink` o `site.GetPage`.
   NUNCA hardcodees `/temas/...` (el sitio vive bajo `/Web/`).
6. **Imágenes:** se guardan como `/uploads/<archivo>` y se referencian con `| relURL` → `/Web/uploads/...`.
7. **Privacidad — NUNCA publicar:** columnas internas de RR.HH. (*Horas, Modalidad, Observaciones*),
   correos personales, notas internas.
8. **Commits chicos y claros**, en español. Explica qué cambiaste y por qué.

## Hechos de arquitectura
- **Navbar = `#site-header`** (id del tema). Por defecto navy `#0A1533` + texto blanco. En el HOME,
  `html.neuro-home #site-header` lo hace transparente sobre el hero (un JS en `custom.html` agrega la
  clase `neuro-home` cuando existe `.neuro-hero`). En páginas internas se fuerza navy con
  `html:not(.neuro-home) #site-header { background:#0A1533 !important }`.
- **Taxonomía `temas` VIVA (Camino B):** `layouts/temas/list.html` es la nube que lee
  `site.Taxonomies.temas.ByCount`; `layouts/temas/term.html` es la página de cada tema (lista
  `.Pages` por sección). Cualquier tag escrito libremente en `temas:` (en fichas, noticias, labs,
  eventos) crea su term page solo y entra a la nube. Las 9 carpetas `content/temas/<slug>/_index.md`
  son descripciones curadas de esos términos; los demás tags son libres.
- **Ficha de académico:** `content/academicos/<slug>/index.md` (excepciones: `HB/HB.md`, `JS/JS.md`).
  Campos: `title, role, degree, email, orcid, portafolio, temas` (lista), `image`,
  `afiliacion` (lista de `{texto,url,rol}`), `youtube`, `bio, publicaciones, proyectos, body`.
  `afiliacion/publicaciones/proyectos` son LISTAS (ver regla 4).
- **Paleta:** azul `#1C4599`, cian `#16C8E6`, navy `#0A1230`/`#0A1533`. Vars en `:root`:
  `--neuro-blue --neuro-cyan --neuro-ink --neuro-mist --neuro-mist2 --neuro-text --neuro-muted --neuro-line`.
- **Fuentes:** Sora (títulos), IBM Plex Sans (cuerpo), Roboto Condensed (rótulos).
- **Taxonomías** (`config/_default/hugo.yaml`): `author: authors`, `tag: tags`,
  `publication_type: publication_types`, `temas: temas`.
- Build tira **warnings de deprecación** de Hugo (cascade._target, languageCode, .Site.Data,
  .Site.LanguageCode) — no son fatales; limpiar en algún momento.

## Archivos clave
- CSS/navbar/hero/JS: `layouts/_partials/hooks/head-end/custom.html`
- Nube de temas: `layouts/temas/list.html` · Página de tema: `layouts/temas/term.html`
  (legado sin uso: `layouts/temas/single.html`)
- Ficha académico: `layouts/academicos/single.html` (tiene guardas defensivas en `afiliacion`)
- Config CMS: `.pages.yml` · Config Hugo: `config/_default/hugo.yaml`
- Workflows: `.github/workflows/deploy.yml` + `build.yml` (build = `hugo --minify`)
- Imágenes: `static/uploads/`

## Trabajo pendiente (en orden sugerido)
0. **Antes que nada:** confirmar que `layouts/temas/term.html` y
   `layouts/_partials/hooks/head-end/custom.html` están commiteados, y **resincronizar `home-etapa3`
   con `main`** (`git checkout home-etapa3; git merge main`). Luego trabajar en `home-etapa3`.
1. **Foto en la noticia completa:** mostrar la imagen de portada arriba del single de blog
   (`layouts/blog/single.html` o el partial de portada): `{{ with .Params.image }}<img object-fit:cover>{{ end }}`.
2. **Laboratorios:** en `.pages.yml` (colección `laboratorios`) agregar `logo` (image) y `website`
   (URL); en `layouts/laboratorios/single.html` mostrar logo + summary + enlace. Crear
   `layouts/laboratorios/list.html` (índice). Labs actuales: **LabONCE** y **Neurosistemas**.
3. **Logos de Labs en el Landing**, bajo Noticias (recorrer
   `where site.RegularPages "Section" "laboratorios"` y mostrar `.Params.logo`).
4. **Sección institucional/colaboradores en el Landing** (bajo Labs): enlaces a U. de Chile, Facultad
   de Medicina, y colaboradores GERO / CEIA / ANID. Idealmente CMS-safe vía `data/colaboradores.yaml`.
   (Confirmar URLs/logos con Hayo; aclarar a qué "CEIA" se refiere.)
5. **Blindar `publicaciones` y `proyectos`** en `academicos/single.html` (regla 4).
6. **`menus.yaml`:** "Quiénes somos" → "El Departamento"; "Labs" vs "Laboratorios"; quitar "Temas"
   viejo; agregar "Actualidad".
7. **Page Find** (buscador navbar; hoy `header.search: false` en `params.yaml`).
8. **Contacto:** decidir formulario (Formspree u otro) vs solo datos.
9. Limpiar deprecations de Hugo.

## FLAGS de contenido a verificar con Hayo
- 2 fichas sin tema (Manzur #20, Martínez #21 — con Camino B se puede crear el tag, ej. "Neuroeducación").
- 4 perfiles parciales por completar. Categorías RR.HH. a confirmar (Morales, Helo, Salech, Rivera, Olguín).
- Género de Manzur (#20) asumido masculino — confirmar.

## Pages CMS (para Hayo/Francisca)
`app.pagescms.org` → login GitHub → repo `Web`. Commitea directo a la rama elegida (sin preview):
**apuntarlo a `home-etapa3`**, no a `main`. Tras editar por CMS, hacer `git pull` antes de editar local.
Riesgo: puede aplanar listas a string y romper el build (por eso la regla 4).

## Modelos en Claude Code
- Por defecto trabaja en **Sonnet** (edición de plantillas, git, builds: le sobra).
- Sube a **Opus** (`/model`) solo para razonamiento delicado o arquitectura en el código,
  p.ej. blindar `publicaciones`/`proyectos` contra el aplanado de listas del CMS. El chat
  (Opus) avisará cuando una tarea lo amerite.
