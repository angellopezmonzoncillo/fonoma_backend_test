# Custom Instructions for Unit Test Generation

When generating unit tests for this FastAPI project, follow these guidelines:

## Project Context
- This is a FastAPI backend application for order processing
- Main application entry point: `app/main.py`
- Business logic: `app/routers/solution/controller.py`
- Data models: `app/models/solutions.py`
- Existing tests: `app/test_solution.py`

## Testing Framework and Patterns
- Use Python's built-in `unittest` framework (following existing pattern)
- Use `fastapi.testclient.TestClient` for API endpoint testing
- Test files should be placed in the `app/` directory with `test_` prefix

## Test Structure Guidelines
1. **Import Structure**: Follow the existing pattern:
   ```python
   import unittest
   from fastapi.testclient import TestClient
   from main import app
   ```

2. **Test Class Structure**: Create test classes inheriting from `unittest.TestCase`:
   ```python
   class TestClassName(unittest.TestCase):
       def setUp(self):
           self.client = TestClient(app)
   ```

3. **Test Method Naming**: Use descriptive test method names starting with `test_`:
   - `test_<function_name>_<scenario>`
   - Example: `test_process_orders_completed_status`

## Testing Priorities
1. **API Endpoints**: Test all HTTP methods, status codes, and response formats
2. **Business Logic**: Test the `process_orders` function with different criteria
3. **Data Validation**: Test Pydantic model validation (price validation, quantity validation)
4. **Edge Cases**: Test with empty orders, invalid data, boundary conditions
5. **Error Handling**: Test exception scenarios and error responses

## Specific Test Cases to Generate
- Valid order processing for each criterion ('completed', 'pending', 'canceled', 'all')
- Invalid data validation (negative prices, zero quantities)
- Empty order lists
- Invalid JSON payloads
- HTTP status code validation (200, 422, etc.)
- Response format validation

## Test Data
Use realistic test data similar to the existing dataset:
```python
test_orders = [
    {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
    {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
    # ... more test data
]
```

## Assertions
- Use appropriate assertions: `assertEqual`, `assertTrue`, `assertRaises`
- Validate both response data and HTTP status codes
- Test floating-point calculations with appropriate precision

## Running Tests
Tests should be runnable with:
```bash
cd app && python -m unittest test_<filename>.py
```

## Coverage Goals
- Aim for comprehensive test coverage of business logic
- Test both happy path and error scenarios
- Include integration tests for the full API workflow