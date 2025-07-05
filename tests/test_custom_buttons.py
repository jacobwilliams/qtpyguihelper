#!/usr/bin/env python3
"""
Test suite for custom buttons functionality in qtpyguihelper.
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Add the qtpyguihelper module to the path
sys.path.insert(0, str(Path(__file__).parent))

from qtpyguihelper import GuiBuilder, ConfigLoader, CustomButtonConfig


def test_custom_button_config():
    """Test CustomButtonConfig dataclass."""
    print("Testing CustomButtonConfig...")

    # Test basic config
    button_config = CustomButtonConfig(
        name="test_button",
        label="Test Button"
    )
    assert button_config.name == "test_button"
    assert button_config.label == "Test Button"
    assert button_config.enabled is True
    assert button_config.tooltip is None
    assert button_config.icon is None
    assert button_config.style is None

    # Test config with all parameters
    button_config2 = CustomButtonConfig(
        name="full_button",
        label="Full Button",
        tooltip="This is a tooltip",
        enabled=False,
        icon="icon.png",
        style="color: red;"
    )
    assert button_config2.name == "full_button"
    assert button_config2.label == "Full Button"
    assert button_config2.tooltip == "This is a tooltip"
    assert button_config2.enabled is False
    assert button_config2.icon == "icon.png"
    assert button_config2.style == "color: red;"

    print("✓ CustomButtonConfig tests passed")


def test_config_loader_custom_buttons():
    """Test ConfigLoader with custom buttons."""
    print("Testing ConfigLoader with custom buttons...")

    # Create test configuration
    config_data = {
        "fields": [
            {
                "name": "test_field",
                "type": "text",
                "label": "Test Field"
            }
        ],
        "custom_buttons": [
            {
                "name": "button1",
                "label": "Button 1"
            },
            {
                "name": "button2",
                "label": "Button 2",
                "tooltip": "This is button 2",
                "enabled": False,
                "style": "background-color: red;"
            }
        ]
    }

    # Test loading configuration
    loader = ConfigLoader()
    config = loader.load_from_dict(config_data)

    # Verify custom buttons are loaded
    assert config.custom_buttons is not None
    assert len(config.custom_buttons) == 2

    button1 = config.custom_buttons[0]
    assert button1.name == "button1"
    assert button1.label == "Button 1"
    assert button1.enabled is True
    assert button1.tooltip is None

    button2 = config.custom_buttons[1]
    assert button2.name == "button2"
    assert button2.label == "Button 2"
    assert button2.tooltip == "This is button 2"
    assert button2.enabled is False
    assert button2.style == "background-color: red;"

    print("✓ ConfigLoader custom buttons tests passed")


def test_config_validation():
    """Test configuration validation for custom buttons."""
    print("Testing custom buttons configuration validation...")

    loader = ConfigLoader()

    # Test valid configuration
    valid_config = {
        "fields": [
            {"name": "field1", "type": "text", "label": "Field 1"}
        ],
        "custom_buttons": [
            {"name": "btn1", "label": "Button 1"}
        ]
    }

    try:
        loader.load_from_dict(valid_config)
        print("✓ Valid configuration accepted")
    except Exception as e:
        print(f"✗ Valid configuration rejected: {e}")
        return False

    # Test missing required keys
    invalid_configs = [
        # Missing name
        {
            "fields": [{"name": "field1", "type": "text", "label": "Field 1"}],
            "custom_buttons": [{"label": "Button 1"}]
        },
        # Missing label
        {
            "fields": [{"name": "field1", "type": "text", "label": "Field 1"}],
            "custom_buttons": [{"name": "btn1"}]
        },
        # Duplicate button names
        {
            "fields": [{"name": "field1", "type": "text", "label": "Field 1"}],
            "custom_buttons": [
                {"name": "btn1", "label": "Button 1"},
                {"name": "btn1", "label": "Button 2"}
            ]
        },
        # Non-list custom_buttons
        {
            "fields": [{"name": "field1", "type": "text", "label": "Field 1"}],
            "custom_buttons": "not a list"
        }
    ]

    for i, invalid_config in enumerate(invalid_configs):
        try:
            loader.load_from_dict(invalid_config)
            print(f"✗ Invalid configuration {i+1} was accepted")
            return False
        except ValueError:
            print(f"✓ Invalid configuration {i+1} correctly rejected")
        except Exception as e:
            print(f"✗ Invalid configuration {i+1} rejected with unexpected error: {e}")
            return False

    print("✓ Configuration validation tests passed")
    return True


def test_gui_builder_custom_buttons():
    """Test GuiBuilder with custom buttons."""
    print("Testing GuiBuilder with custom buttons...")

    # Create QApplication for widget tests
    try:
        from qtpy.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
    except:
        print("Warning: Could not create QApplication. GUI tests may fail.")

    # Create test configuration file
    config_data = {
        "window": {
            "title": "Test Custom Buttons",
            "width": 400,
            "height": 300
        },
        "fields": [
            {
                "name": "test_field",
                "type": "text",
                "label": "Test Field"
            }
        ],
        "custom_buttons": [
            {
                "name": "test_btn",
                "label": "Test Button",
                "tooltip": "This is a test button"
            },
            {
                "name": "action_btn",
                "label": "Action Button",
                "style": "background-color: blue; color: white;"
            }
        ]
    }

    # Create temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        config_path = f.name

    try:
        # Test GUI creation (without showing)
        gui = GuiBuilder(config_path)

        # Test getting custom button names
        button_names = gui.get_custom_button_names()
        assert len(button_names) == 2
        assert "test_btn" in button_names
        assert "action_btn" in button_names

        # Test callback registration
        callback_called = {"value": False}

        def test_callback(form_data):
            callback_called["value"] = True
            assert isinstance(form_data, dict)

        gui.set_custom_button_callback("test_btn", test_callback)

        # Verify callback is registered
        assert "test_btn" in gui.custom_button_callbacks
        assert gui.custom_button_callbacks["test_btn"] is test_callback

        # Test removing callback
        gui.remove_custom_button_callback("test_btn")
        assert "test_btn" not in gui.custom_button_callbacks

        print("✓ GuiBuilder custom buttons tests passed")
        return True

    except Exception as e:
        print(f"✗ GuiBuilder custom buttons test failed: {e}")
        return False
    finally:
        # Clean up temporary file
        try:
            os.unlink(config_path)
        except:
            pass


def test_no_custom_buttons():
    """Test that configurations without custom buttons still work."""
    print("Testing configuration without custom buttons...")

    # Create QApplication for widget tests
    try:
        from qtpy.QtWidgets import QApplication
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
    except:
        print("Warning: Could not create QApplication. GUI tests may fail.")

    config_data = {
        "fields": [
            {
                "name": "test_field",
                "type": "text",
                "label": "Test Field"
            }
        ]
    }

    loader = ConfigLoader()
    config = loader.load_from_dict(config_data)

    # Verify custom_buttons is None when not specified
    assert config.custom_buttons is None

    # Create temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f)
        config_path = f.name

    try:
        # Test GUI creation
        gui = GuiBuilder(config_path)

        # Test getting custom button names (should be empty)
        button_names = gui.get_custom_button_names()
        assert len(button_names) == 0

        print("✓ No custom buttons test passed")
        return True

    except Exception as e:
        print(f"✗ No custom buttons test failed: {e}")
        return False
    finally:
        # Clean up temporary file
        try:
            os.unlink(config_path)
        except:
            pass


def main():
    """Run all tests."""
    print("Running custom buttons tests...\n")

    tests = [
        test_custom_button_config,
        test_config_loader_custom_buttons,
        test_config_validation,
        test_gui_builder_custom_buttons,
        test_no_custom_buttons
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            failed += 1
        print()

    print(f"Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())
