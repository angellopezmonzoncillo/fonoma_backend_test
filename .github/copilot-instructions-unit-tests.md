# Custom Instructions for Unit Test Generation

When generating unit tests for this FastAPI project, follow these guidelines:

## Context7 MCP Integration
- **ALWAYS** consult the Context7 MCP server when generating tests for this project
- Use Context7 to get up-to-date documentation for testing frameworks and libraries
- For FastAPI testing, query Context7 with: `Use Context7 to get FastAPI testing documentation and best practices`
- For unittest patterns, query: `Use Context7 to get Python unittest framework documentation and patterns`
- For Pydantic validation testing, query: `Use Context7 to get Pydantic testing documentation and validation patterns`

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

## Context7 Usage for Test Generation
When generating tests, use Context7 to ensure best practices:

### For FastAPI Testing:
```
Use Context7 to provide examples of FastAPI TestClient usage for POST endpoints with JSON validation
```

### For Pydantic Model Testing:
```
Use Context7 to show Pydantic validation testing patterns and error handling
```

### For Business Logic Testing:
```
Use Context7 to demonstrate comprehensive unit testing patterns for financial calculation functions
```

### Context7 Query Examples:
- `"FastAPI testing with TestClient POST requests and validation errors - use context7"`
- `"Python unittest patterns for API endpoint testing with JSON payloads - use context7"`
- `"Pydantic model validation testing with custom validators - use context7"`
- `"Testing floating point calculations in Python unittest framework - use context7"`

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
Tests should be runnable with multiple approaches:

### Basic Test Execution:
```bash
cd app && python -m unittest test_<filename>.py
```

### Comprehensive Test Execution:
```bash
# Run all tests with verbose output
cd app && python -m unittest discover -v

# Run specific test class
cd app && python -m unittest test_solution.TestSolutionEndpoint -v

# Run specific test method
cd app && python -m unittest test_solution.TestSolutionEndpoint.test_process_orders_completed_status -v

# Run tests with coverage (if coverage package available)
cd app && python -m coverage run -m unittest discover && python -m coverage report -m
```

### FastAPI Test Client Execution:
```bash
# Run with pytest style if available
cd app && python -m pytest test_*.py -v

# Run with FastAPI's test client directly
cd app && python -c "import test_solution; test_solution.main()"
```

## Test Result Reporting

### Generate Comprehensive Test Reports:
1. **Basic Test Results:**
   ```bash
   cd app && python -m unittest discover -v 2>&1 | tee test_results.txt
   ```

2. **Coverage Reports (if coverage installed):**
   ```bash
   cd app && python -m coverage run -m unittest discover
   cd app && python -m coverage report -m > coverage_report.txt
   cd app && python -m coverage html  # Generates HTML report in htmlcov/
   ```

3. **JUnit XML Reports (if xmlrunner available):**
   ```bash
   cd app && python -c "
   import xmlrunner
   import unittest
   
   # Discover and run tests with XML output
   loader = unittest.TestLoader()
   suite = loader.discover('.')
   runner = xmlrunner.XMLTestRunner(output='test-reports')
   runner.run(suite)
   "
   ```

4. **Custom Test Report Generation:**
   ```bash
   cd app && python -c "
   import unittest
   import sys
   from datetime import datetime
   
   class TestResultReporter:
       def generate_report(self):
           # Run tests and capture results
           loader = unittest.TestLoader()
           suite = loader.discover('.')
           runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=2)
           result = runner.run(suite)
           
           # Generate summary report
           print(f'\n=== TEST EXECUTION REPORT ===')
           print(f'Generated at: {datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")}')
           print(f'Tests run: {result.testsRun}')
           print(f'Failures: {len(result.failures)}')
           print(f'Errors: {len(result.errors)}')
           print(f'Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%')
           
           if result.failures:
               print(f'\nFAILURES:')
               for test, trace in result.failures:
                   print(f'- {test}: {trace.split(chr(10))[-2]}')
           
           if result.errors:
               print(f'\nERRORS:')
               for test, trace in result.errors:
                   print(f'- {test}: {trace.split(chr(10))[-2]}')
           
           return result.wasSuccessful()
   
   reporter = TestResultReporter()
   success = reporter.generate_report()
   sys.exit(0 if success else 1)
   "
   ```

### Report Output Structure:
- **test_results.txt**: Detailed test execution log
- **coverage_report.txt**: Line-by-line coverage analysis
- **htmlcov/**: Interactive HTML coverage report
- **test-reports/**: JUnit XML format for CI/CD integration

## Coverage Goals
- Aim for comprehensive test coverage of business logic
- Test both happy path and error scenarios
- Include integration tests for the full API workflow
- Generate coverage reports after each test run to track progress
- Target minimum 80% code coverage for business logic
- Ensure all critical paths in `process_orders` function are tested