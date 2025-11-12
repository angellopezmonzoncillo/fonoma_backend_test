#!/usr/bin/env python3
"""
Fonoma Backend Test Report Generator

This script runs the test suite and generates comprehensive reports
in multiple formats: text, HTML, JSON, and Markdown.

Usage:
    python generate_test_reports.py

The script will:
1. Discover and run all tests in the app directory
2. Generate reports in multiple formats
3. Save reports to the test-reports directory
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
