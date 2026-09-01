import uuid

from flask import (
    Blueprint, render_template, redirect, url_for, flash, request,
    current_app, abort, session
)
from flask_login import login_required, current_user

from extensions import db
from models import Video, Comment, Like, View
from media import save_media

main_bp = Blueprint("main", __name__)


def allowed_file(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def allowed_image(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


@main_bp.route("/")
def index():
    query = request.args.get("q", "").strip()
    videos_query = Video.query.order_by(Video.created_at.desc())
    if query:
        videos_query = videos_query.filter(Video.title.ilike(f"%{query}%"))
    videos = videos_query.all()
    return render_template("index.html", videos=videos, query=query)


def get_viewer_token():
    """Identifica al visitante actual para no contar vistas repetidas:
    'user:<id>' si tiene sesión iniciada, o un id anónimo guardado en su
    cookie de sesión si no."""
    if current_user.is_authenticated:
        return f"user:{current_user.id}"
    if "anon_id" not in session:
        session["anon_id"] = uuid.uuid4().hex
    return f"anon:{session['anon_id']}"


@main_bp.route("/watch/<int:video_id>")
def watch(video_id):
    video = Video.query.get_or_404(video_id)

    token = get_viewer_token()
    already_seen = View.query.filter_by(video_id=video.id, viewer_token=token).first()
    if not already_seen:
        db.session.add(View(video_id=video.id, viewer_token=token))
        video.views = (video.views or 0) + 1
    db.session.commit()

    suggestions = (
        Video.query.filter(Video.id != video.id)
        .order_by(Video.created_at.desc())
        .limit(8)
        .all()
    )
    comments = (
        Comment.query.filter_by(video_id=video.id)
        .order_by(Comment.created_at.desc())
        .all()
    )
    return render_template(
        "watch.html", video=video, suggestions=suggestions, comments=comments
    )


@main_bp.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        external_url = request.form.get("external_url", "").strip()
        file = request.files.get("video_file")
        thumbnail = request.files.get("thumbnail")

        if not title:
            flash("El video necesita un título.", "error")
            return render_template("upload.html")

        video_url = None

        if file and file.filename:
            if not allowed_file(file.filename):
                flash("Formato no permitido. Usa mp4, webm, mov u ogg.", "error")
                return render_template("upload.html")
            video_url = save_media(
                file, "video", current_app.config["UPLOAD_FOLDER"], "uploads"
            )
        elif external_url:
            video_url = external_url
        else:
            flash("Sube un archivo de video o pega un enlace.", "error")
            return render_template("upload.html")

        thumbnail_url = None
        if thumbnail and thumbnail.filename:
            if not allowed_image(thumbnail.filename):
                flash("La miniatura debe ser png, jpg, webp o gif.", "error")
                return render_template("upload.html")
            thumbnail_url = save_media(
                thumbnail, "image", current_app.config["THUMBNAIL_FOLDER"], "thumbnails"
            )

        video = Video(
            title=title,
            description=description,
            video_url=video_url,
            thumbnail_url=thumbnail_url,
            uploader_id=current_user.id,
        )
        db.session.add(video)
        db.session.commit()
        flash("¡Video publicado!", "success")
        return redirect(url_for("main.watch", video_id=video.id))

    return render_template("upload.html")


@main_bp.route("/video/<int:video_id>/like", methods=["POST"])
@login_required
def toggle_like(video_id):
    video = Video.query.get_or_404(video_id)
    existing = Like.query.filter_by(video_id=video.id, user_id=current_user.id).first()
    if existing:
        db.session.delete(existing)
    else:
        db.session.add(Like(video_id=video.id, user_id=current_user.id))
    db.session.commit()
    return redirect(url_for("main.watch", video_id=video.id))


@main_bp.route("/video/<int:video_id>/comment", methods=["POST"])
@login_required
def add_comment(video_id):
    video = Video.query.get_or_404(video_id)
    text = request.form.get("text", "").strip()
    if text:
        db.session.add(Comment(text=text, video_id=video.id, user_id=current_user.id))
        db.session.commit()
    return redirect(url_for("main.watch", video_id=video.id))


@main_bp.route("/video/<int:video_id>/thumbnail", methods=["POST"])
@login_required
def update_thumbnail(video_id):
    video = Video.query.get_or_404(video_id)
    if video.uploader_id != current_user.id:
        abort(403)

    thumbnail = request.files.get("thumbnail")
    if not thumbnail or not thumbnail.filename:
        flash("Selecciona una imagen primero.", "error")
        return redirect(url_for("main.watch", video_id=video.id))
    if not allowed_image(thumbnail.filename):
        flash("La miniatura debe ser png, jpg, webp o gif.", "error")
        return redirect(url_for("main.watch", video_id=video.id))

    video.thumbnail_url = save_media(
        thumbnail, "image", current_app.config["THUMBNAIL_FOLDER"], "thumbnails"
    )
    db.session.commit()
    flash("Miniatura actualizada.", "success")
    return redirect(url_for("main.watch", video_id=video.id))


@main_bp.route("/video/<int:video_id>/delete", methods=["POST"])
@login_required
def delete_video(video_id):
    video = Video.query.get_or_404(video_id)
    if video.uploader_id != current_user.id:
        abort(403)
    db.session.delete(video)
    db.session.commit()
    flash("Video eliminado.", "info")
    return redirect(url_for("main.index"))
