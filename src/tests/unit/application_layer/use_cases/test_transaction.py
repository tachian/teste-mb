import pytest
from unittest.mock import patch, MagicMock
from main.application_layer.use_cases.transaction import TransactionUseCase
from main.app import create_app

@pytest.fixture(autouse=True)
def app_context():
    with create_app().app_context():
        yield
        
@pytest.fixture
def use_case():
    return TransactionUseCase()

@patch("main.application_layer.use_cases.transaction.Transaction")
@patch("main.application_layer.use_cases.transaction.EthereumService")
@patch("main.application_layer.use_cases.transaction.is_whitelist")
@patch("main.application_layer.use_cases.transaction.w3")
def test_validate_already_registered(mock_w3, mock_is_whitelist, mock_ethereum_service, mock_transaction, use_case):
    mock_transaction.get.return_value = True
    result = use_case.validate("0x123")
    assert result == {"valid": False, "reason": "Transaction 0x123 already registered"}

@patch("main.application_layer.use_cases.transaction.Transaction")
@patch("main.application_layer.use_cases.transaction.EthereumService")
@patch("main.application_layer.use_cases.transaction.is_whitelist")
@patch("main.application_layer.use_cases.transaction.w3")
def test_validate_contract_creation(mock_w3, mock_is_whitelist, mock_ethereum_service, mock_transaction, use_case):
    mock_transaction.get.return_value = None
    eth_service = mock_ethereum_service.return_value
    eth_service.get_transaction.return_value = {"to": None}
    result = use_case.validate("0xabc")
    assert result == {"valid": False, "reason": "Contract creation"}

@patch("main.application_layer.use_cases.transaction.Transaction")
@patch("main.application_layer.use_cases.transaction.EthereumService")
@patch("main.application_layer.use_cases.transaction.is_whitelist")
@patch("main.application_layer.use_cases.transaction.w3")
def test_validate_eth_transfer_not_whitelisted(mock_w3, mock_is_whitelist, mock_ethereum_service, mock_transaction, use_case):
    mock_transaction.get.return_value = None
    eth_service = mock_ethereum_service.return_value
    eth_service.get_transaction.return_value = {"to": "0xabc", "input": "0x", "value": 100}
    eth_service.get_transaction_receipt.return_value = {}
    eth_service.to_checksum_address.return_value = "0xabc"
    mock_is_whitelist.return_value = True
    result = use_case.validate("0xdef")
    assert result == {"valid": False, "reason": "Destination not whitelisted"}

@patch("main.application_layer.use_cases.transaction.Transaction")
@patch("main.application_layer.use_cases.transaction.EthereumService")
@patch("main.application_layer.use_cases.transaction.is_whitelist")
@patch("main.application_layer.use_cases.transaction.w3")
def test_validate_eth_transfer_success(mock_w3, mock_is_whitelist, mock_ethereum_service, mock_transaction, use_case):
    mock_transaction.get.return_value = None
    eth_service = mock_ethereum_service.return_value
    eth_service.get_transaction.return_value = {"to": "0xabc", "input": "0x", "value": 1000000000000000000}
    eth_service.get_transaction_receipt.return_value = {}
    eth_service.to_checksum_address.return_value = "0xabc"
    eth_service.from_wei.return_value = 1
    mock_is_whitelist.return_value = False
    mock_transaction.create = MagicMock()
    result = use_case.validate("0x456")
    assert result["valid"] is True
    assert result["transfers"][0]["asset"] == "ETH"
    assert result["transfers"][0]["to"] == "0xabc"
    assert result["transfers"][0]["amount"] == "1"

