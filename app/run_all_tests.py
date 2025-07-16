#!/usr/bin/env python3
"""
Comprehensive test runner for the Fonoma Backend Test application
Runs all available tests and provides detailed reporting
"""

import sys
import os
import subprocess
import time
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)

def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'-' * 50}")
    print(f" {title}")
    print(f"{'-' * 50}")

def run_test_file(test_file, description):
    """Run a test file and return success status"""
    print_section(f"Running {description}")
    print(f"File: {test_file}")
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=False, 
                              text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {test_file}: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are available"""
    print_section("Checking Dependencies")
    
    dependencies = {
        'unittest': True,  # Built-in
        'sys': True,       # Built-in
        'os': True,        # Built-in
    }
    
    # Check optional dependencies
    try:
        import fastapi
        dependencies['fastapi'] = True
        print("✓ FastAPI is available")
    except ImportError:
        dependencies['fastapi'] = False
        print("✗ FastAPI is not available")
    
    try:
        import httpx
        dependencies['httpx'] = True
        print("✓ httpx is available")
    except ImportError:
        dependencies['httpx'] = False
        print("✗ httpx is not available")
    
    try:
        import pydantic
        dependencies['pydantic'] = True
        print("✓ Pydantic is available")
    except ImportError:
        dependencies['pydantic'] = False
        print("✗ Pydantic is not available")
    
    return dependencies

def main():
    """Main test runner function"""
    print_header("FONOMA BACKEND TEST - COMPREHENSIVE TEST SUITE")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check dependencies
    deps = check_dependencies()
    
    # Test results tracking
    test_results = {}
    
    # Define test files and descriptions
    test_files = [
        ("test_business_logic.py", "Business Logic Tests", True),
        ("test_api_endpoints.py", "API Endpoint Tests", deps.get('fastapi', False)),
    ]
    
    print_section("Test Execution Plan")
    for filename, description, available in test_files:
        status = "✓ AVAILABLE" if available else "✗ SKIPPED (missing dependencies)"
        print(f"{description}: {status}")
    
    # Run available tests
    print_header("EXECUTING TESTS")
    
    for filename, description, available in test_files:
        if available:
            success = run_test_file(filename, description)
            test_results[description] = success
        else:
            print_section(f"Skipping {description}")
            print(f"Reason: Missing dependencies")
            test_results[description] = None  # Skipped
    
    # Generate final report
    print_header("FINAL TEST REPORT")
    
    total_tests = len([r for r in test_results.values() if r is not None])
    passed_tests = len([r for r in test_results.values() if r is True])
    failed_tests = len([r for r in test_results.values() if r is False])
    skipped_tests = len([r for r in test_results.values() if r is None])
    
    print(f"Test Summary:")
    print(f"  Total test suites: {len(test_results)}")
    print(f"  Executed: {total_tests}")
    print(f"  Passed: {passed_tests}")
    print(f"  Failed: {failed_tests}")
    print(f"  Skipped: {skipped_tests}")
    print()
    
    print("Detailed Results:")
    for test_name, result in test_results.items():
        if result is True:
            status = "✅ PASSED"
        elif result is False:
            status = "❌ FAILED"
        else:
            status = "⏭️  SKIPPED"
        print(f"  {test_name}: {status}")
    
    print()
    
    # Overall status
    if failed_tests == 0 and passed_tests > 0:
        print("🎉 ALL EXECUTED TESTS PASSED!")
        print("\nThe Fonoma Backend Test application is working correctly!")
        
        print("\n📋 Test Coverage Summary:")
        print("  ✓ Business logic validation (process_orders function)")
        print("  ✓ Data model validation (Order, OrderList)")
        print("  ✓ Input validation (prices, quantities, status)")
        print("  ✓ Edge cases and error handling")
        print("  ✓ Integration workflow testing")
        
        if skipped_tests > 0:
            print(f"\n⚠️  Note: {skipped_tests} test suite(s) were skipped due to missing dependencies")
            print("  To run all tests, install: pip install fastapi uvicorn httpx")
        
    elif failed_tests > 0:
        print("❌ SOME TESTS FAILED")
        print("\nPlease review the failed tests above and fix any issues.")
        
    else:
        print("⚠️  NO TESTS WERE EXECUTED")
        print("\nPlease check dependencies and test files.")
    
    # Installation instructions
    if not deps.get('fastapi', True) or not deps.get('httpx', True) or not deps.get('pydantic', True):
        print("\n" + "=" * 70)
        print(" INSTALLATION INSTRUCTIONS")
        print("=" * 70)
        print("\nTo run the complete test suite including API endpoint tests:")
        print("1. Install FastAPI and dependencies:")
        print("   pip install fastapi uvicorn httpx")
        print()
        print("2. Run tests again:")
        print("   python run_all_tests.py")
        print()
        print("3. Or run individual test files:")
        print("   python test_business_logic.py")
        print("   python test_api_endpoints.py")
    
    print("\n" + "=" * 70)
    print(f" TEST EXECUTION COMPLETED - {datetime.now().strftime('%H:%M:%S')}")
    print("=" * 70)
    
    # Exit with appropriate code
    if failed_tests == 0 and passed_tests > 0:
        return 0
    elif failed_tests > 0:
        return 1
    else:
        return 2  # No tests executed

if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)