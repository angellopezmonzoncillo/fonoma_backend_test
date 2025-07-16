import json
import unittest
from fastapi.testclient import TestClient
from main import app

dataset = {
    "orders": [
        {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
        {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
        {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90, "status": "completed"},
        {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"},
    ]
}

dataset_result = (
    ('completed', 1299.69), 
    ('pending', 999.9), 
    ('canceled', 99.96), 
    ('all', 2399.55)
    )

class TestOrders(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
    def test_process_orders_result (self):
        for ctr in dataset_result:
            dataset["criterion"] = ctr[0]
            response = self.client.post("/fonoma/backend/solution", json=dataset)
            self.assertEqual(float(response.text), ctr[1])
            print(f"criterion: {ctr[0]} -> response: {response.text} - valor esperado: {ctr[1]}")

    def test_process_orders_response_200 (self): 
        dataset["criterion"] = "completed"       
        response = self.client.post("/fonoma/backend/solution", json=dataset)
        self.assertEqual(response.status_code, 200)
        # Agrega aquí las comprobaciones necesarias en la respuesta

if __name__ == '__main__':
    unittest.main()