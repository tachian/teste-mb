import pytest
from unittest.mock import patch, MagicMock
from flask import Flask

from main.application_layer.use_cases.transfer import (
    TransferUseCase, get_token_address, get_nonce_lock, ERC20_ABI
)

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['TESTING'] = True
    return app

@pytest.fixture
def use_case():
    return TransferUseCase()

@pytest.fixture
def mock_ethereum_service():
    mock = MagicMock()
    mock.to_checksum_address.side_effect = lambda x: x
    mock.to_checksum_address.return_value = "0x65aFADD39029741B3b8f0756952C74678c9cEC93"
    mock.to_wei.side_effect = lambda amount, unit: int(float(amount) * 1e18)
    mock.contract.return_value.functions.decimals.return_value.call.return_value = 6
    mock.contract.return_value.functions.transfer.return_value.build_transaction.return_value = {
        'from': '0xfrom',
        'nonce': 1,
        'gasPrice': 100,
    }
    mock.estimate_gas.return_value = 21000
    mock.sign_transaction.return_value = MagicMock(rawTransaction=b'rawtx')
    mock.send_raw_transaction.return_value = MagicMock(hex=lambda: '0xtxhash')
    mock.wait_for_transaction_receipt.return_value = MagicMock(gasUsed=21000, status=1)
    return mock

def test_get_token_address_eth(mock_ethereum_service):
    assert get_token_address("ETH", mock_ethereum_service) is None

def test_get_token_address_supported_token(mock_ethereum_service):
    addr = get_token_address("USDC", mock_ethereum_service)
    assert addr == mock_ethereum_service.to_checksum_address.return_value

def test_get_token_address_unsupported_token(mock_ethereum_service):
    with pytest.raises(ValueError):
        get_token_address("ABC", mock_ethereum_service)

def test_get_nonce_lock_threadsafe():
    lock1 = get_nonce_lock("0xabc")
    lock2 = get_nonce_lock("0xabc")
    assert lock1 is lock2

@patch("main.application_layer.use_cases.transfer.EthereumService")
@patch("main.application_layer.use_cases.transfer.Transfer")
@patch("main.application_layer.use_cases.transfer.db")
@patch("main.application_layer.use_cases.transfer.w3")
def test_execute_eth_success(mock_w3, mock_db, mock_transfer, mock_eth_service, app, use_case):
    mock_eth_service.return_value = MagicMock()
    mock_eth_service.return_value.to_checksum_address.side_effect = lambda x: x
    mock_eth_service.return_value.to_wei.side_effect = lambda amount, unit: int(float(amount) * 1e18)
    mock_w3.eth.get_transaction_count.return_value = 1
    mock_w3.eth.gas_price = 100
    mock_w3.eth.account.sign_transaction.return_value = MagicMock(rawTransaction=b'rawtx')
    mock_eth_service.return_value.send_raw_transaction.return_value = MagicMock(hex=lambda: '0xtxhash')
    mock_eth_service.return_value.wait_for_transaction_receipt.return_value = MagicMock(gasUsed=21000, status=1)
    mock_transfer.create.return_value = MagicMock(uuid="uuid")
    mock_transfer.update_tx_hash.return_value = None
    mock_transfer.update_confirmation.return_value = None

    with app.test_request_context():
        resp = use_case.execute(
            from_address="0xfrom",
            private_key="privkey",
            to_address="0xto",
            asset="ETH",
            amount="1.0"
        )
        assert resp.status_code == 200 or resp.status_code is None
        assert "tx_hash" in resp.json
        assert resp.json["status"] == "confirmed"

@patch("main.application_layer.use_cases.transfer.EthereumService")
@patch("main.application_layer.use_cases.transfer.Transfer")
@patch("main.application_layer.use_cases.transfer.db")
@patch("main.application_layer.use_cases.transfer.w3")
def test_execute_token_success(mock_w3, mock_db, mock_transfer, mock_eth_service, app, use_case):
    mock_eth_service.return_value = MagicMock()
    mock_eth_service.return_value.to_checksum_address.side_effect = lambda x: x
    mock_eth_service.return_value.contract.return_value.functions.decimals.return_value.call.return_value = 6
    mock_eth_service.return_value.contract.return_value.functions.transfer.return_value.build_transaction.return_value = {
        'from': '0xfrom',
        'nonce': 1,
        'gasPrice': 100,
    }
    mock_eth_service.return_value.estimate_gas.return_value = 21000
    mock_eth_service.return_value.sign_transaction.return_value = MagicMock(rawTransaction=b'rawtx')
    mock_eth_service.return_value.send_raw_transaction.return_value = MagicMock(hex=lambda: '0xtxhash')
    mock_eth_service.return_value.wait_for_transaction_receipt.return_value = MagicMock(gasUsed=21000, status=1)
    mock_w3.eth.get_transaction_count.return_value = 1
    mock_w3.eth.gas_price = 100
    mock_transfer.create.return_value = MagicMock(uuid="uuid")
    mock_transfer.update_tx_hash.return_value = None
    mock_transfer.update_confirmation.return_value = None

    with app.test_request_context():
        resp = use_case.execute(
            from_address="0xfrom",
            private_key="privkey",
            to_address="0xto",
            asset="USDC",
            amount="1.0"
        )
        assert resp.status_code == 200 or resp.status_code is None
        assert "tx_hash" in resp.json
        assert resp.json["status"] == "confirmed"

@patch("main.application_layer.use_cases.transfer.EthereumService")
@patch("main.application_layer.use_cases.transfer.Transfer")
@patch("main.application_layer.use_cases.transfer.db")
@patch("main.application_layer.use_cases.transfer.w3")
def test_execute_invalid_amount(mock_w3, mock_db, mock_transfer, mock_eth_service, app, use_case):
    with app.test_request_context():
        resp = use_case.execute(
            from_address="0xfrom",
            private_key="privkey",
            to_address="0xto",
            asset="ETH",
            amount="notanumber"
        )
        # Handle both tuple and Response cases
        if isinstance(resp, tuple):
            response, status_code = resp
        else:
            response = resp
            status_code = resp.status_code

        assert status_code == 400
        assert "error" in response.json