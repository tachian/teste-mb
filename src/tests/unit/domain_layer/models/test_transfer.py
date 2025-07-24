import pytest
from uuid import uuid4, UUID
from unittest.mock import patch, MagicMock
from main.domain_layer.models.transfer import Transfer

@pytest.fixture
def transfer_data():
    return {
        "uuid": uuid4(),
        "tx_hash": "0xabc123",
        "from_address": "0xfrom",
        "to_address": "0xto",
        "asset": "ETH",
        "value": 1.23,
        "status": "pending",
        "gas_used": 21000.0,
        "gas_price": 50.0
    }

def test_transfer_dataclass_fields(transfer_data):
    transfer = Transfer(**transfer_data)
    for key, value in transfer_data.items():
        assert getattr(transfer, key) == value

@patch("main.domain_layer.models.transfer.SQLAlchemyTransferRepository.get")
def test_get_calls_repository(mock_get):
    Transfer.get()
    mock_get.assert_called_once()

@patch("main.domain_layer.models.transfer.SQLAlchemyTransferRepository.create")
def test_create_calls_repository(mock_create):
    Transfer.create("0xabc", "0xfrom", "0xto", "ETH", 1.0, "pending", 21000.0, 50.0)
    mock_create.assert_called_once_with("0xabc", "0xfrom", "0xto", "ETH", 1.0, "pending", 21000.0, 50.0)

@patch("main.domain_layer.models.transfer.SQLAlchemyTransferRepository.update_tx_hash")
def test_update_tx_hash_calls_repository(mock_update):
    uid = uuid4()
    Transfer.update_tx_hash(uid, "0xnewhash")
    mock_update.assert_called_once_with(uuid=uid, tx_hash="0xnewhash")

@patch("main.domain_layer.models.transfer.SQLAlchemyTransferRepository.update_status")
def test_update_status_calls_repository(mock_update):
    uid = uuid4()
    Transfer.update_status(uid, "confirmed")
    mock_update.assert_called_once_with(uuid=uid, status="confirmed")

@patch("main.domain_layer.models.transfer.SQLAlchemyTransferRepository.update_confirmation")
def test_update_confirmation_calls_repository(mock_update):
    uid = uuid4()
    Transfer.update_confirmation(uid, "confirmed", 22000.0, "0xnewhash")
    mock_update.assert_called_once_with(uuid=uid, status="confirmed", gas_used=22000.0, tx_hash="0xnewhash")