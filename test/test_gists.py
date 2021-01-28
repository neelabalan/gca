import unittest
import os
from unittest import mock

from gca.gists import fetch_responses, get_clone_urls

class TestGists( unittest.TestCase ):

    @mock.patch( 'gca.gists.requests.get' )
    def test_fetch_responses( self, mock_get ):
        mock_get.return_value.json.return_value = [{
            'git_pull_url': 'https://gist.github.com/123456789.git',
            'id': '123456789'
        }]

        self.assertEqual(
            fetch_responses( { 'name': 'Rocky', 'public_gists': 1 } ), 
            [{
                'git_pull_url': 'https://gist.github.com/123456789.git',
                'id': '123456789'
            }]
        )

    def test_get_clone_urls( self ):
        responses = [
            { 'id': '81726498', 'git_pull_url': 'https://gist.github.com/81726498.git', 'extrafield': 'golf' },
            { 'id': '98734598', 'git_pull_url': 'https://gist.github.com/98734598.git', 'extrafield': 'kinesis' }
        ]
        self.assertEqual(
            get_clone_urls( responses ),
            [
                ( '81726498', 'https://gist.github.com/81726498.git' ),
                ( '98734598', 'https://gist.github.com/98734598.git' )
            ]
        )


    def test_dump_summary( self ):
        pass

if __name__ == '__main__':
    unittest.main()