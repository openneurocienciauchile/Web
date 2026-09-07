# Guía — Boletín de noticias por correo (Departamento de Neurociencia)

Cada noticia nueva publicada en `content/blog/` se avisa por correo a los
suscriptores, con título, fecha, resumen, imagen de portada y botón a la noticia.
El sitio tiene además una franja de suscripción (Home y Actualidad).

Repo: `github.com/openneurocienciauchile/Web` · Sitio: `https://deptoneuro.med.uchile.cl/`

---

## 1. Cómo funciona (para entenderlo en un minuto)

| Pieza | Qué hace |
|---|---|
| `data/boletin.yaml` | Configuración: remitente, ID de la lista, fecha desde la que se avisa, textos del correo y URL del formulario. Editable por Pages CMS ("Boletín"). |
| `scripts/boletin.py` | Arma el correo y lo manda a la lista como **campaña de Brevo**. |
| `.github/workflows/boletin.yml` | Corre el script **después de cada despliegue exitoso** a `main`, para que el enlace ya esté en línea. También se puede lanzar a mano. |
| `layouts/_partials/boletin.html` | Formulario de suscripción (franja). Si `formulario.accion` está vacío, no se muestra. |
| Secreto `BREVO_API_KEY` | Clave de la API de Brevo, guardada en GitHub (Settings → Secrets → Actions). Nunca en el repo. |

**Reglas de envío**
- Se avisa una sola vez por noticia. Cada envío deja en Brevo una campaña llamada
  `noticia:<carpeta>`; si ya existe, no se repite. No hay estado en el repo.
- No se avisan: borradores (`draft: true`), noticias con `boletin: false`
  (en el CMS: casilla "Avisar por boletín" desmarcada) ni las anteriores a
  `enviar_desde` (hoy `2026-09-04`: las noticias ya publicadas no se mandan).
- Antes de mandar, comprueba que la URL de la noticia responda 200. Si no, no manda
  un enlace roto y lo reintenta en el próximo despliegue.
- Freno: máximo 3 noticias por corrida automática.
- `activo: false` en `data/boletin.yaml` apaga todo el envío.

**La lista de correos vive en Brevo**, no en el repositorio (que es público).

---

## 2. Activarlo — cuatro pasos en Brevo + un secreto (una sola vez)

Sirve la misma cuenta de Brevo que usa LAB ONCE.

1. **Remitente verificado.** Brevo → *Senders & IP → Senders → Add a sender* con el
   correo que dice `remitente.correo` en `data/boletin.yaml` (hoy `hbreinbauer@uchile.cl`).
   Llega un código al correo. Sin esto la API rechaza la campaña.
2. **Lista.** *Contacts → Lists → Create a list*, p. ej. "Neurociencia UChile — Noticias".
   Anotar su **ID numérico** (sale junto al nombre) en `lista_id` de `data/boletin.yaml`.
3. **Clave de API.** Perfil → *SMTP & API → API Keys → Generate a new API key*.
   Guardarla en GitHub:
   ```bash
   gh secret set BREVO_API_KEY -R openneurocienciauchile/Web
   ```
   (pega la clave cuando la pida). O por web: repo → Settings → Secrets and variables →
   Actions → New repository secret → nombre `BREVO_API_KEY`.
4. **Formulario de suscripción.** *Contacts → Forms → Create a subscription form*,
   asociado a esa lista y con **doble opt-in** (así nadie suscribe a otro). En el paso
   *Share*, copiar del código HTML el atributo `action="https://….sibforms.com/serve/…"`
   y pegarlo en `formulario.accion` de `data/boletin.yaml`. Con eso aparece la franja
   en el sitio.

> Si Brevo responde que la cuenta no está validada para campañas, hay que pedir la
> validación desde el panel (trámite único de la cuenta).

---

## 3. Cargar la lista inicial

El archivo `scripts/contactos_iniciales.csv` (está en `.gitignore`, **no se sube**) trae
a Paula Berzesio y a todos los académicos con correo en su ficha. Completa los que
faltan (Paula y los académicos sin correo) y cárgalo:

```bash
cd ~/Git_Web/Neurociencia
~/.venvs/orcid/bin/pip install requests PyYAML          # por si faltan
BREVO_API_KEY=xxxx ~/.venvs/orcid/bin/python scripts/boletin.py importar scripts/contactos_iniciales.csv --simular   # mira
BREVO_API_KEY=xxxx ~/.venvs/orcid/bin/python scripts/boletin.py importar scripts/contactos_iniciales.csv             # carga
```

Formato del CSV: `correo;nombre`, una fila por persona; las filas sin correo se ignoran.
También puedes agregar gente directamente en Brevo (*Contacts → Add a contact*).

---

## 4. Probar antes de la primera noticia real

```bash
cd ~/Git_Web/Neurociencia
~/.venvs/orcid/bin/python scripts/boletin.py enviar --simular            # qué mandaría hoy
~/.venvs/orcid/bin/python scripts/boletin.py vista-previa --slug Neurofest-2026   # escribe boletin-vista-previa.html
BREVO_API_KEY=xxxx ~/.venvs/orcid/bin/python scripts/boletin.py prueba --correo tu@correo.cl --slug Neurofest-2026
```

`prueba` manda el correo real a una sola dirección (sin tocar la lista).

---

## 5. Uso diario

- **Publicar una noticia** (Pages CMS o a mano) y hacer push a `main`. Cuando el
  despliegue termina en verde, el workflow "Boletín — avisar noticias nuevas por
  correo" la manda. Se ve en la pestaña *Actions*.
- **Que una noticia NO salga por correo:** desmarcar "Avisar por boletín" en el CMS
  (o `boletin: false` en el front-matter) **antes** de publicarla.
- **Mandar una noticia puntual o antigua:** Actions → "Boletín — avisar noticias
  nuevas por correo" → *Run workflow* → `slug` = nombre de su carpeta en
  `content/blog/` (p. ej. `Neurofest-2026`). `reenviar` la repite aunque ya exista;
  `simular` solo muestra.
- **Ver qué se mandó:** en Brevo (*Campaigns*) o `python scripts/boletin.py enviados`.
- **Cambiar textos, remitente o lista:** Pages CMS → "Boletín", o `data/boletin.yaml`.

---

## 6. Si algo falla

| Síntoma | Causa probable | Qué hacer |
|---|---|---|
| El workflow corre pero dice "solo simulación" | Falta `BREVO_API_KEY`, `lista_id` es 0 o `activo: false` | Completar paso 2 |
| "Brevo POST /emailCampaigns → 400 … sender" | Remitente no verificado | Paso 2.1 |
| "La URL no responde 200" | El CDN de Pages aún no publicó | Nada: reintenta en el próximo deploy, o *Run workflow* con el slug |
| Cuenta "not validated" | Brevo exige validar la cuenta para campañas | Pedir validación en el panel de Brevo |
| No aparece la franja | `formulario.accion` vacío | Paso 2.4 |
| Se mandó una noticia dos veces | Se usó `reenviar` o se cambió el nombre de la carpeta | El nombre de la carpeta es la llave: no renombrar noticias ya avisadas |
