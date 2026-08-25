# CLAUDE.md — Sitio web Departamento de Neurociencia U. de Chile

Contexto y reglas para trabajar en este repositorio con Claude Code.
Propietario: **Hayo Breinbauer** (otoneurólogo, dev Python). Idioma de trabajo: **español**.
Co-editora de contenido: **Francisca Pérez** (psicóloga).

---

## Qué es este repo
Sitio del Departamento de Neurociencia (Facultad de Medicina, U. de Chile), hecho con
**Hugo v0.162.1 extended + tema Hugo Blox + Tailwind v4**, desplegado en **GitHub Pages**.
- En vivo: `https://deptoneuro.med.uchile.cl/` — **dominio oficial, servido en la RAÍZ**.
  (Migrado el 2026-08-06 desde `openneurocienciauchile.github.io/Web/`; el dominio está
  configurado en Settings → Pages y versionado en `static/CNAME`. La URL antigua de github.io
  redirige sola al dominio propio.)
- Repo: `github.com/openneurocienciauchile/Web`.

## Ramas y despliegue (IMPORTANTE)
- `main` = **producción**. Cada push a `main` dispara el deploy y publica en vivo.
- `home-etapa3` = **rama de trabajo**. Trabaja SIEMPRE aquí.
- **Política de push (actualizada 2026-06-09):** por defecto CADA tarea termina con merge a `main`
  y push para actualizar el sitio en vivo, SIEMPRE que el build local quede verde
  (`HUGO_ENVIRONMENT=production hugo --minify` sin ERROR). Hayo pre-autoriza este flujo; puede vetar
  un push puntual diciéndolo. Si el build queda rojo, NO se hace push.
- El repo está dentro de OneDrive → a veces bloquea archivos en operaciones git; si una operación
  falla por archivo bloqueado, reintenta.
- **Auth de git en macOS (resuelto 2026-08-10):** el remoto exige la cuenta
  `openneurocienciauchile`, pero la cuenta activa de `gh` suele ser `HayoBK` (se usa en los otros
  dos repos). El `osxkeychain` no tenía guardada la credencial de la cuenta del depto, así que
  `git push` moría con
  `fatal: could not read Password for 'https://openneurocienciauchile@github.com': Device not configured`
  — y el sitio "no se actualizaba" porque el push nunca ocurría, aunque el build estuviera verde.
  **Solución aplicada:** se guardó el token de esa cuenta en el keychain, de modo que el push
  funciona con `osxkeychain` y **sin depender de cuál sea la cuenta activa de `gh`**:
  ```bash
  T=$(gh auth token --user openneurocienciauchile)
  printf "protocol=https\nhost=github.com\nusername=openneurocienciauchile\npassword=%s\n\n" "$T" \
    | git credential-osxkeychain store
  ```
  OJO: `credential.helper = !gh auth git-credential` **no** sirve acá — resuelve el token de la
  cuenta ACTIVA de `gh`, así que falla igual apenas se vuelve a `HayoBK` (probado y descartado).
  Si el token se revoca o expira, volver a correr esas dos líneas.
- **Verifica que el push ocurrió de verdad**, no solo el commit: `git log --oneline origin/main..main`
  debe quedar vacío. Un run verde en Actions puede ser de un commit ANTERIOR — mira su hash y fecha
  antes de darlo por publicado.

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
1. **Valida el build antes de commitear.** Corre `HUGO_ENVIRONMENT=production hugo --minify`
   (en PowerShell: `$env:HUGO_ENVIRONMENT="production"; hugo --minify`).
   Si hay `ERROR`, arrégialo y vuelve a correr hasta que quede verde. No commitees en rojo.
   **OJO (descubierto 2026-08-25): el build local NO usa la misma versión de Hugo que el CI.**
   Ver "Versión de Hugo: local 0.162.1 vs CI 0.154.5" más abajo. Un build local verde NO
   garantiza que el CI pase si usaste API de Hugo posterior a 0.154.5.
2. **CMS-safe.** Todo lo que un editor deba poder cambiar va por **Pages CMS** (config en `.pages.yml`),
   no hardcodeado en plantillas.
3. **CSS propio en un solo archivo:** `layouts/_partials/hooks/head-end/custom.html`, con clases
   prefijadas `neuro-` / `nuro-`. El tema NO carga `custom.scss`.
4. **Plantillas defensivas.** Cualquier `{{ range }}` sobre un campo editable por el CMS debe tolerar
   que venga como **string** en vez de **lista** (el CMS a veces aplana listas → rompe el build).
   Patrón: usar `reflect.IsSlice` / `reflect.IsMap` y, si es string, `split` por salto de línea.
   Aplicado en `afiliacion`, `publicaciones` y `proyectos` (academicos/single.html).
