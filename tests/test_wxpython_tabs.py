#!/usr/bin/env python3
"""
Test wxPython backend with tabbed interface to verify field expansion.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_wxpython_tabs() -> None:
    """Test wxPython backend with tabs to ensure fields expand properly."""
    print("Testing wxPython backend with tabs...")

    try:
        # Force wxPython backend
        from vibegui import set_backend
        set_backend('wx')
        print("✓ wxPython backend selected")

        import wx
        from vibegui import WxGuiBuilder

        # Create configuration with tabs
        config = {
            "window": {
                "title": "wxPython Tabs Field Expansion Test",
                "width": 700,
                "height": 500,
                "resizable": True
            },
            "use_tabs": True,
            "submit_button": True,
            "cancel_button": True,
            "submit_label": "Save All",
            "cancel_label": "Cancel",
            "fields": [
                # Personal Info fields
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
                    "max_value": 120,
                    "default_value": 30
                },
                {
                    "name": "bio",
                    "type": "textarea",
                    "label": "Biography",
                    "placeholder": "Tell us about yourself...",
                    "height": 100
                },
                # Preferences fields
                {
                    "name": "theme",
                    "type": "select",
                    "label": "Preferred Theme",
                    "options": ["Light", "Dark", "Auto"],
                    "default_value": "Auto"
                },
                {
                    "name": "notifications",
                    "type": "checkbox",
                    "label": "Enable notifications",
                    "default_value": True
                },
                {
                    "name": "language",
                    "type": "radio",
                    "label": "Language",
                    "options": ["English", "Spanish", "French"],
                    "default_value": "English"
                },
                {
                    "name": "salary",
                    "type": "float",
                    "label": "Expected Salary",
                    "format_string": ".2f",
                    "min_value": 0.0,
                    "default_value": 50000.0
                },
                # Schedule fields
                {
                    "name": "start_date",
                    "type": "date",
                    "label": "Start Date",
                    "default_value": "2025-01-01"
                },
                {
                    "name": "work_hours",
                    "type": "time",
                    "label": "Preferred Work Start Time",
                    "default_value": "09:00"
                },
                {
                    "name": "availability",
                    "type": "select",
                    "label": "Availability",
                    "options": ["Full-time", "Part-time", "Contract", "Flexible"],
                    "default_value": "Full-time"
                },
                {
                    "name": "overtime",
                    "type": "checkbox",
                    "label": "Available for overtime",
                    "default_value": False
                }
            ],
            "tabs": [
                {
                    "name": "personal",
                    "title": "Personal Info",
                    "layout": "form",
                    "fields": ["first_name", "last_name", "email", "age", "bio"],
                    "tooltip": "Enter your personal information"
                },
                {
                    "name": "preferences",
                    "title": "Preferences",
                    "layout": "form",
                    "fields": ["theme", "notifications", "language", "salary"],
                    "tooltip": "Set your preferences"
                },
                {
                    "name": "schedule",
                    "title": "Schedule",
                    "layout": "form",
                    "fields": ["start_date", "work_hours", "availability", "overtime"],
                    "tooltip": "Schedule information"
                }
            ]
        }

        # Create wxPython application
        try:
            from .wx_test_utils import create_wx_app
        except ImportError:
            from wx_test_utils import create_wx_app
        app = create_wx_app()

        # Create GUI builder with wxPython backend
        gui_builder = WxGuiBuilder(config_dict=config)

        # Set up callbacks
        def on_submit(form_data: dict) -> None:
            print("wxPython tabs form submitted:")
            for key, value in form_data.items():
                print(f"  {key}: {value}")
            wx.MessageBox("Tabbed form submitted successfully!", "Success", wx.OK | wx.ICON_INFORMATION)

        def on_cancel() -> None:
            print("wxPython tabs form cancelled")
            wx.MessageBox("Form cancelled by user", "Cancelled", wx.OK | wx.ICON_INFORMATION)

        # Register callbacks
        gui_builder.set_submit_callback(on_submit)
        gui_builder.set_cancel_callback(on_cancel)

        # Show the GUI
        gui_builder.Show()

        print("✓ wxPython tabbed GUI created and shown")
        print("  Note: Verify that fields in each tab expand to fill the window width")

        # Use the utility function to handle pytest vs direct execution
        try:
            from .wx_test_utils import run_wx_gui_for_test
        except ImportError:
            from wx_test_utils import run_wx_gui_for_test

        run_wx_gui_for_test(app, gui_builder)

    except ImportError as e:
        print(f"✗ wxPython not available: {e}")
    except Exception as e:
        print(f"✗ Error with wxPython tabs backend: {e}")
        import traceback
        traceback.print_exc()
