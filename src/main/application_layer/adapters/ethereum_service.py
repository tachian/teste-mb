import logging
from web3 import Web3

logger = logging.getLogger("teste-mb." + __name__)

class EthereumService:
    """Service for managing Ethereum-related operations."""

    def __init__(self, w3: Web3):
        self.w3 = w3

    @property
    def is_connected(self):
        """Check if the service is connected to the Ethereum network."""
        return self.w3.is_connected()
    
    @property
    def gas_price(self):
        """Get the current gas price."""
        return self.w3.eth.gas_price


    def create(self):
        """Create Ethereum account."""
        
        logger.info(
            "Creating Ethereum account",
            extra={
                "props": {
                    "service": "Ethereum",
                    "service method": "create",
                }
            }
        )

        try:
            return self.w3.eth.account.create()
        
        except Exception as e:
            logger.exception(
                "Error while trying to create Ethereum account",
                extra={
                    "props": {
                        "service": "Ethereum",
                        "service method": "create",
                        "error message": str(e)
                    }
                })
            raise e
        
    def get_transaction(self, tx_hash: str):
        """Get transaction details by hash."""
        
        logger.info(
            "Getting transaction by hash",
            extra={
                "props": {
                    "service": "Ethereum",
                    "service method": "get_transaction",
                    "tx_hash": tx_hash
                }
            }
        )

        try:
            return self.w3.eth.get_transaction(tx_hash)
        
        except Exception as e:
            logger.exception(
                "Error while trying to get transaction",
                extra={
                    "props": {
                        "service": "Ethereum",
                        "service method": "get_transaction",
                        "tx_hash": tx_hash,
                        "error message": str(e)
                    }
                })
            raise e
        
    def get_transaction_receipt(self, tx_hash: str):
        """Get transaction receipt by hash."""
        
        logger.info(
            "Getting transaction receipt by hash",
            extra={
                "props": {
                    "service": "Ethereum",
                    "service method": "get_transaction_receipt",
                    "tx_hash": tx_hash
                }
            }
        )

        try:
            return self.w3.eth.get_transaction_receipt(tx_hash)
        
        except Exception as e:
            logger.exception(
                "Error while trying to get transaction receipt",
                extra={
                    "props": {
                        "service": "Ethereum",
                        "service method": "get_transaction_receipt",
                        "tx_hash": tx_hash,
                        "error message": str(e)
                    }
                })
            raise e
        
    def to_checksum_address(self, address: str):
        """Convert address to checksum format."""
        
        logger.info(
            "Converting address to checksum format",
            extra={
                "props": {
                    "service": "Ethereum",
                    "service method": "to_checksum_address",
                    "address": address
                }
            }
        )

        try:
            return self.w3.to_checksum_address(address)
        
        except Exception as e:
            logger.exception(
                "Error while trying to convert address to checksum format",
                extra={
                    "props": {
                        "service": "Ethereum",
                        "service method": "to_checksum_address",
                        "address": address,
                        "error message": str(e)
                    }
                })
            raise e
        
    def from_wei(self, value: int, unit: str):
        """Convert value from wei to specified unit."""
        
        logger.info(
            "Converting value from wei",
            extra={
                "props": {
                    "service": "Ethereum",
                    "service method": "from_wei",
                    "value": value,
                    "unit": unit
                }
            }
        )

        try:
            return self.w3.from_wei(value, unit)
        
        except Exception as e:
            logger.exception(
                "Error while trying to convert value from wei",
                extra={
                    "props": {
                        "service": "Ethereum",
                        "service method": "from_wei",
                        "value": value,
                        "unit": unit,
                        "error message": str(e)
                    }
                })
            raise e
        
    def to_wei(self, value: float, unit: str):
        """Convert value to wei from specified unit."""
        
        logger.info(
            "Converting value to wei",
            extra={
                "props": {
                    "service": "Ethereum",
                    "service method": "to_wei",
                    "value": value,
                    "unit": unit
                }
            }
        )

        try:
            return self.w3.to_wei(value, unit)
        
        except Exception as e:
            logger.exception(
                "Error while trying to convert value to wei",
                extra={
                    "props": {
                        "service": "Ethereum",
                        "service method": "to_wei",
                        "value": value,
                        "unit": unit,
                        "error message": str(e)
                    }
                })
            raise e
        
    def get_transaction_count(self, address: str):
        """Get the number of transactions sent from an address."""
        
        logger.info(
            "Getting transaction count for address",
            extra={
                "props": {
                    "service": "Ethereum",
                    "service method": "get_transaction_count",
                    "address": address
                }
            }
        )

        try:
            return self.w3.eth.get_transaction_count(address)
        
        except Exception as e:
            logger.exception(
                "Error while trying to get transaction count",
                extra={
                    "props": {
                        "service": "Ethereum",
                        "service method": "get_transaction_count",
                        "address": address,
                        "error message": str(e)
                    }
                })
            raise e
        
    def contract(self, address: str, abi: list):
        """Get a contract instance."""
        
        logger.info(
            "Getting contract instance",
            extra={
                "props": {
                    "service": "Ethereum",
                    "service method": "contract",
                    "address": address
                }
            }
        )

        try:
            return self.w3.eth.contract(address=self.to_checksum_address(address), abi=abi)
        
        except Exception as e:
            logger.exception(
                "Error while trying to get contract instance",
                extra={
                    "props": {
                        "service": "Ethereum",
                        "service method": "contract",
                        "address": address,
                        "error message": str(e)
                    }
                })
            raise e
    
    def estimate_gas(self, transaction: dict):
        """Estimate gas for a transaction."""
        
        logger.info(
            "Estimating gas for transaction",
            extra={
                "props": {
                    "service": "Ethereum",
                    "service method": "estimate_gas",
                    "transaction": transaction
                }
            }
        )

        try:
            return self.w3.eth.estimate_gas(transaction)
        
        except Exception as e:
            logger.exception(
                "Error while trying to estimate gas",
                extra={
                    "props": {
                        "service": "Ethereum",
                        "service method": "estimate_gas",
                        "transaction": transaction,
                        "error message": str(e)
                    }
                })
            raise e
        
    def send_transaction(self, transaction: dict):
        """Send a transaction."""
        
        logger.info(
            "Sending transaction",
            extra={
                "props": {
                    "service": "Ethereum",
                    "service method": "send_transaction",
                    "transaction": transaction
                }
            }
        )

        try:
            return self.w3.eth.send_transaction(transaction)
        
        except Exception as e:
            logger.exception(
                "Error while trying to send transaction",
                extra={
                    "props": {
                        "service": "Ethereum",
                        "service method": "send_transaction",
                        "transaction": transaction,
                        "error message": str(e)
                    }
                })
            raise e
        
    def wait_for_transaction_receipt(self, tx_hash: str, timeout: int = 120):
        """Wait for a transaction receipt."""
        
        logger.info(
            "Waiting for transaction receipt",
            extra={
                "props": {
                    "service": "Ethereum",
                    "service method": "wait_for_transaction_receipt",
                    "tx_hash": tx_hash,
                    "timeout": timeout
                }
            }
        )

        try:
            return self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=timeout)
        
        except Exception as e:
            logger.exception(
                "Error while trying to wait for transaction receipt",
                extra={
                    "props": {
                        "service": "Ethereum",
                        "service method": "wait_for_transaction_receipt",
                        "tx_hash": tx_hash,
                        "timeout": timeout,
                        "error message": str(e)
                    }
                })
            raise e
    
    def sign_transaction(self, tx: dict, private_key: str):
        """Sign transaction"""
        
        logger.info(
            "Signing transaction",
            extra={
                "props": {
                    "service": "Ethereum",
                    "service method": "sign_transaction",
                    "tx": tx,
                    "private_key": private_key
                }
            }
        )

        try:
            return self.w3.eth.account.sign_transaction(tx, private_key)
        
        except Exception as e:
            logger.exception(
                "Error while trying to sign transaction",
                extra={
                    "props": {
                        "service": "Ethereum",
                        "service method": "sign_transaction",
                        "tx": tx,
                        "private_key": private_key,
                        "error message": str(e)
                    }
                })
            raise e
        
    def send_raw_transaction(self, tx: dict):
        """Send raw transaction"""
        
        logger.info(
            "Signing transaction",
            extra={
                "props": {
                    "service": "Ethereum",
                    "service method": "send_raw_transaction",
                    "tx": tx,
                }
            }
        )

        try:
            return self.w3.eth.send_raw_transaction(tx)
        
        except Exception as e:
            logger.exception(
                "Error while trying to send raw transaction",
                extra={
                    "props": {
                        "service": "Ethereum",
                        "service method": "send_raw_transaction",
                        "tx": tx,
                        "error message": str(e)
                    }
                })
            raise e