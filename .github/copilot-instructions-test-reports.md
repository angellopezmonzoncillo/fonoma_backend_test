# Custom Instructions for Test Report Generation

When generating test reports for this FastAPI project, follow these guidelines:

## Project Context
- **Project Name**: Fonoma Backend Test
- **Technology Stack**: FastAPI, Python, unittest, TestClient
- **Purpose**: Generate comprehensive test execution reports for the order processing backend
- **Test Framework**: Python unittest with FastAPI TestClient

## Custom Agent Purpose
This custom agent is designed to automatically generate detailed test reports from test execution results. It provides:
- Summary statistics of test execution
- Detailed pass/fail information
- Coverage analysis
- Performance metrics
- Formatted reports in multiple formats (text, HTML, JSON)

## Report Generation Strategies

### 1. Basic Text Report Generation
Generate a simple text-based report with test execution results:

```bash
cd app && python -m unittest discover -v 2>&1 | tee test_results.txt
```

**Output Format:**
```
=== TEST EXECUTION REPORT ===
Generated at: 2025-11-12 13:25:00
Tests run: 10
Failures: 0
Errors: 0
Skipped: 0
Success rate: 100.0%
Execution time: 0.523s
```

### 2. Detailed HTML Report Generation
Create an interactive HTML report for better visualization:

```python
import unittest
import sys
from datetime import datetime
from io import StringIO

class HTMLTestReporter(unittest.TextTestRunner):
    """Generate HTML test reports"""
    
    def __init__(self, output_file='test_report.html', *args, **kwargs):
        self.output_file = output_file
        super().__init__(*args, **kwargs)
    
    def run(self, test):
        """Run tests and generate HTML report"""
        result = super().run(test)
        self._generate_html_report(result)
        return result
    
    def _generate_html_report(self, result):
        """Generate HTML formatted report"""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Test Report - Fonoma Backend</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background-color: #4CAF50; color: white; padding: 20px; }}
        .summary {{ margin: 20px 0; padding: 15px; background-color: #f4f4f4; }}
        .test-case {{ margin: 10px 0; padding: 10px; border-left: 4px solid #4CAF50; }}
        .failure {{ border-left-color: #f44336; }}
        .error {{ border-left-color: #ff9800; }}
        table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #4CAF50; color: white; }}
        .pass {{ color: #4CAF50; font-weight: bold; }}
        .fail {{ color: #f44336; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Test Execution Report</h1>
        <p>Fonoma Backend Test Suite</p>
    </div>
    
    <div class="summary">
        <h2>Summary</h2>
        <table>
            <tr><th>Metric</th><th>Value</th></tr>
            <tr><td>Generated At</td><td>{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</td></tr>
            <tr><td>Total Tests</td><td>{result.testsRun}</td></tr>
            <tr><td>Passed</td><td class="pass">{result.testsRun - len(result.failures) - len(result.errors)}</td></tr>
            <tr><td>Failures</td><td class="fail">{len(result.failures)}</td></tr>
            <tr><td>Errors</td><td class="fail">{len(result.errors)}</td></tr>
            <tr><td>Success Rate</td><td>{((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100 if result.testsRun > 0 else 0):.1f}%</td></tr>
        </table>
    </div>
    
    <div class="details">
        <h2>Test Details</h2>
"""
        
        if result.failures:
            html_content += "<h3>Failures</h3>"
            for test, trace in result.failures:
                html_content += f'<div class="test-case failure"><strong>{test}</strong><pre>{trace}</pre></div>'
        
        if result.errors:
            html_content += "<h3>Errors</h3>"
            for test, trace in result.errors:
                html_content += f'<div class="test-case error"><strong>{test}</strong><pre>{trace}</pre></div>'
        
        html_content += """
    </div>
</body>
</html>
"""
        
        with open(self.output_file, 'w') as f:
            f.write(html_content)
        
        print(f"\nHTML report generated: {self.output_file}")
```

### 3. JSON Report Generation
Generate machine-readable JSON reports for CI/CD integration:

