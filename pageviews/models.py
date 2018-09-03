from enum import Enum
from itertools import groupby

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func, select

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

    id = db.Column(db.BigInteger, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    os = db.Column(db.Enum(OsChoices), nullable=False)
    device = db.Column(db.Enum(DeviceChoices), nullable=False)

    @hybrid_property
    def month(self):
        return self.datetime.month

    @hybrid_property
    def year(self):
        return self.datetime.year

    @month.expression
    def month(cls):
        return (
            select([func.extract('month', cls.datetime)])
            .correlate(cls)
        )

    @year.expression
    def year(cls):
        return (
            select([func.extract('year', cls.datetime)])
            .correlate(cls)
        )


class User(db.Model):

    __tablename__ = 'user'

    LOYALTY_CUTOFF = 10

    id = db.Column(db.BigInteger, primary_key=True)
    visits = db.relationship('Visit', backref=db.backref('user', lazy=True))

    @hybrid_property
    def is_loyal(self):
        grouped = groupby(
            self.visits,
            lambda visit: (visit.month, visit.year)
        )
        return max(
            len(list(group)) for key, group in grouped
        ) >= self.LOYALTY_CUTOFF

    @is_loyal.expression
    def is_loyal(cls):
        visits_per_month = (
            select([func.count(Visit.id)])
            .where(Visit.user_id==cls.id)
            .group_by(Visit.year, Visit.month)
            .order_by(func.count(Visit.id).desc())
            .correlate(cls)
        )
        return visits_per_month.as_scalar() >= cls.LOYALTY_CUTOFF
