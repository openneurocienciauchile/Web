# Guía de Proyecto — Sitio Web · Departamento de Neurociencia, U. de Chile

> **Qué es este archivo.** Una guía viva del proyecto del sitio web, pensada para
> dar contexto a Claude (u otra IA) y retomar el trabajo en cualquier momento sin
> tener que reexplicar todo. Se actualiza a medida que el proyecto avanza.
>
> **Cómo usarlo.** Al empezar una sesión, cargar/compartir este archivo y pedir a
> la IA que lo lea primero. Mantener al día las secciones de *Avances*, *Roadmap*
> y *Registro de cambios*.
>
> **Nota de privacidad.** Este repositorio es PÚBLICO. No incluir aquí secretos,
> tokens, contraseñas ni datos personales sensibles. Solo documentación de proyecto.

Última actualización: 2026-06-04

---

## 1. Resumen del proyecto

- **Objetivo:** rediseñar y poner en valor el sitio web del Departamento de
  Neurociencia de la Facultad de Medicina de la Universidad de Chile.
- **Naturaleza:** sitio institucional multi-página, multi-editor, con CMS para que
  personas sin perfil técnico puedan publicar (noticias, eventos, etc.).
- **Dirección de diseño aprobada:** "científico moderno" — base oscura sofisticada,
  frontis real de la Facultad, red neuronal animada, acentos vivos azul→cian,
  secciones limpias.

## 2. Stack y dónde vive

- **Generador:** Hugo (sitio estático) con el tema **Hugo Blox** (módulos de Go;
  base `HugoBlox/kit/templates/academic-cv`).
- **Repositorio:** `https://github.com/openneurocienciauchile/Web` (público).
- **Sitio en vivo:** `https://openneurocienciauchile.github.io/Web/`
  (GitHub Pages, servido bajo el path `/Web/`).
- **Deploy:** vía GitHub Actions, **solo al hacer push/merge a `main`**
  (workflows `deploy.yml` y `hugo.yml`). Las demás ramas NO publican.
  Un PR hacia `main` dispara solo un build de validación (`build.yml`), sin desplegar.

## 3. Estructura relevante del repo

- `content/_index.md` — home (secciones tipo "blocks" de Hugo Blox).
- `content/temas/<slug>/` — 9 áreas temáticas (contenido real).
- `content/academicos/`, `content/laboratorios/`, `content/quienes-somos/`,
  `content/eventos/`, `content/blog/` (noticias), `content/formacion/`, `content/contactos/`.
- `assets/scss/custom.scss` — estilos personalizados del sitio.
- `layouts/_partials/hooks/head-end/custom.html` — se inyecta al `<head>`
  (fuentes, scripts globales, inyección de íconos sociales en la navbar).
- `layouts/_partials/hbx/blocks/{news-grid,evento-card}/block.html` — bloques propios.
- `layouts/_partials/blocks/quienes-somos.html` — partial propio.
- `layouts/_partials/header.html` — área de marca/navbar (⚠ ver Problemas conocidos).
- `static/uploads/` — imágenes servibles por URL (logos, frontis, fotos, etc.).
- `.pages.yml` — configuración del CMS (Pages CMS) para edición no técnica.

## 4. Diagnóstico inicial (estado base del sitio)

Lo que funciona bien:
- Infraestructura real: bloques propios, workflows de deploy, CMS configurado.
- Arquitectura de contenido coherente: 9 áreas temáticas, secciones institucionales.

Lo que falta / conviene corregir (pendiente salvo que se marque hecho):
- **Contenido demo del template aún publicado:** académico de prueba (`academicos/AP`),
  `projects/` (pandas/pytorch/scikit), `publications/` demo, `courses/hugo-blox/`,
  `slides/example/`, noticias/eventos de prueba, `laboratorios/Lab Prueba`.
- **Idioma del sitio en inglés:** `hugo.yaml` con `defaultContentLanguage: en` y
  `languages.yaml` solo `en` (en-us). El contenido es español → debería ser `es`.
- **Identidad vacía:** `params.yaml` `identity.name: " "` → `og:title`/`og:site_name`
  salen en blanco al compartir.
- **Carpetas con espacios** en algunos bundles (URLs/feas, posibles problemas de build).
- **`og:image` apunta a `.svg`** (no renderiza en WhatsApp/LinkedIn → mejor PNG/JPG).
- **`README.md`** sigue siendo el de marketing del template.

## 5. Decisiones de diseño y marca

- **Paleta de marca:** azul **#1C4599** · cian (acento vivo) **#16C8E6** ·
  gris **#66656A**. Tinta oscura de fondo ~#0A1230.
- **Tipografías:** Sora (títulos), IBM Plex Sans (cuerpo), Roboto Condensed
  (rótulos/etiquetas, en eco al logo). Cargadas vía el hook `head-end`.
- **Kit de logos** (provisto por el equipo, carpeta `logos_neurociencia_uchile`):
  - horizontal fondo-claro / fondo-oscuro (+HD); escudo azul/blanco/gris;
    favicons (16/32/48/180/512/.ico); íconos de app.
  - Tipografía del logo: Roboto Condensed. El escudo es raster (para gran formato
    convendría un SVG vectorial a futuro).
