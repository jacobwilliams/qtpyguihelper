#!/usr/bin/env python3
"""
Quick test to verify wxPython integration and backend selection.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_backend_detection() -> None:
    """Test backend detection and availability."""
    print("=== Backend Detection Test ===")

    from vibegui import get_available_backends, get_backend_info, is_backend_available

    available = get_available_backends()
    print(f"Available backends: {available}")

    print(f"Qt available: {is_backend_available('qt')}")
    print(f"wxPython available: {is_backend_available('wx')}")

    current_info = get_backend_info()
    print(f"Current backend: {current_info['backend']}")

    assert len(available) > 0, "No available backends detected"

def test_backend_switching() -> None:
    """Test switching between backends."""
    print("\n=== Backend Switching Test ===")

    from vibegui import set_backend, get_backend, get_available_backends

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
            assert False, f"Failed to set {backend} backend"

    assert True, "All backends tested successfully"

def test_unified_interface() -> None:
    """Test the unified GuiBuilder interface."""
    print("\n=== Unified Interface Test ===")

    try:
        from vibegui import GuiBuilder, set_backend, is_backend_available

        # Create a simple configuration
        config = {
            "window": {"title": "Test", "width": 400, "height": 300},
            "fields": [
                {"name": "test_field", "type": "text", "label": "Test Field"}
            ]
        }

        # Force wxPython backend for this test if available
        if is_backend_available('wx'):
            # Create wxPython app before setting backend
            from .wx_test_utils import create_wx_app
            _app = create_wx_app()  # Keep app alive during test

            # Set wxPython backend
            set_backend('wx')
            print("✓ wxPython backend set for unified interface test")
        elif is_backend_available('qt'):
            # Fall back to Qt if wxPython not available
            from qtpy.QtWidgets import QApplication
            qt_app = QApplication.instance()
            if qt_app is None:
                _qt_app = QApplication(sys.argv)
            set_backend('qt')
            print("✓ Qt backend set for unified interface test (wxPython not available)")
        else:
            print("✗ No GUI backends available")
            assert False, "No GUI backends available for testing"

        # Test that we can create the builder without errors
        builder = GuiBuilder(config_dict=config)
        print(f"✓ Unified GuiBuilder created successfully with {builder.backend} backend")

        # Test that we can get/set data
        test_data = {"test_field": "test_value"}
        builder.set_form_data(test_data)
        retrieved_data = builder.get_form_data()

        assert retrieved_data["test_field"] == "test_value", "Data setting/getting failed"
        print("✓ Form data operations working")

        assert True, "Unified interface test passed"

    except Exception as e:
        print(f"✗ Unified interface test failed: {e}")
        assert False, "Unified interface test failed"

def test_widget_factories() -> None:
    """Test that both widget factories can be imported and work."""
    print("\n=== Widget Factory Test ===")

    try:
        from vibegui import WidgetFactory, WxWidgetFactory
        from vibegui.config_loader import FieldConfig

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

        assert True, "Widget factory test passed"

    except Exception as e:
        print(f"✗ Widget factory test failed: {e}")
        assert False, "Widget factory test failed"

def test_configuration_loading() -> None:
    """Test configuration loading with all backends."""
    print("\n=== Configuration Loading Test ===")

    try:
        from vibegui.config_loader import ConfigLoader

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

        assert True, "Configuration loading test passed"

    except Exception as e:
        print(f"✗ Configuration loading test failed: {e}")
        assert False, "Configuration loading test failed"

