from dataclasses import dataclass
from uuid import UUID

from main.application_layer.adapters.SQLAlchemyTransactionRepository import SQLAlchemyTransactionRepository

class Transaction:
    """Transaction model representing a financial transaction."""

    uuid: UUID
    tx_hash: str
    asset: str
    to_address: str
    value: float

    @classmethod
    def get(cls):
        """Retrieve all transactions."""
        return SQLAlchemyTransactionRepository.get()
    
    @classmethod
    def create(cls, tx_hash: str, asset: str, to_address: str, value: float):
        """Add a new transaction to the repository."""
        return SQLAlchemyTransactionRepository.create(tx_hash, asset, to_address, value)