- **Hero:** frontis de la Facultad + degradado azul + red neuronal animada (canvas).
- **Navbar (objetivo):** transparente sobre el hero, logo blanco, se vuelve sólida
  azul/navy al hacer scroll (sin franja blanca). *Pendiente — etapa 2.*

## 6. Estrategia Git

Ramas:
- `main` — rama de producción; **solo aquí se despliega**. No se toca hasta aprobar.
- `Respaldo_Manual_20260603` — copia congelada del estado base. **No tocar.**
- `Claude_HBK_Attempt_20260603` — **rama de trabajo** del rediseño.
- `chore/upgrade-hugoblox-*` — ramas automáticas del workflow de actualización del
  tema (se pueden limpiar a futuro; no estorban).

Flujo de trabajo acordado (la IA no hace push; entrega parches):
1. La IA prepara cambios sobre la rama de trabajo y entrega un **parche** (`.patch`).
2. Aplicar con `git am <archivo>.patch` estando en la rama de trabajo.
3. Previsualizar con `hugo server` (recomendado, porque la IA no puede compilar Hugo).
4. `git push` a la rama de trabajo → abrir PR a `main` (build de validación).
5. Revisar el preview; cuando esté conforme, merge a `main` (recién ahí se publica).

## 7. Avances

- **2026-06-04 — Etapa 1 (hero + áreas de investigación):** parche
  `01-rediseno-home-hero-temas.patch`.
  - `content/_index.md`: nuevos bloques `markdown` `hero-neuro` y `temas-home`
    (noticias, seminario y redes sin cambios).
  - `assets/scss/custom.scss`: paleta de marca, estilos de hero y grilla de temas,
    animación de aparición al scroll, fondo del sitio limpio (reemplaza el degradado
    rojo/azul previo).
  - `layouts/_partials/hooks/head-end/custom.html`: fuentes + script de red neuronal;
    se conserva la inyección de íconos sociales.
  - `static/uploads/`: `logo-neurociencia-blanco.png`, `escudo-blanco.png`, `frontis.jpg`.
  - Estado: parche entregado; **pendiente de aplicar/preview/merge**.

## 8. Roadmap (por etapas)

- **Etapa 1 — Hero + áreas de investigación.** *(entregada, por aplicar)*
- **Etapa 2 — Navbar + re-skin de Noticias y Seminario** a la nueva estética
  (requiere preview en vivo por tocar internals del tema).
- **Etapa 3 — Limpieza de contenido demo** del template.
- **Etapa 4 — Configuración:** idioma `es`, identidad del sitio, SEO (`og:image`),
  favicons instalados (`static/`), corregir `README`.
- **Etapa 5 — Poblar contenido real:** académicos, laboratorios, fichas de temas.

## 9. Convenciones técnicas

- El sitio se sirve bajo `/Web/`. Las rutas internas y de assets usan ese prefijo
  (p. ej. `/Web/uploads/frontis.jpg`, `/Web/temas/<slug>/`). Si cambia el `baseURL`,
  revisar estas rutas.
- Patrón de diseño usado: secciones nuevas como **bloques `markdown` con HTML**,
  estilos en `custom.scss` (scoping por `id` de bloque, p. ej. `#hero-neuro`,
  `#temas-home`), fuentes y JS global en el hook `head-end`.
- Imágenes servibles por URL → `static/uploads/`. Imágenes procesadas por el tema →
  `assets/media/`.
- Animación de aparición: clase `.rv` en elementos; el script les agrega `.in`.

## 10. Problemas conocidos / deuda técnica

- `layouts/_partials/header.html` tiene **CSS pegado dentro del HTML** (bug); apunta a
  `/uploads/logo.png`. Revisar/arreglar en la etapa de navbar.
- Hay **dos workflows de deploy** (`deploy.yml` y `hugo.yml`) que se disparan en `main`
  con el mismo grupo de concurrencia `pages` → conviene dejar uno solo a futuro.
- Customizaciones de navbar repartidas entre `header.html`, inyección por JS en
  `head-end` y reglas `!important` en `custom.scss` → consolidar al rediseñar la navbar.
- Múltiples ramas `chore/upgrade-hugoblox-*` acumuladas.

## 11. Cómo retomar con una IA

1. Compartir/cargar este archivo y pedir que lo lea antes de actuar.
2. Indicar en qué etapa estamos (ver *Avances* y *Roadmap*).
3. Recordar las reglas de seguridad git: trabajar en `Claude_HBK_Attempt_20260603`,
   no tocar `main` ni el respaldo, entrega por parches, deploy solo al merge.
4. La IA en este entorno **no puede compilar Hugo** (los módulos del tema se bajan de
   un proxy de Go bloqueado); por eso el preview local/PR es el validador final.

## 12. Registro de cambios

- **2026-06-04** — Creación de la guía. Definida dirección de diseño "científico
  moderno", paleta e tipografías de marca. Creadas ramas de respaldo y de trabajo.
  Entregada Etapa 1 (hero + áreas de investigación) como parche.
