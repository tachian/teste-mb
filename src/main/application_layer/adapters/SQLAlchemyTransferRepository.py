import logging

from main.app import db
from main.application_layer.persistency.tables import transfer_table

logger = logging.getLogger("teste-mb." + __name__)

class SQLAlchemyTransferRepository:
    """Repository for managing transfers using SQLAlchemy."""

    @classmethod
    def get(cls):
        """Retrieve all transfers."""
        
        logger.info(
            "Getting Transfers",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service method": "get",
                }
            }
        )

        try:
            transfers = db.session.query(transfer_table).all()

            return [
                TransferFactory(
                    uuid=transfer.uuid,
                    tx_hash=transfer.tx_hash,
                    from_address=transfer.from_address,
                    to_address=transfer.to_address,
                    asset=transfer.asset,
                    value=transfer.value,
                    status=transfer.status,
                    gas_used=transfer.gas_used,
                    gas_price=transfer.gas_price,
                ).create_transfer() for transfer in transfers
            ]
        except Exception as e:
            logger.exception(
                "Error while trying to get Transfers",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service method": "get",
                        "error message": str(e)
                    }
                })
            raise e 