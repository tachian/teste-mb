import unittest
from unittest.mock import MagicMock, patch
from main.application_layer.adapters.ethereum_service import EthereumService

class TestEthereumService(unittest.TestCase):
    def setUp(self):
        self.mock_w3 = MagicMock()
        self.service = EthereumService(self.mock_w3)

    def test_is_connected(self):
        self.mock_w3.is_connected.return_value = True
        self.assertTrue(self.service.is_connected)
        self.mock_w3.is_connected.assert_called_once()

    def test_gas_price(self):
        self.mock_w3.eth.gas_price = 12345
        self.assertEqual(self.service.gas_price, 12345)

    def test_create(self):
        mock_account = MagicMock()
        self.mock_w3.eth.account.create.return_value = mock_account
        result = self.service.create()
        self.assertEqual(result, mock_account)
        self.mock_w3.eth.account.create.assert_called_once()

    def test_get_transaction(self):
        self.mock_w3.eth.get_transaction.return_value = {"hash": "0xabc"}
        result = self.service.get_transaction("0xabc")
        self.assertEqual(result, {"hash": "0xabc"})
        self.mock_w3.eth.get_transaction.assert_called_once_with("0xabc")

    def test_get_transaction_receipt(self):
        self.mock_w3.eth.get_transaction_receipt.return_value = {"status": 1}
        result = self.service.get_transaction_receipt("0xabc")
        self.assertEqual(result, {"status": 1})
        self.mock_w3.eth.get_transaction_receipt.assert_called_once_with("0xabc")

    def test_to_checksum_address(self):
        self.mock_w3.to_checksum_address.return_value = "0xABC"
        result = self.service.to_checksum_address("0xabc")
        self.assertEqual(result, "0xABC")
        self.mock_w3.to_checksum_address.assert_called_once_with("0xabc")

    def test_from_wei(self):
        self.mock_w3.from_wei.return_value = 1.23
        result = self.service.from_wei(123, "ether")
        self.assertEqual(result, 1.23)
        self.mock_w3.from_wei.assert_called_once_with(123, "ether")

    def test_to_wei(self):
        self.mock_w3.to_wei.return_value = 123
        result = self.service.to_wei(1.23, "ether")
        self.assertEqual(result, 123)
        self.mock_w3.to_wei.assert_called_once_with(1.23, "ether")

    def test_get_transaction_count(self):
        self.mock_w3.eth.get_transaction_count.return_value = 7
        result = self.service.get_transaction_count("0xabc")
        self.assertEqual(result, 7)
        self.mock_w3.eth.get_transaction_count.assert_called_once_with("0xabc")

    def test_contract(self):
        with patch.object(self.service, 'to_checksum_address', return_value="0xABC") as mock_checksum:
            self.mock_w3.eth.contract.return_value = "contract"
            abi = [{"type": "function"}]
            result = self.service.contract("0xabc", abi)
            self.assertEqual(result, "contract")
            mock_checksum.assert_called_once_with("0xabc")
            self.mock_w3.eth.contract.assert_called_once_with(address="0xABC", abi=abi)

    def test_estimate_gas(self):
        self.mock_w3.eth.estimate_gas.return_value = 21000
        tx = {"from": "0xabc"}
        result = self.service.estimate_gas(tx)
        self.assertEqual(result, 21000)
        self.mock_w3.eth.estimate_gas.assert_called_once_with(tx)

    def test_send_transaction(self):
        self.mock_w3.eth.send_transaction.return_value = "tx_hash"
        tx = {"from": "0xabc"}
        result = self.service.send_transaction(tx)
        self.assertEqual(result, "tx_hash")
        self.mock_w3.eth.send_transaction.assert_called_once_with(tx)

    def test_wait_for_transaction_receipt(self):
        self.mock_w3.eth.wait_for_transaction_receipt.return_value = {"status": 1}
        result = self.service.wait_for_transaction_receipt("0xabc", timeout=10)
        self.assertEqual(result, {"status": 1})
        self.mock_w3.eth.wait_for_transaction_receipt.assert_called_once_with("0xabc", timeout=10)

    def test_sign_transaction(self):
        self.mock_w3.eth.account.sign_transaction.return_value = "signed"
        tx = {"from": "0xabc"}
        result = self.service.sign_transaction(tx, "privkey")
        self.assertEqual(result, "signed")
        self.mock_w3.eth.account.sign_transaction.assert_called_once_with(tx, "privkey")

    def test_send_raw_transaction(self):
        self.mock_w3.eth.send_raw_transaction.return_value = "raw_hash"
        tx = b"raw"
        result = self.service.send_raw_transaction(tx)
        self.assertEqual(result, "raw_hash")
        self.mock_w3.eth.send_raw_transaction.assert_called_once_with(tx)
