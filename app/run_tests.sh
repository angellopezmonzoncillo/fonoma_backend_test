#!/bin/bash

# Test runner script for Fonoma Backend Test
# Makes it easy to run different test configurations

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Fonoma Backend Test - Test Runner${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# Change to app directory
cd "$(dirname "$0")"

# Function to run a specific test
run_test() {
    local test_file=$1
    local description=$2
    
    echo -e "${YELLOW}Running: ${description}${NC}"
    echo -e "File: ${test_file}"
    echo
    
    if python "$test_file"; then
        echo -e "${GREEN}✅ ${description} - PASSED${NC}"
        return 0
    else
        echo -e "${RED}❌ ${description} - FAILED${NC}"
        return 1
    fi
}

# Parse command line arguments
case "${1:-all}" in
    "business"|"logic")
        echo "Running business logic tests only..."
        run_test "test_business_logic.py" "Business Logic Tests"
        ;;
    
    "api"|"endpoints")
        echo "Running API endpoint tests only..."
        run_test "test_api_endpoints.py" "API Endpoint Tests"
        ;;
    
    "all"|"")
        echo "Running all available tests..."
        run_test "run_all_tests.py" "Complete Test Suite"
        ;;
    
    "help"|"-h"|"--help")
        echo "Usage: $0 [test_type]"
        echo
        echo "Available test types:"
        echo "  business, logic    - Run business logic tests only"
        echo "  api, endpoints     - Run API endpoint tests only"
        echo "  all (default)      - Run all available tests"
        echo "  help               - Show this help message"
        echo
        echo "Examples:"
        echo "  $0                 # Run all tests"
        echo "  $0 business        # Run business logic tests"
        echo "  $0 api             # Run API tests"
        exit 0
        ;;
    
    *)
        echo -e "${RED}Error: Unknown test type '${1}'${NC}"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac

echo
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Test execution completed${NC}"
echo -e "${BLUE}========================================${NC}"