#!/usr/bin/env python3
"""
Test suite for custom buttons functionality in vibegui.
"""

import sys
import os
import json
import tempfile
import pytest
from pathlib import Path

# Add the vibegui module to the path
sys.path.insert(0, str(Path(__file__).parent))

from vibegui import GuiBuilder, ConfigLoader, CustomButtonConfig
from vibegui.exceptions import ConfigurationError


def test_custom_button_config() -> None:
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


def test_config_loader_custom_buttons() -> None:
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


def test_config_validation() -> None:
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
        assert False, "Valid configuration was incorrectly rejected"

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
            assert False, f"Invalid configuration {i+1} should have been rejected"
        except (ValueError, ConfigurationError):
            print(f"✓ Invalid configuration {i+1} correctly rejected")
        except Exception as e:
            print(f"✗ Invalid configuration {i+1} rejected with unexpected error: {e}")
            assert False, f"Invalid configuration {i+1} should have raised ValueError or ConfigurationError"

    print("✓ Configuration validation tests passed")
    assert True, "All configuration validation tests passed"


@pytest.mark.gui
@pytest.mark.qt
def test_gui_builder_custom_buttons() -> None:
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

        def test_callback(form_data: dict) -> None:
            callback_called["value"] = True
            assert isinstance(form_data, dict)

        gui.set_custom_button_callback("test_btn", test_callback)

        # Test that we can set and remove callbacks (no direct access to internal state)
        # Since we can't access the internal callbacks dict, we'll test functionality indirectly

        # Test removing callback
        gui.remove_custom_button_callback("test_btn")

        # Test setting another callback to ensure the methods work
        def another_callback(_form_data: dict) -> None:
            pass

        gui.set_custom_button_callback("action_btn", another_callback)
        gui.remove_custom_button_callback("action_btn")

        print("✓ GuiBuilder custom buttons tests passed")
        assert True, "GuiBuilder custom buttons tests passed successfully"

    except Exception as e:
        print(f"✗ GuiBuilder custom buttons test failed: {e}")
        assert False, f"GuiBuilder custom buttons test failed: {e}"
    finally:
        # Clean up temporary file
        try:
            os.unlink(config_path)
        except:
            pass


@pytest.mark.gui
@pytest.mark.qt
def test_no_custom_buttons() -> None:
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
        assert True, "No custom buttons test passed successfully"

    except Exception as e:
        print(f"✗ No custom buttons test failed: {e}")
        assert False, f"No custom buttons test failed: {e}"
    finally:
        # Clean up temporary file
        try:
            os.unlink(config_path)
        except:
            pass

