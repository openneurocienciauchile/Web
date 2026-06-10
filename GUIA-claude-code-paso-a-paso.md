# Guía paso a paso — Claude Code + flujo híbrido (chat ↔ code)

Para Hayo. Pensada para que no falle nada. Sigue el orden tal cual.

---

## PARTE 0 — El plan híbrido (cuándo uso cada cosa)

Hay dos "Claude" y cada uno sirve para algo distinto:

| Para esto…                                                        | Usa…                          |
|-------------------------------------------------------------------|-------------------------------|
| Escribir/editar código del sitio, correr `hugo`, git, depurar builds | **Claude Code** (terminal)    |
| Planificar, decidir arquitectura/diseño, redactar, ver capturas, buscar en la web, documentos de traspaso | **Chat** (claude.ai / app)    |

**Regla simple:** si la tarea *toca archivos del repo o corre comandos* → Claude Code. Si es *pensar,
decidir o escribir texto* → chat.

**¿Este chat o uno nuevo?** Este hilo ya está largo (gasta más memoria y va más lento). Recomendación:
- **Para construir:** abre **Claude Code** (no es un "hilo", es la terminal en tu PC).
- **Para planificar/diseñar:** abre un **hilo de chat NUEVO** y pega el documento `CONTINUACION-etapa6`
  al inicio. Arranca liviano y rápido.

Los dos comparten contexto vía los documentos: **Claude Code lee `CLAUDE.md`** (lo dejas en el repo) y
**el chat lee el `CONTINUACION-etapa6`** (lo pegas tú).

---

## PARTE 1 — Instalar Claude Code en Windows (una sola vez)

1. Abre **PowerShell** (busca "PowerShell" en el menú inicio; no hace falta admin).

2. Permite ejecutar el instalador (si nunca lo hiciste):
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   Si pregunta, responde `S` (Sí).

3. Instala Claude Code (instalador nativo, no necesita Node.js):
   ```powershell
   irm https://claude.ai/install.ps1 | iex
   ```

4. **Cierra PowerShell y ábrelo de nuevo** (para que reconozca el comando).

5. Verifica que quedó instalado:
   ```powershell
   claude --version
   ```
   Debe imprimir un número de versión. Si dice "no se reconoce el comando", cierra y abre la terminal otra
   vez; si persiste, ve a "Problemas comunes" al final.

---

## PARTE 2 — Dejar el `CLAUDE.md` en el repo y entrar

1. Copia el archivo **`CLAUDE.md`** (te lo entregué) a la **raíz del repo**:
   ```powershell
   Copy-Item "$HOME\Downloads\CLAUDE.md" "D:\Titan-Onedrive\OneDrive\2-Casper\00-Academia\Paginas Web Hayo Made\Depto Neurociencia UChile\Git_Using\Web\CLAUDE.md" -Force
   ```

2. Entra a la carpeta del repo:
   ```powershell
   cd "D:\Titan-Onedrive\OneDrive\2-Casper\00-Academia\Paginas Web Hayo Made\Depto Neurociencia UChile\Git_Using\Web"
   ```

3. Arranca Claude Code:
   ```powershell
   claude
   ```

4. **La primera vez te pedirá iniciar sesión**: se abre el navegador, entras con tu cuenta Claude
   (la misma del Pro/Max), autorizas, y vuelve solo a la terminal. Listo.

---

## PARTE 3 — Tu primera sesión en Claude Code (qué decirle)

Cuando estés dentro de `claude` (verás un prompt esperando que escribas), **pega este mensaje** tal cual:

> Lee el `CLAUDE.md` de la raíz. Antes de tocar nada: confirma que `layouts/temas/term.html` y
> `layouts/_partials/hooks/head-end/custom.html` están commiteados; muéstrame `git status` y la rama
> actual. Luego resincroniza `home-etapa3` con `main` (sin pushear). Después corre el build de
> producción (`$env:HUGO_ENVIRONMENT="production"; hugo --minify`) y dime si queda verde. No hagas push
> a `main`: cuando algo esté listo, lo reviso yo y te aviso. Trabajaremos en `home-etapa3`.

A partir de ahí, le pides las tareas de a una, por ejemplo:

> Tarea 1: en el single de las noticias, muestra la imagen de portada arriba del todo, con buen
> encuadre, igual que en la tarjeta. Valida el build y muéstrame el diff antes de commitear.

**Cómo se trabaja con él (a prueba de tontos):**
- Te va a pedir **permiso** antes de editar archivos o correr comandos. Lee qué propone y aprueba/rechaza.
- Hazlo **de a una tarea**. Cuando termine, abre el preview (`npm run dev` en otra terminal, o pídele que
  lo levante) y míralo.
- Si te gusta, dile **"haz commit en `home-etapa3`"**. Si no, dile qué cambiar.
- **Para publicar en vivo** (merge a `main`) lo decides TÚ explícitamente; Claude Code no lo hará solo.
- Para salir: escribe `/exit` o cierra la terminal. El trabajo queda en los archivos/commits.

Comandos útiles dentro de Claude Code: `/help` (ayuda), `/clear` (limpia el contexto de la charla),
`/exit` (salir).

---

## PARTE 4 — Volver al chat / cuándo

Vuelve al **chat** (un hilo nuevo, pegando `CONTINUACION-etapa6`) cuando necesites:
- decidir **diseño** o arquitectura (ej. cómo se ve la sección institucional, qué colaboradores),
- **redactar** textos, nombres, descripciones,
- analizar una **captura de pantalla** o un error raro,
- **buscar en la web** (URLs/logos de colaboradores, dudas de Hugo),
- actualizar el **documento de traspaso**.

Cuando una decisión del chat afecte el código, se la pasas a Claude Code como instrucción. Y cada cierto
tiempo, pídele al chat (o a Claude Code) que **actualice `CLAUDE.md` y el `CONTINUACION`** para no perder
contexto entre sesiones.

---

## PARTE 5 — Problemas comunes

- **`claude` no se reconoce tras instalar:** cierra y abre la terminal. Si sigue, reinicia el PC (refresca
  el PATH).
- **Bloqueo de archivos / errores git raros:** es OneDrive. Cierra editores/Explorador apuntando a la
  carpeta y reintenta. (A futuro conviene sacar el repo de OneDrive.)
- **El build (`hugo --minify`) tira WARN de "deprecated":** son avisos, no errores; el build igual sirve.
  Solo preocúpate si aparece una línea con `ERROR`.
- **`hugo` se queja de módulos:** corre `hugo mod get` una vez y reintenta.
- **Pages CMS:** apúntalo a `home-etapa3`, no a `main`. Tras editar por el CMS, en tu PC haz `git pull`
  antes de seguir editando local.

---

## Resumen en una frase
**Construir → Claude Code (terminal, lee `CLAUDE.md`). Pensar/diseñar → chat nuevo (lee
`CONTINUACION-etapa6`). Publicar a `main` → solo cuando tú lo apruebes.**
