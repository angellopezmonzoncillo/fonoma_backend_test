# Unit Tests for Fonoma Backend Test

This directory contains comprehensive unit tests for the Fonoma Backend Test application.

## Test Files

### 1. `test_business_logic.py`
**Standalone business logic tests** - No external dependencies required

Tests the core functionality using mock implementations:
- ✅ Order processing with different criteria (`completed`, `pending`, `canceled`, `all`)
- ✅ Input validation (negative prices, zero quantities, invalid status)
- ✅ Edge cases and boundary conditions
- ✅ Decimal precision and rounding
- ✅ Error handling and exception scenarios
- ✅ Integration workflow testing

**Coverage:**
- `process_orders` function logic
- Order model validation
- OrderList model validation
- Complete business workflow

### 2. `test_api_endpoints.py`
**API endpoint tests** - Requires FastAPI dependencies

Tests the REST API functionality:
- ✅ POST `/fonoma/backend/solution` endpoint
- ✅ GET `/fonoma/backend/example` endpoint
- ✅ HTTP status codes validation
- ✅ Request/response validation
- ✅ Error handling and validation errors
- ✅ Response format validation

**Prerequisites:**
```bash
pip install fastapi uvicorn httpx
```

### 3. `run_all_tests.py`
**Comprehensive test runner**

Executes all available tests and provides detailed reporting:
- Dependency checking
- Test execution planning
- Comprehensive reporting
- Installation instructions

## Quick Start

### Run All Tests
```bash
cd app
python run_all_tests.py
```

### Run Individual Test Suites
```bash
# Business logic tests (no dependencies required)
python test_business_logic.py

# API endpoint tests (requires FastAPI)
python test_api_endpoints.py
```

## Test Results Summary

✅ **21 business logic tests** - All passing
- Process orders functionality: 8 tests
- Order validation: 8 tests  
- OrderList validation: 4 tests
- Integration workflow: 1 test

⏭️ **API endpoint tests** - Available when dependencies installed
- Solution endpoint: 8 tests
- Example endpoint: 2 tests
- Response format: 2 tests

## Installation for Complete Testing

To run all tests including API endpoint validation:

```bash
# Install required dependencies
pip install fastapi uvicorn httpx

# Run complete test suite
python run_all_tests.py
```

## Test Data

Tests use realistic sample data including:
- Orders with different statuses (completed, pending, canceled)
- Various price points and quantities
- Edge cases (high prices, large quantities)
- Invalid data scenarios

### Sample Test Case
```python
# Sample data from README example
orders = [
    {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
    {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
    {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90, "status": "completed"},
    {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"},
]

# Expected result for "completed" criterion: 1299.69
```

## Validation Features Tested

### Input Validation
- ❌ Negative prices rejected
- ❌ Zero or negative quantities rejected  
- ❌ Invalid status values rejected
- ❌ Invalid criterion values rejected

### Business Logic
- ✅ Correct filtering by status
- ✅ Accurate revenue calculation
- ✅ Proper decimal rounding
- ✅ Empty order list handling

### API Functionality
- ✅ Correct HTTP status codes
- ✅ JSON request/response handling
- ✅ Error message formatting
- ✅ CORS headers validation

## Framework

- **Testing Framework:** Python's built-in `unittest`
- **API Testing:** FastAPI's `TestClient`
- **Mocking:** Custom mock implementations for standalone testing
- **Coverage:** Comprehensive business logic and API endpoint coverage

## Architecture

The test suite is designed to:
1. **Work without external dependencies** for core business logic
2. **Gracefully handle missing dependencies** with clear instructions
3. **Provide comprehensive coverage** of all application functionality
4. **Support both unit and integration testing** approaches

## Running in CI/CD

The test suite is designed for automated testing:

```bash
# Basic tests (always available)
python test_business_logic.py

# Complete tests (with dependencies)
pip install fastapi uvicorn httpx
python run_all_tests.py
```

Exit codes:
- `0`: All tests passed
- `1`: Some tests failed  
- `2`: No tests executed (dependency issues)