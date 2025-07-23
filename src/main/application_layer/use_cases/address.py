from main.app import w3
from main.application_layer.use_cases import transaction
from main.application_layer.adapters.ethereum_service import EthereumService
from main.domain_layer.models.address import Address

class Address:

    @transaction
    def generate(self, quantity: int):

        ethereum_service = EthereumService(w3=w3)

        generated = []

        for _ in range(quantity):
            account = ethereum_service.create()
            Address.create(
                address=account.address,
                private_key=account.key.hex()
            )
            generated.append(account.address)

        return generated
    
    def get(self):
        return Address.get()
