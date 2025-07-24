import pytest
from unittest.mock import patch, MagicMock
from uuid import uuid4, UUID
from main.application_layer.adapters.transfer_repository import SQLAlchemyTransferRepository

@pytest.fixture
def mock_db_session():
    with patch("main.application_layer.adapters.transfer_repository.db") as mock_db:
        yield mock_db

@pytest.fixture
def mock_transfer_table():
    with patch("main.application_layer.adapters.transfer_repository.transfer_table") as mock_table:
        yield mock_table

@pytest.fixture
def mock_transfer_factory():
    with patch("main.application_layer.adapters.transfer_repository.TransferFactory") as mock_factory:
        yield mock_factory

def make_transfer_row(uuid=None):
    m = MagicMock()
    m.uuid = uuid or uuid4()
    m.tx_hash = "0xabc"
    m.from_address = "0xfrom"
    m.to_address = "0xto"
    m.asset = "ETH"
    m.value = 1.23
    m.status = "pending"
    m.gas_used = 21000
    m.gas_price = 100
    return m

def test_get_all_transfers(mock_db_session, mock_transfer_table, mock_transfer_factory):
    transfer_row = make_transfer_row()
    mock_db_session.session.query.return_value.all.return_value = [transfer_row]
    mock_transfer_factory.return_value.create_transfer.return_value = "transfer_obj"

    result = SQLAlchemyTransferRepository.get()
    assert result == ["transfer_obj"]
    mock_transfer_factory.assert_called_once_with(
        uuid=transfer_row.uuid,
        tx_hash=transfer_row.tx_hash,
        from_address=transfer_row.from_address,
        to_address=transfer_row.to_address,
        asset=transfer_row.asset,
        value=transfer_row.value,
        status=transfer_row.status,
        gas_used=transfer_row.gas_used,
        gas_price=transfer_row.gas_price,
    )

def test_get_transfer_by_uuid(mock_db_session, mock_transfer_table, mock_transfer_factory):
    transfer_row = make_transfer_row()
    mock_db_session.session.query.return_value.filter.return_value.first.return_value = transfer_row
    mock_transfer_factory.return_value.create_transfer.return_value = "transfer_obj"
    test_uuid = transfer_row.uuid

    result = SQLAlchemyTransferRepository.get(uuid=test_uuid)
    assert result == "transfer_obj"
    mock_transfer_factory.assert_called_once()

def test_create_transfer_success(mock_db_session, mock_transfer_table, mock_transfer_factory):
    inserted_uuid = uuid4()
    mock_cursor = MagicMock()
    mock_cursor.inserted_primary_key = [inserted_uuid]
    mock_db_session.session.execute.return_value = mock_cursor
    mock_transfer_factory.return_value.create_transfer.return_value = "transfer_obj"

    with patch.object(SQLAlchemyTransferRepository, "get", return_value="transfer_obj") as mock_get:
        result = SQLAlchemyTransferRepository.create(
            tx_hash="0xabc",
            from_address="0xfrom",
            to_address="0xto",
            asset="ETH",
            value=1.23,
            status="pending",
            gas_used=21000,
            gas_price=100
        )
        assert result == "transfer_obj"
        mock_get.assert_called_once_with(uuid=inserted_uuid)

def test_update_status_success(mock_db_session, mock_transfer_table, mock_transfer_factory):
    test_uuid = uuid4()
    with patch.object(SQLAlchemyTransferRepository, "get", return_value="transfer_obj") as mock_get:
        result = SQLAlchemyTransferRepository.update_status(uuid=test_uuid, status="confirmed")
        assert result == "transfer_obj"
        mock_get.assert_called_once_with(uuid=test_uuid)

def test_update_tx_hash_success(mock_db_session, mock_transfer_table, mock_transfer_factory):
    test_uuid = uuid4()
    with patch.object(SQLAlchemyTransferRepository, "get", return_value="transfer_obj") as mock_get:
        result = SQLAlchemyTransferRepository.update_tx_hash(uuid=test_uuid, tx_hash="0xnew")
        assert result == "transfer_obj"
        mock_get.assert_called_once_with(uuid=test_uuid)

def test_update_confirmation_success(mock_db_session, mock_transfer_table, mock_transfer_factory):
    test_uuid = uuid4()
    with patch.object(SQLAlchemyTransferRepository, "get", return_value="transfer_obj") as mock_get:
        result = SQLAlchemyTransferRepository.update_confirmation(
            uuid=test_uuid,
            status="confirmed",
            gas_used=22000,
            tx_hash="0xnew"
        )
        assert result == "transfer_obj"
        mock_get.assert_called_once_with(uuid=test_uuid)

def test_get_raises_exception_logs_and_raises(mock_db_session, mock_transfer_table, caplog):
    mock_db_session.session.query.side_effect = Exception("DB error")
    with pytest.raises(Exception):
        SQLAlchemyTransferRepository.get()
    assert "Error while trying to get Transfers" in caplog.text

def test_create_raises_exception_logs_and_raises(mock_db_session, mock_transfer_table, caplog):
    mock_db_session.session.execute.side_effect = Exception("Insert error")
    with pytest.raises(Exception):
        SQLAlchemyTransferRepository.create(
            tx_hash="0xabc",
            from_address="0xfrom",
            to_address="0xto",
            asset="ETH",
            value=1.23,
            status="pending",
            gas_used=21000,
            gas_price=100
        )
    assert "Error while trying to create Transaction" in caplog.text