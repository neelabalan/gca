import unittest
import os
from unittest import mock

from gca.utils import get_user_response

class TestUtils( unittest.TestCase ):
    @mock.patch( 'gca.utils.requests.get' )
    def test_get_user_response( self, mock_get ):
        mock_get.return_value.json.return_value = {
            'public_gists': 1,
            'type': 'Org',
            'public_repos': 10,
            'name': 'bloom',
            'login': 'bloom'
        }

        mock_get.return_value.status_code = 200
        self.assertEqual(
            get_user_response( 'existinguser' ),
            {
                'repositories': {
                    'type': 'Org',
                    'public_repos': 10,
                    'name': 'bloom'
                },
                'gists': {
                    'public_gists': 1,
                    'name': 'bloom'
                }
            }
        )

        # no user test
        mock_get.return_value.status_code = 404
        self.assertEqual(
            get_user_response( 'nosuchuser' ),
            None
        )

