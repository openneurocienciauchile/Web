# CONTINUACIÓN — Etapa de features (traspaso a hilo nuevo)

Carpeta de trabajo: `E:\Git_Use_WebUchile` (repo clonado, fuera de OneDrive).
Última actualización: 2026-06-07 (tareas 1-3 terminadas).

## Recordatorios vivos (revisar SIEMPRE; el chat los repite al final de cada turno)
- [ ] Logos colaboradores: subir uchile / medicina-uchile / gero / anid (.png o .svg) a
      static/uploads/colaboradores/. Mientras falten, la sección muestra los nombres en texto.
      Fuentes oficiales ya identificadas (Wikimedia, ICBM, anid.cl, gerochile.cl).
- [ ] upgrade.yml: fix commiteado en home-etapa3 (006d68a) pero NO en main → el correo de
      fallo semanal del workflow programado seguirá hasta hacer cherry-pick a main (con OK).
- [ ] GUIA-claude-code-paso-a-paso.md: archivo untracked; decidir si versionar o .gitignore.
- [x] Tarea 5 (blindar publicaciones/proyectos en academicos/single.html): HECHA en Opus.
- [ ] Consistencia menú/títulos: el menú dirá "Actualidad" (→/blog/) y "El Departamento"
      (→/quienes-somos/), pero el title de content/blog/_index.md es "Blog" y el de
      quienes-somos es "Quiénes Somos". Evaluar alinear los títulos de página.

## ⚠️ CÓMO TRABAJAMOS — MODO DUAL (dos ventanas)
1. **Chat de Cowork (Claude app, Opus)** = el cerebro. Planifica, investiga y **entrega bloques
   en español listos para pegar** en Claude Code. Revisa diffs/salidas. NO edita el repo.
2. **Claude Code (terminal sobre E:\Git_Use_WebUchile)** = las manos. Edita, build, git. Lo
   maneja Hayo pegando los bloques. **Nunca push a main sin OK de Hayo.**
Cada ronda: el chat da un bloque → Hayo lo corre → pega de vuelta el diff/salida → el chat revisa
y da el siguiente. Para tareas delicadas, usar Plan Mode (Shift+Tab) en Claude Code.
(Se probó "edición directa" una vez y se descartó: Claude Code se confunde con cambios ajenos.)

## Contexto
Sitio del Depto. de Neurociencia (Fac. Medicina, U. de Chile). Hugo 0.162.1 extended + Hugo Blox
+ Tailwind v4, GitHub Pages bajo `/Web/`. Repo: github.com/openneurocienciauchile/Web.
En vivo: https://openneurocienciauchile.github.io/Web/

## Estado al 2026-06-07
Rama de trabajo `home-etapa3`. Tareas 1-3 hechas y commiteadas:
- 77341fe feat(blog): imagen de portada en el single de noticia (map+string).
- 407d6bf fix(laboratorios): single tolera image string y blinda directores/temas.
- 262a83b feat(laboratorios): Neurosistemas + LAB ONCE completos; borra Lab Prueba.
- a3dd245 feat(landing): tira de logos de labs (labs-strip) bajo Noticias.
Build local y CI: VERDE (229 páginas, 0 errores). Logos en static/uploads/: lab-once-logo.png,
neurosistemas-logo.png. **Publicación a main: PENDIENTE** (ver al final).

## Gotchas críticos
- El chat NO hace git (sandbox ve todo modificado). Git = Claude Code en Windows.
- YAML: valores con `: `/`#`/comillas → entre comillas dobles (si no, rompe el build).
- Dependencias locales: npm, NO pnpm (Windows, bug Hugo #14852). En CI (Ubuntu) pnpm OK.
- El CMS aplana listas → guarda reflect.IsSlice/IsMap en todo range editable. Aplicado en
  afiliacion, publicaciones y proyectos de academicos/single.html.
- Sitio bajo /Web/: usar relURL/.RelPermalink/site.GetPage/site.BaseURL; nunca hardcodear.
- Labs = branch bundles → recorrer con .Sections, no RegularPages. Campo CMS: image + sitio_web.
- term.html ya lista labs por tema (basta poner temas: correctos en cada lab).
- Imágenes: `| relURL` sobre `/uploads/x.png` (slash inicial) PIERDE el `/Web/`. Usar
  `strings.TrimPrefix "/" | relURL`. (Arreglado en labs y temas; ver regla 6 de CLAUDE.md.)
- Modelo: el chat avisa Sonnet vs Opus al inicio de cada tarea. Opus solo para la tarea 5.
- Preview: hugo server.

## Backlog restante
- JSlab (menor): body copiado de LAB ONCE; reescribir summary/body propios y, si hay, logo.
4. Sección institucional/colaboradores en el Landing (U. de Chile, Fac. Medicina, GERO/CEIA/ANID),
   CMS-safe vía data/colaboradores.yaml. Confirmar URLs/logos y qué es "CEIA".
5. ✅ HECHO. Blindados publicaciones y proyectos en academicos/single.html (regla 4).
6. menus.yaml: "Quiénes somos"→"El Departamento"; "Labs" vs "Laboratorios"; quitar "Temas"; agregar "Actualidad".
7. PageFind (buscador navbar; hoy header.search:false).
8. Contacto: formulario vs solo datos.
9. Limpiar deprecations de Hugo.

## Flags de contenido
- Neurosistemas: José Ignacio Egaña quedó como texto (sin ficha); enlazarlo si se crea su ficha.
- LAB ONCE: sitio_web temporal al Wix (hayobk.wixsite.com/labonce) mientras labonce.cl está caído.

## MENSAJE INICIAL para pegar en el nuevo hilo de Cowork
Hola. Continuamos el sitio del Depto. de Neurociencia U. de Chile (repo Hugo en
E:\Git_Use_WebUchile, rama home-etapa3). Lee primero CONTINUACION-etapa-features.md y CLAUDE.md.
Trabajamos en MODO DUAL: tú planificas/investigas y me entregas BLOQUES listos para pegar en
Claude Code; NO editas el repo tú mismo. Yo ejecuto en Claude Code (edits, build, git) y te pego
el diff/salida para que revises. Para tareas delicadas, dime que use Plan Mode. NUNCA push a main
sin mi OK. Confírmame que leíste ambos archivos y resúmeme en 3 líneas el estado y el próximo
pendiente. Luego arrancamos con: [JSlab / tarea 4 / tarea 5].
