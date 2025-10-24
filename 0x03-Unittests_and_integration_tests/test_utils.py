#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """Unit tests for the access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test that access_nested_map returns correct values."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),             # Empty dict, key "a" doesn't exist
        ({"a": 1}, ("a", "b")),   # "b" doesn't exist under "a"
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that KeyError is raised when path is invalid."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        # Check that the KeyError message matches the missing key
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": True}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test that get_json returns expected result and calls requests.get."""
        # Mock the response from requests.get
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function
        result = get_json(test_url)

        # Assertions
        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)