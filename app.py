import os
from datetime import datetime

from flask import Flask

from config import Config
from extensions import db, login_manager
from models import User


def timesince(dt):
    if not dt:
        return ""
    diff = datetime.utcnow() - dt
    seconds = diff.total_seconds()
    if seconds < 60:
        return "justo ahora"
    if seconds < 3600:
        return f"hace {int(seconds // 60)} min"
    if seconds < 86400:
        return f"hace {int(seconds // 3600)} h"
    if seconds < 2592000:
        return f"hace {int(seconds // 86400)} d"
    return dt.strftime("%d/%m/%Y")


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    app.jinja_env.filters["timesince"] = timesince

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from auth import auth_bp
    from main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["AVATAR_FOLDER"], exist_ok=True)
    os.makedirs(app.config["THUMBNAIL_FOLDER"], exist_ok=True)

    with app.app_context():
        db.create_all()
        from seed_data import seed_if_empty
        seed_if_empty()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
