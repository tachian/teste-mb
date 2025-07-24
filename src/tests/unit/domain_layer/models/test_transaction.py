import pytest
from uuid import uuid4
from unittest.mock import patch, MagicMock
from main.domain_layer.models.transaction import Transaction

@pytest.fixture
def sample_transaction_data():
    return {
        "uuid": uuid4(),
        "tx_hash": "0xabc123",
        "asset": "ETH",
        "to_address": "0xdef456",
        "value": 1.23
    }

def test_transaction_dataclass_fields(sample_transaction_data):
    tx = Transaction(**sample_transaction_data)
    assert tx.uuid == sample_transaction_data["uuid"]
    assert tx.tx_hash == "0xabc123"
    assert tx.asset == "ETH"
    assert tx.to_address == "0xdef456"
    assert tx.value == 1.23

@patch("main.domain_layer.models.transaction.SQLAlchemyTransactionRepository.get_transaction")
def test_get_transaction_by_hash(mock_get_transaction):
    mock_tx = MagicMock()
    mock_get_transaction.return_value = mock_tx
    tx_hash = "0xabc123"
    result = Transaction.get(tx_hash=tx_hash)
    mock_get_transaction.assert_called_once_with(tx_hash=tx_hash)
    assert result == mock_tx

@patch("main.domain_layer.models.transaction.SQLAlchemyTransactionRepository.get_transactions")
def test_get_all_transactions(mock_get_transactions):
    mock_txs = [MagicMock(), MagicMock()]
    mock_get_transactions.return_value = mock_txs
    result = Transaction.get()
    mock_get_transactions.assert_called_once()
    assert result == mock_txs

@patch("main.domain_layer.models.transaction.SQLAlchemyTransactionRepository.create")
def test_create_transaction(mock_create):
    mock_tx = MagicMock()
    mock_create.return_value = mock_tx
    tx_hash = "0xabc123"
    asset = "ETH"
    to_address = "0xdef456"
    value = 1.23
    result = Transaction.create(tx_hash, asset, to_address, value)
    mock_create.assert_called_once_with(tx_hash, asset, to_address, value)
    assert result == mock_tx