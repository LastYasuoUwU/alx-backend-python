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

    @patch('client.GithubOrgClient.org', new_callable=lambda: property(lambda self: {"repos_url": "https://api.github.com/orgs/test/repos"}))
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
            
            # Assert the result is the expected repos_url from the payload
            self.assertEqual(result, expected_payload["repos_url"])