5. **Links internos:** usa `relURL`, `.RelPermalink`, `.Parent.RelPermalink` o `site.GetPage`.
   Desde 2026-08-06 el sitio se sirve en la RAÍZ del dominio (ya no bajo `/Web/`), así que un
   path absoluto no se rompe — pero `relURL` sigue siendo la forma correcta de enlazar: deja el
   sitio inmune a un futuro cambio de `baseURL` y es lo que usan todas las plantillas.
   Convención: path SIN slash inicial (`"temas/" | relURL`) o `.RelPermalink`/`site.GetPage`.
6. **Imágenes:** se guardan como `/uploads/<archivo>`. Referenciar en plantillas con
   `strings.TrimPrefix "/" | relURL` (o `printf "%s%s" site.BaseURL (. | strings.TrimPrefix "/")`),
   que es lo aplicado en news-card, blog/single, labs-strip, laboratorios/single+list,
   temas/term+single. En HTML crudo dentro de `.md` (home, quiénes-somos, labs) no hay `relURL`
   disponible: ahí van rutas absolutas `/uploads/...`, correctas al servir en raíz.
7. **Privacidad — NUNCA publicar:** columnas internas de RR.HH. (*Horas, Modalidad, Observaciones*),
   correos personales, notas internas.
8. **Commits chicos y claros**, en español. Explica qué cambiaste y por qué.
9. **YAML en front-matter:** cualquier valor escalar con `: ` (dos puntos + espacio), `#` o
   comillas debe ir **entre comillas dobles**, o el build muere con `mapping value is not allowed
   in this context` (pasó con un `summary` de LAB ONCE).

## Hechos de arquitectura
- **Versión de Hugo: local 0.162.1 vs CI 0.154.5 (IMPORTANTE, 2026-08-25).** `hugoblox.yaml`
  declara `build.hugo_version: '0.162.1'`, pero `.github/workflows/build.yml` la lee con
  `yq '.hugo_version'` **a nivel raíz** — clave que no existe, porque está anidada bajo
  `build:`. Al no encontrarla cae siempre a su `DEFAULT_VERSION="0.154.5"`, así que **el CI
  nunca ha compilado con 0.162.1**. Se descubrió cuando un deploy murió con
  `can't evaluate field Data in type interface {}` por usar `hugo.Data` (que no existe en
  0.154.5) mientras el build local pasaba sin chistar.
  **Regla práctica: escribe plantillas compatibles con 0.154.5.** En particular usa
  `site.Data`, nunca `hugo.Data`. Para validar de verdad contra la versión del CI, baja ese
  binario y compila con él:
  ```bash
  curl -sL -o h.pkg https://github.com/gohugoio/hugo/releases/download/v0.154.5/hugo_extended_0.154.5_darwin-universal.pkg
  pkgutil --expand-full h.pkg hpkg     # el binario queda en hpkg/Payload/hugo
  HUGO_ENVIRONMENT=production ./hpkg/Payload/hugo --minify
  ```
  Alinear ambas versiones (arreglando el `yq` a `.build.hugo_version`) es una tarea aparte y
  con riesgo propio: subiría producción de 0.154.5 a 0.162.1 de golpe. Decisión de Hayo.
- **Publicaciones vía ORCID (2026-08-25).** `scripts/orcid_sync.py` lee el ORCID iD del
  front-matter de cada ficha, consulta la API pública de ORCID, deduplica, enriquece con
  Crossref y escribe `data/publicaciones_orcid.json`. Si ORCID o Crossref fallan, conserva el
  JSON anterior y sale en 0: nunca rompe el build. Corre solo con el cron de
  `.github/workflows/orcid.yml` (08:25 UTC diario) que **commitea directo a `main`** — por eso
  `main` puede avanzar sola en ese archivo y conviene hacer `git pull` antes de tocarlo.
  El iD de cada persona vive SOLO en su ficha (una fuente de verdad); `data/orcid_opciones.yaml`
  guarda únicamente año mínimo, uso de Crossref y tipos aceptados.
  Consumen ese JSON `layouts/publicaciones/list.html` (el agregado del Departamento) y el
  bloque "Desde ORCID" de `layouts/academicos/single.html`, que emparejan por el nombre de la
  ficha contra el campo `miembros` de cada publicación. Corolario: **si cambias el `title` de
  una ficha, sus publicaciones desaparecen hasta la próxima corrida del cron.**
  Deps de Python locales: hay un venv en `~/.venvs/orcid` (Homebrew Python bloquea `pip install`
  global por PEP 668). Tests sin red: `~/.venvs/orcid/bin/python scripts/test_orcid_sync.py`.
