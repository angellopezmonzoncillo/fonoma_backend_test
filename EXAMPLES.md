# Test Report Generator - Usage Examples

This document provides examples of using the custom agent for test report generation.

## Example 1: Basic Usage

Generate all reports with a single command:

```bash
python generate_test_reports.py
```

**Output:**
```
============================================================
FONOMA TEST REPORT GENERATOR
============================================================

Running tests...

test_app_health_check ... ok
test_solution_endpoint_exists ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.002s

OK

============================================================
GENERATING REPORTS
============================================================

✓ Text report generated: test-reports/test_report.txt
✓ JSON report generated: test-reports/test_report.json
✓ HTML report generated: test-reports/test_report.html
✓ Markdown report generated: test-reports/test_report.md

============================================================
REPORT GENERATION COMPLETE
============================================================

Reports saved to: test-reports
```

## Example 2: Viewing Reports

### Text Report
```bash
cat test-reports/test_report.txt
```

Output:
```
============================================================
TEST EXECUTION REPORT
Fonoma Backend Test Suite
============================================================

Generated at: 2025-11-12 13:34:29

SUMMARY
------------------------------------------------------------
Total Tests Run:  2
Passed:           2
Failures:         0
Errors:           0
Skipped:          0
Success Rate:     100.0%
------------------------------------------------------------

🎉 ALL TESTS PASSED! 🎉
```

### JSON Report
```bash
cat test-reports/test_report.json
```

Output:
```json
{
  "timestamp": "2025-11-12T13:34:29.806501",
  "test_suite": "Fonoma Backend Test Suite",
  "summary": {
    "total_tests": 2,
    "passed": 2,
    "failures": 0,
    "errors": 0,
    "skipped": 0,
    "success_rate": 100.0
  },
  "failures": [],
  "errors": []
}
```

## Example 3: Using with CI/CD

### GitHub Actions
```yaml
name: Run Tests and Generate Reports

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: pip install -r requirements.txt
    
    - name: Generate test reports
      run: python generate_test_reports.py
    
    - name: Upload test reports
      uses: actions/upload-artifact@v3
      with:
        name: test-reports
        path: test-reports/
    
    - name: Comment PR with results
      if: github.event_name == 'pull_request'
      run: |
        cat test-reports/test_report.md >> $GITHUB_STEP_SUMMARY
```

## Example 4: Custom Agent Instructions

The custom agent instructions provide guidelines for generating test reports. Here's how to use them with GitHub Copilot:

1. Open the custom agent instructions file:
   - `.github/copilot-instructions-test-reports.md`

2. The instructions include:
   - Report generation strategies
   - Multiple format options (Text, JSON, HTML, Markdown)
   - Best practices for test reporting
   - CI/CD integration examples

3. When GitHub Copilot is asked to generate test reports, it will:
   - Follow the guidelines in the custom agent instructions
   - Generate comprehensive reports
   - Include all necessary metrics and details

## Example 5: Programmatic Usage

You can also use the test report generator programmatically:

```python
from generate_test_reports import TestReportGenerator

# Create generator instance
generator = TestReportGenerator(
    test_directory='app',
    output_directory='test-reports'
)

# Run tests
result = generator.run_tests()

# Generate specific format
generator.generate_html_report()  # Only HTML

# Or generate all formats
success = generator.generate_all_reports()
```

## Example 6: Integration with Pre-commit Hook

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
echo "Running tests and generating reports..."
python generate_test_reports.py

if [ $? -eq 0 ]; then
    echo "✓ All tests passed"
    exit 0
else
    echo "✗ Tests failed"
    echo "Check test-reports/test_report.txt for details"
    exit 1
fi
```

## Benefits

1. **Multiple Formats**: Choose the format that best suits your needs
2. **Comprehensive**: Includes all test statistics and details
3. **Easy to Use**: Single command generates all reports
4. **CI/CD Ready**: Perfect for automated workflows
5. **Visual**: HTML reports provide interactive visualizations
6. **Shareable**: Easy to share with team members

## Troubleshooting

### Tests not found
Ensure tests are in the `app/` directory and follow the `test_*.py` naming convention.

### Permission denied
Make the script executable:
```bash
chmod +x generate_test_reports.py
```

### Reports not generated
Check that the `test-reports/` directory has write permissions.

## Further Reading

- Custom Agent Instructions: `.github/copilot-instructions-test-reports.md`
- Unit Test Guidelines: `.github/copilot-instructions-unit-tests.md`
- Project README: `README.md`