@patch("main.application_layer.use_cases.transaction.Transaction")
@patch("main.application_layer.use_cases.transaction.EthereumService")
@patch("main.application_layer.use_cases.transaction.is_whitelist")
@patch("main.application_layer.use_cases.transaction.w3")
def test_validate_erc20_transfer_not_whitelisted(mock_w3, mock_is_whitelist, mock_ethereum_service, mock_transaction, use_case):
    mock_transaction.get.return_value = None
    eth_service = mock_ethereum_service.return_value
    mock_w3.keccak.return_value.hex.return_value = "0xa9059cbb"
    tx = {"to": "0xcontract", "input": "0xa9059cbb", "value": 0}
    eth_service.get_transaction.return_value = tx
    log = {
        "topics": [MagicMock(hex=MagicMock(return_value="0xa9059cbb")), None, MagicMock(hex=MagicMock(return_value="0x000000000000000000000000abcdefabcdefabcdefabcdefabcdefabcdef"))],
        "address": "0xcontract",
        "data": MagicMock(hex=MagicMock(return_value="0x00000000000000000000000000000000000000000000000000000000000003e8"))
    }
    eth_service.get_transaction_receipt.return_value = {"logs": [log]}
    eth_service.to_checksum_address.return_value = "0xabcdefabcdefabcdefabcdefabcdefabcdefabcdef"
    mock_is_whitelist.return_value = True
    result = use_case.validate("0x789")
    assert result == {"valid": False, "reason": "Destination not whitelisted"}

@patch("main.application_layer.use_cases.transaction.Transaction")
@patch("main.application_layer.use_cases.transaction.EthereumService")
@patch("main.application_layer.use_cases.transaction.is_whitelist")
@patch("main.application_layer.use_cases.transaction.w3")
def test_validate_erc20_transfer_success(mock_w3, mock_is_whitelist, mock_ethereum_service, mock_transaction, use_case):
    mock_transaction.get.return_value = None
    eth_service = mock_ethereum_service.return_value
    mock_w3.keccak.return_value.hex.return_value = "0xa9059cbb"
    tx = {"to": "0xcontract", "input": "0xa9059cbb", "value": 0}
    eth_service.get_transaction.return_value = tx
    log = {
        "topics": [MagicMock(hex=MagicMock(return_value="0xa9059cbb")), None, MagicMock(hex=MagicMock(return_value="0x000000000000000000000000abcdefabcdefabcdefabcdefabcdefabcdef"))],
        "address": "0xcontract",
        "data": MagicMock(hex=MagicMock(return_value="0x00000000000000000000000000000000000000000000000000000000000003e8"))
    }
    eth_service.get_transaction_receipt.return_value = {"logs": [log]}
    eth_service.to_checksum_address.return_value = "0xabcdefabcdefabcdefabcdefabcdefabcdefabcdef"
    mock_is_whitelist.return_value = False

    contract_mock = MagicMock()
    contract_mock.functions.symbol().call.return_value = "TKN"
    contract_mock.functions.decimals().call.return_value = 18
    eth_service.contract.return_value = contract_mock

    mock_transaction.create = MagicMock()
    result = use_case.validate("0x101")
    assert result["valid"] is True
    assert result["transfers"][0]["asset"] == "TKN"
    assert result["transfers"][0]["to"] == "0xabcdefabcdefabcdefabcdefabcdefabcdefabcdef"
    assert result["transfers"][0]["amount"] == str(1000 / (10 ** 18))

@patch("main.application_layer.use_cases.transaction.Transaction")
@patch("main.application_layer.use_cases.transaction.EthereumService")
@patch("main.application_layer.use_cases.transaction.is_whitelist")
@patch("main.application_layer.use_cases.transaction.w3")
def test_validate_no_valid_transfers(mock_w3, mock_is_whitelist, mock_ethereum_service, mock_transaction, use_case):
    mock_transaction.get.return_value = None
    eth_service = mock_ethereum_service.return_value
    eth_service.get_transaction.return_value = {"to": "0xabc", "input": "0x", "value": 0}
    eth_service.get_transaction_receipt.return_value = {"logs": []}
    result = use_case.validate("0x202")
    assert result == {"valid": False, "reason": "No valid transfers to whitelisted addresses"}