- **Navbar = `#site-header`** (id del tema). Por defecto navy `#0A1533` + texto blanco. En el HOME,
  `html.neuro-home #site-header` lo hace transparente sobre el hero (un JS en `custom.html` agrega la
  clase `neuro-home` cuando existe `.neuro-hero`). En páginas internas se fuerza navy con
  `html:not(.neuro-home) #site-header { background:#0A1533 !important }`.
- **Taxonomía `temas` VIVA (Camino B):** `layouts/temas/list.html` es la nube que lee
  `site.Taxonomies.temas.ByCount`; `layouts/temas/term.html` es la página de cada tema (lista
  `.Pages` por sección). Cualquier tag escrito libremente en `temas:` (en fichas, noticias, labs,
  eventos) crea su term page solo y entra a la nube. Las 9 carpetas `content/temas/<slug>/_index.md`
  son descripciones curadas de esos términos; los demás tags son libres.
- **`page-body my-10` y la franja blanca (CONVENCIÓN, 2026-08-10):** el tema envuelve TODO el
  contenido en `<div class="page-body my-10">`. Ese margen superior de 2.5rem se ve como una
  **franja blanca** entre el navbar y cualquier elemento que abra la página **a sangre y con fondo
  oscuro** — pasó con las barras de breadcrumb de noticias (`.npost-breadcrumb`) y eventos
  (`.evs-breadcrumb`). **Regla: al primer elemento de la plantilla, si va a sangre, agrégale la
  clase `neuro-bleed-top`.** La regla `.page-body:has(> .neuro-bleed-top){ margin-top:0 }` vive en
  `custom.html` y se encarga sola; no hay que tocar ese archivo de nuevo. En páginas que empiezan
  con fondo claro NO se pone la clase: ahí el margen sí se quiere.
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
- **Lab individual:** es una sección (`_index.md`) → Hugo NO usa `single.html`. `laboratorios/list.html`
  ramifica con `{{ if .Parent.IsHome }}` (portada=grilla) `{{ else }}` (lab=`partial "lab-single.html"`).
  Enfoque CMS-safe (sin depender del front-matter).
- **"Próximo seminario":** lógica en `_partials/func/seminario-destacado.html` (próximo futuro; si no,
  el pasado más reciente) y `func/eventos-resto.html`. Render con `_partials/destacado-card.html`
  (variant `hero`/`aside`). Reutilizado en eventos, landing (blox `proximo-seminario`) y Actualidad.
- **Navbar:** internas navy SÓLIDO con `!important` (gana al header transparente del tema); canvas de
  neuronas inyectado solo en internas; menú móvil `#nav-menu` con fondo navy bajo `lg`.
- **`type: landing` + bloque markdown** (HOME, quienes-somos): el HTML queda en contenedor angosto →
  full-bleed con `left:50%;margin-left:-50vw;width:100vw`. El tema pinta `h1` oscuros → títulos sobre
  navy necesitan `color:#fff !important`.

## Archivos clave
- CSS/navbar/hero/JS + CSS de "El Departamento" (`.dep-*`): `layouts/_partials/hooks/head-end/custom.html`
- Nube de temas: `layouts/temas/list.html` · Página de tema: `layouts/temas/term.html`
  (legado sin uso: `layouts/temas/single.html`)
- Ficha académico: `layouts/academicos/single.html` (tiene guardas defensivas en `afiliacion`)
- Labs: `layouts/laboratorios/list.html` (ramifica portada vs detalle con `.Parent.IsHome`) +
  `layouts/_partials/lab-single.html` (vista de detalle del lab). YA NO existe `laboratorios/single.html`.
- Eventos/Actualidad: `layouts/eventos/list.html`, `layouts/blog/list.html` + partials
  `layouts/_partials/func/seminario-destacado.html`, `layouts/_partials/func/eventos-resto.html`,
  `layouts/_partials/destacado-card.html`. Blox del landing: `_partials/hbx/blocks/proximo-seminario/block.html`.
- "El Departamento": `content/quienes-somos/_index.md` (todo el HTML va en su bloque markdown; el
  partial `_partials/blocks/quienes-somos.html` está vacío).
- "Formación": `layouts/formacion/list.html` (CSS propio `form-` adentro).
- Config CMS: `.pages.yml` · Config Hugo: `config/_default/hugo.yaml`
- Workflows: `.github/workflows/deploy.yml` + `build.yml` (build = `hugo --minify`)
- Imágenes: `static/uploads/`

## Trabajo pendiente (en orden sugerido)
0. ✅ HECHO. `term.html` y `custom.html` commiteados; `home-etapa3` resincronizada con `main`.
1. ✅ HECHO (commit `77341fe`). **Foto en la noticia completa**: `layouts/blog/single.html`
   muestra la portada arriba del artículo (resuelve `image` map de HugoBlox o string de Pages CMS).
