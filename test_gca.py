import unittest
from gca import _get_numberof_repos_gists_and_type
from unittest import mock

class GcaTests( unittest.TestCase ):
    @mock.patch('gca.requests.get') 
    def test_get_numberof_repos_gists_and_type( self, mock_get ):
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

    def test_write_readme_for_gist( self ):
        pass

    def test_get_gitclone_info( self ):
        pass





if __name__ == '__main__':
    unittest.main()