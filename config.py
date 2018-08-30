import os


class Default():
    pass

class Development(Default):
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']
