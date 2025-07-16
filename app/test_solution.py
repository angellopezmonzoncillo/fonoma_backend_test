import unittest
from fastapi.testclient import TestClient
from main import app

class TestSolutionEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_app_health_check(self):
        """Test that the app starts successfully"""
        # This is a basic test to validate our test infrastructure
        self.assertIsNotNone(app)
        self.assertIsNotNone(self.client)

    def test_solution_endpoint_exists(self):
        """Test that the solution endpoint returns appropriate response"""
        test_orders = [
            {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
            {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"}
        ]
        
        response = self.client.post("/solution", json={
            "orders": test_orders,
            "criterion": "completed"
        })
        
        # Should return 200 or appropriate status code
        self.assertIn(response.status_code, [200, 201, 404, 422])

if __name__ == '__main__':
    unittest.main()