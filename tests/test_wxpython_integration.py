#!/usr/bin/env python3
"""
Quick test to verify wxPython integration and backend selection.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_backend_detection():
    """Test backend detection and availability."""
    print("=== Backend Detection Test ===")

    from qtpyguihelper import get_available_backends, get_backend_info, is_backend_available

    available = get_available_backends()
    print(f"Available backends: {available}")

    print(f"Qt available: {is_backend_available('qt')}")
    print(f"wxPython available: {is_backend_available('wx')}")

    current_info = get_backend_info()
    print(f"Current backend: {current_info['backend']}")

    return len(available) > 0

def test_backend_switching():
    """Test switching between backends."""
    print("\n=== Backend Switching Test ===")

    from qtpyguihelper import set_backend, get_backend, get_available_backends

    available = get_available_backends()

    for backend in available:
        try:
            print(f"Testing {backend} backend...")
            set_backend(backend)
            current = get_backend()
            assert current == backend, f"Expected {backend}, got {current}"
            print(f"✓ {backend} backend set successfully")
        except Exception as e:
            print(f"✗ Error with {backend} backend: {e}")
            return False

    return True

def test_unified_interface():
    """Test the unified GuiBuilder interface."""
    print("\n=== Unified Interface Test ===")

    try:
        from qtpyguihelper import GuiBuilder

        # Create a simple configuration
        config = {
            "window": {"title": "Test", "width": 400, "height": 300},
            "fields": [
                {"name": "test_field", "type": "text", "label": "Test Field"}
            ]
        }

        # Test that we can create the builder without errors
        builder = GuiBuilder(config_dict=config)
        print(f"✓ Unified GuiBuilder created successfully with {builder.backend} backend")

        # Test that we can get/set data
        test_data = {"test_field": "test_value"}
        builder.set_form_data(test_data)
        retrieved_data = builder.get_form_data()

        assert retrieved_data["test_field"] == "test_value", "Data setting/getting failed"
        print("✓ Form data operations working")

        return True

    except Exception as e:
        print(f"✗ Unified interface test failed: {e}")
        return False

def test_widget_factories():
    """Test that both widget factories can be imported and work."""
    print("\n=== Widget Factory Test ===")

    try:
        from qtpyguihelper import WidgetFactory, WxWidgetFactory
        from qtpyguihelper.config_loader import FieldConfig

        # Test basic widget factory creation
        qt_factory = WidgetFactory()
        wx_factory = WxWidgetFactory()
        print("✓ Both widget factories imported successfully")

        # Test field config creation
        field_config = FieldConfig(
            name="test",
            type="text",
            label="Test Field",
            required=False
        )
        print("✓ Field configuration created successfully")

        return True

    except Exception as e:
        print(f"✗ Widget factory test failed: {e}")
        return False

def test_configuration_loading():
    """Test configuration loading with both backends."""
    print("\n=== Configuration Loading Test ===")

    try:
        from qtpyguihelper.config_loader import ConfigLoader

        # Test programmatic configuration
        config_dict = {
            "window": {
                "title": "Backend Test",
                "width": 500,
                "height": 400
            },
            "layout": "form",
            "fields": [
                {
                    "name": "name",
                    "type": "text",
                    "label": "Name",
                    "required": True
                },
                {
                    "name": "age",
                    "type": "int",
                    "label": "Age",
                    "min_value": 0,
                    "max_value": 120
                },
                {
                    "name": "height",
                    "type": "float",
                    "label": "Height",
                    "format_string": ".2f"
                },
                {
                    "name": "active",
                    "type": "checkbox",
                    "label": "Active"
                }
            ],
            "submit_button": True,
            "custom_buttons": [
                {
                    "name": "test_btn",
                    "label": "Test Button"
                }
            ]
        }

        loader = ConfigLoader()
        config = loader.load_from_dict(config_dict)

        print(f"✓ Configuration loaded: {len(config.fields)} fields")
        print(f"✓ Custom buttons: {len(config.custom_buttons)}")
        print(f"✓ Field types: {[f.type for f in config.fields]}")

        return True

    except Exception as e:
        print(f"✗ Configuration loading test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("QtPyGuiHelper Integration Test")
    print("=" * 50)

    tests = [
        test_backend_detection,
        test_backend_switching,
        test_widget_factories,
        test_configuration_loading,
        test_unified_interface
    ]

    passed = 0
    total = len(tests)

    for test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                print(f"✗ {test_func.__name__} failed")
        except Exception as e:
            print(f"✗ {test_func.__name__} crashed: {e}")

    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! wxPython integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
