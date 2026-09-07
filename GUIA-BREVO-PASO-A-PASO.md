# Activar el boletín en Brevo — paso a paso, sin supuestos

Sitio: **Departamento de Neurociencia** (`deptoneuro.med.uchile.cl`, repo `openneurocienciauchile/Web`).
Tiempo estimado: 20–30 minutos. Se hace **una sola vez**.

Vas a salir con **cuatro cosas** en la mano, y cada una va a un lugar concreto:

| # | Qué obtienes en Brevo | Dónde lo pegas |
|---|---|---|
| A | Remitente verificado (`hbreinbauer@uchile.cl`) | Nada que pegar: ya está escrito en `data/boletin.yaml` |
| B | **ID de la lista** (un número, p. ej. `7`) | `data/boletin.yaml` → `lista_id` |
| C | **Clave de API** (texto largo `xkeysib-…`) | GitHub → secreto `BREVO_API_KEY` (¡nunca en el repo!) |
| D | **URL del formulario** (`https://….sibforms.com/serve/…`) | `data/boletin.yaml` → `formulario.accion` |

Al final hay un paso E (cargar la lista inicial) y F (probar). Los enlaces directos que doy
te llevan a la pantalla exacta; si Brevo te pide iniciar sesión, entra con la cuenta que usas
para LAB ONCE y vuelve a pegar el enlace.

> Los nombres de menú de Brevo cambian de vez en cuando. Por eso doy **la URL directa** de cada
> pantalla además del camino por menús. Si un botón no se llama exactamente igual, busca el más
> parecido: la pantalla es la misma.

---

## Paso 0 — Abre las dos cosas que vas a editar

1. Abre Brevo en el navegador: <https://app.brevo.com> (cuenta de LAB ONCE).
2. En el Mac, abre el archivo `~/Git_Web/Neurociencia/data/boletin.yaml` con cualquier
   editor de texto (VS Code, TextEdit en modo texto plano…). Vas a tocar solo dos líneas:
   `lista_id:` y `accion:`.

---

## Paso A — Verificar el remitente

Brevo solo deja enviar "desde" un correo que haya comprobado que es tuyo.

1. Ve a **<https://app.brevo.com/senders>** (menú: tu nombre arriba a la derecha → **Senders,
   Domains & Dedicated IPs** → pestaña **Senders**).
2. Mira la lista. **Si ya aparece `hbreinbauer@uchile.cl` con un tic verde / "Verified", salta
   al Paso B.** (Puede estar, si lo verificaste para LAB ONCE.)
3. Si no está: botón **Add a sender**.
   - *From name*: `Departamento de Neurociencia`
   - *From email*: `hbreinbauer@uchile.cl`
   - Guarda.
4. Brevo manda un correo a `hbreinbauer@uchile.cl` con un **código de 6 dígitos** (o un enlace).
   Ábrelo en tu correo uchile (revisa spam si no llega en 2 minutos), copia el código y pégalo
   en la ventana de Brevo → **Verify**.
5. Resultado esperado: el remitente aparece con estado **Verified**.

> ¿Prefieres que el correo salga de otra dirección (p. ej. del Departamento)? Verifica esa en
> vez de la mía y cámbiala en `data/boletin.yaml` → `remitente.correo`. Tiene que ser una
> casilla a la que puedas entrar para leer el código.

**Cuándo NO te tienes que preocupar:** Brevo puede mostrar un aviso amarillo diciendo que el
dominio `uchile.cl` no está "autenticado" (DKIM/DMARC). Eso mejora la entrega pero **no es
obligatorio** para que funcione; requiere tocar el DNS de la Universidad, que no controlas.
Ignóralo por ahora.

---

## Paso B — Crear la lista y anotar su ID

1. Ve a **<https://app.brevo.com/contact/list>** (menú: **Contacts** → **Lists**).
2. Botón **Create a list** (arriba a la derecha).
   - *List name*: `Neurociencia UChile — Noticias`
   - Si pregunta carpeta/folder, deja la que ofrece por defecto.
   - **Create list**.
3. Ahora en la tabla de listas verás tu lista nueva. **El ID es el número que aparece junto al
   nombre**, normalmente en una columna "ID" o entre paréntesis, p. ej. `Neurociencia UChile —
   Noticias (ID 7)`. Si no lo ves, haz clic en la lista: la dirección del navegador termina en
   `/contact/list/7` — ese `7` es el ID.
4. Abre `data/boletin.yaml` y cambia:
   ```yaml
   lista_id: 0
   ```
   por (con TU número):
   ```yaml
   lista_id: 7
   ```
   Sin comillas. Guarda el archivo.

---

## Paso C — Crear la clave de API y guardarla en GitHub

La clave es lo que le permite al robot de GitHub hablar con tu cuenta de Brevo. **Se muestra
una sola vez**: si la pierdes, se crea otra, no pasa nada.

1. Ve a **<https://app.brevo.com/settings/keys/api>** (menú: tu nombre → **SMTP & API** →
   pestaña **API Keys**).
