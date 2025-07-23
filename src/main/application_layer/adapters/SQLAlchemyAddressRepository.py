import logging

from main.app import db
from main.application_layer.persistency.tables import address_table
from main.domain_layer.factories import AddressFactory

logger = logging.getLogger("teste-mb." + __name__)

class SQLAlchemyAddressRepository:
    """Repository for managing addresses using SQLAlchemy."""

    @classmethod
    def get(cls):
        """Retrieve an address by its string representation."""

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
                    question_uuid=address.address,
                    is_correct=address.private_key
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

        return self.db.session.query(self.db.Address).filter_by(address=address).first()

    def create(self, address, private_key):
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
                address=address,
                private_key=private_key
            )
            db.session.execute(new_address)
            db.session.commit()
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

    
