#!/usr/bin/env python3
"""
Quick test of wxPython backend functionality.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from qtpyguihelper import set_backend, GuiBuilder


def test_wx_backend():
    """Test basic wxPython backend functionality."""
    print("Testing wxPython backend...")
    
    # Force wxPython backend
    set_backend('wx')
    
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
    
    def on_submit(form_data):
        print("Form submitted:", form_data)
    
    def on_cancel():
        print("Form cancelled")
    
    # Create GUI
    gui = GuiBuilder(config_dict=config)
    gui.set_submit_callback(on_submit)
    gui.set_cancel_callback(on_cancel)
    
    print(f"Created GUI with backend: {gui.backend}")
    print("GUI created successfully! Close the window to exit.")
    
    # Show the window
    gui.show()
    
    # Run the application
    import wx
    if wx.App.Get() is None:
        app = wx.App()
        app.MainLoop()


if __name__ == "__main__":
    test_wx_backend()