2. Botón **Generate a new API key**.
   - *Name*: `boletin-neurociencia-github`
   - *Expiración*: elige **No expiration** (si no, dentro de un año el boletín dejaría de
     funcionar sin aviso). Si Brevo obliga a poner fecha, anota en tu calendario renovarla.
   - Si aparece una opción "Create MCP server API key", **déjala desmarcada**.
   - **Generate**.
3. Aparece la clave, un texto largo que empieza con `xkeysib-`. Botón **Copy**. **No cierres
   la ventana todavía** hasta terminar el punto 4.
4. Guárdala en GitHub. Dos formas, elige una:

   **Forma 1 — terminal (la más simple).** En Claude Code o en Terminal:
   ```bash
   gh secret set BREVO_API_KEY -R openneurocienciauchile/Web
   ```
   Te dice `? Paste your secret:` → pega la clave (Cmd+V; no se ve nada al pegar, es normal)
   → Enter. Respuesta esperada: `✓ Set Actions secret BREVO_API_KEY for openneurocienciauchile/Web`.
   Si responde "HTTP 403/404" o "not found", es porque `gh` está activo con la cuenta HayoBK:
   corre antes `gh auth switch --user openneurocienciauchile`, repite el `gh secret set`, y
   después vuelve con `gh auth switch --user HayoBK`. O usa la Forma 2, que no depende de eso.

   **Forma 2 — por la web.** Abre
   <https://github.com/openneurocienciauchile/Web/settings/secrets/actions> → **New repository
   secret** → *Name*: `BREVO_API_KEY` (así, en mayúsculas) → *Secret*: pega la clave →
   **Add secret**.
5. Ahora sí, cierra la ventana de Brevo con **OK**. Comprobación: en la página de secretos de
   GitHub debe aparecer `BREVO_API_KEY` con la fecha de hoy.

> Guarda la clave también en tu gestor de contraseñas (1Password/Keychain) con el nombre
> "Brevo API boletín". La vas a necesitar en el Paso E para cargar la lista desde tu Mac.

---

## Paso D — Crear el formulario de suscripción

Este es el formulario que aparece en el sitio ("Recibe las noticias del Departamento en tu
correo"). Brevo lo hospeda; el sitio solo le manda el correo que la persona escribe.

1. Ve a **<https://app.brevo.com/forms>** (menú: **Contacts** → **Forms**, o **Marketing** →
   **Forms**).
2. Botón **Create a form** (o **Create a subscription form**). Si pregunta el tipo, elige
   **Subscription form** / "Sign-up form" (NO pop-up, NO update-profile).
   - *Form name*: `Neurociencia — suscripción noticias`.
3. El editor tiene **4 pasos arriba: Design → Settings → Lists → Share**. En cada uno:

   **Design.** Deja un solo campo: **Email**. Si el formulario trae otros campos (nombre,
   apellido…), bórralos; el sitio solo envía el correo. El aspecto no importa: **el sitio no
   muestra el diseño de Brevo**, usa su propio formulario. Haz clic en **Next** / **Save & next**.

   **Settings.** Aquí está lo importante:
   - Elige **Double confirmation email** ("Double opt-in"). Así la persona recibe un correo
     "confirma tu suscripción" y solo entra a la lista si hace clic. Evita que alguien
     suscriba a otro por molestar. Deja la plantilla de confirmación por defecto (o la de
     LAB ONCE si Brevo la ofrece).
   - Si ofrece "Redirect URL after subscription"/página de éxito, puedes dejarla en blanco.
   - **Next**.

   **Lists.** Marca **solo** la lista `Neurociencia UChile — Noticias` (la del Paso B).
   Desmarca cualquier otra. **Next**.

   **Share.** Es la pantalla donde se obtiene la URL. Verás varias pestañas u opciones:
   *Quick share* (un enlace a una página de Brevo), *Iframe*, y **HTML** (a veces "Simple
   HTML" o "HTML code"). Elige **HTML**.
4. Se muestra un bloque grande de código. **No hay que copiar todo**: busca dentro la línea que
   empieza con `<form` y dentro de ella el trozo `action="https://...sibforms.com/serve/...."`.
   Es un enlace larguísimo (150–250 caracteres) que termina en `==` o similar.
   - Truco: Cmd+F dentro de la caja de código, escribe `action=` y te lleva justo ahí.
   - Copia **solo lo que está entre las comillas** después de `action=`, desde `https://`
     hasta antes de la comilla de cierre.
5. Abre `data/boletin.yaml` y en el bloque `formulario:` cambia
   ```yaml
     accion: ""
   ```
   por (pegando TU enlace, entre comillas dobles, en una sola línea):
   ```yaml
     accion: "https://abcd1234.sibforms.com/serve/MUIFA...=="
   ```
   Guarda.
6. En Brevo pulsa **Save** / **Activate** para que el formulario quede **activo** (algunas
   versiones lo dejan como borrador hasta que confirmas).

> Para saber cómo se ve el enlace correcto: el de LAB ONCE está en
> `~/Git_Web/LabONCE/config/_default/params.yaml`, línea `action:`. El tuyo tendrá la misma
> pinta con otros caracteres.

---

## Checkpoint — publicar la configuración

Ya tocaste `data/boletin.yaml` (dos líneas). Pega esto en Claude Code (Sonnet):

```bash
cd ~/Git_Web/Neurociencia && git diff data/boletin.yaml
HUGO_ENVIRONMENT=production hugo --minify
git add data/boletin.yaml && git commit -m "Boletín: lista y formulario de Brevo configurados"
git checkout main && git pull --ff-only origin main && git merge --ff-only home-etapa3 && git push origin main && git checkout home-etapa3
```

El `git diff` debe mostrar exactamente dos líneas cambiadas (`lista_id` y `accion`). Si
muestra otra cosa, para y pregúntame.

Cuando el deploy termine (1–2 min, pestaña Actions en GitHub, todo verde), abre
<https://deptoneuro.med.uchile.cl/> y baja hasta las noticias: **debe verse la franja
"Boletín — Recibe las noticias del Departamento en tu correo"** con la casilla y el botón.
Además, en Actions verás que corrió por primera vez "Boletín — avisar noticias nuevas por
correo": entra y comprueba que dice **"Nada que avisar"** (correcto: las noticias existentes son
anteriores a `enviar_desde` y no se mandan).

