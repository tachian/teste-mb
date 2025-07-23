import logging
import uuid

from main.app import db
from main.application_layer.persistency.tables import transfer_table
from main.domain_layer.factories import TransferFactory

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
        
    @classmethod
    def create(
        cls, 
        tx_hash:str, 
        from_address:str, 
        to_address:str, 
        asset:str, 
        value:float, 
        status:str, 
        gas_used:float, 
        gas_price:float):

        logger.info(
            "Creating Transfer",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service method": "create",
                    "tx_hash":tx_hash,
                    "from_address":from_address,
                    "to_address":to_address,
                    "asset":asset,
                    "value":value,
                    "status":status,
                    "gas_used":gas_used,
                    "gas_price":gas_price
                }
            }
        )
        try:
            insert_stmt = transfer_table.insert().values(
                uuid=uuid.uuid4(),
                tx_hash=tx_hash,
                from_address=from_address,
                to_address=to_address,
                asset=asset,
                value=value,
                status=status,
                gas_used=gas_used,
                gas_price=gas_price
            )
            db.session.execute(insert_stmt)
            db.session.flush()
        except Exception as e:
            logger.exception(
                "Error while trying to create Transaction",
                extra={
                        "props": {
                        "service": "PostgreSQL",
                        "service method": "create",
                        "tx_hash":tx_hash,
                        "from_address":from_address,
                        "to_address":to_address,
                        "asset":asset,
                        "value":value,
                        "status":status,
                        "gas_used":gas_used,
                        "gas_price":gas_price,
                        "error message": str(e)
                    }
                })
            raise e
