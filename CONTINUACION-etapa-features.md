# CONTINUACIÓN — Sitio Depto. de Neurociencia U. de Chile

Carpeta de trabajo: `E:\Git_Use_WebUchile` (repo clonado, fuera de OneDrive).
Última actualización: 2026-06-10 — **etapa UI/UX CERRADA** (sobre la etapa de features previa).

## Estado: etapa UI/UX CERRADA ✅
Rama `home-etapa3` sincronizada con `main`; todo publicado y desplegado.
En vivo: https://openneurocienciauchile.github.io/Web/

Hecho en la etapa UI/UX (2026-06-10, todo en main):
- Navbar: navy SÓLIDO en páginas internas con `!important` (le gana al header transparente-al-tope
  del tema); regla `html:not(.neuro-home) #site-header{background:linear-gradient(118deg,#09102A,#163482,#0C1A46)!important}`.
  Degradado azul + canvas de "red neuronal" animado inyectado SOLO en navbar interna (no en el HOME).
- Menú móvil: `#nav-menu` con fondo navy bajo `lg` (≤1023px) para que las opciones se lean.
- Redes sociales: SOLO X / Instagram / YouTube (LinkedIn eliminado de todos lados). URLs nuevas:
  X `https://x.com/NeuroUChile`, IG `https://www.instagram.com/neuro_uchile/`,
  YouTube `https://www.youtube.com/@neurocienciauchile6900`. `header.html` confirmado MUERTO (no se
  renderiza); los íconos del navbar salen del script inyectado en `custom.html`.
- Contacto: bajo las redes se dejó SOLO el botón "Cómo llegar" (se quitaron los otros 3 de `.ct-quick`).
- Laboratorios — VISTA DE DETALLE: los labs son secciones (`_index.md`) → Hugo usa `list.html`, NUNCA
  `single.html`. Solución CMS-safe: `list.html` ramifica con `{{ if .Parent.IsHome }}` (portada =
  grilla) `{{ else }}` (lab individual = `{{ partial "lab-single.html" . }}`). Se creó el partial
  `layouts/_partials/lab-single.html` (logo + sitio web + directores + temas + contenido) y se BORRÓ
  `layouts/laboratorios/single.html`. Cuerpo de JSlab corregido (ya no es copia de LAB ONCE).
- Actualidad / Eventos — "próximo seminario": partials reutilizables
  `func/seminario-destacado.html` (→ dict {page,reciente}: próximo seminario futuro; si no hay, el
  pasado más reciente con reciente=true) y `func/eventos-resto.html` (todos los eventos salvo el
  destacado: futuros asc → pasados desc), más `destacado-card.html` (variant hero|aside). El tipo
  seminario/evento ya existía en el CMS (`tipo`). Aplicado en: `eventos/list.html` (destacado + grilla
  del resto con filtros), blox `proximo-seminario` en el Landing (bajo Noticias + botón "Otros eventos"),
  y `blog/list.html` (Actualidad en 2/3 noticias + 1/3 aside: destacado + lista compacta de eventos).
  Decisiones de Hayo: fallback = último seminario realizado; orden del resto = futuros y luego pasados.
- "El Departamento" (`content/quienes-somos/_index.md`, es un `type: landing` con un bloque markdown;
  la plantilla `_partials/blocks/quienes-somos.html` está vacía): rediseño con hero navy (foto del
  equipo `equipo-departamento.jpg` destacada en primer plano + `departamento.jpg` difuminada al fondo),
  título en BLANCO (`.dep-h1{color:#fff!important}` porque el tema pinta los h1 oscuros), texto a ancho
  completo (franjas full-bleed `left:50%/-50vw` para escapar del contenedor angosto del bloque markdown),
  misiones en tarjetas con íconos SVG, franja "Nuestro Jefe de Departamento" (José Luis Valdés) y
  "Consejo de Departamento" (6 fotos enlazadas: Sierralta, Morales, Fuentes, Olguín, Rivera, Breinbauer).
- "Formación" (`layouts/formacion/list.html`): rediseño elegante, dos tarjetas grandes con el título
  del Diplomado y del Magíster destacados (Sora + subrayado animado + chip de tipo). Conserva la lógica
  `external_link`. CSS propio en la misma plantilla con prefijo `form-`.
- POLÍTICA DE PUSH: a partir de hoy cada tarea cierra con push a `main` si el build queda verde
  (Hayo pre-autorizó; puede vetar un push puntual). Documentado en CLAUDE.md.

## Recordatorios vivos (revisar SIEMPRE; el chat los repite al final de cada turno)
- [ ] Deprecations del TEMA (`.Site.Data`, `.Site.AllPages`, `.Site.LanguageCode`,
      `.Language.LanguageCode`): NO están en nuestro código, las emite Hugo Blox. Solo se limpian
      actualizando el tema → correr el workflow "Upgrade HugoBlox" manual (Actions → Run workflow),
      revisar el PR, probar build local en 0.162.1, merge. Proyecto aparte, no urgente.
- [ ] Tras cualquier deploy: confirmar en Actions que "Deploy website to GitHub Pages" queda verde.
- [ ] FOTOS faltantes (hoy con iniciales): **José Luis Valdés** y **Paola Morales** (eugenia-morales)
      no tienen `image` en su ficha → cargar por CMS y reemplazar el placeholder de iniciales por la foto
      en `content/quienes-somos/_index.md` (cards `.dep-person`/`.dep-jefe`).
- [ ] EVENTOS DE PRUEBA: existen `content/eventos/evento de prueba/` y `content/eventos/prueba/` (datos
      basura). Mientras estén, el destacado de "próximo seminario" muestra el de prueba EN VIVO. Limpiar
      con `git rm -r` o cargar un seminario real por CMS.
