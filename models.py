from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db

# Paleta usada para generar miniaturas por gradiente (sin imágenes externas)
THUMB_PALETTES = [
    ("#FFB020", "#FF7A59"),
    ("#4FD1C5", "#2E7D8C"),
    ("#7C5CFF", "#3A2E8C"),
    ("#FF5C8A", "#B0206B"),
    ("#4FD16B", "#1F8C4C"),
    ("#20A4FF", "#1F4C8C"),
]


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    videos = db.relationship("Video", backref="uploader", lazy=True, cascade="all, delete-orphan")
    comments = db.relationship("Comment", backref="author", lazy=True, cascade="all, delete-orphan")
    likes = db.relationship("Like", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    video_url = db.Column(db.String(500), nullable=False)  # local o de Cloudinary
    thumbnail_url = db.Column(db.String(500), nullable=True)  # local o de Cloudinary
    views = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    uploader_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    comments = db.relationship("Comment", backref="video", lazy=True, cascade="all, delete-orphan")
    likes = db.relationship("Like", backref="video", lazy=True, cascade="all, delete-orphan")
    view_records = db.relationship("View", backref="video", lazy=True, cascade="all, delete-orphan")

    @property
    def thumb_colors(self):
        return THUMB_PALETTES[self.id % len(THUMB_PALETTES)]

    @property
    def like_count(self):
        return len(self.likes)

    def liked_by(self, user):
        if not user or not user.is_authenticated:
            return False
        return any(like.user_id == user.id for like in self.likes)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class Like(db.Model):
    __tablename__ = "likes"

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    __table_args__ = (db.UniqueConstraint("video_id", "user_id", name="unique_like"),)


class View(db.Model):
    """Registra quién ya vio un video para no contar vistas repetidas.

    'viewer_token' identifica al visitante: 'user:<id>' si tiene sesión
    iniciada, o 'anon:<uuid>' guardado en su cookie de sesión si es anónimo.
    """
    __tablename__ = "views"

    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey("video.id"), nullable=False)
    viewer_token = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint("video_id", "viewer_token", name="unique_view"),)
