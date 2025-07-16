import unittest
import sys
import os
from typing import List, Dict

# Add the current directory to the Python path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import our business logic functions directly
from routers.solution.controller import process_orders
from models.solutions import Order, OrderList


class TestProcessOrdersFunction(unittest.TestCase):
    """Test cases for the process_orders business logic function"""
    
    def setUp(self):
        """Set up test data for each test case"""
        self.test_orders = [
            {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
            {"id": 2, "item": "Smartphone", "quantity": 2, "price": 499.95, "status": "pending"},
            {"id": 3, "item": "Headphones", "quantity": 3, "price": 99.90, "status": "completed"},
            {"id": 4, "item": "Mouse", "quantity": 4, "price": 24.99, "status": "canceled"},
            {"id": 5, "item": "Tablet", "quantity": 1, "price": 299.50, "status": "pending"},
        ]
    
    def test_process_orders_completed_status(self):
        """Test filtering orders by completed status"""
        order_list = OrderList(orders=self.test_orders, criterion="completed")
        result = process_orders(order_list)
        
        # Expected: Laptop (999.99 * 1) + Headphones (99.90 * 3) = 999.99 + 299.70 = 1299.69
        expected = 1299.69
        self.assertEqual(result, expected)
    
    def test_process_orders_pending_status(self):
        """Test filtering orders by pending status"""
        order_list = OrderList(orders=self.test_orders, criterion="pending")
        result = process_orders(order_list)
        
        # Expected: Smartphone (499.95 * 2) + Tablet (299.50 * 1) = 999.90 + 299.50 = 1299.40
        expected = 1299.40
        self.assertEqual(result, expected)
    
    def test_process_orders_canceled_status(self):
        """Test filtering orders by canceled status"""
        order_list = OrderList(orders=self.test_orders, criterion="canceled")
        result = process_orders(order_list)
        
        # Expected: Mouse (24.99 * 4) = 99.96
        expected = 99.96
        self.assertEqual(result, expected)
    
    def test_process_orders_all_status(self):
        """Test processing all orders regardless of status"""
        order_list = OrderList(orders=self.test_orders, criterion="all")
        result = process_orders(order_list)
        
        # Expected: All orders total = 1299.69 + 1299.40 + 99.96 = 2699.05
        expected = 2699.05
        self.assertEqual(result, expected)
    
    def test_process_orders_empty_list(self):
        """Test processing an empty order list"""
        order_list = OrderList(orders=[], criterion="all")
        result = process_orders(order_list)
        
        expected = 0.0
        self.assertEqual(result, expected)
    
    def test_process_orders_no_matching_status(self):
        """Test when no orders match the criterion"""
        # Create orders with only 'completed' status
        orders = [
            {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"}
        ]
        order_list = OrderList(orders=orders, criterion="pending")
        result = process_orders(order_list)
        
        expected = 0.0
        self.assertEqual(result, expected)
    
    def test_process_orders_decimal_precision(self):
        """Test that results are properly rounded to 2 decimal places"""
        orders = [
            {"id": 1, "item": "Item1", "quantity": 3, "price": 33.333, "status": "completed"}
        ]
        order_list = OrderList(orders=orders, criterion="completed")
        result = process_orders(order_list)
        
        # Expected: 33.333 * 3 = 99.999, rounded to 100.00
        expected = 100.0
        self.assertEqual(result, expected)


class TestOrderValidation(unittest.TestCase):
    """Test cases for Order model validation"""
    
    def test_valid_order_creation(self):
        """Test creating a valid order"""
        order_data = {
            "id": 1,
            "item": "Laptop",
            "quantity": 1,
            "price": 999.99,
            "status": "completed"
        }
        order = Order(**order_data)
        
        self.assertEqual(order.id, 1)
        self.assertEqual(order.item, "Laptop")
        self.assertEqual(order.quantity, 1)
        self.assertEqual(order.price, 999.99)
        self.assertEqual(order.status, "completed")
    
    def test_negative_price_validation(self):
        """Test that negative prices are rejected"""
        order_data = {
            "id": 1,
            "item": "Laptop",
            "quantity": 1,
            "price": -100.0,
            "status": "completed"
        }
        
        with self.assertRaises(ValueError) as context:
            Order(**order_data)
        
        self.assertIn("no puede ser negativo", str(context.exception))
    
    def test_zero_quantity_validation(self):
        """Test that zero quantity is rejected"""
        order_data = {
            "id": 1,
            "item": "Laptop",
            "quantity": 0,
            "price": 999.99,
            "status": "completed"
        }
        
        with self.assertRaises(ValueError) as context:
            Order(**order_data)
        
        self.assertIn("debe ser mayor a 0", str(context.exception))
    
    def test_negative_quantity_validation(self):
        """Test that negative quantity is rejected"""
        order_data = {
            "id": 1,
            "item": "Laptop",
            "quantity": -1,
            "price": 999.99,
            "status": "completed"
        }
        
        with self.assertRaises(ValueError) as context:
            Order(**order_data)
        
        self.assertIn("debe ser mayor a 0", str(context.exception))
    
    def test_invalid_status_validation(self):
        """Test that invalid status values are rejected"""
        order_data = {
            "id": 1,
            "item": "Laptop",
            "quantity": 1,
            "price": 999.99,
            "status": "invalid_status"
        }
        
        with self.assertRaises(ValueError):
            Order(**order_data)


class TestOrderListValidation(unittest.TestCase):
    """Test cases for OrderList model validation"""
    
    def test_valid_order_list_creation(self):
        """Test creating a valid order list"""
        orders = [
            {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"},
            {"id": 2, "item": "Mouse", "quantity": 2, "price": 24.99, "status": "pending"}
        ]
        order_list = OrderList(orders=orders, criterion="all")
        
        self.assertEqual(len(order_list.orders), 2)
        self.assertEqual(order_list.criterion, "all")
    
    def test_invalid_criterion_validation(self):
        """Test that invalid criterion values are rejected"""
        orders = [
            {"id": 1, "item": "Laptop", "quantity": 1, "price": 999.99, "status": "completed"}
        ]
        
        with self.assertRaises(ValueError):
            OrderList(orders=orders, criterion="invalid_criterion")
    
    def test_empty_orders_list(self):
        """Test that empty orders list is valid"""
        order_list = OrderList(orders=[], criterion="all")
        
        self.assertEqual(len(order_list.orders), 0)
        self.assertEqual(order_list.criterion, "all")


if __name__ == '__main__':
    # Create a test suite with all test cases
    test_suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestProcessOrdersFunction,
        TestOrderValidation,
        TestOrderListValidation
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run the tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)