#!/usr/bin/env python3
"""
Test script for wxPython backend tabs using the correct configuration structure.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_wx_tabs_simple() -> None:
    """Test wxPython backend with tabs using the correct configuration structure."""
    print("Testing wxPython Backend with Tabs (Correct Structure)...")

    try:
        # Force wxPython backend
        from vibegui import set_backend
        set_backend('wx')
        print("✓ wxPython backend selected")

        # Import wxPython
        import wx

        # Use the same configuration structure as tabbed_config.json
        config = {
            "window": {
                "title": "wxPython Tabs Field Expansion Test",
                "width": 700,
                "height": 500,
                "resizable": True
            },
            "use_tabs": True,
            "fields": [
                {
                    "name": "first_name",
                    "type": "text",
                    "label": "First Name",
                    "placeholder": "Enter your first name",
                    "required": True
                },
                {
                    "name": "last_name",
                    "type": "text",
                    "label": "Last Name",
                    "placeholder": "Enter your last name",
                    "required": True
                },
                {
                    "name": "email",
                    "type": "email",
                    "label": "Email Address",
                    "placeholder": "your.email@example.com",
                    "required": True
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
                    "name": "theme",
                    "type": "select",
                    "label": "Theme",
                    "options": ["Light", "Dark", "Auto"],
                    "default_value": "Light"
                },
                {
                    "name": "notifications",
                    "type": "checkbox",
                    "label": "Enable notifications",
                    "default_value": True
                },
                {
                    "name": "language",
                    "type": "select",
                    "label": "Language",
                    "options": ["English", "Spanish", "French", "German"],
                    "default_value": "English"
                },
                {
                    "name": "font_size",
                    "type": "int",
                    "label": "Font Size",
                    "min_value": 8,
                    "max_value": 24,
                    "default_value": 12
                }
            ],
            "tabs": [
                {
                    "name": "personal",
                    "title": "Personal Info",
                    "layout": "form",
                    "fields": ["first_name", "last_name", "email", "age"],
                    "tooltip": "Personal information fields"
                },
                {
                    "name": "preferences",
                    "title": "Preferences",
                    "layout": "form",
                    "fields": ["theme", "notifications", "language", "font_size"],
                    "tooltip": "User preferences"
                }
            ],
            "submit_button": True,
            "cancel_button": True
        }

        # Create wxPython application
        from .wx_test_utils import create_wx_app
        app = create_wx_app()

        # Create GUI builder with wxPython backend
        from vibegui import WxGuiBuilder
        gui_builder = WxGuiBuilder(config_dict=config)

        # Set up callbacks
        def on_submit(form_data: dict) -> None:
            print("wxPython tabs form submitted:")
            for key, value in form_data.items():
                print(f"  {key}: {value}")
            wx.MessageBox("Form submitted successfully! Check console for data.", "Success", wx.OK | wx.ICON_INFORMATION)

        def on_cancel() -> None:
            print("wxPython tabs form cancelled")
            wx.MessageBox("Form cancelled by user", "Cancelled", wx.OK | wx.ICON_INFORMATION)

        # Register callbacks
        gui_builder.set_submit_callback(on_submit)
        gui_builder.set_cancel_callback(on_cancel)

        # Show the GUI
        gui_builder.Show()

        print("✓ wxPython tabs GUI created and shown")
        print("  - Notice how fields expand to fit the tab width")
        print("  - Switch between tabs to see field expansion in each")

        # Use the utility function to handle pytest vs direct execution
        try:
            from .wx_test_utils import run_wx_gui_for_test
        except ImportError:
            from wx_test_utils import run_wx_gui_for_test

        run_wx_gui_for_test(app, gui_builder)

    except ImportError as e:
        print(f"✗ wxPython not available: {e}")
    except Exception as e:
        print(f"✗ Error with wxPython tabs: {e}")
        import traceback
        traceback.print_exc()
