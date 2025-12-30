#!/usr/bin/env python3
"""
Test script for integer vs float field functionality.
"""

import os
import sys

# Add the library to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from vibegui.config_loader import ConfigLoader
from vibegui.qt.qt_widget_factory import WidgetFactory
from qtpy.QtWidgets import QSpinBox, QDoubleSpinBox


def test_int_vs_float_fields():
    """Test that int and float fields create appropriate widgets."""
    print("Testing Int vs Float Field Types...")
    print("=" * 50)

    # Create QApplication if needed
    try:
        from qtpy.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
    except ImportError:
        print("Warning: Could not create QApplication. Widget tests may fail.")

    # Create a test configuration with both int and float fields
    config = {
        "window": {"title": "Int vs Float Test", "width": 400, "height": 300},
        "layout": "form",
        "fields": [
            {
                "name": "age",
                "type": "int",
                "label": "Age",
                "min_value": 0,
                "max_value": 150,
                "default_value": 25
            },
            {
                "name": "quantity",
                "type": "int",
                "label": "Quantity",
                "min_value": 1,
                "max_value": 1000,
                "default_value": 10
            },
            {
                "name": "height",
                "type": "float",
                "label": "Height (cm)",
                "min_value": 50.0,
                "max_value": 250.0,
                "format_string": ".1f",
                "default_value": 175.5
            },
            {
                "name": "weight",
                "type": "float",
                "label": "Weight (kg)",
                "format_string": ".2f",
                "default_value": 70.25
            },
            {
                "name": "legacy_number",
                "type": "number",
                "label": "Legacy Number",
                "default_value": 42.5
            }
        ]
    }

    try:
        # Test 1: Configuration loading
        print("\n1. Testing configuration loading...")
        loader = ConfigLoader()
        gui_config = loader.load_from_dict(config)
        print(f"   ✓ Configuration loaded: {len(gui_config.fields)} fields")

        # Test 2: Widget creation and type verification
        print("\n2. Testing widget creation and types...")
        factory = WidgetFactory()

        expected_types = {
            "age": QSpinBox,
            "quantity": QSpinBox,
            "height": QDoubleSpinBox,
            "weight": QDoubleSpinBox,
            "legacy_number": QDoubleSpinBox  # number type should create QDoubleSpinBox
        }

        for field in gui_config.fields:
            widget = factory.create_widget(field)
            expected_type = expected_types[field.name]
            actual_type = type(widget)

            print(f"   • {field.name} ({field.type}):")
            print(f"     - Expected: {expected_type.__name__}")
            print(f"     - Actual: {actual_type.__name__}")

            if isinstance(widget, expected_type):
                print(f"     - ✓ CORRECT widget type")

                # Test specific properties
                if isinstance(widget, QSpinBox):
                    print(f"     - Range: {widget.minimum()} to {widget.maximum()}")
                    print(f"     - Value: {widget.value()}")
                elif isinstance(widget, QDoubleSpinBox):
                    print(f"     - Range: {widget.minimum()} to {widget.maximum()}")
                    print(f"     - Decimals: {widget.decimals()}")
                    print(f"     - Value: {widget.value()}")

            else:
                print(f"     - ✗ WRONG widget type")
                assert False, "WRONG widget type"

        # Test 3: Value handling
        print("\n3. Testing value handling...")
        test_values = {
            "age": 30,           # int
            "quantity": 5,       # int
            "height": 180.5,     # float
            "weight": 75.25,     # float
            "legacy_number": 99.9 # number (should work as float)
        }

        for field_name, test_value in test_values.items():
            success = factory.set_widget_value(field_name, test_value)
            if success:
                retrieved_value = factory.get_widget_value(field_name)
                print(f"   ✓ {field_name}: Set {test_value} -> Got {retrieved_value} ({type(retrieved_value).__name__})")

                # Verify data types
                widget = factory.widgets[field_name]
                if isinstance(widget, QSpinBox):
                    assert isinstance(retrieved_value, int), f"QSpinBox should return int, got {type(retrieved_value)}"
                elif isinstance(widget, QDoubleSpinBox):
                    assert isinstance(retrieved_value, float), f"QDoubleSpinBox should return float, got {type(retrieved_value)}"

            else:
                print(f"   ✗ Failed to set value for {field_name}")
                assert False, f"Failed to set value for {field_name}"

        # Test 4: Get all values with correct types
        print("\n4. Testing get_all_values with type verification...")
        all_values = factory.get_all_values()
        print("   Retrieved values with types:")
        for key, value in all_values.items():
            print(f"     - {key}: {value} ({type(value).__name__})")

            # Verify expected types based on field type
            field = next((f for f in gui_config.fields if f.name == key), None)
            if field:
                if field.type == "int":
                    assert isinstance(value, int), f"Int field {key} should return int, got {type(value)}"
                elif field.type == "float":
                    assert isinstance(value, float), f"Float field {key} should return float, got {type(value)}"
                elif field.type == "number":
                    assert isinstance(value, (int, float)), f"Number field {key} should return numeric type, got {type(value)}"

        print("\n" + "=" * 50)
        print("All int vs float field tests passed! ✓")
        print("\nField type summary:")
        print("• 'int' fields use QSpinBox and return integer values")
        print("• 'float' fields use QDoubleSpinBox with format control")
        print("• 'number' fields use QDoubleSpinBox (legacy compatibility)")
        print("• Proper type enforcement and value handling")

        assert True, "All tests passed successfully!"

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        assert False, "Int vs Float field tests failed"