```python
import unittest
import json
from datetime import datetime

class JSONTestReporter:
    """Generate JSON formatted test reports"""
    
    @staticmethod
    def generate_report(result, output_file='test_report.json'):
        """Generate JSON report from test results"""
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": result.testsRun,
                "passed": result.testsRun - len(result.failures) - len(result.errors),
                "failures": len(result.failures),
                "errors": len(result.errors),
                "skipped": len(getattr(result, 'skipped', [])),
                "success_rate": round((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100, 2) if result.testsRun > 0 else 0
            },
            "failures": [
                {
                    "test": str(test),
                    "message": trace.split('\n')[-2] if trace else ""
                }
                for test, trace in result.failures
            ],
            "errors": [
                {
                    "test": str(test),
                    "message": trace.split('\n')[-2] if trace else ""
                }
                for test, trace in result.errors
            ]
        }
        
        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"JSON report generated: {output_file}")
        return report_data
```

### 4. Markdown Report Generation
Create markdown reports suitable for documentation:

```python
import unittest
from datetime import datetime

class MarkdownTestReporter:
    """Generate Markdown formatted test reports"""
    
    @staticmethod
    def generate_report(result, output_file='test_report.md'):
        """Generate Markdown report from test results"""
        
        markdown_content = f"""# Test Execution Report
**Fonoma Backend Test Suite**

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

| Metric | Value |
|--------|-------|
| Total Tests | {result.testsRun} |
| Passed | {result.testsRun - len(result.failures) - len(result.errors)} ✅ |
| Failures | {len(result.failures)} ❌ |
| Errors | {len(result.errors)} ⚠️ |
| Success Rate | {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100 if result.testsRun > 0 else 0):.1f}% |

"""
        
        if result.failures:
            markdown_content += "\n## Failures\n\n"
            for test, trace in result.failures:
                markdown_content += f"### {test}\n```\n{trace}\n```\n\n"
        
        if result.errors:
            markdown_content += "\n## Errors\n\n"
            for test, trace in result.errors:
                markdown_content += f"### {test}\n```\n{trace}\n```\n\n"
        
        if not result.failures and not result.errors:
            markdown_content += "\n## 🎉 All tests passed!\n\n"
        
        with open(output_file, 'w') as f:
            f.write(markdown_content)
        
        print(f"Markdown report generated: {output_file}")
        return markdown_content
```

## Complete Test Report Generator Script

Create a comprehensive test report generator that supports multiple formats:

