#!/usr/bin/env python3
"""
Test tkinter backend functionality.
"""

import sys
import os
import pytest

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import set_backend but NOT GuiBuilder at module level for Tkinter tests
from vibegui import set_backend, is_backend_available

# Set backend at module level
set_backend('tk')


@pytest.mark.gui
@pytest.mark.tk
def test_tkinter_backend_availability() -> None:
    """Test that tkinter backend is available."""
    print("Testing tkinter Backend Availability")
    print("====================================")

    # Check if tkinter is available
    assert is_backend_available('tk'), "tkinter backend should be available"
    print("✓ tkinter backend is available")


# @pytest.mark.gui
# @pytest.mark.tk
def test_tkinter_backend_creation() -> None:
    """Test that we can create a tkinter GUI builder without showing it."""

    import tkinter as tk

    # Import GuiBuilder INSIDE test function (like demo does)
    from vibegui import GuiBuilder

    print("Testing tkinter Backend Creation")
    print("================================")

    # NOTE: Do NOT call get_backend_info() for Tkinter on macOS - it corrupts state
    # and causes crashes in gui.show()

    # Create a simple config
    config = {
        "window": {
            "title": "Test tkinter GUI",
            "width": 400,
            "height": 300
        },
        "layout": "form",
        "fields": [
            {
                "name": "test_text",
                "type": "text",
                "label": "Test Field",
                "default_value": "Hello tkinter!"
            },
            {
                "name": "test_number",
                "type": "int",
                "label": "Test Number",
                "default_value": 42
            },
            {
                "name": "test_checkbox",
                "type": "checkbox",
                "label": "Test Checkbox",
                "default_value": True
            }
        ]
    }

    # Create GUI builder (but don't show it)
    gui = GuiBuilder(config_dict=config)
    print(f"✓ Created GUI with backend: {gui.backend}")

    # Verify it's using tkinter
    assert gui.backend == 'tk', f"Expected tk backend, got {gui.backend}"

    # Show the GUI to build widgets (but don't run the event loop)
    print('showing gui...')
    gui.show()
    print('gui shown')

    # Test getting form data
    form_data = gui.get_form_data()
    print(f"✓ Form data: {form_data}")

    # Verify default values are set
    assert form_data['test_text'] == "Hello tkinter!", f"Expected 'Hello tkinter!', got {form_data['test_text']}"
    assert form_data['test_number'] == 42, f"Expected 42, got {form_data['test_number']}"
    assert form_data['test_checkbox'] is True, f"Expected True, got {form_data['test_checkbox']}"

    print("✓ Default values verified")

    # Test setting field values
    gui.set_field_value('test_text', 'Modified text')
    gui.set_field_value('test_number', 100)
    gui.set_field_value('test_checkbox', False)

    # Verify changes
    updated_data = gui.get_form_data()
    assert updated_data['test_text'] == 'Modified text'
    assert updated_data['test_number'] == 100
    assert updated_data['test_checkbox'] is False

    print("✓ Field value setting verified")

    # Clean up
    gui.close()
    print("✓ GUI closed successfully")

# test_tkinter_backend_creation()

