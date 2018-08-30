from flask import Flask

from .extensions import db
from . import api


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    register_blueprints(app)
    set_config(app)
    return app

def set_config(app):
    ENV = app.config.get('ENV', 'default')
    app.config.from_object(f'config.{ENV.title()}')

def register_blueprints(app):
    app.register_blueprint(api.blueprint)