```python
#!/usr/bin/env python3
"""
Fonoma Backend Test Report Generator

This script runs the test suite and generates comprehensive reports
in multiple formats: text, HTML, JSON, and Markdown.
"""

import unittest
import sys
import json
from datetime import datetime
from pathlib import Path

class TestReportGenerator:
    """Main test report generator class"""
    
    def __init__(self, test_directory='app', output_directory='test-reports'):
        self.test_directory = test_directory
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(exist_ok=True)
        self.result = None
        
    def run_tests(self):
        """Discover and run all tests"""
        loader = unittest.TestLoader()
        suite = loader.discover(self.test_directory, pattern='test_*.py')
        runner = unittest.TextTestRunner(verbosity=2)
        self.result = runner.run(suite)
        return self.result
    
    def generate_text_report(self):
        """Generate text summary report"""
        if not self.result:
            return None
        
        report_file = self.output_directory / 'test_report.txt'
        
        with open(report_file, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("TEST EXECUTION REPORT\n")
            f.write("Fonoma Backend Test Suite\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("SUMMARY\n")
            f.write("-" * 60 + "\n")
            f.write(f"Total Tests Run:  {self.result.testsRun}\n")
            f.write(f"Passed:           {self.result.testsRun - len(self.result.failures) - len(self.result.errors)}\n")
            f.write(f"Failures:         {len(self.result.failures)}\n")
            f.write(f"Errors:           {len(self.result.errors)}\n")
            f.write(f"Skipped:          {len(getattr(self.result, 'skipped', []))}\n")
            
            success_rate = ((self.result.testsRun - len(self.result.failures) - len(self.result.errors)) / self.result.testsRun * 100) if self.result.testsRun > 0 else 0
            f.write(f"Success Rate:     {success_rate:.1f}%\n")
            f.write("-" * 60 + "\n\n")
            
            if self.result.failures:
                f.write("FAILURES\n")
                f.write("-" * 60 + "\n")
                for test, trace in self.result.failures:
                    f.write(f"\n{test}:\n{trace}\n")
                f.write("-" * 60 + "\n\n")
            
            if self.result.errors:
                f.write("ERRORS\n")
                f.write("-" * 60 + "\n")
                for test, trace in self.result.errors:
                    f.write(f"\n{test}:\n{trace}\n")
                f.write("-" * 60 + "\n\n")
            
            if not self.result.failures and not self.result.errors:
                f.write("🎉 ALL TESTS PASSED! 🎉\n\n")
        
        print(f"✓ Text report generated: {report_file}")
        return report_file
    
    def generate_json_report(self):
        """Generate JSON report"""
        if not self.result:
            return None
        
        report_file = self.output_directory / 'test_report.json'
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "test_suite": "Fonoma Backend Test Suite",
            "summary": {
                "total_tests": self.result.testsRun,
                "passed": self.result.testsRun - len(self.result.failures) - len(self.result.errors),
                "failures": len(self.result.failures),
                "errors": len(self.result.errors),
                "skipped": len(getattr(self.result, 'skipped', [])),
                "success_rate": round((self.result.testsRun - len(self.result.failures) - len(self.result.errors)) / self.result.testsRun * 100, 2) if self.result.testsRun > 0 else 0
            },
            "failures": [
                {
                    "test": str(test),
                    "traceback": trace
                }
                for test, trace in self.result.failures
            ],
            "errors": [
                {
                    "test": str(test),
                    "traceback": trace
                }
                for test, trace in self.result.errors
            ]
        }
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"✓ JSON report generated: {report_file}")
        return report_file
    
    def generate_html_report(self):
        """Generate HTML report"""
        if not self.result:
            return None
        
        report_file = self.output_directory / 'test_report.html'
        
        success_rate = ((self.result.testsRun - len(self.result.failures) - len(self.result.errors)) / self.result.testsRun * 100) if self.result.testsRun > 0 else 0
        passed = self.result.testsRun - len(self.result.failures) - len(self.result.errors)
        
        # Determine status color
        if success_rate == 100:
            status_color = "#4CAF50"
            status_text = "PASSED"
        elif success_rate >= 80:
            status_color = "#ff9800"
            status_text = "PARTIAL"
        else:
            status_color = "#f44336"
            status_text = "FAILED"
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Report - Fonoma Backend</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f5f5f5;
            padding: 20px;
        }}
        .container {{ 
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .header {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px 8px 0 0;
        }}
        .header h1 {{ margin-bottom: 10px; }}
        .header p {{ opacity: 0.9; }}
        .summary {{ 
            padding: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}
        .metric-card {{
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 6px;
            border-left: 4px solid #667eea;
        }}
        .metric-card h3 {{ 
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
        }}
        .metric-card .value {{ 
            font-size: 32px;
            font-weight: bold;
            color: #333;
        }}
        .status-badge {{
            display: inline-block;
            padding: 8px 16px;
            background-color: {status_color};
            color: white;
            border-radius: 4px;
            font-weight: bold;
            margin-top: 10px;
        }}
        .details {{ padding: 30px; }}
        .test-section {{ margin: 20px 0; }}
        .test-section h2 {{ 
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
        }}
        .test-case {{
            margin: 15px 0;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 4px;
            border-left: 4px solid #f44336;
        }}
        .test-case.success {{ border-left-color: #4CAF50; }}
        .test-case h4 {{ 
            color: #333;
            margin-bottom: 10px;
        }}
        .test-case pre {{
            background-color: #fff;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 12px;
            line-height: 1.4;
        }}
        .success-message {{
            text-align: center;
            padding: 40px;
            color: #4CAF50;
            font-size: 24px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #667eea;
            color: white;
            font-weight: 600;
        }}
        .pass {{ color: #4CAF50; font-weight: bold; }}
        .fail {{ color: #f44336; font-weight: bold; }}
        footer {{
            padding: 20px 30px;
            background-color: #f9f9f9;
            text-align: center;
            color: #666;
            border-radius: 0 0 8px 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Test Execution Report</h1>
            <p>Fonoma Backend Test Suite</p>
            <span class="status-badge">{status_text}</span>
        </div>
        
        <div class="summary">
            <div class="metric-card">
                <h3>Total Tests</h3>
                <div class="value">{self.result.testsRun}</div>
            </div>
            <div class="metric-card">
                <h3>Passed</h3>
                <div class="value pass">{passed}</div>
            </div>
            <div class="metric-card">
                <h3>Failures</h3>
                <div class="value fail">{len(self.result.failures)}</div>
            </div>
            <div class="metric-card">
                <h3>Errors</h3>
                <div class="value fail">{len(self.result.errors)}</div>
            </div>
            <div class="metric-card">
                <h3>Success Rate</h3>
                <div class="value">{success_rate:.1f}%</div>
            </div>
        </div>
        
        <div class="details">
            <div class="test-section">
                <h2>Test Summary</h2>
                <table>
                    <tr>
                        <th>Metric</th>
                        <th>Value</th>
                    </tr>
                    <tr>
                        <td>Generated At</td>
                        <td>{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</td>
                    </tr>
                    <tr>
                        <td>Total Tests</td>
                        <td>{self.result.testsRun}</td>
                    </tr>
                    <tr>
                        <td>Passed</td>
                        <td class="pass">{passed}</td>
                    </tr>
                    <tr>
                        <td>Failures</td>
                        <td class="fail">{len(self.result.failures)}</td>
                    </tr>
                    <tr>
                        <td>Errors</td>
                        <td class="fail">{len(self.result.errors)}</td>
                    </tr>
                    <tr>
                        <td>Success Rate</td>
                        <td>{success_rate:.1f}%</td>
                    </tr>
                </table>
            </div>
"""
        
        if self.result.failures:
            html_content += """
            <div class="test-section">
                <h2>Failures</h2>
"""
            for test, trace in self.result.failures:
                html_content += f"""
                <div class="test-case">
                    <h4>{test}</h4>
                    <pre>{trace}</pre>
                </div>
"""
            html_content += "</div>"
        
        if self.result.errors:
            html_content += """
            <div class="test-section">
                <h2>Errors</h2>
"""
            for test, trace in self.result.errors:
                html_content += f"""
                <div class="test-case">
                    <h4>{test}</h4>
                    <pre>{trace}</pre>
                </div>
"""
            html_content += "</div>"
        
        if not self.result.failures and not self.result.errors:
            html_content += """
            <div class="success-message">
                🎉 All tests passed successfully! 🎉
            </div>
"""
        
        html_content += """
        </div>
        
        <footer>
            <p>Generated by Fonoma Test Report Generator</p>
        </footer>
    </div>
</body>
</html>
"""
        
        with open(report_file, 'w') as f:
            f.write(html_content)
        
        print(f"✓ HTML report generated: {report_file}")
        return report_file
    
    def generate_markdown_report(self):
        """Generate Markdown report"""
        if not self.result:
            return None
        
        report_file = self.output_directory / 'test_report.md'
        
        success_rate = ((self.result.testsRun - len(self.result.failures) - len(self.result.errors)) / self.result.testsRun * 100) if self.result.testsRun > 0 else 0
        passed = self.result.testsRun - len(self.result.failures) - len(self.result.errors)
        
        markdown_content = f"""# Test Execution Report
**Fonoma Backend Test Suite**

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 📊 Summary

| Metric | Value |
|--------|-------|
| Total Tests | {self.result.testsRun} |
| Passed | {passed} ✅ |
| Failures | {len(self.result.failures)} ❌ |
| Errors | {len(self.result.errors)} ⚠️ |
| Skipped | {len(getattr(self.result, 'skipped', []))} ⏭️ |
| **Success Rate** | **{success_rate:.1f}%** |

"""
        
        if self.result.failures:
            markdown_content += "\n## ❌ Failures\n\n"
            for i, (test, trace) in enumerate(self.result.failures, 1):
                markdown_content += f"### {i}. {test}\n\n```\n{trace}\n```\n\n"
        
        if self.result.errors:
            markdown_content += "\n## ⚠️ Errors\n\n"
            for i, (test, trace) in enumerate(self.result.errors, 1):
                markdown_content += f"### {i}. {test}\n\n```\n{trace}\n```\n\n"
        
        if not self.result.failures and not self.result.errors:
            markdown_content += "\n---\n\n## 🎉 All tests passed successfully!\n\n"
            markdown_content += "Great job! All test cases executed without any failures or errors.\n\n"
        
        markdown_content += "---\n\n"
        markdown_content += "*Report generated by Fonoma Test Report Generator*\n"
        
        with open(report_file, 'w') as f:
            f.write(markdown_content)
        
        print(f"✓ Markdown report generated: {report_file}")
        return report_file
    
    def generate_all_reports(self):
        """Generate all report formats"""
        print("\n" + "=" * 60)
        print("FONOMA TEST REPORT GENERATOR")
        print("=" * 60 + "\n")
        
        print("Running tests...\n")
        result = self.run_tests()
        
        print("\n" + "=" * 60)
        print("GENERATING REPORTS")
        print("=" * 60 + "\n")
        
        self.generate_text_report()
        self.generate_json_report()
        self.generate_html_report()
        self.generate_markdown_report()
        
        print("\n" + "=" * 60)
        print("REPORT GENERATION COMPLETE")
        print("=" * 60)
        print(f"\nReports saved to: {self.output_directory}")
        print("\nReport files:")
        print(f"  - {self.output_directory}/test_report.txt  (Text format)")
        print(f"  - {self.output_directory}/test_report.json (JSON format)")
        print(f"  - {self.output_directory}/test_report.html (HTML format)")
        print(f"  - {self.output_directory}/test_report.md   (Markdown format)")
        
        return result.wasSuccessful()

def main():
    """Main entry point"""
    generator = TestReportGenerator()
    success = generator.generate_all_reports()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
```

