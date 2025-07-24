from dataclasses import dataclass
from uuid import UUID

from main.application_layer.adapters.transaction_repository import SQLAlchemyTransactionRepository

@dataclass
class Transaction:
    """Transaction model representing a financial transaction."""

    uuid: UUID
    tx_hash: str
    asset: str
    to_address: str
    value: float

    @classmethod
    def get(cls, tx_hash: str = None):
        """Retrieve all transactions."""
        if tx_hash:
            return SQLAlchemyTransactionRepository.get_transaction(tx_hash=tx_hash)
        
        return SQLAlchemyTransactionRepository.get_transactions()
    
    @classmethod
    def create(cls, tx_hash: str, asset: str, to_address: str, value: float):
        """Add a new transaction to the repository."""
        return SQLAlchemyTransactionRepository.create(tx_hash, asset, to_address, value)