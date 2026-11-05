from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from backend.database import db
from models.user import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if not username or not password:
            flash("Please enter both username and password.", "error")
            return render_template("login.html", csrf_token=session.get("csrf_token", ""))

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("index"))

        flash("Invalid username or password.", "error")

    return render_template("login.html", csrf_token=session.get("csrf_token", ""))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        email = (request.form.get("email") or "").strip()
        password = request.form.get("password") or ""

        if not username or not email or not password:
            flash("Please complete all fields.", "error")
            return render_template("register.html", csrf_token=session.get("csrf_token", ""))

        if len(password) < 8:
            flash("Password must be at least 8 characters long.", "error")
            return render_template("register.html", csrf_token=session.get("csrf_token", ""))

        if User.query.filter_by(username=username).first() is not None:
            flash("This username already exists.", "error")
            return render_template("register.html", csrf_token=session.get("csrf_token", ""))

        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("index"))

    return render_template("register.html", csrf_token=session.get("csrf_token", ""))


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
