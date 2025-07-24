from dataclasses import dataclass
from uuid import UUID

from main.application_layer.adapters.transfer_repository import SQLAlchemyTransferRepository

@dataclass
class Transfer:
    """Transfer model representing a financial transfer."""
    
    uuid: UUID
    tx_hash: str
    from_address: str
    to_address: str
    asset: str
    value: float
    status: str
    gas_used: float
    gas_price: float

    @classmethod
    def get(cls):
        """Retrieve all transfers."""
        return SQLAlchemyTransferRepository.get()
    
    @classmethod
    def create(cls, tx_hash: str, from_address: str, to_address: str, asset: str, value: float, status: str, gas_used: float, gas_price: float):
        """Add a new transfer to the repository."""
        return SQLAlchemyTransferRepository.create(tx_hash, from_address, to_address, asset, value, status, gas_used, gas_price)
    
    @classmethod
    def update_tx_hash(cls, uuid: UUID, tx_hash: str):
        """Update transfer tx_hash."""
        return SQLAlchemyTransferRepository.update_tx_hash(uuid=uuid, tx_hash=tx_hash)

    @classmethod
    def update_status(cls, uuid: UUID, status: str):
        """Update transfer status."""
        return SQLAlchemyTransferRepository.update_status(uuid=uuid, status=status)
    
    @classmethod
    def update_confirmation(cls, uuid: UUID, status: str, gas_used: float, tx_hash: str):
        """Update transfer with confirmation attribs"""
        return SQLAlchemyTransferRepository.update_confirmation(uuid=uuid, status=status, gas_used=gas_used, tx_hash=tx_hash)