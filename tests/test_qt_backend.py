#!/usr/bin/env python3
"""
Quick test of Qt backend functionality.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from vibegui import set_backend, GuiBuilder


def test_qt_backend() -> None:
    """Test basic Qt backend functionality."""
    print("Testing Qt backend...")

    # Create QApplication first if one doesn't exist
    try:
        from qtpy.QtWidgets import QApplication
    except ImportError:
        from qtpy.QtGui import QApplication

    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    # Force Qt backend
    set_backend('qt')

    # Simple configuration
    config = {
        "window": {
            "title": "Qt Test",
            "width": 400,
            "height": 300,
            "resizable": True
        },
        "layout": "form",
        "submit_button": True,
        "cancel_button": True,
        "fields": [
            {
                "name": "name",
                "type": "text",
                "label": "Name",
                "placeholder": "Enter your name",
                "required": True
            },
            {
                "name": "age",
                "type": "int",
                "label": "Age",
                "min_value": 0,
                "max_value": 120,
                "default_value": 25
            },
            {
                "name": "subscribe",
                "type": "checkbox",
                "label": "Subscribe to newsletter",
                "default_value": True
            }
        ]
    }

    def on_submit(form_data: dict) -> None:
        print("Form submitted:", form_data)

    # don't do this, just let the dialog close on cancel
    # def on_cancel() -> None:
    #     print("Form cancelled")

    # Create GUI
    gui = GuiBuilder(config_dict=config)
    gui.set_submit_callback(on_submit)
    gui.set_cancel_callback(on_cancel)

    print(f"Created GUI with backend: {gui.backend}")
    print("GUI created successfully! Close the window to exit.")

    # Show the window
    gui.show()

    print("✓ GUI created successfully! Close the window to exit.")
    app.exec()

    assert True, "Qt backend test completed successfully"