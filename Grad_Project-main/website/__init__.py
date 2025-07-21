from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
DB_NAME = "Grad_Project_DB"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "your_secret_key_here"

    # Database configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        "mysql+pymysql://root:Bitirme.proj.24@localhost/Grad_Project_DB"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True  # For debugging SQL queries

    # Initialize database
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
