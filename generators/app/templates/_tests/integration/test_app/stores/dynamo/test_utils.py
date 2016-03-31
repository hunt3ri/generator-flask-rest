import unittest
from app.stores.dynamo import utils

DYNAMODB_CONFIG = {
    'region_name': 'eu-west-1',
    'endpoint_url': 'https://dynamodb.eu-west-1.amazonaws.com'
}


class TestUtils(unittest.TestCase):

    @unittest.skip('Used for dev')
    def test_init_connections_raises_error_if_os_vars_not_found(self):
        with self.assertRaises(RuntimeError):
            utils.initialise_dynamo_connection(DYNAMODB_CONFIG)

    @unittest.skip('Used for dev')
    def test_init_connections_success(self):
        dynamo = utils.initialise_dynamo_connection(DYNAMODB_CONFIG)
