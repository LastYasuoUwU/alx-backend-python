#!/usr/bin/env python3
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from typing import Dict


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


class TestGetJson(unittest.TestCase):
    """Test cases for utils.get_json function."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """Test that get_json returns expected result."""
        # Configure mock to return a Mock with json method
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function
        result = get_json(test_url)

        # Assert requests.get was called once with test_url
        mock_get.assert_called_once_with(test_url)

        # Assert the result equals the test_payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Unit tests for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result and only calls method once."""

        class TestClass:
            """Test class for memoization."""

            def a_method(self):
                """Method to be called by memoized property."""
                return 42

            @memoize
            def a_property(self):
                """Memoized property that calls a_method."""
                return self.a_method()

        # Create an instance of TestClass
        test_obj = TestClass()

        # Mock the a_method to track calls
        with patch.object(test_obj, 'a_method', return_value=42) as mock_method:
            # Call a_property twice
            result1 = test_obj.a_property
            result2 = test_obj.a_property

            # Assert that both calls return the correct result
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Assert that a_method was only called once (memoization working)
            mock_method.assert_called_once()
