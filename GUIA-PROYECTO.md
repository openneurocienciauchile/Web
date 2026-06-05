# Guía de Proyecto — Sitio Web · Departamento de Neurociencia, U. de Chile

> **Qué es este archivo.** Guía viva del proyecto del sitio web, para dar contexto a
> Claude (u otra IA) y retomar el trabajo sin reexplicar todo. Se mantiene al día.
>
> **Privacidad.** El repositorio es PÚBLICO. No incluir secretos, tokens ni datos
> personales sensibles — solo documentación del proyecto.

Última actualización: 2026-06-04

---

## 1. Resumen

Rediseño y mejora del sitio del Departamento de Neurociencia (Facultad de Medicina, U. de Chile).
Sitio institucional, multi-página, multi-editor (con CMS). Identidad de diseño aprobada:
"científico moderno" — fondo azul oscuro, frontis de la Facultad, red neuronal animada,
acentos azul→cian, logo oficial blanco. La navbar es continua con el azul del hero.

## 2. Stack y dónde vive

- **Hugo + Hugo Blox** (Hugo Blox Kit 0.11.0; **Tailwind CSS v4**). Módulos de Go.
- **Repo:** github.com/openneurocienciauchile/Web (público).
- **En vivo:** https://openneurocienciauchile.github.io/Web/ (GitHub Pages, bajo `/Web/`).
- **Deploy:** GitHub Actions, **solo al hacer push/merge a `main`**. Otras ramas no publican;
  un PR a `main` solo corre el build de validación.
- **Build local:** requiere Node + `npm install` (instala el CLI de Tailwind) y luego
  `npm run dev` (= `hugo server --disableFastRender`). El binario `tailwindcss` es
  imprescindible; sin él, el build falla.

## 3. Lecciones técnicas clave (¡importantes!)

- **El tema NO carga `assets/scss/custom.scss`** (usa Tailwind v4, no el pipeline SCSS).
  → Todo el CSS personalizado del rediseño va en un `<style>` dentro de
  `layouts/_partials/hooks/head-end/custom.html` (que sí se inyecta). Clases con prefijo
  `neuro-` para no chocar con Bootstrap/Tailwind (`.btn`, `.lead`, etc.).
- **La navbar la dibuja el tema:** `<header id="site-header">` con `.navbar-brand` (logo,
  desde `assets/media/logo.svg`) y `.nav-link` (menú). Se restiliza por CSS en el head-end.
- **Los PNG "fondo-oscuro" del kit traen el negro HORNEADO** (no son transparentes).
  Para usarlos sobre el azul hay que convertir la luminancia en canal alfa (negro→transparente).
  Así se generó el `logo.svg` blanco transparente del navbar.
- La IA del entorno de trabajo **no puede compilar Hugo** (proxy de módulos bloqueado):
  el preview local (`npm run dev`) o el build del PR es el validador final. **Previsualizar
  SIEMPRE antes de mergear a `main`.**

## 4. Estrategia Git

- `main` — producción; **solo aquí se despliega**.
- `Respaldo_Manual_20260603` — copia congelada del estado base. No tocar.
- Ramas de trabajo: se crea **una rama nueva desde `main`** por cada tanda de cambios,
  se aplica el parche (`git am`), se previsualiza, se sube y se mergea por PR.
- La IA no hace push; entrega **parches `.patch`** numerados que se aplican con `git am`.
- (Ramas viejas `Claude_HBK_Attempt_20260603` y `chore/upgrade-hugoblox-*` se pueden limpiar.)

## 5. Identidad de marca

- **Color:** azul #1C4599 · cian #16C8E6 · gris #66656A · tinta #0A1230.
- **Tipografías:** Sora (títulos), IBM Plex Sans (cuerpo), Roboto Condensed (rótulos).
- **Logo:** kit oficial en `logos_neurociencia_uchile` (horizontal claro/oscuro, escudo,
  favicons, íconos app). En navbar/footer se usa el horizontal blanco (transparentado).
- **Favicons:** del kit, en `static/uploads/` + `<link>` en el head.

## 6. Estado actual (qué hay en producción)

- ✅ **Etapa 1 — Hero + grilla de áreas.** (Rehecha: el CSS vive en head-end, no en SCSS.)
- ✅ **Etapa 2 — Navbar continua azul + logo blanco oficial + favicons.** En producción.
- 🔄 **Etapa 3 — Ajustes de home (EN CURSO):**
  - Texto del hero más sobrio, que refleja una comunidad amplia repartida en facultades,
    sedes y hospitales + red de colaboradores; neurociencia básica y clínica; tradición e
    innovación al servicio de la salud. (Basado en "Quiénes Somos".)
  - **Nodos de la red neuronal más visibles** (mayor opacidad/contraste).
  - **TEMAS eliminado del home** (los íconos de áreas gustaron — reservarlos para reuso).
  - **Noticias como primer contenido** del home + indicador "Noticias ↓" en el hero.