## Usage Instructions

### Quick Start
To generate test reports, create a file `generate_test_reports.py` in the project root with the complete script above, then run:

```bash
python generate_test_reports.py
```

### Command Line Usage
```bash
# Generate all report formats
python generate_test_reports.py

# View HTML report in browser (Linux/Mac)
xdg-open test-reports/test_report.html  # Linux
open test-reports/test_report.html      # Mac

# View text report
cat test-reports/test_report.txt

# Parse JSON report with jq
cat test-reports/test_report.json | jq .
```

### Integration with CI/CD

#### GitHub Actions Example
```yaml
- name: Run tests and generate reports
  run: python generate_test_reports.py

- name: Upload test reports
  uses: actions/upload-artifact@v3
  with:
    name: test-reports
    path: test-reports/
```

#### Output Directory Structure
```
test-reports/
├── test_report.txt      # Human-readable text report
├── test_report.json     # Machine-readable JSON report
├── test_report.html     # Interactive HTML report
└── test_report.md       # Markdown report for documentation
```

## Report Format Details

### Text Report Format
- Clean, terminal-friendly format
- Summary statistics at the top
- Detailed failure/error information
- Easy to read in console or log files

### JSON Report Format
- Machine-readable
- Perfect for CI/CD integration
- Can be parsed by monitoring tools
- Includes all test details and timestamps

