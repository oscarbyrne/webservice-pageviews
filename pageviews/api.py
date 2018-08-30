from flask import Blueprint


blueprint = Blueprint('api', __name__)

@blueprint.route('/')
def hello_world():
    return 'Hello, World!'
