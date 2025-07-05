#!/usr/bin/env python3
"""
Demo script showing how to use the QtPyGuiHelper library.
"""

import sys
import os
import json
from pathlib import Path

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from qtpyguihelper import GuiBuilder
from qtpy.QtWidgets import QApplication, QMessageBox


def on_registration_submit(form_data):
    """Callback function for registration form submission."""
    print("Registration form submitted with data:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")

    # Show a success message
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Registration Successful")
    msg.setText(f"Welcome, {form_data.get('first_name', 'User')}!\nYour registration has been processed.")
    msg.exec()


def on_settings_submit(form_data):
    """Callback function for settings form submission."""
    print("Settings saved:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")


def on_cancel():
    """Callback function for form cancellation."""
    print("Form cancelled by user")


def demo_user_registration():
    """Demo the user registration form."""
    print("Starting User Registration Demo...")

    # Create the application
    app = QApplication(sys.argv)

    # Create GUI from JSON file
    config_path = os.path.join(os.path.dirname(__file__), "examples", "user_registration.json")
    gui = GuiBuilder(config_path=config_path)

    # Set callbacks
    gui.set_submit_callback(on_registration_submit)
    gui.set_cancel_callback(on_cancel)

    # Show the GUI
    gui.show()

    # Run the application
    app.exec()


def demo_settings_form():
    """Demo the settings form."""
    print("Starting Settings Form Demo...")

    # Create the application
    app = QApplication(sys.argv)

    # Create GUI from JSON file
    config_path = os.path.join(os.path.dirname(__file__), "examples", "settings_form.json")
    gui = GuiBuilder(config_path=config_path)

    # Set callbacks
    gui.set_submit_callback(on_settings_submit)

    # Show the GUI
    gui.show()

    # Run the application
    app.exec()


def demo_project_form():
    """Demo the project form."""
    print("Starting Project Form Demo...")

    # Create the application
    app = QApplication(sys.argv)

    # Create GUI from JSON file
    config_path = os.path.join(os.path.dirname(__file__), "examples", "project_form.json")
    gui = GuiBuilder(config_path=config_path)

    # Set callbacks
    gui.set_submit_callback(lambda data: print(f"Project saved: {data}"))

    # Show the GUI
    gui.show()

    # Run the application
    app.exec()


def demo_programmatic_config():
    """Demo creating a GUI from a programmatic configuration."""
    print("Starting Programmatic Configuration Demo...")

    # Define configuration as a dictionary
    config = {
        "window": {
            "title": "Contact Form",
            "width": 400,
            "height": 300
        },
        "layout": "form",
        "fields": [
            {
                "name": "name",
                "type": "text",
                "label": "Full Name",
                "required": True,
                "placeholder": "Enter your full name"
            },
            {
                "name": "email",
                "type": "email",
                "label": "Email",
                "required": True
            },
            {
                "name": "phone",
                "type": "text",
                "label": "Phone Number",
                "placeholder": "(555) 123-4567"
            },
            {
                "name": "message",
                "type": "textarea",
                "label": "Message",
                "required": True,
                "placeholder": "Enter your message here...",
                "height": 100
            },
            {
                "name": "urgent",
                "type": "checkbox",
                "label": "This is urgent"
            }
        ],
        "submit_button": True,
        "submit_label": "Send Message",
        "cancel_button": True
    }

    # Create the application
    app = QApplication(sys.argv)

    # Create GUI from dictionary
    gui = GuiBuilder(config_dict=config)

    # Set callbacks
    def on_contact_submit(form_data):
        print("Contact form submitted:")
        for key, value in form_data.items():
            print(f"  {key}: {value}")

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Message Sent")
        msg.setText("Your message has been sent successfully!")
        msg.exec()

    gui.set_submit_callback(on_contact_submit)

    # Connect to field change events
    def on_field_change(field_name, value):
        print(f"Field '{field_name}' changed to: {value}")

    gui.fieldChanged.connect(on_field_change)

    # Show the GUI
    gui.show()

    # Run the application
    app.exec()


