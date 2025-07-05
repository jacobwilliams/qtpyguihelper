#!/usr/bin/env python3
"""
Test runner for qtpyguihelper library.
Run specific tests or all tests in the test suite.

Usage:
    python run_tests.py                    # Run all tests
    python run_tests.py comprehensive      # Run comprehensive test suite
    python run_tests.py backend           # Run backend tests
    python run_tests.py qt                # Run Qt-specific tests
    python run_tests.py wx                # Run wxPython-specific tests
    python run_tests.py tabs              # Run tab-related tests
    python run_tests.py config            # Run configuration tests
"""

import sys
import os
import subprocess
from pathlib import Path

# Add the library to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
tests_dir = project_root / "tests"

def run_test(test_file):
    """Run a single test file."""
    test_path = tests_dir / test_file
    if test_path.exists():
        print(f"\n{'='*50}")
        print(f"Running: {test_file}")
        print(f"{'='*50}")
        try:
            result = subprocess.run([sys.executable, str(test_path)],
                                  capture_output=False, cwd=str(project_root))
            return result.returncode == 0
        except Exception as e:
            print(f"Error running {test_file}: {e}")
            return False
    else:
        print(f"Test file not found: {test_file}")
        return False

def run_tests_by_pattern(pattern):
    """Run tests matching a pattern."""
    test_files = sorted([f.name for f in tests_dir.glob(f"test_*{pattern}*.py")])
    if not test_files:
        print(f"No test files found matching pattern: *{pattern}*")
        return

    passed = 0
    failed = 0

    for test_file in test_files:
        if run_test(test_file):
            passed += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print(f"Test Results for pattern '{pattern}':")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Total:  {passed + failed}")
    print(f"{'='*60}")

def run_all_tests():
    """Run all test files."""
    test_files = sorted([f.name for f in tests_dir.glob("test_*.py")])

    passed = 0
    failed = 0

    for test_file in test_files:
        if run_test(test_file):
            passed += 1
        else:
            failed += 1

    print(f"\n{'='*60}")
    print(f"All Tests Results:")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Total:  {passed + failed}")
    print(f"{'='*60}")

def list_tests():
    """List all available tests."""
    test_files = sorted([f.name for f in tests_dir.glob("test_*.py")])
    print("Available tests:")
    for test_file in test_files:
        print(f"  {test_file}")

def main():
    """Main test runner."""
    if len(sys.argv) < 2:
        print("Running all tests...")
        run_all_tests()
        return

    command = sys.argv[1].lower()

    if command == "list":
        list_tests()
    elif command == "comprehensive":
        run_test("test_comprehensive.py")
    elif command == "backend":
        run_tests_by_pattern("backend")
    elif command == "qt":
        run_tests_by_pattern("qt")
    elif command == "wx":
        run_tests_by_pattern("wx")
    elif command == "tabs":
        run_tests_by_pattern("tab")
    elif command == "config":
        run_test("test_config.py")
    elif command == "all":
        run_all_tests()
    else:
        # Try to run a specific test file
        test_file = f"test_{command}.py"
        if not run_test(test_file):
            # Try the command as a direct filename
            if not run_test(command):
                print(f"Unknown command or test: {command}")
                print("\nAvailable commands:")
                print("  list, comprehensive, backend, qt, wx, tabs, config, all")
                print("  Or specify a test name like: python run_tests.py float_fields")

if __name__ == "__main__":
    main()
