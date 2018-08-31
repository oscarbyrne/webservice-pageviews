from marshmallow_enum import EnumField


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
