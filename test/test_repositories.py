import unittest
import os
from unittest import mock

from gca.repositories import fetch_responses, get_clone_urls, execute_cloning


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
            'gca.repositories':[
                { 'name': 'MeeseeksBox', 'clone_url': 'git@github.com:rick/meeseeksbox', 'extrafield': 'golf' },
                { 'name': 'vindicator', 'clone_url': 'git@github.com:rick/vindicator', 'extrafield': 'kinesis' }
            ]
        }
        self.assertEqual(
            get_clone_urls( responses ),
            [
                ( 'MeeseeksBox', 'git@github.com:rick/meeseeksbox' ),
                ( 'vindicator', 'git@github.com:rick/vindicator' )
            ]
        )

    @mock.patch( 'gca.repositories.subprocess' )
    def test_execute_cloning( self, mock_subp ):
        url_map = {
            'gca.repositories':[
                ('repo1', 'git@github.com:user1/repo1'), 
                ('repo2', 'git@github.com:user2/repo2')
            ]
        }
        execute_cloning( url_map )
        mock_subp.run.assert_any_call(
            args   = ['git', 'clone', 'git@github.com:user1/repo1'],
            stdout = mock_subp.DEVNULL,
            stderr = mock_subp.DEVNULL
        )


    def test_dump_summary( self ):
        pass


