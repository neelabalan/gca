import unittest
import os
from unittest import mock

from gca.repositories import fetch_responses, get_clone_urls


class TestRepositories( unittest.TestCase ):

    @mock.patch( 'gca.repositories.requests.get' )
    def test_fetch_responses( self, mock_get ):
        mock_get.return_value.json.return_value = [{
            'ssh_url': 'git@github.com:xenonbloom/AnatomyPark',
            'repo_name': 'AnatomyPark'
        }]
        self.assertEqual(
            fetch_responses({
                'repositories': { 'name': 'xenonbloom', 'public_repos': 1, 'type': 'User' } 
            }), 
            [{
                'ssh_url': 'git@github.com:xenonbloom/AnatomyPark',
                'repo_name': 'AnatomyPark'
            }]
        )

    def test_get_clone_urls( self ):
        responses = { 
            'repositories':[
                { 'name': 'MeeseeksBox', 'ssh_url': 'git@github.com:rick/meeseeksbox', 'extrafield': 'golf' },
                { 'name': 'vindicator', 'ssh_url': 'git@github.com:rick/vindicator', 'extrafield': 'kinesis' }
            ]
        }
        self.assertEqual(
            get_clone_urls( responses ),
            [
                ( 'MeeseeksBox', 'git@github.com:rick/meeseeksbox' ),
                ( 'vindicator', 'git@github.com:rick/vindicator' )
            ]
        )

    def test_dump_summary( self ):
        pass


