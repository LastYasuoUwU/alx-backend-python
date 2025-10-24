# Unit Test for `access_nested_map` Function

## 📘 Overview

This project demonstrates how to write **unit tests** in Python using the `unittest` framework and the `parameterized` library.

The focus of this task is testing the function `access_nested_map` located in the `utils` module.  
This function is used to retrieve values from a **nested dictionary** (a dictionary inside another dictionary) by following a given sequence of keys.

---

## 🧩 Function Description

**File:** `utils.py`

```python
def access_nested_map(nested_map, path):
    """Access nested map by following keys in the path."""
    for key in path:
        nested_map = nested_map[key]
    return nested_map
```
