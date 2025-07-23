from dataclasses import dataclass
from uuid import UUID

from main.application_layer.adapters.SQLAlchemyAddressRepository import SQLAlchemyAddressRepository

@dataclass
class Address:
    uuid: UUID
    address: str
    private_key: str

    @classmethod
    def get(cls):
        """Retrieve an address by its string representation."""
        return SQLAlchemyAddressRepository.get()
    
    @classmethod
    def create(cls, address: str, private_key: str):
        """Add a new address to the repository."""
        return SQLAlchemyAddressRepository.create(address, private_key)