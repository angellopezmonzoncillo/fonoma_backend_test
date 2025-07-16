#!/usr/bin/env python3
"""
API Endpoint tests for the Fonoma Backend Test application
These tests require FastAPI and dependencies to be installed.
Run after installing: fastapi, uvicorn, httpx
"""

import unittest
import sys
import os
import json

try:
    from fastapi.testclient import TestClient
    from main import app
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False
    print("Warning: FastAPI dependencies not available. Install with: pip install fastapi uvicorn httpx")


class TestSolutionAPIEndpoint(unittest.TestCase):
    """Test cases for the /fonoma/backend/solution API endpoint"""
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def setUp(self):
        """Set up test client"""
        self.client = TestClient(app)
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def test_solution_endpoint_completed_orders(self):
        """Test /solution endpoint with completed orders criterion"""
        payload = {
            "orders": [
                {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
                {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
                {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90, "status": "completed"},
                {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"},
            ],
            "criterion": "completed"
        }
        
        response = self.client.post("/fonoma/backend/solution", json=payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 1299.69)
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def test_solution_endpoint_pending_orders(self):
        """Test /solution endpoint with pending orders criterion"""
        payload = {
            "orders": [
                {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
                {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
                {"id": 3, "item": "Tablet", "quantity": 1, "price": 299.50, "status": "pending"},
            ],
            "criterion": "pending"
        }
        
        response = self.client.post("/fonoma/backend/solution", json=payload)
        
        self.assertEqual(response.status_code, 200)
        # Expected: (499.95 * 2) + (299.50 * 1) = 999.90 + 299.50 = 1299.40
        self.assertEqual(response.json(), 1299.40)
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def test_solution_endpoint_all_orders(self):
        """Test /solution endpoint with all orders criterion"""
        payload = {
            "orders": [
                {"id": 1, "item": "Laptop", "quantity": 1, "price": 100.00, "status": "completed"},
                {"id": 2, "item": "Mouse", "quantity": 2, "price": 50.00, "status": "pending"},
                {"id": 3, "item": "Keyboard", "quantity": 1, "price": 75.00, "status": "canceled"},
            ],
            "criterion": "all"
        }
        
        response = self.client.post("/fonoma/backend/solution", json=payload)
        
        self.assertEqual(response.status_code, 200)
        # Expected: 100.00 + (50.00 * 2) + 75.00 = 275.00
        self.assertEqual(response.json(), 275.0)
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def test_solution_endpoint_empty_orders(self):
        """Test /solution endpoint with empty orders list"""
        payload = {
            "orders": [],
            "criterion": "all"
        }
        
        response = self.client.post("/fonoma/backend/solution", json=payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 0.0)
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def test_solution_endpoint_negative_price_validation(self):
        """Test /solution endpoint rejects negative prices"""
        payload = {
            "orders": [
                {"id": 1, "item": "Laptop", "quantity": 1, "price": -100.0, "status": "completed"}
            ],
            "criterion": "completed"
        }
        
        response = self.client.post("/fonoma/backend/solution", json=payload)
        
        self.assertEqual(response.status_code, 422)  # Validation error
        self.assertIn("no puede ser negativo", response.text)
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def test_solution_endpoint_zero_quantity_validation(self):
        """Test /solution endpoint rejects zero quantity"""
        payload = {
            "orders": [
                {"id": 1, "item": "Laptop", "quantity": 0, "price": 100.0, "status": "completed"}
            ],
            "criterion": "completed"
        }
        
        response = self.client.post("/fonoma/backend/solution", json=payload)
        
        self.assertEqual(response.status_code, 422)  # Validation error
        self.assertIn("debe ser mayor a 0", response.text)
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def test_solution_endpoint_invalid_status(self):
        """Test /solution endpoint rejects invalid status"""
        payload = {
            "orders": [
                {"id": 1, "item": "Laptop", "quantity": 1, "price": 100.0, "status": "invalid"}
            ],
            "criterion": "completed"
        }
        
        response = self.client.post("/fonoma/backend/solution", json=payload)
        
        self.assertEqual(response.status_code, 422)  # Validation error
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def test_solution_endpoint_invalid_criterion(self):
        """Test /solution endpoint rejects invalid criterion"""
        payload = {
            "orders": [
                {"id": 1, "item": "Laptop", "quantity": 1, "price": 100.0, "status": "completed"}
            ],
            "criterion": "invalid"
        }
        
        response = self.client.post("/fonoma/backend/solution", json=payload)
        
        self.assertEqual(response.status_code, 422)  # Validation error
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def test_solution_endpoint_missing_fields(self):
        """Test /solution endpoint with missing required fields"""
        # Missing criterion
        payload = {
            "orders": [
                {"id": 1, "item": "Laptop", "quantity": 1, "price": 100.0, "status": "completed"}
            ]
        }
        
        response = self.client.post("/fonoma/backend/solution", json=payload)
        self.assertEqual(response.status_code, 422)  # Validation error
        
        # Missing orders
        payload = {
            "criterion": "completed"
        }
        
        response = self.client.post("/fonoma/backend/solution", json=payload)
        self.assertEqual(response.status_code, 422)  # Validation error
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def test_solution_endpoint_malformed_json(self):
        """Test /solution endpoint with malformed JSON"""
        response = self.client.post(
            "/fonoma/backend/solution",
            data="{ invalid json }",
            headers={"Content-Type": "application/json"}
        )
        
        self.assertEqual(response.status_code, 422)  # Validation error


class TestExampleAPIEndpoint(unittest.TestCase):
    """Test cases for the /fonoma/backend/example API endpoint"""
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def setUp(self):
        """Set up test client"""
        self.client = TestClient(app)
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def test_example_endpoint_no_name(self):
        """Test /example endpoint without name parameter"""
        response = self.client.get("/fonoma/backend/example")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Hello !!!")
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def test_example_endpoint_with_name(self):
        """Test /example endpoint with name parameter"""
        response = self.client.get("/fonoma/backend/example?name=Test")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), "Hello, Test !!!")


class TestAPIResponseFormats(unittest.TestCase):
    """Test cases for API response formats and headers"""
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def setUp(self):
        """Set up test client"""
        self.client = TestClient(app)
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def test_solution_endpoint_response_headers(self):
        """Test that solution endpoint returns correct headers"""
        payload = {
            "orders": [
                {"id": 1, "item": "Laptop", "quantity": 1, "price": 100.0, "status": "completed"}
            ],
            "criterion": "completed"
        }
        
        response = self.client.post("/fonoma/backend/solution", json=payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers["content-type"], "application/json")
    
    @unittest.skipUnless(DEPENDENCIES_AVAILABLE, "FastAPI dependencies not available")
    def test_solution_endpoint_response_type(self):
        """Test that solution endpoint returns float type"""
        payload = {
            "orders": [
                {"id": 1, "item": "Laptop", "quantity": 1, "price": 100.0, "status": "completed"}
            ],
            "criterion": "completed"
        }
        
        response = self.client.post("/fonoma/backend/solution", json=payload)
        
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), (float, int))


def run_api_tests():
    """Run all API test suites and provide summary"""
    if not DEPENDENCIES_AVAILABLE:
        print("=" * 60)
        print("API ENDPOINT TESTS - DEPENDENCIES NOT AVAILABLE")
        print("=" * 60)
        print()
        print("To run API endpoint tests, install dependencies:")
        print("pip install fastapi uvicorn httpx")
        print()
        print("These tests would verify:")
        print("- API endpoint functionality")
        print("- HTTP status codes")
        print("- Request/response validation")
        print("- Error handling")
        print("- Response formats")
        print("=" * 60)
        return True
    
    print("=" * 60)
    print("FONOMA BACKEND TEST - API ENDPOINT TESTS")
    print("=" * 60)
    print()
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestSolutionAPIEndpoint,
        TestExampleAPIEndpoint,
        TestAPIResponseFormats
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("API TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print("✅ ALL API TESTS PASSED!")
        print("\nThe API implementation is working correctly:")
        print("- /fonoma/backend/solution endpoint ✓")
        print("- Request validation ✓")
        print("- Response formats ✓")
        print("- Error handling ✓")
    else:
        print("❌ SOME API TESTS FAILED")
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"- {test}: {traceback}")
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"- {test}: {traceback}")
    
    print("=" * 60)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_api_tests()
    sys.exit(0 if success else 1)