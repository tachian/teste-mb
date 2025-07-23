from uuid import UUID
from flask_restx import fields, Model


class NullableString(fields.String):
    __schema_type__ = ['string', 'null']
    __schema_example__ = 'nullable string'