- [ ] (Opcional) JSlab: falta logo (no hay archivo) y sitio web; body es un borrador a confirmar con
      Jimena Sierralta. Cargar logo/web por CMS.
- [ ] (Opcional) Chip del Magíster dice "Postgrado" (viene del `tag`); cambiar el tag a "Magíster" en CMS
      si se quiere ese rótulo.
- [ ] (Opcional) Verificar que la foto `static/uploads/equipo-departamento.jpg` quedó cargada (la dejó Hayo).
- [ ] (Opcional) Contacto: precisar oficina/piso si se desea.

## ⚠️ CÓMO TRABAJAMOS — MODO DUAL (dos ventanas)
1. **Chat de Cowork (Claude app)** = el cerebro. Planifica, investiga y entrega BLOQUES en español
   listos para pegar en Claude Code. Revisa diffs/salidas. NO edita el repo.
2. **Claude Code (terminal sobre E:\Git_Use_WebUchile)** = las manos. Edita, build, git. Lo maneja
   Hayo pegando los bloques. **Push a main por defecto al cerrar cada tarea con build verde**
   (Hayo lo pre-autorizó 2026-06-09; puede vetar un push puntual).
Cada ronda: el chat da un bloque → Hayo lo corre → pega el diff/salida → el chat revisa.
Excepción útil: archivos binarios (logos) los deja Hayo en disco; el chat no puede escribirlos.
Modelo: el chat recomienda Sonnet vs Opus al iniciar cada tarea (default Sonnet).

## Contexto
Sitio del Depto. de Neurociencia (Fac. Medicina, U. de Chile). Hugo 0.162.1 extended + Hugo Blox
+ Tailwind v4, GitHub Pages bajo `/Web/`. Repo: github.com/openneurocienciauchile/Web.
Ramas: `main` = producción (deploy automático) · `home-etapa3` = trabajo.

## Gotchas críticos
- El chat NO hace git (su sandbox ve todo modificado). Git = Claude Code en Windows.
- YAML: valores con `: `/`#`/comillas → entre comillas dobles (si no, rompe el build).
- Dependencias locales: npm, NO pnpm (Windows, bug Hugo #14852). En CI (Ubuntu) pnpm OK.
- CMS aplana listas → guarda `reflect.IsSlice`/`IsMap` en todo range editable. Aplicado en
  afiliacion, publicaciones y proyectos (academicos/single.html).
- **relURL sin slash inicial**: `"/x" | relURL` pierde el `/Web/` (imagen rota / link 404).
  Imágenes: `strings.TrimPrefix "/" | relURL`. Links: `"ruta/" | relURL` o `.RelPermalink`.
  (Reglas 5 y 6 de CLAUDE.md.)
- **PageFind**: requiere (a) `window.hbb.assetPaths.pagefind` con ruta `/Web/` (en custom.html), y
  (b) `data-pagefind-body` en las plantillas custom de contenido — si alguna página lo usa,
  PageFind EXCLUYE toda página que no lo tenga. El índice se genera en `deploy.yml`
  (`pnpm run pagefind`); NO se prueba con `hugo server` (probar: `pnpm run pagefind` + servir public/).
- Deploy: `deploy.yml` es el único auto-deployer; `hugo.yml` quedó desactivado. Hugo 0.162.1 en
  `hugoblox.yaml` = versión local (CI = validación local).
- Labs = branch bundles → recorrer con `.Sections`. term.html lista labs por tema. La ficha de un lab
  individual NO usa `single.html` (es sección); `list.html` ramifica con `.Parent.IsHome` y delega el
  detalle al partial `lab-single.html`.
- Páginas que son `type: landing` con bloque markdown (HOME, quienes-somos): el tema mete el HTML en un
  contenedor angosto → para ancho completo usar el truco full-bleed `left:50%;margin-left:-50vw;width:100vw`.
  Además el tema pinta los `h1` oscuros → si el título va sobre fondo navy, forzar `color:#fff !important`.
- Preview local: `hugo server`. Build CI: `HUGO_ENVIRONMENT=production hugo --minify`.

## Flags de contenido
- Neurosistemas: José Ignacio Egaña quedó como texto (sin ficha); enlazar si se crea su ficha.
- LAB ONCE: sitio_web temporal al Wix (hayobk.wixsite.com/labonce) mientras labonce.cl está caído.
- Logo Fac. Medicina: trae fondo oscuro incrustado (recuadro oscuro en la tarjeta blanca); cambiar
  si se consigue versión con fondo transparente.

## MENSAJE INICIAL para pegar en el nuevo hilo de Cowork
Hola. Sitio del Depto. de Neurociencia U. de Chile (repo Hugo en E:\Git_Use_WebUchile; ramas
main = producción / home-etapa3 = trabajo). Lee primero CONTINUACION-etapa-features.md y CLAUDE.md.
Trabajamos en MODO DUAL: tú planificas/investigas y me entregas BLOQUES en español listos para
pegar en Claude Code; NO editas el repo. Yo ejecuto en Claude Code (edits, build, git) y te pego
el diff/salida. Push a main por defecto al cerrar cada tarea con build verde (puedo vetar un push
puntual). Al iniciar cada tarea, recomiéndame Sonnet vs Opus.
La etapa UI/UX quedó CERRADA y desplegada. Confírmame que leíste ambos archivos, resúmeme
en 3 líneas el estado, y propón próximos pasos (ej.: cargar/limpiar contenido real de eventos y
fotos faltantes del Consejo, actualizar Hugo Blox para limpiar las deprecations del tema, o nuevas features).
