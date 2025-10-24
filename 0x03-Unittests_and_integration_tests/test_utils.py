#!/usr/bin/env python3
import unittest
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)



print(access_nested_map({"a": 1}, ("a",)))           # → 1
print(access_nested_map({"a": {"b": 2}}, ("a",)))    # → {"b": 2}
print(access_nested_map({"a": {"b": 2}}, ("a", "b"))) # → 2