@pytest.mark.gui
@pytest.mark.tk
def test_tkinter_all_field_types() -> None:
    """Test that all field types can be created with tkinter backend."""
    print("Testing All tkinter Field Types")
    print("===============================")

    set_backend('tk')
    from vibegui import GuiBuilder

    # Config with all supported field types
    config = {
        "window": {
            "title": "All Field Types Test",
            "width": 600,
            "height": 800
        },
        "layout": "form",
        "fields": [
            {
                "name": "text_field",
                "type": "text",
                "label": "Text Field",
                "default_value": "test text"
            },
            {
                "name": "number_field",
                "type": "number",
                "label": "Number Field",
                "default_value": 123.45
            },
            {
                "name": "int_field",
                "type": "int",
                "label": "Integer Field",
                "default_value": 42,
                "min_value": 0,
                "max_value": 100
            },
            {
                "name": "float_field",
                "type": "float",
                "label": "Float Field",
                "default_value": 3.14159
            },
            {
                "name": "email_field",
                "type": "email",
                "label": "Email Field",
                "default_value": "test@example.com"
            },
            {
                "name": "password_field",
                "type": "password",
                "label": "Password Field"
            },
            {
                "name": "textarea_field",
                "type": "textarea",
                "label": "Textarea Field",
                "default_value": "Multi-line\ntext here"
            },
            {
                "name": "checkbox_field",
                "type": "checkbox",
                "label": "Checkbox Field",
                "default_value": True
            },
            {
                "name": "radio_field",
                "type": "radio",
                "label": "Radio Field",
                "options": ["Option 1", "Option 2", "Option 3"],
                "default_value": "Option 2"
            },
            {
                "name": "select_field",
                "type": "select",
                "label": "Select Field",
                "options": ["First Choice", "Second Choice", "Third Choice"],
                "default_value": "Second Choice"
            },
            {
                "name": "date_field",
                "type": "date",
                "label": "Date Field",
                "default_value": "2023-12-25"
            },
            {
                "name": "time_field",
                "type": "time",
                "label": "Time Field",
                "default_value": "14:30:00"
            },
            {
                "name": "datetime_field",
                "type": "datetime",
                "label": "DateTime Field",
                "default_value": "2023-12-25 14:30:00"
            },
            {
                "name": "range_field",
                "type": "range",
                "label": "Range Field",
                "min_value": 0,
                "max_value": 100,
                "default_value": 50
            },
            {
                "name": "file_field",
                "type": "file",
                "label": "File Field"
            },
            {
                "name": "color_field",
                "type": "color",
                "label": "Color Field",
                "default_value": "#ff0000"
            },
            {
                "name": "url_field",
                "type": "url",
                "label": "URL Field",
                "default_value": "https://example.com"
            }
        ]
    }

    # Create GUI builder
    gui = GuiBuilder(config_dict=config)
    print(f"✓ Created GUI with {len(config['fields'])} field types")

    # Show the GUI to build widgets (but don't run the event loop)
    gui.show()

    # Test that all fields were created
    form_data = gui.get_form_data()
    field_names = [field['name'] for field in config['fields']]

    for field_name in field_names:
        assert field_name in form_data, f"Field {field_name} not found in form data"
        print(f"✓ Field '{field_name}' created successfully")

    # Test some specific default values
    print(f"Debug: select_field value = {form_data['select_field']}")
    assert form_data['text_field'] == "test text"
    assert form_data['int_field'] == 42
    assert form_data['checkbox_field'] is True
    assert form_data['radio_field'] == "Option 2"
    assert form_data['select_field'] == "Second Choice", f"Expected 'Second Choice', got '{form_data['select_field']}'"
    assert form_data['range_field'] == 50
    assert form_data['color_field'] == "#ff0000"

    print("✓ Default values verified for all field types")

    # Clean up
    gui.close()
    print("✓ All field types test completed successfully")


@pytest.mark.gui
@pytest.mark.tk
def test_tkinter_tabs() -> None:
    """Test tkinter backend with tabbed interface."""
    print("Testing tkinter Tabs")
    print("===================")

    set_backend('tk')
    from vibegui import GuiBuilder

    # Config with tabs
    config = {
        "window": {
            "title": "Tabs Test",
            "width": 500,
            "height": 400
        },
        "use_tabs": True,
        "fields": [
            {
                "name": "personal_name",
                "type": "text",
                "label": "Name",
                "default_value": "John Doe"
            },
            {
                "name": "personal_age",
                "type": "int",
                "label": "Age",
                "default_value": 30
            },
            {
                "name": "contact_email",
                "type": "email",
                "label": "Email",
                "default_value": "john@example.com"
            },
            {
                "name": "contact_phone",
                "type": "text",
                "label": "Phone",
                "default_value": "555-1234"
            }
        ],
        "tabs": [
            {
                "name": "personal",
                "title": "Personal Info",
                "fields": ["personal_name", "personal_age"]
            },
            {
                "name": "contact",
                "title": "Contact Info",
                "fields": ["contact_email", "contact_phone"]
            }
        ]
    }

    # Create GUI builder
    gui = GuiBuilder(config_dict=config)
    print("✓ Created tabbed GUI")

    # Show the GUI to build widgets (but don't run the event loop)
    gui.show()

    # Test that all fields are accessible
    form_data = gui.get_form_data()
    expected_fields = ["personal_name", "personal_age", "contact_email", "contact_phone"]

    for field_name in expected_fields:
        assert field_name in form_data, f"Field {field_name} not found in tabbed form"
        print(f"✓ Tab field '{field_name}' accessible")

    # Verify default values
    assert form_data['personal_name'] == "John Doe"
    assert form_data['personal_age'] == 30
    assert form_data['contact_email'] == "john@example.com"
    assert form_data['contact_phone'] == "555-1234"

    print("✓ Tab default values verified")

    # Clean up
    gui.close()
    print("✓ Tabs test completed successfully")