def demo_data_persistence():
    """Demo data loading and saving functionality."""
    print("Starting Data Persistence Demo...")

    # Create the application
    app = QApplication(sys.argv)

    # Create GUI from JSON file
    config_path = os.path.join(os.path.dirname(__file__), "examples", "project_form.json")
    gui = GuiBuilder(config_path=config_path)

    # Load existing data if available
    data_path = os.path.join(os.path.dirname(__file__), "examples", "project_data.json")
    if os.path.exists(data_path):
        success = gui.load_data_from_file(data_path)
        if success:
            print(f"Loaded existing data from {data_path}")
        else:
            print("Failed to load existing data")

    # Set up save functionality
    def on_submit_and_save(form_data):
        print("Project data submitted:")
        for key, value in form_data.items():
            print(f"  {key}: {value}")

        # Save to output file
        output_path = os.path.join(os.path.dirname(__file__), "project_output.json")
        success = gui.save_data_to_file(output_path)
        if success:
            print(f"Data saved to {output_path}")

        # Also save with metadata
        metadata_path = os.path.join(os.path.dirname(__file__), "project_output_with_metadata.json")
        success = gui.save_data_with_metadata_to_file(metadata_path)
        if success:
            print(f"Data with metadata saved to {metadata_path}")

        # Show success message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Data Saved")
        msg.setText(f"Project data has been saved successfully!\nOutput: {output_path}")
        msg.exec()

    gui.set_submit_callback(on_submit_and_save)

    # Show the GUI
    gui.show()

    # Run the application
    app.exec()


def demo_tabbed_interface():
    """Demo the tabbed interface functionality."""
    print("Starting Tabbed Interface Demo...")

    # Create the application
    app = QApplication(sys.argv)

    # Create GUI from JSON file
    config_path = os.path.join(os.path.dirname(__file__), "examples", "simple_tabs.json")
    gui = GuiBuilder(config_path=config_path)

    # Set callbacks
    def on_submit_tabs(form_data):
        print("Tabbed form submitted:")
        for key, value in form_data.items():
            print(f"  {key}: {value}")

        # Show success message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Form Submitted")
        msg.setText("Tabbed form data has been submitted successfully!")
        msg.exec()

    gui.set_submit_callback(on_submit_tabs)

    # Show the GUI
    gui.show()

    # Run the application
    app.exec()


def demo_complex_tabs():
    """Demo a complex tabbed configuration interface."""
    print("Starting Complex Tabbed Configuration Demo...")

    # Create the application
    app = QApplication(sys.argv)

    # Create GUI from JSON file
    config_path = os.path.join(os.path.dirname(__file__), "examples", "tabbed_config.json")
    gui = GuiBuilder(config_path=config_path)

    # Set callbacks
    def on_save_config(form_data):
        print("Configuration saved:")
        for key, value in form_data.items():
            print(f"  {key}: {value}")

        # Save to file
        output_path = os.path.join(os.path.dirname(__file__), "tabbed_config_output.json")
        success = gui.save_data_to_file(output_path)
        if success:
            print(f"Configuration saved to {output_path}")

        # Show success message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Configuration Saved")
        msg.setText(f"Configuration has been saved successfully!\nOutput: {output_path}")
        msg.exec()

    gui.set_submit_callback(on_save_config)

    # Show the GUI
    gui.show()

    # Run the application
    app.exec()


def demo_nested_fields():
    """Demo nested field names with dot notation."""
    print("Starting Nested Fields Demo...")

    # Create the application
    app = QApplication(sys.argv)

    # Create GUI from JSON file
    config_path = os.path.join(os.path.dirname(__file__), "examples", "nested_config.json")
    gui = GuiBuilder(config_path=config_path)

    # Load existing nested data if available
    data_path = os.path.join(os.path.dirname(__file__), "examples", "nested_data.json")
    if os.path.exists(data_path):
        success = gui.load_data_from_file(data_path)
        if success:
            print(f"Loaded existing nested data from {data_path}")
        else:
            print("Failed to load existing nested data")

    # Set callbacks
    def on_save_nested_config(form_data):
        print("Nested configuration saved:")
        # Print the nested structure
        def print_nested(data, indent=0):
            for key, value in data.items():
                if isinstance(value, dict):
                    print("  " * indent + f"{key}:")
                    print_nested(value, indent + 1)
                else:
                    print("  " * indent + f"{key}: {value}")

        print_nested(form_data)

        # Save to file
        output_path = os.path.join(os.path.dirname(__file__), "nested_config_output.json")
        success = gui.save_data_to_file(output_path)
        if success:
            print(f"Nested configuration saved to {output_path}")

        # Show success message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Nested Configuration Saved")
        msg.setText(f"Nested configuration has been saved successfully!\nOutput: {output_path}")
        msg.exec()

    gui.set_submit_callback(on_save_nested_config)

    # Show the GUI
    gui.show()

    # Run the application
    app.exec()


