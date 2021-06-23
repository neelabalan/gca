import unittest
import os
from unittest import mock


class TestGists( unittest.TestCase ):

    @mock.patch( 'gca.gists.requests.get' )
    def test_fetch_responses( self, mock_get ):
        mock_get.return_value.json.return_value = [{
            'git_pull_url': 'https://gist.github.com/123456789.git',
            'id': '123456789'
        }]

        self.assertEqual(
            fetch_responses({
                'gists': { 'name': 'Rocky', 'public_gists': 1 } 
            }), 
            [{
                'git_pull_url': 'https://gist.github.com/123456789.git',
                'id': '123456789'
            }]
        )

    def test_get_clone_urls( self ):
        responses = {
            'gca.gists': [
                { 'id': '81726498', 'git_pull_url': 'https://gist.github.com/81726498.git', 'extrafield': 'golf' },
                { 'id': '98734598', 'git_pull_url': 'https://gist.github.com/98734598.git', 'extrafield': 'kinesis' }
            ]
        }

        self.assertEqual(
            get_clone_urls( responses ),
            [
                ( '81726498', 'https://gist.github.com/81726498.git' ),
                ( '98734598', 'https://gist.github.com/98734598.git' )
            ]
        )

    @mock.patch( 'gca.gists.subprocess' )
    def test_execute_cloning( self, mock_subp ):
        url_map = {
            'gca.gists':[
                ('gist1', 'https://gist.github.com/gist1'), 
                ('gist2', 'https://gist.github.com/gist2')
            ]
        }
        execute_cloning( url_map )
        mock_subp.run.assert_any_call(
            args   = ['git', 'clone', 'https://gist.github.com/gist2'],
            stdout = mock_subp.DEVNULL,
            stderr = mock_subp.DEVNULL
        )


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


