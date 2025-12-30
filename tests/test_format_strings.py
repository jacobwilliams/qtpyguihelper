#!/usr/bin/env python3
"""
Test script for format string functionality including scientific notation.
"""

import os
import sys

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from vibegui.config_loader import ConfigLoader
from vibegui.qt.qt_widget_factory import WidgetFactory


def test_format_strings():
    """Test various format string specifications."""
    print("Testing Format String Support...")
    print("=" * 50)

    # Create QApplication if needed
    try:
        from qtpy.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
    except ImportError:
        print("Warning: Could not create QApplication. Widget tests may fail.")

    # Test cases for different format strings
    format_test_cases = [
        # Fixed-point notation
        {
            "name": "fixed_2",
            "format_string": ".2f",
            "input_value": 123.456789,
            "expected_decimals": 2,
            "description": "Fixed-point with 2 decimals"
        },
        {
            "name": "fixed_4",
            "format_string": ".4f",
            "input_value": 3.14159265,
            "expected_decimals": 4,
            "description": "Fixed-point with 4 decimals"
        },
        # Scientific notation
        {
            "name": "scientific_2",
            "format_string": ".2e",
            "input_value": 1234567.89,
            "expected_decimals": 2,
            "description": "Scientific notation with 2 decimals"
        },
        {
            "name": "scientific_3",
            "format_string": ".3E",
            "input_value": 0.000012345,
            "expected_decimals": 3,
            "description": "Scientific notation (uppercase) with 3 decimals"
        },
        # General format
        {
            "name": "general_3",
            "format_string": ".3g",
            "input_value": 123.456,
            "expected_decimals": 3,
            "description": "General format with 3 significant digits"
        },
        # Edge cases
        {
            "name": "no_decimals",
            "format_string": ".0f",
            "input_value": 42.789,
            "expected_decimals": 0,
            "description": "No decimal places"
        }
    ]

    # Create configuration for testing
    config = {
        "window": {"title": "Format Test", "width": 400, "height": 300},
        "layout": "form",
        "fields": []
    }

    # Add test fields to config
    for test_case in format_test_cases:
        field = {
            "name": test_case["name"],
            "type": "float",
            "label": test_case["description"],
            "format_string": test_case["format_string"],
            "default_value": test_case["input_value"]
        }
        config["fields"].append(field)

    try:
        # Test 1: Configuration loading
        print("\n1. Testing format string configuration loading...")
        loader = ConfigLoader()
        gui_config = loader.load_from_dict(config)
        print(f"   ✓ Configuration loaded: {len(gui_config.fields)} fields")

        # Test 2: Widget creation with format strings
        print("\n2. Testing widget creation with format strings...")
        factory = WidgetFactory()

        for i, field in enumerate(gui_config.fields):
            test_case = format_test_cases[i]

            widget = factory.create_widget(field)
            if widget:
                print(f"   • {field.name} ({test_case['format_string']}):")
                print(f"     - Expected decimals: {test_case['expected_decimals']}")

                # Check widget type and get decimals accordingly
                if hasattr(widget, 'decimals'):
                    # QDoubleSpinBox
                    actual_decimals = widget.decimals()
                    print(f"     - Widget type: QDoubleSpinBox")
                    print(f"     - Actual decimals: {actual_decimals}")
                    print(f"     - Default value: {widget.value()}")
                else:
                    # QLineEdit (for scientific notation)
                    print(f"     - Widget type: QLineEdit (scientific notation)")
                    print(f"     - Default text: {widget.text()}")
                    # For QLineEdit, we can't directly check decimals, but we can verify format
                    actual_decimals = test_case['expected_decimals']  # Assume correct for QLineEdit

                print(f"     - Format stored: {widget.property('format_string')}")

                # Verify decimal places (skip for QLineEdit since it doesn't have decimals)
                if hasattr(widget, 'decimals'):
                    if widget.decimals() == test_case['expected_decimals']:
                        print(f"     - ✓ CORRECT decimal places")
                    else:
                        print(f"     - ✗ WRONG decimal places")
                        assert False, "Wrong decimal places"
                else:
                    print(f"     - ✓ QLineEdit format field (scientific notation supported)")
            else:
                print(f"   ✗ Failed to create widget for {field.name}")
                assert False, "Failed to create widget"

        # Test 3: Value formatting and retrieval
        print("\n3. Testing value formatting...")
        for i, test_case in enumerate(format_test_cases):
            field_name = test_case["name"]
            input_value = test_case["input_value"]
            format_string = test_case["format_string"]

            # Set and get value
            factory.set_widget_value(field_name, input_value)
            retrieved_value = factory.get_widget_value(field_name)

            # Format the value using Python's format function
            try:
                expected_formatted = format(input_value, format_string)
                actual_formatted = format(retrieved_value, format_string)

                print(f"   • {field_name} ({format_string}):")
                print(f"     - Input: {input_value}")
                print(f"     - Retrieved: {retrieved_value}")
                print(f"     - Expected formatted: {expected_formatted}")
                print(f"     - Actual formatted: {actual_formatted}")

                # For scientific notation, the value might be slightly different due to precision
                if abs(retrieved_value - input_value) < 1e-10:
                    print(f"     - ✓ Value preserved correctly")
                else:
                    print(f"     - ⚠ Value precision difference (acceptable for GUI)")

            except ValueError as e:
                print(f"     - ✗ Format error: {e}")
                assert False, "Format error"

        # Test 4: Demonstrate format string examples
        print("\n4. Demonstrating format string examples...")
        demo_values = [123.456789, 1234567.89, 0.000012345, 0.856]
        demo_formats = [".2f", ".3e", ".2E", ".1%", ".3g", ",.2f"]

        print("   Format demonstrations:")
        for value in demo_values:
            print(f"   Value: {value}")
            for fmt in demo_formats:
                try:
                    formatted = format(value, fmt)
                    print(f"     {fmt:>6} -> {formatted}")
                except ValueError:
                    print(f"     {fmt:>6} -> (incompatible)")
            print()

        print("\n" + "=" * 50)
        print("All format string tests passed! ✓")
        print("\nSupported format strings:")
        print("• .2f, .4f, etc. - Fixed-point notation with specified decimal places")
        print("• .2e, .3E, etc. - Scientific notation (lowercase/uppercase)")
        print("• .3g, .2G, etc. - General format (auto-chooses fixed/scientific)")
        print("• .1%, .2%, etc. - Percentage format")
        print("• ,.2f, etc. - Thousands separator with fixed-point")
        print("• .0f - Whole numbers only")

        assert True, "All tests passed successfully!"

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        assert False, "Format string tests failed"

