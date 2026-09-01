import os
from urllib.parse import urlsplit, urlunsplit

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def _normalize_db_url(url):
    """SQLAlchemy 2.x ya no acepta el prefijo 'postgres://' que todavía
    entregan algunos proveedores (Render, Heroku, Neon en formatos viejos).
    Lo convertimos a 'postgresql://'. Además forzamos el driver 'pg8000'
    (Python puro, no necesita compilarse) en vez del 'psycopg2' por
    defecto, que da problemas en versiones nuevas de Python en Windows.
    Quitamos también el '?sslmode=require' que traen algunos proveedores,
    porque pg8000 configura el cifrado SSL de otra forma (ver
    SQLALCHEMY_ENGINE_OPTIONS más abajo)."""
    if not url:
        return url
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+pg8000://", 1)
        parts = urlsplit(url)
        url = urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))
    return url


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    SQLALCHEMY_DATABASE_URI = _normalize_db_url(
        os.environ.get("DATABASE_URL")
    ) or f"sqlite:///{os.path.join(BASE_DIR, 'signal.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Postgres (Neon, Render...) exige conexión cifrada. Con el driver
    # pg8000 eso se activa así, no con "?sslmode=require" en la URL.
    SQLALCHEMY_ENGINE_OPTIONS = (
        {"connect_args": {"ssl_context": True}}
        if SQLALCHEMY_DATABASE_URI.startswith("postgresql+pg8000://")
        else {}
    )

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")
    AVATAR_FOLDER = os.path.join(BASE_DIR, "static", "avatars")
    THUMBNAIL_FOLDER = os.path.join(BASE_DIR, "static", "thumbnails")
    MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # 200 MB max upload
    ALLOWED_EXTENSIONS = {"mp4", "webm", "mov", "ogg"}
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}
