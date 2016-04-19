import unittest
from unittest.mock import patch
from app.models.customers import Customer
from app.stores.dynamo.customer_store import CustomerStore

DYNAMODB_CONFIG = {
    'region_name': 'eu-west-1',
    'endpoint_url': 'https://dynamodb.eu-west-1.amazonaws.com'
}


class TestCustomerStore(unittest.TestCase):

    test_cust = None
    customer_store = None

    @patch.object(CustomerStore, 'config', DYNAMODB_CONFIG)
    def setUp(self):
        self.test_cust = Customer({'emailAddress': 'iain@hunter.com', 'firstName': 'Testy', 'surname': 'McTest'})
        self.customer_store = CustomerStore()
        self.customer_store.save(self.test_cust)  # This demonstrates save functionality

    def tearDown(self):
        self.customer_store.delete(self.test_cust.email_address)

    def test_get_returns_test_customer(self):
        # Act
        cust = self.customer_store.get(self.test_cust.email_address)

        # Assert
        self.assertEqual(cust, self.test_cust)

    def test_get_returns_none_if_customer_not_found(self):
        # Act
        cust = self.customer_store.get('noone@nothere.com')

        # Assert
        self.assertEqual(cust, None, 'Unmatched customer should return None, not raise an exception')


    def test_update_changes_values(self):
        # Arrange
        self.test_cust.first_name = 'Iain'
        self.test_cust.surname = 'Hunter'

        # Act
        self.customer_store.update(self.test_cust)

        # Assert
        updated_cust = self.customer_store.get(self.test_cust.email_address)

        self.assertEqual(updated_cust.first_name, 'Iain')
        self.assertEqual(updated_cust.surname, 'Hunter')
