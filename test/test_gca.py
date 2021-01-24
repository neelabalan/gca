import unittest
import os
from gca.gca import _get_numberof_repos_gists_and_type, write_readme_for_gist
from unittest import mock
from collections import namedtuple

gist_info = namedtuple('gistinfo', ['id', 'files', 'description', 'url'])


class GcaTests(unittest.TestCase):
    @mock.patch('gca.gca.requests.get')
    def test_get_numberof_repos_gists_and_type(self, mock_get):
        mock_get.return_value.json.return_value = {
            'public_repos': 1,
            'public_gists': 1,
            'type': 'org'
        }
        mock_get.return_value.status_code = 200
        self.assertEqual(
            _get_numberof_repos_gists_and_type('existing_user'),
            (1, 1, 'org')
        )

        # no user test
        mock_get.return_value.status_code = 404
        self.assertEqual(
            _get_numberof_repos_gists_and_type('existing_user'),
            (None, None)
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


    def test_get_gitclone_info(self):
        pass


if __name__ == '__main__':
    unittest.main()
