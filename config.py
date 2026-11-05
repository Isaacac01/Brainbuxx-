import os
import secrets
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user

from backend.auth import auth_bp
from backend.chat import chat_bp
from backend.database import init_extensions, login_manager
from config import Config
from models.user import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    if not app.config.get("SECRET_KEY"):
        app.config["SECRET_KEY"] = secrets.token_hex(32)

    @app.before_request
    def ensure_csrf_token():
        if "csrf_token" not in session:
            session["csrf_token"] = secrets.token_urlsafe(32)

    init_extensions(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return render_template("index.html", csrf_token=session.get("csrf_token", ""))
        return redirect(url_for("auth.login"))

    @app.route("/health")
    def health_check():
        return jsonify({"status": "ok", "service": "BrainBuxx"})

    @app.after_request
    def after_request(response):
        if request.path.startswith("/api/") and request.method in {"POST", "PATCH", "DELETE"}:
            expected = session.get("csrf_token")
            provided = request.headers.get("X-CSRFToken")
            if expected and provided != expected:
                response = jsonify({"error": "CSRF validation failed."})
                response.status_code = 403
        return response

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)

    @app.context_processor
    def inject_context():
        return {
            "current_user": current_user,
            "csrf_token": session.get("csrf_token", ""),
        }

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
