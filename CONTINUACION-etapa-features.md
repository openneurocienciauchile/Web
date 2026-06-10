# CONTINUACIÓN — Sitio Depto. de Neurociencia U. de Chile

Carpeta de trabajo: `E:\Git_Use_WebUchile` (repo clonado, fuera de OneDrive).
Última actualización: 2026-06-09 — **etapa de features CERRADA**.

## Estado: etapa de features CERRADA ✅
Rama `home-etapa3` sincronizada con `main`; todo publicado y desplegado.
En vivo: https://openneurocienciauchile.github.io/Web/

Hecho en esta etapa (todo en main):
- Noticias: imagen de portada en el single.
- Laboratorios: Neurosistemas + LAB ONCE; single/list/strip blindados; logos.
- Landing: tira de logos de labs + sección "Instituciones y colaboradores" (data-driven,
  tarjetas blancas) con logos de U. de Chile, Fac. Medicina, GERO y ANID.
- Académicos: `publicaciones` y `proyectos` blindados contra el aplanado de listas del CMS (regla 4).
- Menús: "El Departamento", "Laboratorios", "Actualidad" (Temas se mantuvo).
- Buscador PageFind operativo (ver gotcha): ruta `/Web/` + `data-pagefind-body` en contenido real
  (académicos, blog, labs, temas, eventos).
- Contacto: página "solo datos" — Av. Independencia 1027, Pabellón H; tel +56 2 2978 6033;
  correo paula.bersezio@uchile.cl (Paula Bersezio, Secretaría Dirección); mapa + redes.
- Fix de imágenes y de links internos: slash inicial en `relURL` perdía el `/Web/` (reglas 5 y 6).
- CI: desactivado el schedule de `upgrade.yml` (fallaba los lunes) y el auto-deploy duplicado de
  `hugo.yml`; `deploy.yml` es el ÚNICO deployer (incluye el índice PageFind). Hugo unificado a 0.162.1.
- `cascade._target` → `cascade.target` (deprecation).

## Recordatorios vivos (revisar SIEMPRE; el chat los repite al final de cada turno)
- [ ] Deprecations del TEMA (`.Site.Data`, `.Site.AllPages`, `.Site.LanguageCode`,
      `.Language.LanguageCode`): NO están en nuestro código, las emite Hugo Blox. Solo se limpian
      actualizando el tema → correr el workflow "Upgrade HugoBlox" manual (Actions → Run workflow),
      revisar el PR, probar build local en 0.162.1, merge. Proyecto aparte, no urgente.
- [ ] Tras cualquier deploy: confirmar en Actions que "Deploy website to GitHub Pages" queda verde.
- [ ] (Opcional) JSlab: body copiado de LAB ONCE; reescribir summary/body propios.
- [ ] (Opcional) Contacto: precisar oficina/piso si se desea.

## ⚠️ CÓMO TRABAJAMOS — MODO DUAL (dos ventanas)
1. **Chat de Cowork (Claude app)** = el cerebro. Planifica, investiga y entrega BLOQUES en español
   listos para pegar en Claude Code. Revisa diffs/salidas. NO edita el repo.
2. **Claude Code (terminal sobre E:\Git_Use_WebUchile)** = las manos. Edita, build, git. Lo maneja
   Hayo pegando los bloques. **Nunca push a main sin OK de Hayo.**
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
- Labs = branch bundles → recorrer con `.Sections`. term.html lista labs por tema.
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
el diff/salida. NUNCA push a main sin mi OK. Al iniciar cada tarea, recomiéndame Sonnet vs Opus.
La etapa de features quedó CERRADA y desplegada. Confírmame que leíste ambos archivos, resúmeme
en 3 líneas el estado, y propón próximos pasos (ej.: actualizar Hugo Blox para limpiar las
deprecations del tema, poblar/depurar contenido, o nuevas features).
