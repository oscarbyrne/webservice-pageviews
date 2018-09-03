from flask import (
    Blueprint,
    request,
)
from flask_restful import (
    Api,
    Resource,
)
from sqlalchemy import and_
from webargs.fields import DelimitedList
from webargs.flaskparser import use_kwargs
from marshmallow import Schema

from .util import IntEnumField
from .models import (
    Visit,
    User,
)


blueprint = Blueprint('api', __name__)
api = Api(blueprint)


class FilterArgs(Schema):

    os = DelimitedList(
        IntEnumField(Visit.OsChoices, by_value=True),
        missing=[choice.value for choice in Visit.OsChoices]
    )

    device = DelimitedList(
        IntEnumField(Visit.DeviceChoices, by_value=True),
        missing=[choice.value for choice in Visit.DeviceChoices]
    )

    class Meta:
        strict = True


class UserCount(Resource):

    @staticmethod
    def query(os, device):
        return User.query.join(User.visits).filter(
            and_(
                Visit.os.in_(os),
                Visit.device.in_(device)
            )
        )

    @use_kwargs(FilterArgs)
    def get(self, **kwargs):
        return {
            'count': self.query(**kwargs).distinct().count()
        }


class LoyalUserCount(UserCount):

    @staticmethod
    def query(**kwargs):
        return UserCount.query(**kwargs).filter(
            User.is_loyal
        )


api.add_resource(UserCount, '/unique-users')
api.add_resource(LoyalUserCount, '/loyal-users')
