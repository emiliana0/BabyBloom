from flask import Flask
from config import Config
from app.extensions import db, login_manager, migrate


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.main import main
    app.register_blueprint(main)

    from app.auth import auth
    app.register_blueprint(auth)

    from app.children import children
    app.register_blueprint(children)

    from app.notes import notes
    app.register_blueprint(notes)

    from app.gallery import gallery
    app.register_blueprint(gallery)

    from app.sharing import sharing
    app.register_blueprint(sharing)

    from app.admin import admin
    app.register_blueprint(admin)

    from app.advice import advice
    app.register_blueprint(advice)

    return app