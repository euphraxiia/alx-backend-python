# Unit Tests and Integration Tests

This directory contains unit tests and integration tests for the project.

## Test Files

### test_utils.py

Contains parameterized unit tests for the `access_nested_map` function from the `utils` module.

#### TestAccessNestedMap

A test class that inherits from `unittest.TestCase` and tests the `access_nested_map` function with various nested map structures and paths.

The tests use the `@parameterized.expand` decorator to test multiple input combinations:
- Simple nested map: `{"a": 1}` with path `("a",)` → expected: `1`
- Nested map with one level: `{"a": {"b": 2}}` with path `("a",)` → expected: `{"b": 2}`
- Nested map with two levels: `{"a": {"b": 2}}` with path `("a", "b")` → expected: `2`

## Running Tests

To run the tests, use:

```bash
python3 -m pytest test_utils.py
```

Or:

```bash
python3 -m unittest test_utils.py
```

## Requirements

- Python 3.x
- parameterized library (`pip install parameterized`)

