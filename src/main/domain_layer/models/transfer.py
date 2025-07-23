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