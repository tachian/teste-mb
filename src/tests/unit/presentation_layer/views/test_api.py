import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from main.presentation_layer.views.api import blueprint

@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(blueprint)
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_healthz(client):
    resp = client.get('/api/healthz')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['service'] == 'teste-mb API HealthCheck'
    assert data['version'] == '1.0'

@patch('main.presentation_layer.views.api.AddressUseCase')
def test_generate_success(mock_address_usecase, client):
    mock_instance = mock_address_usecase.return_value
    mock_instance.generate.return_value = ['addr1', 'addr2']
    resp = client.post('/api/generate', json={'quantity': 2})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['status'] == 'success'
    assert data['generated_addresses'] == ['addr1', 'addr2']

@patch('main.presentation_layer.views.api.AddressUseCase')
def test_generate_failure(mock_address_usecase, client):
    mock_instance = mock_address_usecase.return_value
    mock_instance.generate.side_effect = Exception("fail")
    resp = client.post('/api/generate', json={'quantity': 1})
    assert resp.status_code == 400
    data = resp.get_json()
    assert "fail" in data['message']

@patch('main.presentation_layer.views.api.AddressUseCase')
def test_addresses_success(mock_address_usecase, client):
    mock_addr = MagicMock()
    mock_addr.uuid = 'uuid1'
    mock_addr.address = 'address1'
    mock_instance = mock_address_usecase.return_value
    mock_instance.get.return_value = [mock_addr]
    resp = client.get('/api/addresses')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data == [{'uuid': 'uuid1', 'address': 'address1'}]

@patch('main.presentation_layer.views.api.AddressUseCase')
def test_addresses_failure(mock_address_usecase, client):
    mock_instance = mock_address_usecase.return_value
    mock_instance.get.side_effect = Exception("fail")
    resp = client.get('/api/addresses')
    assert resp.status_code == 400
    data = resp.get_json()
    assert "fail" in data['message']

@patch('main.presentation_layer.views.api.ValidateMapping')
@patch('main.presentation_layer.views.api.TransactionUseCase')
def test_validate_success(mock_tx_usecase, mock_validate_mapping, client):
    mock_validate_mapping.return_value.tx_hash = 'txhash'
    mock_tx_usecase.return_value.validate.return_value = {'valid': True}
    resp = client.post('/api/validate', data=json.dumps({'tx_hash': 'txhash'}), content_type='application/json')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data == {'valid': True}

@patch('main.presentation_layer.views.api.ValidateMapping')
@patch('main.presentation_layer.views.api.TransactionUseCase')
def test_validate_failure(mock_tx_usecase, mock_validate_mapping, client):
    mock_validate_mapping.return_value.tx_hash = 'txhash'
    mock_tx_usecase.return_value.validate.side_effect = Exception("fail")
    resp = client.post('/api/validate', data=json.dumps({'tx_hash': 'txhash'}), content_type='application/json')
    assert resp.status_code == 400
    data = resp.get_json()
    assert "fail" in data['message']

@patch('main.presentation_layer.views.api.TransactionUseCase')
def test_transactions_success(mock_tx_usecase, client):
    mock_tx_usecase.return_value.get_transanctions.return_value = [{'id': 1}]
    resp = client.get('/api/transactions')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data == [{'id': 1}]

@patch('main.presentation_layer.views.api.TransactionUseCase')
def test_transactions_failure(mock_tx_usecase, client):
    mock_tx_usecase.return_value.get_transanctions.side_effect = Exception("fail")
    resp = client.get('/api/transactions')
    assert resp.status_code == 400
    data = resp.get_json()
    assert "fail" in data['message']

@patch('main.presentation_layer.views.api.TransferMapping')
@patch('main.presentation_layer.views.api.TransferUseCase')
def test_transfer_success(mock_transfer_usecase, mock_transfer_mapping, client):
    mock_transfer_mapping.return_value.from_address = 'from'
    mock_transfer_mapping.return_value.private_key = 'key'
    mock_transfer_mapping.return_value.to_address = 'to'
    mock_transfer_mapping.return_value.asset = 'asset'
    mock_transfer_mapping.return_value.amount = 10
    mock_transfer_usecase.return_value.execute.return_value = {'tx': 'hash'}
    payload = {
        'from_address': 'from',
        'private_key': 'key',
        'to_address': 'to',
        'asset': 'asset',
        'amount': 10
    }
    resp = client.post('/api/transfer', data=json.dumps(payload), content_type='application/json')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data == {'tx': 'hash'}

@patch('main.presentation_layer.views.api.TransferMapping')
@patch('main.presentation_layer.views.api.TransferUseCase')
def test_transfer_failure(mock_transfer_usecase, mock_transfer_mapping, client):
    mock_transfer_mapping.return_value.from_address = 'from'
    mock_transfer_mapping.return_value.private_key = 'key'
    mock_transfer_mapping.return_value.to_address = 'to'
    mock_transfer_mapping.return_value.asset = 'asset'
    mock_transfer_mapping.return_value.amount = 10
    mock_transfer_usecase.return_value.execute.side_effect = Exception("fail")
    payload = {
        'from_address': 'from',
        'private_key': 'key',
        'to_address': 'to',
        'asset': 'asset',
        'amount': 10
    }
    resp = client.post('/api/transfer', data=json.dumps(payload), content_type='application/json')
    assert resp.status_code == 400
    data = resp.get_json()
    assert "fail" in data['message']