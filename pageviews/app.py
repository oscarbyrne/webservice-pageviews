from flask import Flask

from .extensions import (
    db,
    migrate,
)
from . import (
    api,
    commands,
)


def create_app():
    app = Flask(__name__)
    set_config(app)
    db.init_app(app)
    migrate.init_app(app, db)
    register_blueprints(app)
    register_commands(app)
    return app

def set_config(app):
    ENV = app.config.get('ENV', 'default')
    app.config.from_object(f'config.{ENV.title()}')

def register_blueprints(app):
    app.register_blueprint(api.blueprint)

def register_commands(app):
    app.cli.add_command(commands.add_visits_from_file)
