# Signal 📡

Una plataforma de video estilo YouTube construida con **Flask**, pensada como
proyecto de portafolio. Incluye autenticación de usuarios, subida de videos
(archivo local o enlace externo), likes y comentarios, con una identidad
visual propia (tema "señal de transmisión").

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-black)

## ✨ Características

- Registro / inicio de sesión de usuarios (Flask-Login)
- Subida de videos: archivo local **o** enlace directo a un video
- Página de reproducción con vistas, likes y comentarios
- Búsqueda de videos por título
- Miniaturas generadas por gradiente (sin depender de imágenes externas)
- Datos de demostración listos para usar (`seed.py`) con videos de código
  abierto de Blender Foundation, para que el proyecto se vea completo
  apenas lo clonas — sin necesidad de subir archivos de video pesados a Git

## 🚀 Instalación y ejecución local

```bash
# 1. Clona el repositorio
git clone <tu-repo-url>
cd youtube-clone

# 2. Crea un entorno virtual
python -m venv venv
source venv/bin/activate      # En Windows: venv\Scripts\activate

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Pobla la base de datos con datos de ejemplo
python seed.py

# 5. Ejecuta la app
python app.py
```

Abre `http://localhost:5000` en tu navegador.

**Cuenta de demostración:** usuario `demo`, contraseña `demo1234`.

## 🗂️ Estructura del proyecto

```
youtube-clone/
├── app.py              # Fábrica de la app Flask
├── config.py            # Configuración (DB, uploads, etc.)
├── extensions.py         # db y login_manager
├── models.py             # Modelos: User, Video, Comment, Like, View
├── auth.py               # Rutas de autenticación y perfil
├── main.py               # Rutas principales (home, watch, upload...)
├── seed_data.py            # Datos de demostración (reutilizable)
├── seed.py                  # Script manual para sembrar en local
├── clean_demo_comments.py    # Utilidad de limpieza puntual
├── render.yaml                 # Blueprint de despliegue en Render
├── Procfile                     # Comando de arranque en producción
├── templates/                     # Plantillas Jinja2
└── static/
    ├── css/style.css                # Estilos (identidad visual propia)
    ├── uploads/                       # Videos subidos (ignorado por git)
    ├── avatars/                        # Fotos de perfil (ignorado por git)
    └── thumbnails/                      # Miniaturas subidas (ignorado por git)
```

## 🌐 Desplegar en vivo (Render + Neon + Cloudinary)

Así cualquiera que entre a tu repositorio puede usar la app real —
registrarse, subir sus propios videos y que esos archivos **persistan
de verdad**, no solo durante la sesión.

- **Render** corre la app.
- **Neon** guarda la base de datos (usuarios, videos, likes, comentarios)
  — Postgres gratis de forma permanente, a diferencia del Postgres
  gratis de Render que expira a los 30 días.
- **Cloudinary** guarda los archivos que la gente suba (video, avatar,
  miniatura) — gratis, sin tarjeta, y persisten para siempre sin
  importar que el servidor se reinicie. Esto es necesario porque
  ningún hosting gratuito da disco permanente en el servidor mismo;
  la solución real es no depender de él.

**Límite del plan gratis de Render:** el servicio "duerme" tras 15 min
sin visitas y tarda unos 30-60 segundos en despertar en la siguiente
visita. Es normal, no es un error.

### 1. Crea la base de datos en Neon

1. Ve a [neon.tech](https://neon.tech) y crea una cuenta gratis.
2. Crea un proyecto nuevo.
3. Copia el **Connection string** (empieza con `postgresql://...`).

### 2. Crea el almacenamiento en Cloudinary

1. Ve a [cloudinary.com](https://cloudinary.com) y crea una cuenta gratis.
2. En el dashboard principal copia el **API Environment variable**
   — se ve así: `CLOUDINARY_URL=cloudinary://123456789:abcdefg@tu-cloud-name`.
   Guarda el valor completo, incluyendo `cloudinary://`.

### 3. Despliega en Render

1. Sube este proyecto a un repositorio en GitHub.
2. Ve a [render.com](https://render.com) y crea una cuenta gratis.
3. Click en **New +** → **Blueprint**, y conecta tu repositorio
   (Render detecta el archivo `render.yaml` incluido en el proyecto).
4. Cuando te pida las variables, pega:
   - `DATABASE_URL` → el connection string de Neon
   - `CLOUDINARY_URL` → el valor completo de Cloudinary
5. Dale a **Apply**. Render instala dependencias y arranca la app sola.
6. Cuando termine, te da una URL pública (algo como
   `https://signal-youtube-clone.onrender.com`) — esa es tu app en vivo.

La primera vez que arranca, la app crea las tablas y siembra los 6
videos de ejemplo automáticamente — no necesitas correr ningún comando
a mano en el servidor. A partir de ahí, cualquiera que entre puede
registrarse y subir sus propios videos, avatares y miniaturas, y esos
archivos van a quedar guardados en Cloudinary de forma permanente.

**Nota:** si no configuras `CLOUDINARY_URL`, la app sigue funcionando
igual pero los archivos subidos como archivo (no como enlace) se
pierden cuando Render reinicie el contenedor.



## 🛠️ Stack técnico

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Login
- **Base de datos:** SQLite en local; Postgres (Neon) en producción vía `DATABASE_URL`
- **Archivos subidos:** disco local en desarrollo; Cloudinary en producción vía `CLOUDINARY_URL` (opcional, ver sección de despliegue)
- **Frontend:** Jinja2 + CSS puro (sin frameworks de JS)

## 📌 Notas

- En local, sin `CLOUDINARY_URL` configurado, los archivos subidos se
  guardan en `static/uploads/`, `static/avatars/` y `static/thumbnails/`,
  excluidos del repositorio mediante `.gitignore` para mantenerlo liviano.
- Los videos de la demo se sirven desde enlaces públicos externos, así que
  la app funciona "de fábrica" para cualquiera que la clone y ejecute.
- Para producción, cambia `SECRET_KEY` y usa `DATABASE_URL` (Postgres) y
  `CLOUDINARY_URL` (ver sección de despliegue arriba).

## 📄 Licencia

MIT
