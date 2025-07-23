from dataclasses import dataclass
from uuid import UUID

@dataclass
class AddressFactory:
    uuid: UUID
    address: str
    private_key: str

    def create_address(self):
        """Create an Address instance."""
        from main.domain_layer.models.address import Address
        return Address(
            uuid=self.uuid,
            address=self.address,
            private_key=self.private_key
        )

@dataclass
class TransactionFactory:
    uuid: UUID
    tx_hash: str
    asset: str
    to_address: str
    value: float

    def create_transaction(self):
        """Create a Transaction instance."""
        from main.domain_layer.models.transaction import Transaction
        return Transaction(
            uuid=self.uuid,
            tx_hash=self.tx_hash,
            asset=self.asset,
            to_address=self.to_address,
            value=self.value
        )
    
@dataclass
class TransferFactory:
    uuid: UUID
    tx_hash: str
    from_address: str
    to_address: str
    asset: str
    value: float
    status: str
    gas_used: float
    gas_price: float

    def create_transfer(self):
        """Create a Transfer instance."""
        from main.domain_layer.models.transfer import Transfer
        return Transfer(
            uuid=self.uuid,
            tx_hash=self.tx_hash,
            from_address=self.from_address,
            to_address=self.to_address,
            asset=self.asset,
            value=self.value,
            status=self.status,
            gas_used=self.gas_used,
            gas_price=self.gas_price
        )