def demo_float_fields():
    """Demo float fields with various format specifications."""
    print("Starting Float Fields Demo...")

    # Create the application
    app = QApplication(sys.argv)

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
                "format_string": ".1f",
                "default_value": 85.5,
                "tooltip": "Percentage with 1 decimal place"
            },
            {
                "name": "precision",
                "type": "float",
                "label": "High Precision",
                "format_string": ".4f",
                "default_value": 0.0001,
                "tooltip": "High precision with 4 decimal places"
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
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Float Field Values")
        msg.setText(result_text)
        msg.exec_()

    # Create GUI from config dict
    gui = GuiBuilder(config_dict=config)
    gui.set_submit_callback(handle_submit)

    # Show the GUI
    gui.show()

    # Run the application
    app.exec()


def demo_format_strings():
    """Demo various format string specifications including scientific notation."""
    print("Starting Format Strings Demo...")

    # Create the application
    app = QApplication(sys.argv)

    # Load the format strings example
    config_path = os.path.join(os.path.dirname(__file__), "examples", "format_strings.json")
    gui = GuiBuilder(config_path=config_path)

    def handle_submit(form_data):
        """Handle form submission and show formatted values."""
        result_text = "Format String Examples:\n" + "="*50 + "\n"

        # Define format examples with explanations
        format_examples = {
            "fixed_point_2": (".2f", "Fixed-point, 2 decimals"),
            "fixed_point_4": (".4f", "Fixed-point, 4 decimals"),
            "scientific_2": (".2e", "Scientific notation, 2 decimals"),
            "scientific_3": (".3E", "Scientific notation, 3 decimals (uppercase)"),
            "general_format": (".3g", "General format (auto fixed/scientific)"),
            "percentage": (".1%", "Percentage format"),
            "currency": (",.2f", "Currency with thousands separator"),
            "no_decimals": (".0f", "Whole numbers only")
        }

        for field_name, value in form_data.items():
            if field_name != "_metadata" and field_name in format_examples:
                format_spec, description = format_examples[field_name]
                try:
                    # Show the raw value and formatted version
                    formatted_value = format(value, format_spec)
                    result_text += f"{field_name}:\n"
                    result_text += f"  Raw value: {value} ({type(value).__name__})\n"
                    result_text += f"  Format: {format_spec} ({description})\n"
                    result_text += f"  Formatted: {formatted_value}\n\n"
                except ValueError as e:
                    result_text += f"{field_name}: Format error - {e}\n\n"

        # Show the values
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Format String Results")
        msg.setText(result_text)
        msg.exec_()

    gui.set_submit_callback(handle_submit)

    # Show the GUI
    gui.show()

    # Run the application
    app.exec()


def demo_custom_buttons():
    """Demo custom buttons with callbacks."""
    print("Starting Custom Buttons Demo...")

    app = QApplication(sys.argv)

    # Load custom buttons configuration
    config_path = os.path.join(os.path.dirname(__file__), "examples", "custom_buttons.json")
    gui = GuiBuilder(config_path=config_path)

    def validate_data_callback(form_data):
        """Validate form data."""
        issues = []

        if not form_data.get('first_name', '').strip():
            issues.append("First name is required")
        if not form_data.get('last_name', '').strip():
            issues.append("Last name is required")
        if not form_data.get('email', '').strip():
            issues.append("Email is required")
        elif '@' not in form_data.get('email', ''):
            issues.append("Email must contain @ symbol")

        age = form_data.get('age', 0)
        if age < 18:
            issues.append("Age must be 18 or older")

        salary = form_data.get('salary', 0)
        if salary < 0:
            issues.append("Salary cannot be negative")

        # Show validation results
        if issues:
            msg = "Validation Issues Found:\n\n• " + "\n• ".join(issues)
            QMessageBox.warning(None, "Validation Failed", msg)
        else:
            QMessageBox.information(None, "Validation Passed", "All form data is valid!")

    def clear_all_callback(form_data):
        """Clear all form fields."""
        reply = QMessageBox.question(
            None,
            "Confirm Clear",
            "Are you sure you want to clear all form data?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            gui.clear_form()
            QMessageBox.information(None, "Form Cleared", "All form fields have been cleared.")

    def preview_callback(form_data):
        """Preview form data."""
        preview_text = "Form Data Preview:\n\n"

        for key, value in form_data.items():
            if key and value is not None:
                if isinstance(value, float):
                    preview_text += f"{key.replace('_', ' ').title()}: ${value:,.2f}\n"
                else:
                    preview_text += f"{key.replace('_', ' ').title()}: {value}\n"

        QMessageBox.information(None, "Form Data Preview", preview_text)

    def export_json_callback(form_data):
        """Export form data as JSON."""
        try:
            from qtpy.QtWidgets import QFileDialog
            file_path, _ = QFileDialog.getSaveFileName(
                None,
                "Export Form Data",
                "form_data.json",
                "JSON Files (*.json);;All Files (*)"
            )

            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(form_data, f, indent=2, ensure_ascii=False)
                QMessageBox.information(None, "Export Successful", f"Form data exported to:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(None, "Export Failed", f"Failed to export data:\n{str(e)}")

    def on_submit_custom_buttons(form_data):
        """Handle form submission."""
        print("Form submitted with data:")
        for key, value in form_data.items():
            print(f"  {key}: {value}")

        QMessageBox.information(None, "Form Submitted", "Form data has been submitted successfully!")

    def on_cancel_custom_buttons():
        """Handle form cancellation."""
        print("Form cancelled")
        QMessageBox.information(None, "Cancelled", "Form submission was cancelled.")

    # Register custom button callbacks
    gui.set_custom_button_callback("validate", validate_data_callback)
    gui.set_custom_button_callback("clear", clear_all_callback)
    gui.set_custom_button_callback("preview", preview_callback)
    gui.set_custom_button_callback("export", export_json_callback)

    # Register standard callbacks
    gui.set_submit_callback(on_submit_custom_buttons)
    gui.set_cancel_callback(on_cancel_custom_buttons)

    # Show the GUI
    gui.show()

    print("Custom buttons available:")
    for button_name in gui.get_custom_button_names():
        print(f"  - {button_name}")

    return app.exec()


def main():
    """Main function to run demos."""
    if len(sys.argv) > 1:
        demo_type = sys.argv[1].lower()
    else:
        print("Available demos:")
        print("  python demo.py registration  - User registration form")
        print("  python demo.py settings      - Application settings form")
        print("  python demo.py project       - Project data entry form")
        print("  python demo.py contact       - Programmatic contact form")
        print("  python demo.py persistence   - Data loading and saving demo")
        print("  python demo.py tabs          - Tabbed interface demo")
        print("  python demo.py complex_tabs  - Complex tabbed configuration demo")
        print("  python demo.py nested        - Nested field names demo")
        print("  python demo.py float         - Float fields demo")
        print("  python demo.py format        - Format strings demo")
        print("  python demo.py custom_buttons - Custom buttons demo")
        print()
        demo_type = input("Enter demo type (registration/settings/project/contact/persistence/tabs/complex_tabs/nested/float/format/custom_buttons): ").lower()

    if demo_type == "registration":
        demo_user_registration()
    elif demo_type == "settings":
        demo_settings_form()
    elif demo_type == "project":
        demo_project_form()
    elif demo_type == "persistence":
        demo_data_persistence()
    elif demo_type == "contact":
        demo_programmatic_config()
    elif demo_type == "tabs":
        demo_tabbed_interface()
    elif demo_type == "complex_tabs":
        demo_complex_tabs()
    elif demo_type == "nested":
        demo_nested_fields()
    elif demo_type == "float":
        demo_float_fields()
    elif demo_type == "format":
        demo_format_strings()
    elif demo_type == "custom_buttons":
        demo_custom_buttons()
    else:
        print(f"Unknown demo type: {demo_type}")
        print("Available options: registration, settings, project, contact, persistence, tabs, complex_tabs, nested, float, format, custom_buttons")


if __name__ == "__main__":
    main()
