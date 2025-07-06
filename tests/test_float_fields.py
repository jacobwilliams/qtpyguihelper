#!/usr/bin/env python3
"""
Test script for float field functionality with format enforcement.
"""

import os
import sys

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from qtpyguihelper.config_loader import ConfigLoader
from qtpyguihelper.qt.widget_factory import WidgetFactory


def test_float_field_configuration():
    """Test float field configuration loading and validation."""
    print("Testing Float Field Configuration...")
    print("=" * 50)

    # Create QApplication if needed
    try:
        from qtpy.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
    except ImportError:
        print("Warning: Could not create QApplication. Widget tests may fail.")

    # Create a test configuration with float fields
    config = {
        "window": {"title": "Float Test Form", "width": 400, "height": 300},
        "layout": "form",
        "fields": [
            {
                "name": "basic_float",
                "type": "float",
                "label": "Basic Float",
                "default_value": 3.14159
            },
            {
                "name": "currency",
                "type": "float",
                "label": "Price ($)",
                "min_value": 0.0,
                "max_value": 10000.0,
                "format_string": ".2f",
                "default_value": 99.99,
                "tooltip": "Enter price in dollars"
            },
            {
                "name": "percentage",
                "type": "float",
                "label": "Percentage",
                "min_value": 0.0,
                "max_value": 100.0,
                "format_string": ".1f",
                "default_value": 85.5,
                "tooltip": "Enter percentage value"
            },
            {
                "name": "precision",
                "type": "float",
                "label": "High Precision",
                "format_string": ".4f",
                "default_value": 0.0001,
                "tooltip": "High precision decimal value"
            }
        ]
    }

    try:
        # Test 1: Configuration loading
        print("\n1. Testing float field configuration loading...")
        loader = ConfigLoader()
        gui_config = loader.load_from_dict(config)
        print(f"   ✓ Configuration loaded: {len(gui_config.fields)} fields")

        # Test 2: Verify float field attributes
        print("\n2. Testing float field attributes...")
        float_fields = [f for f in gui_config.fields if f.type == "float"]
        print(f"   ✓ Found {len(float_fields)} float fields")

        for field in float_fields:
            print(f"   • {field.name}:")
            print(f"     - Type: {field.type}")
            print(f"     - Format: {field.format_string}")
            print(f"     - Default: {field.default_value}")
            print(f"     - Range: {field.min_value} to {field.max_value}")

        # Test 3: Widget creation
        print("\n3. Testing float widget creation...")
        factory = WidgetFactory()

        for field in float_fields:
            widget = factory.create_widget(field)
            if widget:
                print(f"   ✓ Widget created for {field.name}")
                print(f"     - Widget type: {type(widget).__name__}")
                if hasattr(widget, 'decimals'):
                    print(f"     - Decimals: {widget.decimals()}")
                if hasattr(widget, 'minimum'):
                    print(f"     - Minimum: {widget.minimum()}")
                if hasattr(widget, 'maximum'):
                    print(f"     - Maximum: {widget.maximum()}")
                if hasattr(widget, 'value'):
                    print(f"     - Default value: {widget.value()}")
            else:
                print(f"   ✗ Failed to create widget for {field.name}")
                assert False, f"Failed to create widget for {field.name}"

        # Test 4: Value handling
        print("\n4. Testing float value handling...")
        test_values = {
            "basic_float": 2.71828,
            "currency": 123.45,
            "percentage": 67.8,
            "precision": 0.12345
        }

        for field_name, test_value in test_values.items():
            success = factory.set_widget_value(field_name, test_value)
            if success:
                retrieved_value = factory.get_widget_value(field_name)
                print(f"   ✓ {field_name}: Set {test_value}, Got {retrieved_value}")
            else:
                print(f"   ✗ Failed to set value for {field_name}")
                assert False, f"Failed to set value for {field_name}"

        # Test 5: Get all values
        print("\n5. Testing get_all_values...")
        all_values = factory.get_all_values()
        print("   ✓ Retrieved all values:")
        for key, value in all_values.items():
            print(f"     - {key}: {value} ({type(value).__name__})")

        print("\n" + "=" * 50)
        print("All float field tests passed! ✓")
        print("\nFloat field features:")
        print("• Support for float data type with configurable precision")
        print("• Format string enforcement (e.g., '.2f', '.4f')")
        print("• Configurable decimal places")
        print("• Range validation (min/max values)")
        print("• Proper step size based on decimal precision")
        print("• Integration with existing widget factory")

        # Test completed successfully

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        assert False, f"Test failed with error: {e}"


def test_float_format_strings():
    """Test various format string scenarios."""
    print("\nTesting Float Format Strings...")
    print("=" * 50)

    # Create QApplication if needed
    try:
        from qtpy.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
    except ImportError:
        print("Warning: Could not create QApplication. Widget tests may fail.")

    format_tests = [
        {"format_string": ".2f", "expected_decimals": 2},
        {"format_string": ".4f", "expected_decimals": 4},
        {"format_string": ".1f", "expected_decimals": 1},
        {"format_string": ".0f", "expected_decimals": 0},
        {"format_string": None, "expected_decimals": 2},  # Default to 2 decimal places
    ]

    factory = WidgetFactory()

    for i, test_case in enumerate(format_tests):
        field_config_data = {
            "name": f"test_field_{i}",
            "type": "float",
            "label": f"Test Field {i}",
            "format_string": test_case["format_string"],
            "default_value": 123.456789
        }

        # Create a minimal config
        config = {
            "window": {"title": "Test"},
            "fields": [field_config_data]
        }

        loader = ConfigLoader()
        gui_config = loader.load_from_dict(config)
        field = gui_config.fields[0]

        widget = factory.create_widget(field)
        actual_decimals = widget.decimals() if hasattr(widget, 'decimals') else None

        print(f"Test {i+1}: format='{test_case['format_string']}'")
        print(f"  Expected decimals: {test_case['expected_decimals']}")
        print(f"  Actual decimals: {actual_decimals}")

        if actual_decimals == test_case['expected_decimals']:
            print("  ✓ PASS")
        else:
            print("  ✗ FAIL")
            assert False, f"Expected {test_case['expected_decimals']} decimals, got {actual_decimals}"

    print("\n✓ All format string tests passed!")
    # Test completed successfully


def main():
    """Run the float field tests."""
    print("QtPyGuiHelper Float Field Test Suite")
    print("=" * 50)

    # Create QApplication for widget tests
    try:
        from qtpy.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
    except ImportError:
        print("Warning: Could not create QApplication. Widget tests may fail.")

    tests = [
        test_float_field_configuration,
        test_float_format_strings
    ]

    results = []
    for test_func in tests:
        try:
            test_func()  # Tests now use assertions instead of returning values
            results.append(True)
        except Exception as e:
            print(f"Test failed with exception: {e}")
            import traceback
            traceback.print_exc()
            results.append(False)

    passed = sum(results)
    total = len(results)

    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("\n🎉 All float field tests passed! The functionality is working correctly.")
        assert True, "All tests passed successfully!"
    else:
        print(f"\n❌ {total - passed} test(s) failed. Please check the implementation.")
        assert False, "Some tests failed"


if __name__ == "__main__":
    sys.exit(main())
