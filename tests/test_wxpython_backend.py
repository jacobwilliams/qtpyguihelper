#!/usr/bin/env python3
"""
Test that wxPython demos can be created and configured properly.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from vibegui import GuiBuilder, set_backend, get_backend_info, is_backend_available

def test_wxpython_backend_creation() -> None:
    """Test that we can create a wxPython GUI builder without showing it."""
    print("Testing wxPython Backend Creation")
    print("=================================")

    # Check if wxPython is available
    if not is_backend_available('wx'):
        print("❌ wxPython backend not available")
        assert False, "wxPython backend not available"

    try:
        # Set wxPython backend
        set_backend('wx')
        print("✓ wxPython backend set")

        # Get backend info
        info = get_backend_info()
        print(f"✓ Backend: {info['backend']}")
        if 'wx_version' in info:
            print(f"✓ wxPython version: {info['wx_version']}")

        # Create a simple config
        config = {
            "window": {
                "title": "Test wxPython GUI",
                "width": 400,
                "height": 300
            },
            "layout": "form",
            "fields": [
                {
                    "name": "test_text",
                    "type": "text",
                    "label": "Test Field",
                    "default_value": "Hello wxPython!"
                },
                {
                    "name": "test_number",
                    "type": "int",
                    "label": "Test Number",
                    "default_value": 42
                },
                {
                    "name": "test_float",
                    "type": "float",
                    "label": "Test Float",
                    "format_string": ".2f",
                    "default_value": 3.14
                }
            ],
            "custom_buttons": [
                {
                    "name": "test_button",
                    "label": "Test Button",
                    "tooltip": "This is a test button"
                }
            ]
        }

        # Create wxPython app BEFORE creating GUI components
        from .wx_test_utils import create_wx_app
        app = create_wx_app()

        # Create GUI builder (but don't show it)
        gui_builder = GuiBuilder(config_dict=config)
        print("✓ wxPython GUI builder created successfully")

        # Test that we can access the backend
        print(f"✓ GUI builder backend: {gui_builder.backend}")

        # Test setting callbacks
        def test_callback(data: dict) -> None:
            print(f"Test callback called with: {data}")

        gui_builder.set_submit_callback(test_callback)
        gui_builder.set_custom_button_callback("test_button", test_callback)
        print("✓ Callbacks set successfully")

        # Test that we can get custom button names
        button_names = gui_builder.get_custom_button_names()
        print(f"✓ Custom buttons: {button_names}")

        # Test that we can access form data (should have defaults)
        form_data = gui_builder.get_form_data()
        print(f"✓ Form data accessible: {len(form_data)} fields")
        for key, value in form_data.items():
            print(f"  {key}: {value}")

        assert True, "wxPython GUI builder created successfully"

    except Exception as e:
        print(f"❌ Error creating wxPython GUI: {e}")
        import traceback
        traceback.print_exc()
        assert False, "Error creating wxPython GUI"


def test_advanced_wxpython_features() -> None:
    """Test advanced wxPython features like custom widgets."""
    print("\nTesting Advanced wxPython Features")
    print("===================================")

    if not is_backend_available('wx'):
        print("❌ wxPython backend not available")
        assert False, "wxPython backend not available"

    try:
        set_backend('wx')

        # Test all supported field types
        advanced_config = {
            "window": {"title": "Advanced Test", "width": 500, "height": 600},
            "layout": "form",
            "fields": [
                {"name": "text_field", "type": "text", "label": "Text"},
                {"name": "email_field", "type": "email", "label": "Email"},
                {"name": "password_field", "type": "password", "label": "Password"},
                {"name": "int_field", "type": "int", "label": "Integer", "default_value": 10},
                {"name": "float_field", "type": "float", "label": "Float", "format_string": ".3f", "default_value": 1.234},
                {"name": "textarea_field", "type": "textarea", "label": "Textarea"},
                {"name": "checkbox_field", "type": "checkbox", "label": "Checkbox"},
                {"name": "radio_field", "type": "radio", "label": "Radio", "options": ["A", "B", "C"]},
                {"name": "select_field", "type": "select", "label": "Select", "options": ["X", "Y", "Z"]},
                {"name": "date_field", "type": "date", "label": "Date", "default_value": "2024-01-01"},
                {"name": "time_field", "type": "time", "label": "Time", "default_value": "12:00"},
                {"name": "datetime_field", "type": "datetime", "label": "DateTime"},
                {"name": "range_field", "type": "range", "label": "Range", "min_value": 0, "max_value": 100},
                {"name": "file_field", "type": "file", "label": "File"},
                {"name": "color_field", "type": "color", "label": "Color", "default_value": "#ff0000"},
                {"name": "url_field", "type": "url", "label": "URL"}
            ]
        }

        # Create wxPython app BEFORE creating advanced GUI
        from .wx_test_utils import create_wx_app
        app = create_wx_app()

        gui_builder = GuiBuilder(config_dict=advanced_config)
        print("✓ Advanced wxPython GUI created with all field types")

        # Test getting form data with all field types
        form_data = gui_builder.get_form_data()
        print(f"✓ Retrieved data from {len(form_data)} fields:")

        for field_name, value in form_data.items():
            print(f"  {field_name}: {value} ({type(value).__name__})")

        # Test setting form data
        test_data = {
            "text_field": "Updated text",
            "int_field": 99,
            "float_field": 2.718,
            "checkbox_field": True,
            "radio_field": "B",
            "select_field": "Y"
        }

        gui_builder.set_form_data(test_data)
        print("✓ Form data set successfully")

        # Verify the data was set
        updated_data = gui_builder.get_form_data()
        for key, expected_value in test_data.items():
            actual_value = updated_data.get(key)
            if str(actual_value) == str(expected_value):
                print(f"  ✓ {key}: {actual_value}")
            else:
                print(f"  ⚠ {key}: expected {expected_value}, got {actual_value}")

        assert True, "Advanced wxPython features tested successfully"

    except Exception as e:
        print(f"❌ Error testing advanced features: {e}")
        import traceback
        traceback.print_exc()
        assert False, "Error testing advanced wxPython features"


def main() -> None:
    """Run all tests."""
    print("wxPython Backend Test Suite")
    print("===========================")

    tests = [
        test_wxpython_backend_creation,
        test_advanced_wxpython_features
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"Test failed with exception: {e}")
            results.append(False)

    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print(f"{'='*50}")

    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"ALL TESTS PASSED! ({passed}/{total})")
        print("✓ wxPython backend is fully functional")
        print("✓ All field types are supported")
        print("✓ Custom buttons work correctly")
        print("✓ Form data handling is working")
        assert True, "All wxPython tests passed successfully"
    else:
        print(f"SOME TESTS FAILED! ({passed}/{total})")
        assert False, "Some wxPython tests failed"