---

## Paso E — Cargar la lista inicial (Paula + académicos)

El archivo `~/Git_Web/Neurociencia/scripts/contactos_iniciales.csv` está en tu Mac (no se
sube al repo). Ábrelo con un editor de texto: es una tabla `correo;nombre`, una persona por
línea. Ya trae a los 20 académicos que tienen correo en su ficha del sitio. Las líneas que
empiezan con `;` son personas **sin correo** (Paula Berzesio y 15 académicos): escribe el correo
delante del `;` en las que conozcas; las que queden vacías simplemente se ignoran.

Luego, en Terminal o Claude Code (reemplaza `xkeysib-…` por tu clave del Paso C):

```bash
cd ~/Git_Web/Neurociencia
~/.venvs/orcid/bin/pip install -q requests PyYAML
BREVO_API_KEY="xkeysib-…" ~/.venvs/orcid/bin/python scripts/boletin.py importar scripts/contactos_iniciales.csv --simular
```

Esto **solo muestra** la lista de gente que va a cargar. Si se ve bien, corre lo mismo **sin**
`--simular`. Respuesta esperada: una línea `✓ correo: creado` por persona. Comprueba en Brevo
(**Contacts → Lists → tu lista**) que aparecen.

> Estos contactos entran **sin** pasar por el correo de confirmación (los cargas tú). Es lo
> normal para una lista interna de colegas. Cualquiera puede darse de baja con el enlace del
> pie de cada correo.

---

## Paso F — Probar de verdad (sin molestar a nadie)

```bash
cd ~/Git_Web/Neurociencia
BREVO_API_KEY="xkeysib-…" ~/.venvs/orcid/bin/python scripts/boletin.py prueba --correo hbreinbauer@uchile.cl --slug Neurofest-2026
```

Te llega **a ti solo** el correo tal como lo recibirían los suscriptores, con la noticia de
NeuroFest. Revisa que se vea la imagen, el título y que el botón "Leer la noticia" abra la
página. Si el correo cae en spam la primera vez, márcalo como "no es spam": es normal con un
remitente nuevo.

Prueba también el formulario del sitio: escribe un correo tuyo distinto (p. ej. gmail) en la
franja → **Suscribirme** → debe decir "¡Gracias! Revisa tu correo…" → te llega el correo de
confirmación de Brevo → haz clic → en Brevo apareces en la lista.

---

## Desde ahora, ¿qué pasa solo?

- Publicas una noticia (Pages CMS o a mano) → push a `main` → deploy → **el correo sale solo**,
  una única vez por noticia, a toda la lista.
- Si una noticia **no** debe salir por correo: desmarca "Avisar por boletín" en el CMS antes de
  publicarla.
- Para mandar a mano una noticia (p. ej. la de NeuroFest, que quedó antes de la fecha de
  arranque): GitHub → **Actions** → "Boletín — avisar noticias nuevas por correo" → **Run
  workflow** → en `slug` escribe `Neurofest-2026` → **Run workflow**.

## Si algo se ve raro

| Ves… | Es porque… | Haz… |
|---|---|---|
| En Actions el boletín dice "solo simulación" | Falta el secreto, o `lista_id` sigue en 0 | Repite Paso C / Paso B |
| `Brevo POST /emailCampaigns → 400` con "sender" | El remitente no está verificado | Paso A |
| `400` con "list" o "recipients" | El `lista_id` no es de tu cuenta | Revisa el número en Paso B |
| `401 Unauthorized` | La clave está mal pegada o expiró | Genera otra (Paso C) y vuelve a `gh secret set` |
| "account not validated" / "not allowed to send campaigns" | Brevo bloquea campañas hasta validar la cuenta nueva | Escribe a soporte de Brevo desde el panel; con la cuenta de LAB ONCE no debería pasar |
| No aparece la franja en el sitio | `accion` quedó vacío o con comillas rotas | Paso D.5; el valor va en UNA línea entre comillas dobles |
| El correo de prueba no llega | Está en spam, o el remitente no está verificado | Revisa spam; Paso A |
