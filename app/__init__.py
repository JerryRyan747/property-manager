from flask import Flask
from config import Config

from app.extensions import db, migrate
###from app.models.user import User
###from app.models.property import property


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    from app import models

    from app.routes.main import main
    app.register_blueprint(main)

    return app
