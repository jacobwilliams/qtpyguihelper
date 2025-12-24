#!/usr/bin/env python3
"""
Simple example showing basic vibegui usage.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from vibegui import GuiBuilder
    from qtpy.QtWidgets import QApplication, QMessageBox

    def on_form_submit(form_data: dict) -> None:
        """Handle form submission."""
        print("Form submitted with data:")
        for key, value in form_data.items():
            print(f"  {key}: {value}")

        # Show success message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Success")
        msg.setText(f"Hello {form_data.get('name', 'User')}!\nForm submitted successfully.")
        msg.exec()

    def main() -> None:
        """Create and run a simple form."""
        # Simple configuration
        config = {
            "window": {
                "title": "Simple Example",
                "width": 400,
                "height": 250
            },
            "layout": "form",
            "fields": [
                {
                    "name": "name",
                    "type": "text",
                    "label": "Your Name",
                    "required": True,
                    "placeholder": "Enter your name"
                },
                {
                    "name": "email",
                    "type": "email",
                    "label": "Email",
                    "placeholder": "your@email.com"
                },
                {
                    "name": "age",
                    "type": "number",
                    "label": "Age",
                    "min_value": 1,
                    "max_value": 120
                },
                {
                    "name": "subscribe",
                    "type": "checkbox",
                    "label": "Subscribe to updates"
                }
            ],
            "submit_button": True,
            "submit_label": "Submit",
            "cancel_button": True
        }

        # Create application
        app = QApplication(sys.argv)

        # Create GUI
        gui = GuiBuilder(config_dict=config)
        gui.set_submit_callback(on_form_submit)

        # Show GUI
        gui.show()

        # Run application
        app.exec()

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"Import error: {e}")
    print("Make sure you have a Qt binding installed: PySide6 (or PyQt6) and qtpy")
