#!/usr/bin/env python3
"""
Test script for wxPython backend tabs to verify field expansion.
"""

import sys
import os

# Handle imports for both direct execution and pytest
try:
    from . import wx_test_utils
except ImportError:
    import wx_test_utils

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_wx_tabs() -> None:
    """Test wxPython backend with tabs to verify field expansion."""
    print("Testing wxPython Backend with Tabs...")

    # Force wxPython backend
    from vibegui import set_backend
    set_backend('wx')
    print("✓ wxPython backend selected")

    # Import wxPython
    import wx

    # Use the existing tabbed configuration file
    config_path = os.path.join(os.path.dirname(__file__), "..", "examples", "tabbed_config.json")
    if not os.path.exists(config_path):
        print(f"✗ Configuration file not found: {config_path}")
        assert False, "Configuration file not found"

    # Create wxPython application
    try:
        from .wx_test_utils import create_wx_app
    except ImportError:
        from wx_test_utils import create_wx_app
    app = create_wx_app()

    # Create GUI builder with wxPython backend using the config file
    from vibegui import WxGuiBuilder
    gui_builder = WxGuiBuilder(config_path=config_path)

    # Set up callbacks
    def on_submit(form_data: dict) -> None:
        try:
            print("wxPython tabs form submitted:")
            print("="*50)
            for key, value in form_data.items():
                print(f"  {key}: {value}")
            print("="*50)
            wx.MessageBox("Configuration saved successfully!\n\nCheck the console for submitted data.",
                            "Success", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            print(f"Error in submit callback: {e}")
            wx.MessageBox(f"Error saving configuration: {e}",
                            "Error", wx.OK | wx.ICON_ERROR)

    def on_cancel() -> None:
        print("wxPython tabs form cancelled")
        wx.MessageBox("Configuration cancelled by user", "Cancelled", wx.OK | wx.ICON_INFORMATION)

    def load_defaults(_form_data: dict) -> None:
        """Load default configuration values."""
        defaults = {
            "app_name": "My Demo Application",
            "version": "2.0.0",
            "author": "Demo User",
            "description": "This is a demo application for testing field expansion in tabs.",
            "debug_mode": True,
            "log_level": "DEBUG",
            "max_connections": 200,
            "timeout": 60,
            "database_url": "postgres://demo:password@localhost:5432/demo_db",
            "api_key": "demo_api_key_12345",
            "theme": "Dark",
            "accent_color": "#FF5722",
            "font_size": 16,
            "backup_enabled": True,
            "backup_location": "/home/user/backups",
            "backup_interval": 12,
            "email_notifications": True,
            "notification_email": "demo@example.com"
        }
        gui_builder.set_form_data(defaults)
        print("Default values loaded")
        wx.MessageBox("Default configuration values loaded successfully!",
                        "Defaults Loaded", wx.OK | wx.ICON_INFORMATION)

    def clear_all(_form_data: dict) -> None:
        """Clear all form fields."""
        result = wx.MessageBox("Are you sure you want to clear all fields?",
                                "Confirm Clear", wx.YES_NO | wx.ICON_QUESTION)
        if result == wx.YES:
            gui_builder.clear_form()
            print("All fields cleared")
            wx.MessageBox("All form fields have been cleared.",
                            "Cleared", wx.OK | wx.ICON_INFORMATION)

    # Register callbacks
    gui_builder.set_submit_callback(on_submit)
    gui_builder.set_cancel_callback(on_cancel)

    # Only register custom button callbacks if the buttons exist
    custom_button_names = gui_builder.get_custom_button_names()
    if "load_defaults" in custom_button_names:
        gui_builder.set_custom_button_callback("load_defaults", load_defaults)
    if "clear_all" in custom_button_names:
        gui_builder.set_custom_button_callback("clear_all", clear_all)

    # Show the GUI
    gui_builder.Show()

    print("✓ wxPython tabbed GUI created and shown")
    print("  - Custom buttons available:", custom_button_names)
    print("\nInstructions:")
    print("  1. Resize the window to test field expansion")
    print("  2. Switch between tabs to verify all fields expand properly")
    if custom_button_names:
        print("  3. Try the custom buttons if available")
    print("  4. Submit to see the form data structure")

    # Run appropriately for test environment
    wx_test_utils.run_wx_gui_for_test(app, gui_builder)

