from enum import Enum

from sqlalchemy.ext.hybrid import hybrid_property

from .extensions import db


class Visit(db.Model):

    __tablename__ = 'visit'

    class OsChoices(Enum):
        Undefined = 0
        MacOS = 1
        Windows = 2
        Linux = 3
        iOS = 4
        Android = 5
        WindowsPhone = 6

    class DeviceChoices(Enum):
        Undefined = 0
        Desktop = 1
        Tablet = 2
        Smartphone = 3
        SmartTV =  4
        Watch = 5

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    os = db.Column(db.Enum(OsChoices), nullable=False)
    device = db.Column(db.Enum(DeviceChoices), nullable=False)


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    visits = db.relationship('Visit', backref=db.backref('user', lazy=True))

    @hybrid_property
    def is_loyal(self):
        raise NotImplementedError
