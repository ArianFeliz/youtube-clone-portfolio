from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, current_app
)
from flask_login import login_user, logout_user, login_required, current_user

from extensions import db
from models import User
from media import save_media

auth_bp = Blueprint("auth", __name__)


def allowed_image(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_IMAGE_EXTENSIONS"]


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not username or not email or not password:
            flash("Completa todos los campos.", "error")
        elif User.query.filter_by(username=username).first():
            flash("Ese nombre de usuario ya existe.", "error")
        elif User.query.filter_by(email=email).first():
            flash("Ese correo ya está registrado.", "error")
        elif len(password) < 6:
            flash("La contraseña debe tener al menos 6 caracteres.", "error")
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash(f"¡Bienvenido, {username}!", "success")
            return redirect(url_for("main.index"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier)
        ).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f"Sesión iniciada como {user.username}.", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.index"))

        flash("Usuario o contraseña incorrectos.", "error")

    return render_template("login.html")


@auth_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        new_username = request.form.get("username", "").strip()
        photo = request.files.get("avatar")

        if not new_username:
            flash("El nombre de usuario no puede estar vacío.", "error")
            return render_template("profile.html")

        if new_username != current_user.username:
            taken = User.query.filter(
                User.username == new_username, User.id != current_user.id
            ).first()
            if taken:
                flash("Ese nombre de usuario ya está en uso.", "error")
                return render_template("profile.html")
            current_user.username = new_username

        if photo and photo.filename:
            if not allowed_image(photo.filename):
                flash("Formato de imagen no permitido. Usa png, jpg, webp o gif.", "error")
                return render_template("profile.html")
            current_user.avatar_url = save_media(
                photo, "image", current_app.config["AVATAR_FOLDER"], "avatars"
            )

        db.session.commit()
        flash("Perfil actualizado.", "success")
        return redirect(url_for("auth.profile"))

    return render_template("profile.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada.", "info")
    return redirect(url_for("main.index"))