@pytest.mark.gui
@pytest.mark.tk
def test_tkinter_custom_buttons() -> None:
    """Test tkinter backend with custom buttons."""
    print("Testing tkinter Custom Buttons")
    print("==============================")

    set_backend('tk')
    from vibegui import GuiBuilder

    # Config with custom buttons
    config = {
        "window": {
            "title": "Custom Buttons Test",
            "width": 400,
            "height": 300
        },
        "fields": [
            {
                "name": "test_field",
                "type": "text",
                "label": "Test Field",
                "default_value": "test"
            }
        ],
        "custom_buttons": [
            {
                "name": "clear_button",
                "label": "Clear All",
                "tooltip": "Clear all fields"
            },
            {
                "name": "preset_button",
                "label": "Load Preset",
                "tooltip": "Load preset values"
            }
        ]
    }

    # Track button clicks
    button_clicks = []

    def custom_button_handler(button_config: dict, form_data: dict) -> None:
        button_clicks.append(button_config.name)
        print(f"Custom button clicked: {button_config.name} with data: {form_data}")

    # Create GUI builder
    gui = GuiBuilder(config_dict=config)
    gui.set_custom_button_callback('clear_button', custom_button_handler)
    gui.set_custom_button_callback('preset_button', custom_button_handler)

    print("✓ Created GUI with custom buttons")

    # Show the GUI to build widgets (but don't run the event loop)
    gui.show()

    # Test that the GUI was created without errors
    form_data = gui.get_form_data()
    assert 'test_field' in form_data
    assert form_data['test_field'] == "test"

    print("✓ Custom buttons test setup completed")

    # Clean up
    gui.close()
    print("✓ Custom buttons test completed successfully")


@pytest.mark.gui
@pytest.mark.tk
def test_tkinter_unified_interface() -> None:
    """Test tkinter backend through the unified GuiBuilder interface."""
    print("Testing tkinter Unified Interface")
    print("=================================")

    # Force tkinter backend
    set_backend('tk')
    from vibegui import GuiBuilder

    # Simple config
    config = {
        "window": {
            "title": "Unified Interface Test",
            "width": 500,
            "height": 400
        },
        "layout": "form",
        "fields": [
            {
                "name": "unified_test",
                "type": "text",
                "label": "Unified Test Field",
                "default_value": "Testing unified interface"
            },
            {
                "name": "backend_name",
                "type": "text",
                "label": "Backend",
                "default_value": "tkinter"
            }
        ]
    }

    # Test that unified GuiBuilder uses tkinter backend
    gui = GuiBuilder(config_dict=config)
    assert gui.backend == 'tk', f"Expected tk backend, got {gui.backend}"

    # Show the GUI to build widgets (but don't run the event loop)
    gui.show()

    # Test form operations
    form_data = gui.get_form_data()
    assert form_data['unified_test'] == "Testing unified interface"
    assert form_data['backend_name'] == "tkinter"

    # Test field modification
    gui.set_field_value('unified_test', 'Modified through unified interface')
    updated_data = gui.get_form_data()
    assert updated_data['unified_test'] == 'Modified through unified interface'

    print("✓ Unified interface using tkinter backend")
    print("✓ Form data operations working")
    print("✓ Field modifications working")

    # Clean up
    gui.close()
    print("✓ Unified interface test completed successfully")
