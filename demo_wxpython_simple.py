#!/usr/bin/env python3
"""
Simple wxPython demo showing a working GUI with QtPyGuiHelper.
This demonstrates that the wxPython backend works correctly.
"""

import sys
import os

# Suppress common wxPython warnings on macOS
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="wx")

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

try:
    import wx
    # Suppress OpenGL framebuffer warnings
    if hasattr(wx, 'Log'):
        wx.Log.SetLogLevel(wx.LOG_Warning)
except ImportError:
    print("wxPython is not installed. Please install it with: pip install wxpython")
    sys.exit(1)

from qtpyguihelper import GuiBuilder, set_backend


def on_submit(form_data):
    """Handle form submission."""
    print("\n=== Form Submitted ===")
    for key, value in form_data.items():
        print(f"{key}: {value}")
    print("=====================\n")
    
    # Show a simple message dialog
    try:
        import wx as wx_local
        app = wx_local.GetApp()
        if app:
            wx_local.MessageBox(f"Form submitted successfully!\nName: {form_data.get('name', 'Unknown')}", 
                               "Success", wx_local.OK | wx_local.ICON_INFORMATION)
    except (AttributeError, ImportError, RuntimeError):
        pass


def on_cancel():
    """Handle form cancellation."""
    print("Form cancelled by user")


def create_simple_config():
    """Create a simple form configuration for testing."""
    return {
        "window": {
            "title": "wxPython Demo - QtPyGuiHelper",
            "width": 500,
            "height": 400,
            "resizable": True
        },
        "layout": "form",
        "submit_button": True,
        "cancel_button": True,
        "submit_label": "Submit",
        "cancel_label": "Cancel",
        "fields": [
            {
                "name": "name",
                "type": "text",
                "label": "Full Name",
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
                "name": "email",
                "type": "email",
                "label": "Email",
                "placeholder": "your.email@example.com"
            },
            {
                "name": "subscribe",
                "type": "checkbox",
                "label": "Subscribe to newsletter",
                "default_value": True
            },
            {
                "name": "priority",
                "type": "select",
                "label": "Priority",
                "options": ["Low", "Medium", "High"],
                "default_value": "Medium"
            },
            {
                "name": "notes",
                "type": "textarea",
                "label": "Notes",
                "placeholder": "Enter any additional notes...",
                "height": 60
            }
        ]
    }


def main():
    """Main function to run the wxPython demo."""
    print("QtPyGuiHelper wxPython Demo")
    print("===========================")
    
    try:
        # Force wxPython backend
        set_backend('wx')
        print("✓ wxPython backend selected")
        
        # Create the GUI configuration
        config = create_simple_config()
        
        # Create the GUI builder
        gui_builder = GuiBuilder(config_dict=config)
        print("✓ GUI builder created")
        
        # Set callbacks
        gui_builder.set_submit_callback(on_submit)
        gui_builder.set_cancel_callback(on_cancel)
        print("✓ Callbacks set")
        
        # Show the window
        print("✓ Showing window...")
        gui_builder.show()
        
        # Start the wxPython event loop
        print("✓ Starting wxPython application...")
        
        app = wx.GetApp()  # type: ignore
        if not app:
            app = wx.App()  # type: ignore
        
        print("\n=== GUI is now running ===")
        print("Fill out the form and click Submit to test functionality")
        print("Close the window or click Cancel to exit")
        print("==========================")
        
        app.MainLoop()  # type: ignore
        
    except (ImportError, RuntimeError, AttributeError) as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n✓ Demo completed successfully!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
