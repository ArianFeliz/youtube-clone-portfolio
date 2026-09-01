"""
Guarda archivos subidos por el usuario (video, avatar, miniatura).

Si la variable de entorno CLOUDINARY_URL está configurada, los sube a
Cloudinary (persisten para siempre, sin importar qué le pase al disco
del servidor). Si no está configurada, los guarda en el disco local
—perfecto para desarrollo en tu máquina, donde no hace falta crear
ninguna cuenta externa.
"""
import os
from datetime import datetime

from werkzeug.utils import secure_filename

_cloudinary_configured = False


def cloudinary_enabled():
    return bool(os.environ.get("CLOUDINARY_URL"))


def _ensure_cloudinary_configured():
    global _cloudinary_configured
    if not _cloudinary_configured:
        import cloudinary
        cloudinary.config(cloudinary_url=os.environ["CLOUDINARY_URL"], secure=True)
        _cloudinary_configured = True


def save_media(file_storage, resource_type, local_folder, static_subpath):
    """
    file_storage: el archivo tal como llega de request.files.get(...)
    resource_type: "video" o "image" (solo se usa para Cloudinary)
    local_folder: carpeta absoluta en disco donde guardarlo si no hay Cloudinary
    static_subpath: "uploads", "avatars" o "thumbnails" (para construir la URL local)

    Devuelve la URL final, lista para usar en un <video src> o <img src>.
    """
    if cloudinary_enabled():
        _ensure_cloudinary_configured()
        import cloudinary.uploader
        result = cloudinary.uploader.upload(
            file_storage,
            resource_type=resource_type,
            folder=f"signal/{static_subpath}",
        )
        return result["secure_url"]

    filename = secure_filename(file_storage.filename)
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
    filename = f"{timestamp}_{filename}"
    save_path = os.path.join(local_folder, filename)
    file_storage.save(save_path)
    return f"/static/{static_subpath}/{filename}"
