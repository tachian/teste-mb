import re

class InvalidDataException(Exception):
    pass

class Mapping:
    """ I map from the payload format to a common vocabulary,
    to decouple the lower layers from the partners.
    """

    def __init__(self, *, payload):
        self.payload = payload


class ValidateMapping(Mapping):
    
    @property
    def tx_hash(self):
        return self.payload['tx_hash']
    
class TransferMapping(Mapping):

    @property
    def from_address(self):
        return self.payload['from_address']

    @property
    def private_key(self):
        return self.payload['private_key']
    
    @property
    def private_key(self):
        return self.payload['private_key']
    
    @property
    def to_address(self):
        return self.payload['to_address']
    
    @property
    def asset(self):
        return self.payload['asset']

    @property
    def amount(self):
        return self.payload['amount']
