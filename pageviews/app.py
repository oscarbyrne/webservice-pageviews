from flask import Flask

from .extensions import db
from . import api


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(api.blueprint)
