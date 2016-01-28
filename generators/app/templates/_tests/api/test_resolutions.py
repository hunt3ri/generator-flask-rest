import unittest
from unittest.mock import patch
from app.api.resolutions import Resolutions
from app.models.dto import DTOs
from app import bootstrap_app


class TestResolutions(unittest.TestCase):

    def setUp(self):
        self.app = bootstrap_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.api.resolutions.resolution_store')
    def test_200_response_received_(self, mock_res_store):

        # Arrange
        test_id = '123'
        test_title = 'Test Title'
        dto = DTOs.ResolutionDTO(res_id=test_id, title=test_title)
        mock_res_store.get_or_404.return_value = dto

        # Act
        response, http_status = Resolutions().get(test_id)
        dict_response = dict(response)

        # Assert
        self.assertEqual(http_status, 200, 'Http Status Should be 200')
        self.assertEqual(dict_response.get('title'), test_title)
        self.assertEqual(dict_response.get('url'), 'http://localhost/api/resolution/123')
