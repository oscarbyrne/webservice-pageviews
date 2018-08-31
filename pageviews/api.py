from flask import (
    Blueprint,
    request,
)
from flask_restful import (
    Api,
    Resource,
)
from webargs import fields
from webargs.flaskparser import use_kwargs
from marshmallow import Schema
from marshmallow_enum import EnumField

from .models import Visit


blueprint = Blueprint('api', __name__)
api = Api(blueprint)


class IntEnumField(EnumField):
    """
    Monkey patch fixing marshmallow_enum support for integer-valued enums
    """

    def _deserialize_by_value(self, value, attr, data):
        try:
            value = int(value)
        except ValueError:
            self.fail('by_value', input=value, value=value)
        else:
            return super()._deserialize_by_value(value, attr, data)


class FilterArgs(Schema):

    os = fields.DelimitedList(
        IntEnumField(Visit.OsChoices, by_value=True),
        missing=[str(choice.value) for choice in Visit.OsChoices]
    )

    device = fields.DelimitedList(
        IntEnumField(Visit.DeviceChoices, by_value=True),
        missing=[str(choice.value) for choice in Visit.DeviceChoices]
    )


class UserCount(Resource):

    @use_kwargs(FilterArgs())
    def get(self, **kwargs):
        return {
            'count': FilterArgs().dump(kwargs)
        }


class LoyalUserCount(UserCount):

    pass


api.add_resource(UserCount, '/unique-users')
api.add_resource(LoyalUserCount, '/loyal-users')