2. ✅ HECHO (`407d6bf` + `262a83b`). **Laboratorios**: se arregló imagen (map+string) y se blindó
   `directores`/`temas` con `reflect.IsSlice` en `single.html`; se creó **Neurosistemas** y se
   completó **LAB ONCE** (logo, director, temas, contenido); se borró "Lab Prueba". Se reusa
   `image` (no se agregó `logo`/`website`). `term.html` ya lista los labs por tema. Logos con
   `object-fit:contain`. **Pendiente menor:** JSlab tiene el body copiado de LAB ONCE.
3. ✅ HECHO (commit `a3dd245`). **Logos de Labs en el Landing**: blox propio
   `layouts/_partials/hbx/blocks/labs-strip/block.html`, insertado en `content/_index.md` entre
   Noticias y Redes. Recorre `.Sections` de `/laboratorios` (no `RegularPages`), imagen map/string.
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
- **ORCID iD faltantes (2 de 34):** Marco Contreras y Nicole Rogers. La API pública de ORCID
  solo devuelve homónimos de otras áreas (ver `INFORME-ORCID.md`); lo más simple es pedirles su
  iD y cargarlo por Pages CMS. Sin iD, no aparecen en `/publicaciones/`.
- **Perfiles ORCID vacíos (iD correcto, 0 obras publicadas):** Couve, Catherine Pérez, Pablo
  Henny y Manuel Kukuljan. Su ficha muestra "Aún no hay publicaciones sincronizadas"; se
  arregla solo cuando ellos suban sus trabajos a ORCID, no hay nada que tocar en el sitio.
- 2 fichas sin tema (Manzur #20, Martínez #21 — con Camino B se puede crear el tag, ej. "Neuroeducación").
- 4 perfiles parciales por completar. Categorías RR.HH. a confirmar (Morales, Helo, Salech, Rivera, Olguín).
- Género de Manzur (#20) asumido masculino — confirmar.
- **Fotos faltantes (hoy con iniciales en el Consejo):** José Luis Valdés (`jose-valdes`) y Paola
  Morales (`eugenia-morales`) no tienen `image` en su ficha. Cargar por CMS y reemplazar el placeholder
  en `content/quienes-somos/_index.md`.
- **Eventos de prueba** en `content/eventos/` (`evento de prueba/`, `prueba/`): basura que alimenta el
  destacado "próximo seminario" EN VIVO. Limpiar o cargar seminario real por CMS.
- **JSlab:** sin logo ni sitio web; body es borrador (confirmar con Jimena Sierralta).
- Chip del Magíster dice "Postgrado" (= su `tag`); cambiar el tag a "Magíster" en CMS si se prefiere.

## Pages CMS (para Hayo/Francisca)
`app.pagescms.org` → login GitHub → repo `Web`. Commitea directo a la rama elegida (sin preview):
**apuntarlo a `home-etapa3`**, no a `main`. Tras editar por CMS, hacer `git pull` antes de editar local.
Riesgo: puede aplanar listas a string y romper el build (por eso la regla 4).

## Modelos en Claude Code
- Por defecto trabaja en **Sonnet** (edición de plantillas, git, builds: le sobra).
- Sube a **Opus** (`/model`) solo para razonamiento delicado o arquitectura en el código,
  p.ej. blindar `publicaciones`/`proyectos` contra el aplanado de listas del CMS. El chat
  (Opus) avisará cuando una tarea lo amerite.
- **Protocolo de aviso (acordado con Hayo):** al iniciar cada tarea, el chat (Cowork) debe
  recomendar explícitamente Sonnet vs Opus antes de pasar el bloque. Default Sonnet. La
  tarea pendiente que requiere Opus es la 5 (blindar `publicaciones`/`proyectos`).

## Flujo de trabajo con la app Cowork (MODO DUAL)
Hayo trabaja con DOS herramientas en paralelo sobre este repo:
- **El chat de Cowork (Claude app, Opus)** = el cerebro. Planifica, investiga en la web, decide
  arquitectura y **redacta bloques en español listos para pegar** en Claude Code. Revisa los
  diffs/salidas que Hayo le pega de vuelta. **NO ejecuta cambios en el repo.**
- **Claude Code (terminal sobre E:\Git_Use_WebUchile)** = las manos. Edita archivos, corre hugo,
  hace git. Lo maneja Hayo pegando los bloques del chat. **Push a main por defecto al cerrar cada
  tarea con build verde** (ver Política de push; Hayo puede vetar un push puntual).
- El chat NO corre git (su sandbox Linux ve todo el repo como modificado por CRLF/permisos).
- Nota: se probó una vez "edición directa" (el chat editando archivos) y se volvió al modo dual,
  porque Claude Code se confunde con cambios que no hizo. **Mantener modo dual.**
