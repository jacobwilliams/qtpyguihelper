#!/usr/bin/env python3
"""
Demo script to showcase float field functionality with format enforcement.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from qtpyguihelper.qt.gui_builder import GuiBuilder


def demo_float_fields():
    """Demo float fields with various format specifications."""
    config = {
        "window": {
            "title": "Float Fields Demo",
            "width": 500,
            "height": 600
        },
        "layout": "form",
        "fields": [
            {
                "name": "basic_float",
                "type": "float",
                "label": "Basic Float",
                "default_value": 3.14159,
                "tooltip": "A basic float field with default 2 decimal places"
            },
            {
                "name": "currency",
                "type": "float",
                "label": "Price ($)",
                "min_value": 0.0,
                "max_value": 10000.0,
                "decimals": 2,
                "format_string": ".2f",
                "default_value": 99.99,
                "tooltip": "Currency field with 2 decimal places"
            },
            {
                "name": "percentage",
                "type": "float",
                "label": "Percentage (%)",
                "min_value": 0.0,
                "max_value": 100.0,
                "decimals": 1,
                "format_string": ".1f",
                "default_value": 85.5,
                "tooltip": "Percentage with 1 decimal place"
            },
            {
                "name": "precision",
                "type": "float",
                "label": "High Precision",
                "decimals": 4,
                "format_string": ".4f",
                "default_value": 0.0001,
                "tooltip": "High precision with 4 decimal places"
            },
            {
                "name": "scientific",
                "type": "float",
                "label": "Scientific Value",
                "min_value": 0.000001,
                "max_value": 999999.0,
                "decimals": 6,
                "format_string": ".6e",
                "default_value": 0.000123,
                "tooltip": "Scientific notation style with 6 decimal places"
            },
            {
                "name": "temperature",
                "type": "float",
                "label": "Temperature (°C)",
                "min_value": -273.15,
                "max_value": 1000.0,
                "decimals": 1,
                "format_string": ".1f",
                "default_value": 20.5,
                "tooltip": "Temperature in Celsius"
            }
        ],
        "submit_button": True,
        "submit_label": "Show Values",
        "cancel_button": True
    }

    def handle_submit(form_data):
        """Handle form submission and show the values with their formats."""
        result_text = "Float Field Values:\n" + "="*30 + "\n"

        for field_name, value in form_data.items():
            if field_name != "_metadata":
                result_text += f"{field_name}: {value} (type: {type(value).__name__})\n"

        # Show the values
        from qtpy.QtWidgets import QMessageBox
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Float Field Values")
        msg.setText(result_text)
        msg.exec_()

    # Build and show the GUI
    builder = GuiBuilder(config_dict=config)

    # Connect submit handler
    builder.set_submit_callback(handle_submit)

    builder.show()
    return builder


def main():
    """Run the float fields demo."""
    from qtpy.QtWidgets import QApplication

    app = QApplication(sys.argv)

    print("QtPyGuiHelper Float Fields Demo")
    print("=" * 40)
    print("This demo showcases float fields with:")
    print("• Different decimal precisions")
    print("• Format string enforcement")
    print("• Range validation")
    print("• Various use cases (currency, percentage, scientific)")
    print("\nClick 'Show Values' to see the current float values.")
    print("=" * 40)

    window = demo_float_fields()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