## 7. Diagnóstico del sitio completo (pendientes detectados)

**Contenido demo del template aún presente:** académico de prueba (`academicos/AP`),
`projects/` (pandas/pytorch/scikit), `publications/` demo, `courses/hugo-blox/`,
`slides/example/`, noticias/eventos de prueba, `laboratorios/Lab Prueba`.

**Configuración:** idioma del sitio en inglés (`defaultContentLanguage: en` → debería `es`);
identidad vacía (`identity.name: " "` → og:title/site_name en blanco); `og:image` apunta a un
SVG; `README.md` es el del template.

**Arquitectura de información / menú** (a decidir en conjunto): el menú actual es
Quiénes somos · Académicos · Labs · Temas · Noticias · Eventos · Formación · Contacto.
Preguntas abiertas: ¿"Labs" → "Laboratorios"? ¿qué pasa con "Temas" (se elimina del menú o se
reformula)? ¿"Noticias" y "Eventos" separados o juntos? ¿orden? ¿qué subpáginas cuelgan de cada
sección y con qué título? → esto define títulos de pestañas, breadcrumbs y URLs.

**Re-skin pendiente:** las secciones "Últimas Noticias" y "Próximo Seminario" del home aún usan
el estilo viejo del blox; falta llevarlas a la estética nueva (tarjetas azul→cian, tipografías).

**Páginas internas:** revisar que hereden la identidad visual (encabezados, tipografías,
espaciados) ahora que la navbar es global.

**Deuda técnica:** `layouts/_partials/header.html` está roto (CSS dentro de HTML) y parece sin
uso; hay **dos workflows de deploy** (`deploy.yml` y `hugo.yml`) que conviene unificar; ramas
`chore/upgrade-hugoblox-*` acumuladas; `custom.scss` quedó muerto (se puede vaciar/limpiar).

## 8. Roadmap por etapas (actualizado)

- ✅ **1.** Hero + áreas (rehecha).
- ✅ **2.** Navbar azul + logo blanco + favicons.
- 🔄 **3.** Home: hero sobrio, nodos más visibles, quitar Temas, noticias primero.
- **4. Arquitectura de información / menú:** revisar y fijar títulos, secciones, orden,
  subpáginas y URLs (incluye decidir el futuro de "Temas" y dónde reusar sus íconos).
- **5. Re-skin de Noticias y Seminario** del home a la estética nueva.
- **6. Limpieza de contenido demo** del template.
- **7. Configuración:** idioma `es`, identidad del sitio, SEO (`og:image`), `README`.
- **8. Poblar contenido real:** académicos, laboratorios, "Quiénes somos", contacto.
- **9. Páginas internas:** aplicar identidad visual coherente en todas las secciones.
- **10. Limpieza técnica:** `header.html`, unificar workflows de deploy, vaciar `custom.scss`,
  podar ramas viejas.

## 9. Convenciones técnicas

- El sitio se sirve bajo `/Web/`; rutas internas y assets usan ese prefijo
  (`/Web/uploads/...`, `/Web/temas/...`). Si cambia el `baseURL`, revisarlas.
- Secciones del home: bloques `markdown` con HTML + clases `neuro-` + CSS en el head-end.
  Full-bleed con técnica 100vw.
- Imágenes servibles por URL → `static/uploads/`. Procesadas por el tema → `assets/media/`.
- Aparición al scroll: clase `.neuro-rv` (el script del head-end les agrega `.in`).
- Logo del navbar: `assets/media/logo.svg` (el tema lo inyecta inline).

## 10. Cómo retomar con una IA

1. Leer este archivo primero.
2. Ubicar la etapa actual (§6 y §8).
3. Respetar git: rama nueva desde `main`, parches, preview antes de mergear, no tocar respaldo.
4. Recordar §3 (Tailwind, CSS en head-end, logos con fondo horneado, no se puede compilar Hugo
   en el entorno IA → preview local manda).

## 11. Registro de cambios

- **2026-06-04 (3)** — Etapa 3 en curso: hero con texto sobrio (identidad de comunidad amplia),
  nodos más visibles, Temas fuera del home, Noticias como primer contenido + indicador. Plan
  por etapas actualizado tras revisión completa del sitio.
- **2026-06-04 (2)** — Etapas 1 y 2 en producción (merge a `main`). Navbar continua azul con
  logo blanco oficial (transparentado) y favicons. Documentadas lecciones: el tema usa Tailwind
  (CSS va en head-end), y los PNG "fondo-oscuro" del kit traen el negro horneado.
- **2026-06-04 (1)** — Creación de la guía. Dirección de diseño "científico moderno", paleta y
  tipografías. Ramas de respaldo y trabajo. Primer intento de Etapa 1.
