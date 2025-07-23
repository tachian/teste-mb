import logging

from main.app import db
from main.application_layer.persistency.tables import transaction_table

logger = logging.getLogger("teste-mb." + __name__)

class SQLAlchemyTransactionRepository:
    """Repository for managing transactions using SQLAlchemy."""

    @classmethod
    def get(cls):
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