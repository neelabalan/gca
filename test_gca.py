import unittest
from unittest import mock
from gca import (
    construct_url,
    fetch_response,
    get_clone_urls,
    get_user_response,
    execute_cloning,
)

DEVNULL = -3


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestGca(unittest.TestCase):
    def test_construct_url(self):
        self.assertEqual(
            "https://api.github.com/users/testuser/repos?per_page=100&page={page}",
            construct_url("testuser", "User", "repo"),
        )
        self.assertEqual(
            "https://api.github.com/users/testuser/gists?per_page=100&page={page}",
            construct_url("testuser", "User", "gist"),
        )
        self.assertEqual(
            "https://api.github.com/orgs/testuser/repos?per_page=100&page={page}",
            construct_url("testuser", "Orgs", "repo"),
        )

    @mock.patch("gca.requests")
    def test_fetch_response(self, mock_requests):
        mock_requests.get.side_effect = [
            MockResponse(
                json_data=[
                    {
                        "clone_url": "https://gist.github.com/123456789.git",
                        "name": "testrepo",
                    }
                ],
                status_code=200,
            ),
            MockResponse(json_data=[], status_code=200),
        ]
        self.assertEqual(
            [
                {
                    "clone_url": "https://gist.github.com/123456789.git",
                    "name": "testrepo",
                }
            ],
            fetch_response(
                "https://api.github.com/orgs/testuser/repos?per_page=100&page={page}"
            ),
        )

    def test_get_clone_urls(self):
        response = {
            "repo": [
                {
                    "clone_url": "https://github.com:user1/repo1.git",
                    "ssh_url": "git@github.com:user2/repo2",
                    "name": "project1",
                }
            ]
        }
        self.assertEqual(
            {"project1": "https://github.com:user1/repo1.git"},
            get_clone_urls(response, ssh=False),
        )
        self.assertEqual(
            {"project1": "git@github.com:user2/repo2"},
            get_clone_urls(response, ssh=True),
        )

    @mock.patch("gca.requests")
    def test_get_user_response(self, mock_requests):
        mock_requests.get.return_value = MockResponse(
            json_data={"user": "rick"}, status_code=404
        )
        self.assertEqual(get_user_response("rick"), {"user": "rick"})

    @mock.patch("gca.subprocess")
    def test_execute_cloning(self, mock_subp):
        url_map = {
            "firstrepo": "git@github.com:user1/repo1",
            "secondrepo": "git@github.com:user2/repo2",
        }
        execute_cloning(url_map)
        mock_subp.run.assert_any_call(
            args=["git", "clone", "git@github.com:user1/repo1"],
            stdout=DEVNULL,
            stderr=DEVNULL,
        )


if __name__ == "__main__":
    unittest.main()
