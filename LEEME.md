# Web · MC Odontología y Estética Orofacial (Corrientes)

Sitio estático (HTML/CSS/JS). Sin build, sin npm. Se sube arrastrando la carpeta.

## Datos ya cargados desde Facebook

- Nombre: **MC Odontología y Estética Orofacial**
- Ciudad: **Corrientes** — Dirección: **Pago Largo 909 (3400)**
- WhatsApp: **0379 15-427-0427** → cargado como `5493794270427`
- Formación (Sobre mí): Ortodoncia y Ortopedia (en curso); posgrados en Estética, Prótesis Integrada y Endodoncia
- Tratamientos: placa de descanso (bruxismo), ortodoncia y ortopedia, rehabilitación y prótesis, endodoncia, estética dental, encías y prevención
- Reseñas: "100% recomendado en Facebook (7 opiniones)"

## Falta confirmar / completar (no figura en Facebook)

Editá **`lib/manifest.js`**:

| Campo | Estado |
|---|---|
| `professional` | Ma. Carla Mosquera Córdoba (cargado) |
| `email` | od.carlamosquera@gmail.com (cargado) |
| `instagram` | Hoy apunta al Facebook. Cambiá por el Instagram si tenés |
| `whatsappMessage` | Mensaje que se autocompleta al abrir el chat (opcional) |

En `index.html` revisá también: horarios de atención (hoy dice solo "con turno previo"),
y el texto de obras sociales en Preguntas frecuentes.

## Fotos

Reemplazá en `assets/img/` con el **mismo nombre**:

- `retrato.webp` — foto profesional (vertical 4:5)
- `sonrisa-1.webp`, `sonrisa-2.webp`, `sonrisa-3.webp` — casos antes/después

Si están en JPG/PNG, ponelas en `assets/photos/source/` y avisá para convertirlas.
Las actuales son marcadores con el monograma "MC".

## Publicar en Hostinger

1. Administrador de archivos → carpeta `public_html`.
2. Subí **todo el contenido** de esta carpeta, incluido el archivo `.htaccess`.
3. Listo: `tudominio.com` ya muestra el sitio.

En cada cambio futuro de `styles.css` o `main.js`, subí también `index.html` cambiando
`?v=20260906` por la fecha del día (evita ver la versión vieja en caché).

## Carpeta `tools/`

Solo desarrollo. No hace falta subirla.
