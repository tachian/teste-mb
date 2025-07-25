import logging
import uuid

from main.app import db
from main.application_layer.persistency.tables import address_table
from main.domain_layer.factories import AddressFactory

logger = logging.getLogger("teste-mb." + __name__)

class SQLAlchemyAddressRepository:
    """Repository for managing addresses using SQLAlchemy."""

    @classmethod
    def get(cls):
        """Retrieve addresses."""

        logger.info(
            "Getting Address",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service method": "get",
                }
            }
        )

        try:
            addresses = db.session.query(address_table).all()

            return [
                AddressFactory(
                    uuid=address.uuid,
                    address=address.address,
                    private_key=address.private_key
                ).create_address() for address in addresses
            ]            
        except Exception as e:
            logger.exception(
                "Error while trying to get Address",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service method": "get_provider",
                        "error message": str(e)
                    }
                })
            raise e
        
    @classmethod
    def get_address(cls, address: str):
        """Retrieve addresses."""

        logger.info(
            "Getting Address",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service method": "get",
                    "address": address
                }
            }
        )

        try:
            address_result = db.session.query(address_table).filter(address_table.c.address == address).first()

            return AddressFactory(
                    uuid=address_result.uuid,
                    address=address_result.address,
                    private_key=address_result.private_key
                ).create_address() if address_result else None

        except Exception as e:
            logger.exception(
                "Error while trying to get Address",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service method": "get_provider",
                        "address": address,
                        "error message": str(e)
                    }
                })
            raise e
    
    @classmethod
    def create(cls, address, private_key):
        """Add a new address to the repository."""
        
        logger.info(
            "Creating Address",
            extra={
                "props": {
                    "service": "PostgreSQL",
                    "service method": "create",
                    "address": address,
                    "private_key": private_key
                }
            }
        )

        try:
            new_address = address_table.insert().values(
                uuid=uuid.uuid4(),
                address=address,
                private_key=private_key
            )
            db.session.execute(new_address)
            db.session.flush()

        except Exception as e:
            logger.exception(
                "Error while trying to add Address",
                extra={
                    "props": {
                        "service": "PostgreSQL",
                        "service method": "add_address",
                        "error message": str(e)
                    }
                })
            db.session.rollback()
            raise e

    
