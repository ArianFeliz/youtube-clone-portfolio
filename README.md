# Signal 📡

Una plataforma de video estilo YouTube construida con **Flask**, pensada como
proyecto de portafolio. Incluye autenticación de usuarios, subida de videos
(archivo local o enlace externo), likes y comentarios, con una identidad
visual propia (tema "señal de transmisión").

DEMO EN VIVO: https://signal-youtube-clone.onrender.com/

## ✨ Características

- Registro / inicio de sesión de usuarios (Flask-Login)
- Subida de videos: archivo local **o** enlace directo a un video
- Página de reproducción con vistas, likes y comentarios
- Búsqueda de videos por título
- Miniaturas generadas por gradiente (sin depender de imágenes externas)
- Datos de demostración listos para usar (`seed.py`) con videos de código
  abierto de Blender Foundation, para que el proyecto se vea completo
  apenas lo clonas — sin necesidad de subir archivos de video pesados a Git

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

## 🛠️ Stack técnico

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Login
- **Base de datos:** SQLite en local; Postgres (Neon) en producción vía `DATABASE_URL`
- **Archivos subidos:** disco local en desarrollo; Cloudinary en producción vía `CLOUDINARY_URL` (opcional, ver sección de despliegue)
- **Frontend:** Jinja2 + CSS puro (sin frameworks de JS)

