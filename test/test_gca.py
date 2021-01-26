import unittest
import os
from unittest import mock
from collections import namedtuple

from gca.gca import (
    get_user_info,
    write_readme_for_gist, 
    get_gitclone_info,
    get_gist_info,
    get_repo_info,
    repo_info,
    gist_info,
    user_info
)


class GcaTests(unittest.TestCase):
    @mock.patch('gca.gca.requests.get')
    def test_get_user_info(self, mock_get):
        mock_get.return_value.json.return_value = {
            'public_repos': 1,
            'public_gists': 1,
            'type': 'Org'
        }
        mock_get.return_value.status_code = 200
        self.assertEqual(
            get_user_info('user'),
            user_info(
                username='user', 
                public_repos = 1, 
                public_gists = 1,
                type = 'Org'
            )
        )
        # no user test
        mock_get.return_value.status_code = 404
        self.assertEqual(
            get_user_info('nosuchuser'),
            None
        )

    def test_write_readme_for_gist(self):
        # pass
        self.assertFalse(os.path.isfile('GIST-README.md'))

        write_readme_for_gist(
            [
                gist_info(
                    id='id',
                    files='newfile.md',
                    description='sample description',
                    url='sample.com'
                )
            ]
        )
        self.assertTrue(os.path.isfile('GIST-README.md'))
        os.remove('GIST-README.md')

    @mock.patch('gca.gca.requests.get')
    def test_get_repo_info(self, mock_get):
        mock_get.return_value.json.return_value = [{
            'name': 'AnatomyPark',
            'git_url': 'git@github.com:xenonbloom/AnatomyPark'
        }]
        repos = get_repo_info(
            user_info( 
                username = 'xenonbloom', 
                public_repos = 1,
                public_gists = 1,
                type = 'User'
            )
        )
        self.assertEqual(
            repos, 
            [repo_info(name='AnatomyPark', url='git@github.com:xenonbloom/AnatomyPark')]
        )

    @mock.patch('gca.gca.requests.get')
    def test_get_gist_info(self, mock_get):
        mock_get.return_value.json.return_value = [{
            'id': 'c137',
            'files': {'topsecret.py':1},
            'description': 'schematics for ionic defibulizer',
            'git_pull_url': 'git@github.com:xenonbloom/AnatomyPark'
        }]

        gists = get_gist_info(
            user_info( 
                username = 'xenonbloom', 
                public_repos = 1,
                public_gists = 1,
                type = 'User'
            )
        )
        self.assertEqual(
            gists, 
            [
                gist_info(
                    id          = 'c137',
                    files       = ['topsecret.py'],
                    description = 'schematics for ionic defibulizer',
                    url         = 'git@github.com:xenonbloom/AnatomyPark'
                )
            ]
        )


if __name__ == '__main__':
    unittest.main()
