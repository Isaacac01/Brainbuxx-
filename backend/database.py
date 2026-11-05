from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"


def init_extensions(app: Flask):
    db.init_app(app)
    login_manager.init_app(app)
    with app.app_context():
        db.create_all()
