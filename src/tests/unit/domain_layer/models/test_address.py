import pytest
from uuid import uuid4
from unittest.mock import patch, MagicMock
from main.domain_layer.models.address import Address

@pytest.fixture
def address_data():
    return {
        "uuid": uuid4(),
        "address": "0x1234567890abcdef",
        "private_key": "privkey"
    }

def test_address_dataclass_fields(address_data):
    addr = Address(**address_data)
    assert addr.uuid == address_data["uuid"]
    assert addr.address == address_data["address"]
    assert addr.private_key == address_data["private_key"]

@patch("main.domain_layer.models.address.SQLAlchemyAddressRepository.get_address")
def test_get_with_address(mock_get_address):
    mock_addr = MagicMock()
    mock_get_address.return_value = mock_addr
    result = Address.get(address="0xabc")
    mock_get_address.assert_called_once_with(address="0xabc")
    assert result == mock_addr

@patch("main.domain_layer.models.address.SQLAlchemyAddressRepository.get")
def test_get_without_address(mock_get):
    mock_addr = MagicMock()
    mock_get.return_value = mock_addr
    result = Address.get()
    mock_get.assert_called_once_with()
    assert result == mock_addr

@patch("main.domain_layer.models.address.SQLAlchemyAddressRepository.create")
def test_create_address(mock_create):
    mock_addr = MagicMock()
    mock_create.return_value = mock_addr
    result = Address.create("0xabc", "privkey")
    mock_create.assert_called_once_with("0xabc", "privkey")
    assert result == mock_addr