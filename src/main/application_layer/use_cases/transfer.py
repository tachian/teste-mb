import decimal
import threading
from flask import jsonify

from main.app import w3, db
# from main.application_layer.use_cases import transaction
from main.application_layer.adapters.ethereum_service import EthereumService
from main.domain_layer.models.transfer import Transfer

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"},
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function",
    },
]

nonce_locks = {}
nonce_locks_lock = threading.Lock()

def get_nonce_lock(address):
    with nonce_locks_lock:
        if address not in nonce_locks:
            nonce_locks[address] = threading.Lock()
        return nonce_locks[address]
    
def get_token_address(symbol, ethereum_service):
    symbol = symbol.upper()

    if symbol == "ETH":
        return None  # ETH não tem contrato (é nativo)

    tokens = {
        "USDC": "0x65aFADD39029741B3b8f0756952C74678c9cEC93",
        "USDT": "0xD9BA894E0097f8cC2BBc9D24D308b98e36dc6D02",
        "LINK": "0xAb2059ADBC674c9F2AAc2f11A423010fcd397A6C"
    }

    if symbol not in tokens:
        raise ValueError(f"Token '{symbol}' não suportado.")

    return ethereum_service.to_checksum_address(tokens[symbol])

class TransferUseCase:

    def execute(
        self,     
        from_address: str,
        private_key: str,
        to_address: str,
        asset: str,
        amount: str):

        ethereum_service = EthereumService(w3=w3)

        from_address = ethereum_service.to_checksum_address(from_address)
        to_address = ethereum_service.to_checksum_address(to_address)
        asset = asset.upper()
        try:
            amount = decimal.Decimal(amount)
        except Exception:
            return jsonify({"error": "Invalid amount format"}), 400
        
        status = "pending"
        tx_hash_hex = None
        gas_used = None
        gas_price = None
        new_tx = None
        lock = get_nonce_lock(from_address)
        lock.acquire()
        try:
            # Obter nonce de forma segura
            nonce = w3.eth.get_transaction_count(from_address, 'pending')
            gas_price = w3.eth.gas_price
            gas_price_with_margin = int(gas_price * decimal.Decimal("1.25"))

            if asset == "ETH":
                value = ethereum_service.to_wei(amount, 'ether')
                tx = {
                    'nonce': nonce,
                    'to': to_address,
                    'value': value,
                    'gas': 21000,
                    'gasPrice': gas_price_with_margin,
                }
                signed_tx = w3.eth.account.sign_transaction(tx, private_key)
            else:
                # ABI local para ERC20 transfer

                contract_address = get_token_address(asset, ethereum_service)
                contract = ethereum_service.contract(address=contract_address, abi=ERC20_ABI)
                decimals = contract.functions.decimals().call()
                token_value = int(amount * (10 ** decimals))
                tx = contract.functions.transfer(to_address, token_value).build_transaction({
                    'from': from_address,
                    'nonce': nonce,
                    'gasPrice': gas_price_with_margin,
                })
                gas_estimate = ethereum_service.estimate_gas(tx)
                tx['gas'] = int(gas_estimate * 1.25)
                signed_tx = ethereum_service.sign_transaction(tx, private_key)
            # Registrar como 'sent' antes de enviar
            new_tx = Transfer.create(
                tx_hash="pending",
                from_address=from_address,
                to_address=to_address,
                asset=asset,
                amount=str(amount),
                status="sent",
                gas_used=None,
                gas_price=str(gas_price_with_margin)
            )
            db.session.commit()

            # Enviar transação
            tx_hash = ethereum_service.send_raw_transaction(signed_tx.rawTransaction)
            tx_hash_hex = tx_hash.hex()
            # Atualizar hash
            Transfer.update_tx_hash(uuid=new_tx.uuid, tx_hash=tx_hash)
            db.session.commit()
            # Aguardar confirmação
            receipt = ethereum_service.wait_for_transaction_receipt(tx_hash, timeout=120)
            gas_used = receipt.gasUsed
            status = "confirmed" if receipt.status == 1 else "failed"
            Transfer.update_confirmation(uuid=new_tx.uuid, status=status, gas_used=gas_used, tx_hash=tx_hash)
            return jsonify({
                "tx_hash": tx_hash_hex,
                "status": status,
                "gas_used": gas_used,
                "gas_price": gas_price_with_margin
            })
        except Exception as e:
            db.session.rollback()
            if new_tx:
                Transfer.update_confirmation(uuid=new_tx.uuid, status='erro', gas_used=gas_used, tx_hash=tx_hash_hex or "erro")
                db.session.commit()
            raise e
        finally:
            lock.release()
