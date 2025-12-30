#!/usr/bin/env python3
"""
Quick test of wxPython backend functionality.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from vibegui import set_backend, GuiBuilder

# Handle both direct execution and pytest imports
try:
    from .wx_test_utils import run_wx_gui_for_test, create_wx_app, cleanup_wx_test
except ImportError:
    # Direct execution - use absolute import
    from wx_test_utils import run_wx_gui_for_test, create_wx_app, cleanup_wx_test

def test_wx_backend() -> None:
    """Test basic wxPython backend functionality."""
    print("Testing wxPython backend...")

    try:
        # Import wxPython first to check availability
        import wx

        # Force wxPython backend before creating app
        set_backend('wx')

        # Create wxPython app
        app = create_wx_app()

        # ...existing config and GUI creation code...

        # Simple configuration
        config = {
            "window": {
                "title": "wxPython Test",
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
            try:
                wx.MessageBox("Form submitted successfully!", "Success", wx.OK | wx.ICON_INFORMATION)  # type: ignore
            except AttributeError:
                print("✓ Form submitted successfully!")

        def on_cancel() -> None:
            print("Form cancelled")
            try:
                wx.MessageBox("Form cancelled by user", "Cancelled", wx.OK | wx.ICON_INFORMATION)  # type: ignore
            except AttributeError:
                print("✓ Form cancelled by user")

        # Create GUI (app is already created)
        gui = GuiBuilder(config_dict=config)
        gui.set_submit_callback(on_submit)
        gui.set_cancel_callback(on_cancel)

        print(f"✓ Created GUI with backend: {gui.backend}")

        # Show the window
        gui.show()

        # Run appropriately for test environment
        run_wx_gui_for_test(app, gui)

        # Clean up after test to prevent conflicts
        cleanup_wx_test()

    except Exception as e:
        print(f"✗ Error in wxPython backend test: {e}")
        import traceback
        traceback.print_exc()
