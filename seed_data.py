"""
Lógica de datos de demostración, separada de app.py para poder llamarse
tanto desde el script manual (seed.py) como automáticamente al arrancar
la app en producción, sin generar un import circular.
"""
from extensions import db
from models import User, Video, Like

SAMPLE_BASE = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/"

DEMO_VIDEOS = [
    {
        "title": "Big Buck Bunny — Cortometraje",
        "description": "Un conejo gigante se enfrenta a tres roedores traviesos. "
                        "Cortometraje open-source de Blender Foundation.",
        "file": "BigBuckBunny.mp4",
    },
    {
        "title": "Sintel — Escena principal",
        "description": "Una joven guerrera busca a su dragón perdido. "
                        "Producción abierta de Blender Foundation.",
        "file": "Sintel.mp4",
    },
    {
        "title": "Elephants Dream",
        "description": "El primer cortometraje abierto realizado con Blender.",
        "file": "ElephantsDream.mp4",
    },
    {
        "title": "Tears of Steel",
        "description": "Ciencia ficción: un grupo de guerreros y científicos "
                        "se reúne en Ámsterdam para revertir el pasado.",
        "file": "TearsOfSteel.mp4",
    },
    {
        "title": "For Bigger Blazes",
        "description": "Video de demostración — acción y efectos.",
        "file": "ForBiggerBlazes.mp4",
    },
    {
        "title": "For Bigger Fun",
        "description": "Video de demostración — diversión en movimiento.",
        "file": "ForBiggerFun.mp4",
    },
]


def seed_if_empty():
    """Crea el usuario y los videos de demostración solo si la base de
    datos está vacía. Debe llamarse dentro de un app_context activo."""
    if Video.query.first():
        return False

    demo_user = User.query.filter_by(username="demo").first()
    if not demo_user:
        demo_user = User(username="demo", email="demo@signal.dev")
        demo_user.set_password("demo1234")
        db.session.add(demo_user)
        db.session.commit()

    for item in DEMO_VIDEOS:
        video = Video(
            title=item["title"],
            description=item["description"],
            video_url=SAMPLE_BASE + item["file"],
            uploader_id=demo_user.id,
            views=0,
        )
        db.session.add(video)
    db.session.commit()

    for i, video in enumerate(Video.query.all()):
        if i % 2 == 0:
            db.session.add(Like(video_id=video.id, user_id=demo_user.id))
    db.session.commit()

    return True
