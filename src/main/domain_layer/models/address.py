from dataclasses import dataclass
from uuid import UUID

from main.application_layer.adapters.address_repository import SQLAlchemyAddressRepository

@dataclass
class Address:
    uuid: UUID
    address: str
    private_key: str

    @classmethod
    def get(cls):
        """Retrieve an address by its string representation."""
        return SQLAlchemyAddressRepository.get_adresses()
    
    @classmethod
    def get_address(cls, tx_hash: str):
        """Retrieve an address by its string representation."""
        return SQLAlchemyAddressRepository.get_address(tx_hash=tx_hash)

    @classmethod
    def create(cls, address: str, private_key: str):
        """Add a new address to the repository."""
        return SQLAlchemyAddressRepository.create(address, private_key)