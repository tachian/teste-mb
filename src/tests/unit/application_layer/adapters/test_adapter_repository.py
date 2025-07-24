import unittest
from unittest.mock import patch, MagicMock, call
from main.application_layer.adapters.address_repository import SQLAlchemyAddressRepository

# test_address_repository.py


class TestSQLAlchemyAddressRepository(unittest.TestCase):
    @patch("main.application_layer.adapters.address_repository.AddressFactory")
    @patch("main.application_layer.adapters.address_repository.db")
    @patch("main.application_layer.adapters.address_repository.address_table")
    def test_get(self, mock_address_table, mock_db, mock_factory):
        # Setup
        mock_address1 = MagicMock(uuid="uuid1", address="addr1", private_key="pk1")
        mock_address2 = MagicMock(uuid="uuid2", address="addr2", private_key="pk2")
        mock_db.session.query.return_value.all.return_value = [mock_address1, mock_address2]
        mock_factory.return_value.create_address.side_effect = ["address_obj1", "address_obj2"]

        # Act
        result = SQLAlchemyAddressRepository.get()

        # Assert
        self.assertEqual(result, ["address_obj1", "address_obj2"])
        self.assertEqual(mock_factory.call_count, 2)
        self.assertEqual(
            mock_factory.call_args_list,
            [
                call(uuid="uuid1", address="addr1", private_key="pk1"),
                call(uuid="uuid2", address="addr2", private_key="pk2"),
            ]
        )
        self.assertEqual(mock_factory.return_value.create_address.call_count, 2)

    @patch("main.application_layer.adapters.address_repository.AddressFactory")
    @patch("main.application_layer.adapters.address_repository.db")
    @patch("main.application_layer.adapters.address_repository.address_table")
    def test_get_address_found(self, mock_address_table, mock_db, mock_factory):
        # Setup
        mock_address = MagicMock(uuid="uuid1", address="addr1", private_key="pk1")
        mock_db.session.query.return_value.filter.return_value.first.return_value = mock_address
        mock_factory.return_value.create_address.return_value = "address_obj"

        # Act
        result = SQLAlchemyAddressRepository.get_address("addr1")

        # Assert
        self.assertEqual(result, "address_obj")
        mock_factory.assert_called_once_with(uuid="uuid1", address="addr1", private_key="pk1")
        mock_factory.return_value.create_address.assert_called_once()

    @patch("main.application_layer.adapters.address_repository.AddressFactory")
    @patch("main.application_layer.adapters.address_repository.db")
    @patch("main.application_layer.adapters.address_repository.address_table")
    def test_get_address_not_found(self, mock_address_table, mock_db, mock_factory):
        # Setup
        mock_db.session.query.return_value.filter.return_value.first.return_value = None

        # Act
        result = SQLAlchemyAddressRepository.get_address("addrX")

        # Assert
        self.assertIsNone(result)
        mock_factory.assert_not_called()

    @patch("main.application_layer.adapters.address_repository.db")
    @patch("main.application_layer.adapters.address_repository.address_table")
    def test_create_success(self, mock_address_table, mock_db):
        # Setup
        mock_insert = MagicMock()
        mock_values = MagicMock()
        mock_address_table.insert.return_value = mock_insert
        mock_insert.values.return_value = mock_values

        # Act
        SQLAlchemyAddressRepository.create("addr1", "pk1")

        # Assert
        mock_address_table.insert.assert_called_once()
        mock_insert.values.assert_called_once()
        mock_db.session.execute.assert_called_once_with(mock_values)
        mock_db.session.flush.assert_called_once()

    @patch("main.application_layer.adapters.address_repository.db")
    @patch("main.application_layer.adapters.address_repository.address_table")
    def test_create_exception(self, mock_address_table, mock_db):
        # Setup
        mock_insert = MagicMock()
        mock_values = MagicMock()
        mock_address_table.insert.return_value = mock_insert
        mock_insert.values.return_value = mock_values
        mock_db.session.execute.side_effect = Exception("DB error")

        # Act & Assert
        with self.assertRaises(Exception):
            SQLAlchemyAddressRepository.create("addr1", "pk1")
        mock_db.session.rollback.assert_called_once()