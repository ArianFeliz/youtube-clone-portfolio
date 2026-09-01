"""
Borra los comentarios creados por el usuario 'demo', sin tocar videos,
likes ni otros usuarios. Útil si ya sembraste la base de datos con una
versión anterior de seed.py que sí creaba comentarios de ejemplo.

Uso:
    python clean_demo_comments.py
"""
from app import create_app
from extensions import db
from models import User, Comment


def clean():
    app = create_app()
    with app.app_context():
        demo_user = User.query.filter_by(username="demo").first()
        if not demo_user:
            print("No existe un usuario 'demo' en esta base de datos.")
            return

        deleted = Comment.query.filter_by(user_id=demo_user.id).delete()
        db.session.commit()
        print(f"Listo: se borraron {deleted} comentarios del usuario demo.")


if __name__ == "__main__":
    clean()
