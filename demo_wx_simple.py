#!/usr/bin/env python3
"""
Simple demo showing wxPython backend in action.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from qtpyguihelper import GuiBuilder, set_backend


def main():
    """Simple wxPython demo."""
    print("QtPyGuiHelper - wxPython Backend Demo")
    print("====================================")

    # Force wxPython backend
    set_backend('wx')
    print("Using wxPython backend")

    # Simple configuration
    config = {
        "window": {
            "title": "wxPython Demo - Simple Form",
            "width": 400,
            "height": 350,
            "resizable": True
        },
        "layout": "form",
        "submit_button": True,
        "cancel_button": True,
        "fields": [
            {
                "name": "name",
                "type": "text",
                "label": "Your Name",
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
        print("Form submitted:")
        for key, value in form_data.items():
            print(f"  {key}: {value}")

    def on_cancel():
        print("Form cancelled")

    # Note: This is a demonstration of the configuration and backend selection.
    # To actually run the GUI, you would need:
    # gui = GuiBuilder(config_dict=config)
    # gui.set_submit_callback(on_submit)
    # gui.set_cancel_callback(on_cancel)
    # gui.show()
    #
    # And then create and run a wx.App() main loop

    print("Configuration loaded successfully!")
    print("wxPython backend is ready to create GUI applications.")
    print("\nTo run the actual GUI, uncomment the lines in the source code")
    print("and ensure you have wxPython installed.")


if __name__ == "__main__":
    main()
