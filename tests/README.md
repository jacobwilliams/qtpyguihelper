# QtPyGuiHelper Test Suite

This directory contains all tests for the qtpyguihelper library.

## Running Tests

### Quick Start
```bash
# Run all tests
python run_tests.py

# Run specific test categories
python run_tests.py backend     # Backend switching tests
python run_tests.py qt          # Qt-specific tests
python run_tests.py wx          # wxPython-specific tests
python run_tests.py tabs        # Tab functionality tests
python run_tests.py config      # Configuration loading tests

# Run comprehensive test suite
python run_tests.py comprehensive
```

### Individual Tests
```bash
# Run a specific test file
python run_tests.py float_fields
python run_tests.py custom_buttons
```

### Using pytest (if available)
```bash
# Run all tests with pytest
pytest tests/ -v

# Run specific test files
pytest tests/test_comprehensive.py -v
pytest tests/test_backend_*.py -v
```

## Test Categories

### Core Functionality
- `test_comprehensive.py` - Complete test suite covering all major features
- `test_config.py` - Configuration loading and validation
- `test_backend_integration.py` - Backend switching and integration

### Backend-Specific Tests
- `test_qt_backend.py` - Qt backend functionality
- `test_wx_backend.py` - wxPython backend functionality
- `test_wxpython_backend.py` - Additional wxPython tests
- `test_backend_comprehensive.py` - Cross-backend compatibility

### Feature Tests
- `test_float_fields.py` - Float field formatting and validation
- `test_format_strings.py` - Advanced format string handling
- `test_custom_buttons.py` - Custom button functionality
- `test_data_persistence.py` - Data loading and saving

### UI Layout Tests
- `test_tabs.py` - Basic tab functionality
- `test_qt_tabs.py` - Qt tab implementation
- `test_wx_tabs*.py` - wxPython tab implementations
- `test_tab_field_expansion.py` - Field expansion in tabs
- `test_nested_fields.py` - Nested field name support

### Compatibility Tests
- `test_qt_compatibility.py` - Qt version compatibility
- `test_int_vs_float.py` - Numeric field type handling

## Test Structure

Each test file is self-contained and can be run independently:

```python
#!/usr/bin/env python3
"""Test description."""

import sys
import os
from pathlib import Path

# Add library to path (automatically handled)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_function():
    """Test implementation."""
    # Test code here
    pass

if __name__ == "__main__":
    test_function()
```

## Adding New Tests

1. Create a new file: `test_your_feature.py`
2. Follow the existing test structure
3. Add appropriate imports and setup
4. Implement test functions
5. Run with: `python run_tests.py your_feature`

## Dependencies

Tests are designed to work with minimal dependencies:
- **Required**: qtpyguihelper library
- **Optional**: pytest (for advanced test running)
- **Backend-specific**: PySide6/PyQt6 (Qt tests), wxPython (wx tests)

## Test Results

The test runner provides summary results:
```
==================================================
Test Results:
  Passed: 15
  Failed: 0
  Total:  15
==================================================
```

Individual test failures include detailed error information for debugging.
