from uuid import UUID
from flask_restx import fields, Model


class NullableString(fields.String):
    __schema_type__ = ['string', 'null']
    __schema_example__ = 'nullable string'

validate_model = Model(
    'validate',
    {
        'tx_hash': fields.String(),
    }
)

transfer_model = Model(
    'transfer',
    {
        'from_address': fields.String(),
        'private_key': fields.String(),
        'to_address': fields.String(),
        'asset': fields.String(),
        'amount': fields.Float()
    }
)