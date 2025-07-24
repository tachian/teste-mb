import pytest
from unittest.mock import patch, MagicMock
from main.application_layer.use_cases.address import AddressUseCase
from main.app import create_app

@pytest.fixture(autouse=True)
def app_context():
    with create_app().app_context():
        yield

@pytest.fixture
def mock_ethereum_service():
    with patch('main.application_layer.use_cases.address.EthereumService') as mock_service_cls:
        mock_service = MagicMock()
        mock_account = MagicMock()
        mock_account.address = '0x123'
        mock_account.key.hex.return_value = '0xabc'
        mock_service.create.return_value = mock_account
        mock_service_cls.return_value = mock_service
        yield mock_service

@pytest.fixture
def mock_address_model():
    with patch('main.application_layer.use_cases.address.Address') as mock_address_cls:
        yield mock_address_cls

def test_generate_creates_addresses(mock_ethereum_service, mock_address_model):
    use_case = AddressUseCase()
    result = use_case.generate(2)
    assert result == ['0x123', '0x123']
    assert mock_ethereum_service.create.call_count == 2
    assert mock_address_model.create.call_count == 2
    mock_address_model.create.assert_called_with(address='0x123', private_key='0xabc')

def test_get_returns_addresses(mock_address_model):
    mock_address_model.get.return_value = ['addr1', 'addr2']
    use_case = AddressUseCase()
    result = use_case.get()
    assert result == ['addr1', 'addr2']
    mock_address_model.get.assert_called_once()