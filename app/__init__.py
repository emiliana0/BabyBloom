from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SECRET_KEY"] = "my_secret_key"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///babybloom.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app import models

    from app.routes import main

    app.add_url_rule("/", view_func=main)

    return app