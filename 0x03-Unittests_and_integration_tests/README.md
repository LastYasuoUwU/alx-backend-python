# Unit Testing Utils Module

This project contains comprehensive unit tests for utility functions including nested map access, JSON fetching, and memoization.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Test Classes](#test-classes)
- [Running Tests](#running-tests)
- [Code Style](#code-style)

## Overview

This test suite validates three main utility functions:

- `access_nested_map`: Navigate nested dictionary structures
- `get_json`: Fetch JSON data from URLs
- `memoize`: Cache function results to improve performance

## Installation

### Prerequisites

- Python 3.7+
- pip package manager

### Dependencies

Install required packages:

```bash
pip install parameterized
```

## Test Classes

### TestAccessNestedMap

Tests the `access_nested_map` function which retrieves values from nested dictionaries using a tuple path.

**Test Cases:**

- `test_access_nested_map`: Validates correct value retrieval

  - Simple key access: `{"a": 1}` with path `("a",)` returns `1`
  - Nested dict access: `{"a": {"b": 2}}` with path `("a",)` returns `{"b": 2}`
  - Deep nested access: `{"a": {"b": 2}}` with path `("a", "b")` returns `2`

- `test_access_nested_map_exception`: Validates KeyError handling
  - Empty dict with invalid path
  - Missing nested keys

### TestGetJson

Tests the `get_json` function which fetches JSON data from remote URLs without making actual HTTP calls.

**Features:**

- Uses `unittest.mock.patch` to mock `requests.get`
- Validates correct URL calling behavior
- Verifies returned JSON payload matches expected data

**Test Cases:**

```python
("http://example.com", {"payload": True})
("http://holberton.io", {"payload": False})
```

**Assertions:**

- `requests.get` is called exactly once per test
- Return value matches expected payload

### TestMemoize

Tests the `@memoize` decorator which caches method results to avoid redundant computations.

#### What is Memoization?

Memoization is an optimization technique that stores the results of expensive function calls and returns the cached result when the same inputs occur again.

#### How the Decorator Works

The `@memoize` decorator:

1. Converts a method into a property
2. Stores the result in a private attribute on first access
3. Returns the cached value on subsequent accesses

**Example Usage:**

```python
class MyClass:
    @memoize
    def expensive_operation(self):
        print("Computing...")
        return 42

obj = MyClass()
result1 = obj.expensive_operation  # Prints "Computing..." and returns 42
result2 = obj.expensive_operation  # Just returns 42 (cached)
```

#### Test Implementation

The test verifies that:

1. **Caching works**: Multiple accesses return the same result
2. **Efficiency**: The underlying method is called only once

**Test Structure:**

```python
class TestClass:
    def a_method(self):
        return 42

    @memoize
    def a_property(self):
        return self.a_method()
```

**Test Process:**

1. Create an instance of `TestClass`
2. Mock `a_method` to track calls
3. Access `a_property` twice
4. Verify both accesses return `42`
5. Verify `a_method` was called only once

## Running Tests

### Run All Tests

```bash
python -m unittest test_utils.py
```

### Run Specific Test Class

```bash
python -m unittest test_utils.TestMemoize
```

### Run Specific Test Method

```bash
python -m unittest test_utils.TestMemoize.test_memoize
```

### Verbose Output

```bash
python -m unittest test_utils.py -v
```

### Expected Output

```
test_access_nested_map (test_utils.TestAccessNestedMap) ... ok
test_access_nested_map_exception (test_utils.TestAccessNestedMap) ... ok
test_get_json (test_utils.TestGetJson) ... ok
test_memoize (test_utils.TestMemoize) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
```

## Code Style

This project follows PEP 8 style guidelines:

- Maximum line length: 79 characters
- Proper spacing and indentation
- Descriptive variable names
- Comprehensive docstrings

### Check Style Compliance

```bash
pycodestyle test_utils.py
```

or

```bash
flake8 test_utils.py
```

## Key Testing Concepts

### Mocking

Mocking replaces real objects with test doubles to:

- Avoid external dependencies (HTTP calls, databases)
- Control test behavior
- Track method calls and arguments

### Parameterized Tests

Using `@parameterized.expand` allows running the same test with different inputs:

```python
@parameterized.expand([
    (input1, expected1),
    (input2, expected2),
])
def test_function(self, input_val, expected):
    self.assertEqual(function(input_val), expected)
```

### Benefits of Testing Memoization

1. **Performance verification**: Ensures caching reduces computation
2. **Correctness**: Validates cached results match original results
3. **Regression prevention**: Catches bugs in caching logic

## Project Structure

```
.
├── test_utils.py       # Test suite
├── utils.py            # Utility functions being tested
└── README.md           # This file
```

## Contributing

When adding new tests:

1. Follow existing naming conventions
2. Include descriptive docstrings
3. Maintain PEP 8 compliance
4. Add parameterized tests for multiple scenarios
5. Mock external dependencies

## License

This project is part of a testing and quality assurance learning module.
