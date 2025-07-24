from main.app import w3
from main.application_layer.use_cases import transaction
from main.application_layer.adapters.ethereum_service import EthereumService
from main.domain_layer.models.address import Address
from main.domain_layer.models.transaction import Transaction

def is_whitelist(address: str):
    return Address.get(address=address)

class TransactionUseCase:

    @transaction()
    def validate(self, tx_hash: str):

        ethereum_service = EthereumService(w3=w3)

        transaction = Transaction.get(tx_hash=tx_hash)
        if transaction:
            return {"valid": False, "reason": f"Transaction {tx_hash} already registered"}
        
        tx = ethereum_service.get_transaction(tx_hash=tx_hash)
        receipt = ethereum_service.get_transaction_receipt(tx_hash)

        transfers = []
        if tx["to"] is None:
            return {"valid": False, "reason": "Contract creation"}
        
        # ETH Transfer
        if tx["input"] == "0x" and tx["value"] > 0:
            to_address = ethereum_service.to_checksum_address(tx["to"])
            if is_whitelist(address=to_address):
                return {"valid": False, "reason": "Destination not whitelisted"}

            value = ethereum_service.from_wei(tx["value"], 'ether')
            transfers.append({
                "asset": "ETH",
                "to": to_address,
                "amount": str(value),
            })
        # ERC-20 Token Transfer
        else:

            erc20_transfer_signature = w3.keccak(text="Transfer(address,address,uint256)").hex()[:10]

            for log in receipt["logs"]:
                if log["topics"][0].hex()[:10] == erc20_transfer_signature:
                    to_address = "0x" + log["topics"][2].hex()[-40:]
                    to_address = ethereum_service.to_checksum_address(to_address)

                    if is_whitelist(address=to_address):
                        return {"valid": False, "reason": "Destination not whitelisted"}
                    
                    contract = ethereum_service.contract(address=log["address"], abi=[{
                        "name": "symbol",
                        "outputs": [{"type": "string"}],
                        "inputs": [],
                        "stateMutability": "view",
                        "type": "function"
                    }, {
                        "name": "decimals",
                        "outputs": [{"type": "uint8"}],
                        "inputs": [],
                        "stateMutability": "view",
                        "type": "function"
                    }])

                    symbol = contract.functions.symbol().call()
                    decimals = contract.functions.decimals().call()

                    amount = int(log["data"].hex(), 16) / (10 ** decimals)
                    transfers.append({
                        "asset": symbol,
                        "to": to_address,
                        "amount": str(amount),
                    })

        if transfers:
            for t in transfers:
                Transaction.create(
                    tx_hash=tx_hash,
                    to_address=t["to"],
                    asset=t["asset"],
                    value=t["amount"]
                )
            return {"valid": True, "transfers": transfers}
        else:
            return {"valid": False, "reason": "No valid transfers to whitelisted addresses"}
        
    def get_transanctions(self):

        transactions = Transaction.get()

        return [{
            "hash": t.tx_hash,
            "to": t.to_address,
            "asset": t.asset,
            "amount": t.value
        } for t in transactions]