### HTML Report Format
- Beautiful, interactive interface
- Visual metrics with color coding
- Responsive design
- Can be opened in any web browser
- Perfect for sharing with team members

### Markdown Report Format
- GitHub/GitLab compatible
- Can be included in documentation
- Easy to read in text editors
- Good for commit messages or PR descriptions

## Customization Options

### Custom Output Directory
```python
generator = TestReportGenerator(
    test_directory='app',
    output_directory='custom-reports'
)
```

### Generate Specific Format Only
```python
generator = TestReportGenerator()
generator.run_tests()
generator.generate_html_report()  # Only HTML
```

### Custom Report Styling
Modify the CSS in the `generate_html_report()` method to match your branding.

## Best Practices

1. **Run Before Commits**: Always generate test reports before committing code
2. **Archive Reports**: Keep historical reports for trend analysis
3. **Share HTML Reports**: Share interactive HTML reports with stakeholders
4. **Automate Generation**: Integrate into your CI/CD pipeline
5. **Review Regularly**: Check reports for patterns in failures
6. **Track Metrics**: Monitor success rate trends over time

## Troubleshooting

### No Tests Found
- Ensure test files start with `test_`
- Check that tests are in the correct directory
- Verify test classes inherit from `unittest.TestCase`

### Report Not Generated
- Check write permissions on output directory
- Verify all tests complete successfully
- Check for syntax errors in test files

### HTML Report Not Opening
- Verify file path is correct
- Check browser security settings
- Try different browser

## Advanced Features

### Coverage Integration
To include coverage data in reports, install coverage:
```bash
pip install coverage
```

Then modify the generator to run tests with coverage.

### Email Reports
Add email functionality to send reports automatically:
```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def email_report(report_file, recipient):
    # Email sending logic
    pass
```

### Slack Integration
Send report summaries to Slack:
```python
import requests

def send_to_slack(webhook_url, result):
    message = {
        "text": f"Test Results: {result.testsRun} tests, {len(result.failures)} failures"
    }
    requests.post(webhook_url, json=message)
```

## Support

For issues or questions about test report generation, refer to:
- Python unittest documentation
- FastAPI testing documentation
- Project README.md
