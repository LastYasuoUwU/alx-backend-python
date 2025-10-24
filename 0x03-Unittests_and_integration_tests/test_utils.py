#!/usr/bin/env python3
import unittest
import unittest
from parameterized import parameterized
from utils import access_nested_map


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
        ({}, ("a",)),             # Empty dict, key "a" doesn’t exist
        ({"a": 1}, ("a", "b")),   # "b" doesn’t exist under "a"
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that KeyError is raised when path is invalid."""
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        # Check that the KeyError message matches the missing key
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")
