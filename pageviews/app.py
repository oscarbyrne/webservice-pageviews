from flask import Flask

from .extensions import (
    db,
    migrate,
    ma,
)
from . import (
    api,
    commands,
)


def create_app(environment='development'):
    app = Flask(__name__)
    load_config(app, environment)
    init_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app

def load_config(app, environment='development'):
    ENV = app.config.get('ENV', environment)
    app.config.from_object(f'config.{ENV.title()}')

def init_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

def register_blueprints(app):
    app.register_blueprint(api.blueprint)

def register_commands(app):
    app.cli.add_command(commands.add_visits_from_file)
