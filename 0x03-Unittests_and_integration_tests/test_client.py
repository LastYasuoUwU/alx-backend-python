#!/usr/bin/env python3
"""Unit tests for GithubOrgClient"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        # Setup mock return value
        expected_response = {"login": org_name, "id": 12345}
        mock_get_json.return_value = expected_response

        # Create client instance and access org property
        client = GithubOrgClient(org_name)
        result = client.org

        # Assert get_json was called once with the correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)

        # Assert the result matches the mocked return value
        self.assertEqual(result, expected_response)

    @patch(
        'client.GithubOrgClient.org',
        new_callable=lambda: property(
            lambda self: {
                "repos_url": "https://api.github.com/orgs/test/repos"
            }
        )
    )
    def test_public_repos_url(self, mock_org):
        """Test that _public_repos_url returns the expected URL"""
        # Create a known payload
        expected_payload = {
            "repos_url": "https://api.github.com/orgs/test/repos",
            "login": "test",
            "id": 12345
        }

        # Use patch as a context manager to mock the org property
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=lambda: property(lambda self: expected_payload)
        ):
            # Create client instance
            client = GithubOrgClient("test")

            # Access _public_repos_url
            result = client._public_repos_url

            # Assert the result is the expected repos_url
            self.assertEqual(result, expected_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repos"""
        # Define the payload that get_json will return
        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}},
        ]
        mock_get_json.return_value = test_payload

        # Use patch as a context manager to mock _public_repos_url
        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=lambda: property(
                lambda self: "https://api.github.com/orgs/test/repos"
            )
        ) as mock_public_repos_url:
            # Create client instance
            client = GithubOrgClient("test")

            # Call public_repos method
            result = client.public_repos()

            # Expected list of repo names from the payload
            expected_repos = ["repo1", "repo2", "repo3"]

            # Assert the result matches expected repos
            self.assertEqual(result, expected_repos)

            # Assert _public_repos_url was accessed once
            mock_public_repos_url

            # Assert get_json was called once
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test that has_license returns the expected result"""
        # Call the static method
        result = GithubOrgClient.has_license(repo, license_key)

        # Assert the result matches the expected value
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
