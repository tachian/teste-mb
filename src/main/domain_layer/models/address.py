from dataclasses import dataclass
from uuid import UUID

from main.application_layer.adapters.address_repository import SQLAlchemyAddressRepository

@dataclass
class Address:
    uuid: UUID
    address: str
    private_key: str

    @classmethod
    def get(cls, address:str = None):
        """Retrieve an address by its string representation."""
        if address:
            return SQLAlchemyAddressRepository.get_address(address=address)
        return SQLAlchemyAddressRepository.get()

    @classmethod
    def create(cls, address: str, private_key: str):
        """Add a new address to the repository."""
        return SQLAlchemyAddressRepository.create(address, private_key)