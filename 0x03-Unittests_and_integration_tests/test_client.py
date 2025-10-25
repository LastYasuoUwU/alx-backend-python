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
        
        # Create client instance and call org method
        client = GithubOrgClient(org_name)
        result = client.org()
        
        # Assert get_json was called once with the correct URL
        expected_url = f"https://api.github.com/orgs/{org_name}"
        mock_get_json.assert_called_once_with(expected_url)
        
        # Assert the result matches the mocked return value
        self.assertEqual(result, expected_response)
