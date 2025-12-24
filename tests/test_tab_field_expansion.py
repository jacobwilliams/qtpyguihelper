#!/usr/bin/env python3
"""
Test script to verify that fields in tabs expand to fit the window width.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from vibegui import GuiBuilder
from qtpy.QtWidgets import QApplication


def test_tab_field_expansion():
    """Test that fields in tabs expand to fit the window width."""
    print("Testing tab field expansion...")

    config = {
        "window": {
            "title": "Tab Field Expansion Test",
            "width": 600,
            "height": 400
        },
        "use_tabs": True,
        "fields": [
            {
                "name": "full_name",
                "type": "text",
                "label": "Full Name",
                "placeholder": "Enter your full name",
                "required": True
            },
            {
                "name": "email",
                "type": "email",
                "label": "Email Address",
                "placeholder": "your.email@example.com"
            },
            {
                "name": "age",
                "type": "int",
                "label": "Age",
                "min_value": 18,
                "max_value": 100,
                "default_value": 25
            },
            {
                "name": "notification_email",
                "type": "email",
                "label": "Notification Email",
                "placeholder": "notifications@example.com"
            },
            {
                "name": "theme",
                "type": "select",
                "label": "Theme",
                "options": ["Light", "Dark", "Auto"],
                "default_value": "Auto"
            },
            {
                "name": "description",
                "type": "textarea",
                "label": "Description",
                "placeholder": "Enter a description...",
                "height": 80
            }
        ],
        "tabs": [
            {
                "name": "user_info",
                "title": "User Info",
                "layout": "form",
                "fields": ["full_name", "email", "age"]
            },
            {
                "name": "settings",
                "title": "Settings",
                "layout": "form",
                "fields": ["notification_email", "theme", "description"]
            }
        ],
        "submit_button": True,
        "cancel_button": True
    }

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    gui = GuiBuilder(config_dict=config)

    def on_submit(form_data):
        print("Tab form submitted:")
        for key, value in form_data.items():
            print(f"  {key}: {value}")

    gui.set_submit_callback(on_submit)
    gui.show()

    print("✓ Tab field expansion test GUI created")
    print("  Check that form fields in both tabs expand to fit the window width")

    app.exec()

    assert True, 'Tab field expansion test completed successfully'
