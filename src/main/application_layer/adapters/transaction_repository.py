import logging
import uuid
from main.app import db
from main.application_layer.persistency.tables import transaction_table
from main.domain_layer.factories import TransactionFactory

logger = logging.getLogger("teste-mb." + __name__)

class SQLAlchemyTransactionRepository:
    """Repository for managing transactions using SQLAlchemy."""

    @classmethod
    def get_transactions(cls):
        """Retrieve all transactions."""
        
        logger.info(
            "Getting Transactions",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service method": "get",
                }
            }
        )

        try:
            transactions = db.session.query(transaction_table).all()

            return [
                TransactionFactory(
                    uuid=transaction.uuid,
                    tx_hash=transaction.tx_hash,
                    asset=transaction.asset,
                    to_address=transaction.to_address,
                    value=transaction.value,
                ).create_transaction() for transaction in transactions
            ]
        except Exception as e:
            logger.exception(
                "Error while trying to get Transactions",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service method": "get",
                        "error message": str(e)
                    }
                })
            raise e
        
    @classmethod
    def get_transaction(cls, tx_hash: str):
        """Retrieve transaction for tx_hash"""
        
        logger.info(
            "Getting Transactions",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service method": "get",
                    "tx_hash": tx_hash
                }
            }
        )

        try:
            transaction = db.session.query(transaction_table).filter(transaction_table.c.tx_hash == tx_hash).first()

            return TransactionFactory(
                uuid=transaction.uuid,
                tx_hash=transaction.tx_hash,
                asset=transaction.asset,
                to_address=transaction.to_address,
                value=transaction.value,
            ).create_transaction() if transaction else None
        
        except Exception as e:
            logger.exception(
                "Error while trying to get Transactions",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service method": "get",
                        "tx_hash": tx_hash,
                        "error message": str(e)
                    }
                })
            raise e
        
    @classmethod
    def create(cls, tx_hash: str, asset: str, to_address: str, value: float):
        logger.info(
            "Creating Transaction",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service method": "create_password",
                    "tx_hash": tx_hash,
                    "asset": asset,
                    "to_address": to_address,
                    "value": str(value)
                }
            }
        )

        try:
            insert_stmt = transaction_table.insert().values(
                uuid=uuid.uuid4(),
                tx_hash=tx_hash, 
                asset=asset,
                to_address=to_address,
                value=value)
            db.session.execute(insert_stmt)
            db.session.flush()
        except Exception as e:
            logger.exception(
                "Error while trying to create Transaction",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service method": "create",
                        "tx_hash": tx_hash,
                        "asset": asset,
                        "to_address": to_address,
                        "value": str(value),
                        "error message": str(e)
                    }
                })
            raise e