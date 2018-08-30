import os


class Default():
    ENV = 'default'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # To suppress flask warning for new default

class Development(Default):
    ENV = 'development'
    DEBUG = True
