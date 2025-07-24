import pytest
from unittest.mock import patch, MagicMock
from main.application_layer.adapters.transaction_repository import SQLAlchemyTransactionRepository

@pytest.fixture
def mock_db_session():
    with patch("main.app.db.session") as mock_session:
        yield mock_session

@pytest.fixture
def mock_transaction_table():
    with patch("main.application_layer.persistency.tables.transaction_table") as mock_table:
        yield mock_table

@pytest.fixture
def mock_transaction_factory():
    with patch("main.application_layer.adapters.transaction_repository.TransactionFactory") as mock_factory:
        yield mock_factory

def test_get_transactions_success(mock_db_session, mock_transaction_table, mock_transaction_factory):
    # Arrange
    mock_transaction = MagicMock()
    mock_transaction.uuid = "uuid1"
    mock_transaction.tx_hash = "hash1"
    mock_transaction.asset = "asset1"
    mock_transaction.to_address = "address1"
    mock_transaction.value = 123.45

    mock_db_session.query.return_value.all.return_value = [mock_transaction]
    mock_instance = MagicMock()
    mock_instance.create_transaction.return_value = "transaction_obj"
    mock_transaction_factory.return_value = mock_instance

    # Act
    result = SQLAlchemyTransactionRepository.get_transactions()

    # Assert
    assert result == ["transaction_obj"]
    mock_db_session.query.assert_called_once()
    mock_transaction_factory.assert_called_once_with(
        uuid="uuid1",
        tx_hash="hash1",
        asset="asset1",
        to_address="address1",
        value=123.45
    )

def test_get_transactions_exception(mock_db_session):
    mock_db_session.query.side_effect = Exception("DB error")
    with pytest.raises(Exception) as excinfo:
        SQLAlchemyTransactionRepository.get_transactions()
    assert "DB error" in str(excinfo.value)

def test_get_transaction_found(mock_db_session, mock_transaction_table, mock_transaction_factory):
    mock_transaction = MagicMock()
    mock_transaction.uuid = "uuid2"
    mock_transaction.tx_hash = "hash2"
    mock_transaction.asset = "asset2"
    mock_transaction.to_address = "address2"
    mock_transaction.value = 543.21

    mock_db_session.query.return_value.filter.return_value.first.return_value = mock_transaction
    mock_instance = MagicMock()
    mock_instance.create_transaction.return_value = "transaction_obj2"
    mock_transaction_factory.return_value = mock_instance

    result = SQLAlchemyTransactionRepository.get_transaction("hash2")
    assert result == "transaction_obj2"
    mock_transaction_factory.assert_called_once_with(
        uuid="uuid2",
        tx_hash="hash2",
        asset="asset2",
        to_address="address2",
        value=543.21
    )

def test_get_transaction_not_found(mock_db_session, mock_transaction_table, mock_transaction_factory):
    mock_db_session.query.return_value.filter.return_value.first.return_value = None
    result = SQLAlchemyTransactionRepository.get_transaction("nonexistent")
    assert result is None

def test_get_transaction_exception(mock_db_session):
    mock_db_session.query.side_effect = Exception("DB error")
    with pytest.raises(Exception) as excinfo:
        SQLAlchemyTransactionRepository.get_transaction("hash")
    assert "DB error" in str(excinfo.value)

@patch("main.app.db.session")
@patch("main.application_layer.adapters.transaction_repository.transaction_table")
def test_create_success(mock_transaction_table, mock_db_session):
    mock_insert = MagicMock()
    mock_transaction_table.insert.return_value.values.return_value = mock_insert
    mock_db_session.execute.return_value = None
    mock_db_session.flush.return_value = None

    SQLAlchemyTransactionRepository.create("hash3", "asset3", "address3", 100.0)

    mock_transaction_table.insert.assert_called_once()
    mock_db_session.execute.assert_called_once()
    mock_db_session.flush.assert_called_once()

@patch("main.application_layer.adapters.transaction_repository.transaction_table")
@patch("main.app.db.session")
def test_create_exception(mock_db_session, mock_transaction_table):
    mock_transaction_table.insert.return_value.values.side_effect = Exception("Insert error")
    with pytest.raises(Exception) as excinfo:
        SQLAlchemyTransactionRepository.create("hash4", "asset4", "address4", 200.0)
    assert "Insert error" in str(excinfo.value)