#!/usr/bin/env python3
"""
Demo script showing how to use the vibegui library.
"""

import sys
import os
import json
from pathlib import Path

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# NOTE: Do NOT import Qt widgets at module level!
# They interfere with tkinter on macOS. Import them inside Qt-specific functions only.


def on_registration_submit(form_data: dict) -> None:
    """Callback function for registration form submission."""
    from qtpy.QtWidgets import QMessageBox

    print("Registration form submitted with data:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")

    # Show a success message
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Registration Successful")
    msg.setText(f"Welcome, {form_data.get('first_name', 'User')}!\nYour registration has been processed.")
    msg.exec()


def on_settings_submit(form_data: dict) -> None:
    """Callback function for settings form submission."""
    print("Settings saved:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")


def on_cancel() -> None:
    """Callback function for form cancellation."""
    print("Form cancelled by user")


def demo_user_registration() -> None:
    """Demo the user registration form."""
    from vibegui import GuiBuilder
    from qtpy.QtWidgets import QApplication

    print("Starting User Registration Demo...")

    # Create the application
    app = QApplication(sys.argv)

    # Create GUI from JSON file
    config_path = os.path.join(os.path.dirname(__file__), "user_registration.json")
    gui = GuiBuilder(config_path=config_path)

    # Set callbacks
    gui.set_submit_callback(on_registration_submit)
    gui.set_cancel_callback(on_cancel)

    # Show the GUI
    gui.show()

    # Run the application
    app.exec()


def demo_settings_form() -> None:
    """Demo the settings form."""
    from vibegui import GuiBuilder
    from qtpy.QtWidgets import QApplication

    print("Starting Settings Form Demo...")

    # Create the application
    app = QApplication(sys.argv)

    # Create GUI from JSON file
    config_path = os.path.join(os.path.dirname(__file__), "settings_form.json")
    gui = GuiBuilder(config_path=config_path)

    # Set callbacks
    gui.set_submit_callback(on_settings_submit)

    # Show the GUI
    gui.show()

    # Run the application
    app.exec()


def demo_project_form() -> None:
    """Demo the project form."""
    from vibegui import GuiBuilder
    from qtpy.QtWidgets import QApplication

    print("Starting Project Form Demo...")

    # Create the application
    app = QApplication(sys.argv)

    # Create GUI from JSON file
    config_path = os.path.join(os.path.dirname(__file__), "project_form.json")
    gui = GuiBuilder(config_path=config_path)

    # Set callbacks
    gui.set_submit_callback(lambda data: print(f"Project saved: {data}"))

    # Show the GUI
    gui.show()

    # Run the application
    app.exec()


def demo_programmatic_config() -> None:
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
    from vibegui import GuiBuilder
    from qtpy.QtWidgets import QApplication
    app = QApplication(sys.argv)

    # Create GUI from dictionary
    gui = GuiBuilder(config_dict=config)

    # Set callbacks
    def on_contact_submit(form_data: dict) -> None:
        from qtpy.QtWidgets import QMessageBox

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


def demo_data_persistence() -> None:
    """Demo data loading and saving functionality."""
    from vibegui import GuiBuilder
    from qtpy.QtWidgets import QApplication, QMessageBox

    print("Starting Data Persistence Demo...")

    # Create the application
    app = QApplication(sys.argv)

    # Create GUI from JSON file
    config_path = os.path.join(os.path.dirname(__file__), "project_form.json")
    gui = GuiBuilder(config_path=config_path)

    # Load existing data if available
    data_path = os.path.join(os.path.dirname(__file__), "project_data.json")
    if os.path.exists(data_path):
        success = gui.load_data_from_file(data_path)
        if success:
            print(f"Loaded existing data from {data_path}")
        else:
            print("Failed to load existing data")

    # Set up save functionality
    def on_submit_and_save(form_data: dict) -> None:
        print("Project data submitted:")
        for key, value in form_data.items():
            print(f"  {key}: {value}")

        # Save to output file
        output_path = os.path.join(os.path.dirname(__file__), "project_output.json")
        success = gui.save_data_to_file(output_path)
        if success:
            print(f"Data saved to {output_path}")

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


def demo_tabbed_interface() -> None:
    """Demo the tabbed interface functionality."""
    from vibegui import GuiBuilder
    from qtpy.QtWidgets import QApplication, QMessageBox

    print("Starting Tabbed Interface Demo...")

    # Create the application
    app = QApplication(sys.argv)

    # Create GUI from JSON file
    config_path = os.path.join(os.path.dirname(__file__), "simple_tabs.json")
    gui = GuiBuilder(config_path=config_path)

    # Set callbacks
    def on_submit_tabs(form_data: dict) -> None:
        print("Tabbed form submitted:")
        for key, value in form_data.items():
            print(f"  {key}: {value}")

        # Show success message
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Form Submitted")
        msg.setText("Tabbed form data has been submitted successfully!")
        msg.exec()

    def validate_callback(form_data: dict) -> None:
        """Validate the tabbed form data."""
        issues = []

        # Check required fields
        if not form_data.get('first_name', '').strip():
            issues.append("First name is required")
        if not form_data.get('last_name', '').strip():
            issues.append("Last name is required")
        if not form_data.get('email', '').strip():
            issues.append("Email is required")
        elif '@' not in form_data.get('email', ''):
            issues.append("Email must contain @ symbol")

        # Check numeric fields
        years = form_data.get('years_experience', 0)
        if years < 0:
            issues.append("Years of experience cannot be negative")

        salary = form_data.get('salary', 0)
        if salary < 0:
            issues.append("Salary cannot be negative")

        rating = form_data.get('rating', 0)
        if not (1.0 <= rating <= 10.0):
            issues.append("Rating must be between 1.0 and 10.0")

        # Show validation results
        if issues:
            msg = "Validation Issues Found:\n\n• " + "\n• ".join(issues)
            QMessageBox.warning(None, "Validation Failed", msg)
        else:
            QMessageBox.information(None, "Validation Passed", "All form data is valid!")

    def reset_callback(form_data: dict) -> None:
        """Reset form to default values."""
        reply = QMessageBox.question(
            None,
            "Confirm Reset",
            "Are you sure you want to reset all fields to default values?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # Reload the config to get default values
            gui.load_data_from_dict({
                'experience': 'Mid-level',
                'years_experience': 5,
                'salary': 75000.00,
                'rating': 7.5
            })
            QMessageBox.information(None, "Form Reset", "Form has been reset to default values.")

    gui.set_submit_callback(on_submit_tabs)

    # Register custom button callbacks
    gui.set_custom_button_callback("validate", validate_callback)
    gui.set_custom_button_callback("reset", reset_callback)

    # Show the GUI
    gui.show()

    print("Custom buttons available:")
    for button_name in gui.get_custom_button_names():
        print(f"  - {button_name}")

    # Run the application
    app.exec()


def demo_complex_tabs() -> None:
    """Demo a complex tabbed configuration interface."""
    from vibegui import GuiBuilder
    from qtpy.QtWidgets import QApplication, QMessageBox

    print("Starting Complex Tabbed Configuration Demo...")

    # Create the application
    app = QApplication(sys.argv)

    # Create GUI from JSON file
    config_path = os.path.join(os.path.dirname(__file__), "tabbed_config.json")
    gui = GuiBuilder(config_path=config_path)

    # Set callbacks
    def on_save_config(form_data: dict) -> None:
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


def demo_nested_fields() -> None:
    """Demo nested field names with dot notation."""
    from vibegui import GuiBuilder
    from qtpy.QtWidgets import QApplication, QMessageBox

    print("Starting Nested Fields Demo...")

    # Create the application
    app = QApplication(sys.argv)

    # Create GUI from JSON file
    config_path = os.path.join(os.path.dirname(__file__), "nested_config.json")
    gui = GuiBuilder(config_path=config_path)

    # Load existing nested data if available
    data_path = os.path.join(os.path.dirname(__file__), "nested_data.json")
    if os.path.exists(data_path):
        success = gui.load_data_from_file(data_path)
        if success:
            print(f"Loaded existing nested data from {data_path}")
        else:
            print("Failed to load existing nested data")

    # Set callbacks
    def on_save_nested_config(form_data: dict) -> None:
        print("Nested configuration saved:")
        # Print the nested structure
        def print_nested(data: dict, indent: int = 0) -> None:
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


def demo_float_fields() -> None:
    """Demo float fields with various format specifications."""
    from vibegui import GuiBuilder
    from qtpy.QtWidgets import QApplication, QMessageBox

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

    def handle_submit(form_data: dict) -> None:
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


def demo_format_strings() -> None:
    """Demo various format string specifications including scientific notation."""
    from vibegui import GuiBuilder
    from qtpy.QtWidgets import QApplication, QMessageBox

    print("Starting Format Strings Demo...")

    # Create the application
    app = QApplication(sys.argv)

    # Load the format strings example
    config_path = os.path.join(os.path.dirname(__file__), "format_strings.json")
    gui = GuiBuilder(config_path=config_path)

    def handle_submit(form_data: dict) -> None:
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


def demo_custom_buttons() -> None:
    """Demo custom buttons with callbacks."""
    from vibegui import GuiBuilder
    from qtpy.QtWidgets import QApplication, QMessageBox

    print("Starting Custom Buttons Demo...")

    app = QApplication(sys.argv)

    # Load custom buttons configuration
    config_path = os.path.join(os.path.dirname(__file__), "custom_buttons.json")
    gui = GuiBuilder(config_path=config_path)

    def validate_data_callback(form_data: dict) -> None:
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

    def clear_all_callback(form_data: dict) -> None:
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

    def preview_callback(form_data: dict) -> None:
        """Preview form data."""
        preview_text = "Form Data Preview:\n\n"

        for key, value in form_data.items():
            if key and value is not None:
                if isinstance(value, float):
                    preview_text += f"{key.replace('_', ' ').title()}: ${value:,.2f}\n"
                else:
                    preview_text += f"{key.replace('_', ' ').title()}: {value}\n"

        QMessageBox.information(None, "Form Data Preview", preview_text)

    def export_json_callback(form_data: dict) -> None:
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

    def on_submit_custom_buttons(form_data : dict) -> None:
        """Handle form submission."""
        print("Form submitted with data:")
        for key, value in form_data.items():
            print(f"  {key}: {value}")

        QMessageBox.information(None, "Form Submitted", "Form data has been submitted successfully!")

    def on_cancel_custom_buttons() -> None:
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


def demo_complex_tabs_wx() -> None:
    # Force wxPython backend
    from vibegui import set_backend
    set_backend('wx')
    print("✓ wxPython backend selected")
    from vibegui import GuiBuilder
    import wx

    app = wx.App()

    config_path = os.path.join(os.path.dirname(__file__), "tabbed_config.json")
    gui = GuiBuilder(config_path=config_path)

    # Show the GUI
    gui.show()

    # Run the application
    app.MainLoop()

def demo_wxpython_backend() -> None:
    """Demo the wxPython backend with a working GUI."""
    print("Starting wxPython Backend Demo...")

    try:
        # Force wxPython backend
        from vibegui import set_backend
        set_backend('wx')
        print("✓ wxPython backend selected")

        # Import wxPython
        import wx

        # Create configuration
        config = {
            "window": {
                "title": "wxPython Backend Demo - Cross-Platform GUI",
                "width": 600,
                "height": 500,
                "resizable": True
            },
            "layout": "form",
            "submit_button": True,
            "cancel_button": True,
            "submit_label": "Submit Data",
            "cancel_label": "Cancel",
            "fields": [
                {
                    "name": "name",
                    "type": "text",
                    "label": "Full Name",
                    "placeholder": "Enter your full name",
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
                    "name": "height",
                    "type": "float",
                    "label": "Height (m)",
                    "format_string": ".2f",
                    "min_value": 0.5,
                    "max_value": 3.0,
                    "default_value": 1.75
                },
                {
                    "name": "email",
                    "type": "email",
                    "label": "Email Address",
                    "placeholder": "your.email@example.com",
                    "required": True
                },
                {
                    "name": "subscribe",
                    "type": "checkbox",
                    "label": "Subscribe to newsletter",
                    "default_value": True
                },
                {
                    "name": "category",
                    "type": "select",
                    "label": "Category",
                    "options": ["Student", "Professional", "Retired", "Other"],
                    "default_value": "Professional"
                },
                {
                    "name": "priority",
                    "type": "radio",
                    "label": "Priority Level",
                    "options": ["Low", "Medium", "High"],
                    "default_value": "Medium"
                },
                {
                    "name": "birth_date",
                    "type": "date",
                    "label": "Birth Date",
                    "default_value": "1990-01-01"
                },
                {
                    "name": "notes",
                    "type": "textarea",
                    "label": "Additional Notes",
                    "placeholder": "Enter any additional information...",
                    "height": 80
                }
            ],
            "custom_buttons": [
                {
                    "name": "clear_form",
                    "label": "Clear Form",
                    "tooltip": "Clear all form fields",
                    "enabled": True
                },
                {
                    "name": "load_demo",
                    "label": "Load Demo Data",
                    "tooltip": "Load sample data into the form",
                    "enabled": True
                }
            ]
        }

        # Create wxPython application
        app = wx.App()

        # Create GUI builder with wxPython backend
        from vibegui import set_backend, GuiBuilder
        set_backend('wx')
        gui_builder = GuiBuilder(config_dict=config)

        # Set up callbacks
        def on_submit(form_data: dict) -> None:
            print("wxPython form submitted:")
            for key, value in form_data.items():
                print(f"  {key}: {value}")
            wx.MessageBox("Form submitted successfully!", "Success", wx.OK | wx.ICON_INFORMATION)

        def on_cancel() -> None:
            print("wxPython form cancelled")
            wx.MessageBox("Form cancelled by user", "Cancelled", wx.OK | wx.ICON_INFORMATION)

        def clear_form(_form_data: dict) -> None:
            gui_builder.clear_form()
            print("Form cleared")
            wx.MessageBox("Form cleared successfully!", "Cleared", wx.OK | wx.ICON_INFORMATION)

        def load_demo_data(_form_data: dict) -> None:
            demo_data = {
                "name": "Jane Smith",
                "age": 28,
                "height": 1.65,
                "email": "jane.smith@example.com",
                "subscribe": False,
                "category": "Student",
                "priority": "Medium",
                "birth_date": "1995-03-20",
                "notes": "Demo data for wxPython backend testing."
            }
            gui_builder.set_form_data(demo_data)
            print("Demo data loaded")
            wx.MessageBox("Demo data loaded successfully!", "Data Loaded", wx.OK | wx.ICON_INFORMATION)

        # Register callbacks
        gui_builder.set_submit_callback(on_submit)
        gui_builder.set_cancel_callback(on_cancel)
        gui_builder.set_custom_button_callback("clear_form", clear_form)
        gui_builder.set_custom_button_callback("load_demo", load_demo_data)

        # Show the GUI
        gui_builder.show()

        print("✓ wxPython GUI created and shown")
        print("  - Custom buttons available:", gui_builder.get_custom_button_names())

        # Run the application
        app.MainLoop()

    except ImportError as e:
        print(f"✗ wxPython not available: {e}")
    except Exception as e:
        print(f"✗ Error with wxPython backend: {e}")


def demo_tkinter_backend() -> None:
    """Demo the tkinter backend with a working GUI."""
    print("Starting tkinter Backend Demo...")

    try:
        # Force tkinter backend FIRST, before any GUI imports
        from vibegui import set_backend
        set_backend('tk')
        print("✓ tkinter backend selected")

        # Import tkinter
        import tkinter as tk
        from tkinter import messagebox

        # NOW import GuiBuilder after backend is set
        from vibegui import GuiBuilder

        # Create configuration
        config = {
            "window": {
                "title": "tkinter Backend Demo - Cross-Platform GUI",
                "width": 600,
                "height": 500,
                "resizable": True
            },
            "layout": "form",
            "submit_button": True,
            "cancel_button": True,
            "submit_label": "Submit Data",
            "cancel_label": "Cancel",
            "fields": [
                {
                    "name": "name",
                    "type": "text",
                    "label": "Full Name",
                    "placeholder": "Enter your full name",
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
                    "name": "height",
                    "type": "float",
                    "label": "Height (m)",
                    "min_value": 0.5,
                    "max_value": 3.0,
                    "default_value": 1.75
                },
                {
                    "name": "email",
                    "type": "email",
                    "label": "Email Address",
                    "placeholder": "your.email@example.com",
                    "required": True
                },
                {
                    "name": "subscribe",
                    "type": "checkbox",
                    "label": "Subscribe to newsletter",
                    "default_value": True
                },
                {
                    "name": "category",
                    "type": "select",
                    "label": "Category",
                    "options": ["Student", "Professional", "Retired", "Other"],
                    "default_value": "Professional"
                },
                {
                    "name": "priority",
                    "type": "radio",
                    "label": "Priority Level",
                    "options": ["Low", "Medium", "High"],
                    "default_value": "Medium"
                },
                {
                    "name": "birth_date",
                    "type": "date",
                    "label": "Birth Date",
                    "default_value": "1990-01-01"
                },
                {
                    "name": "notes",
                    "type": "textarea",
                    "label": "Additional Notes",
                    "placeholder": "Enter any additional information...",
                    "height": 80
                }
            ],
            "custom_buttons": [
                {
                    "name": "clear_form",
                    "label": "Clear Form",
                    "tooltip": "Clear all form fields"
                },
                {
                    "name": "load_demo",
                    "label": "Load Demo Data",
                    "tooltip": "Load sample data into the form"
                }
            ]
        }

        # Create GUI builder (backend already set above)
        gui_builder = GuiBuilder(config_dict=config)

        # Set up callbacks
        def on_submit(form_data: dict) -> None:
            print("tkinter form submitted:")
            for key, value in form_data.items():
                print(f"  {key}: {value}")
            messagebox.showinfo("Success", "Form submitted successfully!")

        def on_cancel() -> None:
            print("tkinter form cancelled")
            messagebox.showinfo("Cancelled", "Form cancelled by user")

        def clear_form(button_config: dict, form_data: dict) -> None:
            gui_builder.clear_form()
            print("Form cleared")
            messagebox.showinfo("Cleared", "Form cleared successfully!")

        def load_demo_data(button_config: dict, form_data: dict) -> None:
            demo_data = {
                "name": "Alice Johnson",
                "age": 32,
                "height": 1.68,
                "email": "alice.johnson@example.com",
                "subscribe": True,
                "category": "Professional",
                "priority": "High",
                "birth_date": "1991-05-15",
                "notes": "Demo data for tkinter backend testing."
            }
            gui_builder.set_form_data(demo_data)
            print("Demo data loaded")
            messagebox.showinfo("Data Loaded", "Demo data loaded successfully!")

        # Register callbacks
        gui_builder.set_submit_callback(on_submit)
        gui_builder.set_cancel_callback(on_cancel)
        gui_builder.set_custom_button_callback("clear_form", clear_form)
        gui_builder.set_custom_button_callback("load_demo", load_demo_data)

        # Show the GUI
        gui_builder.show()

        print("✓ tkinter GUI created and shown")

        # Run the application
        gui_builder.run()

    except ImportError as e:
        print(f"✗ tkinter not available: {e}")
        print("  tkinter should be included with Python by default")
    except Exception as e:
        print(f"✗ Error with tkinter backend: {e}")


def demo_gtk_backend() -> None:
    """Demo the GTK backend specifically."""
    print("Starting GTK Backend Demo...")

    try:
        from vibegui import set_backend, GuiBuilder
        set_backend('gtk')

        # Simple form configuration
        config = {
            "window": {"title": "GTK Demo - Settings Form"},
            "fields": [
                {
                    "name": "theme",
                    "label": "Theme",
                    "type": "combo",
                    "choices": ["Dark", "Light", "Auto"],
                    "default_value": "Auto",
                    "required": True
                },
                {
                    "name": "notifications",
                    "label": "Enable Notifications",
                    "type": "checkbox",
                    "default_value": True
                },
                {
                    "name": "volume",
                    "label": "Volume",
                    "type": "int",
                    "min_value": 0,
                    "max_value": 100,
                    "default_value": 75
                },
                {
                    "name": "username",
                    "label": "Username",
                    "type": "text",
                    "required": True,
                    "default_value": "user123"
                },
                {
                    "name": "description",
                    "label": "Description",
                    "type": "textarea",
                    "default_value": "GTK backend demo application"
                }
            ],
            "submit_button": True,
            "submit_label": "Save Settings",
            "cancel_button": True,
            "cancel_label": "Close",
            "custom_buttons": [
                {
                    "name": "reset",
                    "label": "Reset",
                    "tooltip": "Reset to default values"
                }
            ]
        }

        def on_gtk_submit(form_data: dict) -> None:
            """Handle GTK form submission."""
            print("GTK Form submitted with data:")
            for key, value in form_data.items():
                print(f"  {key}: {value}")

        # Create the GUI builder
        gui_builder = GuiBuilder(config_dict=config)
        gui_builder.set_submit_callback(on_gtk_submit)

        print("✓ GTK backend demo starting...")
        print("  Close the window or click 'Close' to exit")

        # Run the application
        gui_builder.run()

    except ImportError as e:
        print(f"✗ GTK not available: {e}")
    except Exception as e:
        print(f"✗ Error with GTK backend: {e}")


def demo_complex_tabs_gtk() -> None:
    """Demo a complex tabbed configuration interface using GTK backend."""
    print("Starting Complex Tabbed Configuration Demo (GTK)...")

    try:
        # Force GTK backend
        from vibegui import set_backend
        set_backend('gtk')
        print("✓ GTK backend selected")

        from vibegui import GuiBuilder

        # Create GUI from JSON file
        config_path = os.path.join(os.path.dirname(__file__), "tabbed_config.json")
        gui = GuiBuilder(config_path=config_path)

        # Set callbacks
        def on_save_config(form_data: dict) -> None:
            print("Configuration saved (GTK):")
            for key, value in form_data.items():
                print(f"  {key}: {value}")

            # Save to file
            output_path = os.path.join(os.path.dirname(__file__), "tabbed_config_output_gtk.json")
            success = gui.save_data_to_file(output_path)
            if success:
                print(f"Configuration saved to {output_path}")

            print("✓ Configuration has been saved successfully!")

        gui.set_submit_callback(on_save_config)

        print("✓ GTK tabbed GUI created and shown")
        print("  - Window size: 800x600 pixels")
        print("  - Multiple tabs available - switch between them")
        print("  - Each tab should show all its fields properly")
        print("  - Tabs should scroll if needed to show all content")
        print("  - Submit to see the form data structure")
        print("  - Should automatically use OS dark theme if enabled")
        print("✓ Starting GTK application...")

        # Show and run the GUI
        gui.run()

    except ImportError as e:
        print(f"✗ GTK not available: {e}")
        print("  Install GTK support: pip install pygobject")
    except Exception as e:
        print(f"✗ Error with GTK backend: {e}")
        import traceback
        traceback.print_exc()
        print("  Note: If tabs appear too small, try the simpler GTK demo:")
        print("  python examples/demo.py gtk")


def demo_flet_backend() -> None:
    """Demo the Flet backend with a simple form."""
    print("Starting Flet Backend Demo...")

    try:
        # Force Flet backend
        from vibegui import set_backend
        set_backend('flet')
        print("✓ Flet backend selected")

        from vibegui import GuiBuilder

        # Create a simple configuration
        config = {
            "window": {
                "title": "Flet Backend Demo",
                "width": 600,
                "height": 500
            },
            "fields": [
                {
                    "name": "username",
                    "label": "Username",
                    "type": "text",
                    "required": True,
                    "placeholder": "Enter your username"
                },
                {
                    "name": "email",
                    "label": "Email",
                    "type": "email",
                    "required": True,
                    "placeholder": "user@example.com"
                },
                {
                    "name": "password",
                    "label": "Password",
                    "type": "password",
                    "required": True
                },
                {
                    "name": "theme",
                    "label": "Preferred Theme",
                    "type": "select",
                    "options": ["Light", "Dark", "System"],
                    "default_value": "System"
                },
                {
                    "name": "notifications",
                    "label": "Enable Notifications",
                    "type": "checkbox",
                    "default_value": True
                },
                {
                    "name": "description",
                    "label": "About You",
                    "type": "textarea",
                    "placeholder": "Tell us about yourself..."
                }
            ],
            "submit_button": True,
            "submit_label": "Save Settings",
            "cancel_button": True,
            "cancel_label": "Close"
        }

        def on_flet_submit(form_data: dict) -> None:
            """Handle Flet form submission."""
            print("Flet Form submitted with data:")
            for key, value in form_data.items():
                print(f"  {key}: {value}")

        # Create the GUI builder
        gui_builder = GuiBuilder(config_dict=config)
        gui_builder.set_submit_callback(on_flet_submit)

        print("✓ Flet backend demo starting...")
        print("  Flet uses Material Design UI")
        print("  Automatically adapts to system theme")
        print("  Close the window or click 'Close' to exit")

        # Run the application
        gui_builder.run()

    except ImportError as e:
        print(f"✗ Flet not available: {e}")
        print("  Install Flet support: pip install flet")
    except Exception as e:
        print(f"✗ Error with Flet backend: {e}")
        import traceback
        traceback.print_exc()


def demo_complex_tabs_flet() -> None:
    """Demo a complex tabbed configuration interface using Flet backend."""
    print("Starting Complex Tabbed Configuration Demo (Flet)...")

    try:
        # Force Flet backend
        from vibegui import set_backend
        set_backend('flet')
        print("✓ Flet backend selected")

        from vibegui import GuiBuilder

        # Create GUI from JSON file
        config_path = os.path.join(os.path.dirname(__file__), "tabbed_config.json")
        gui = GuiBuilder(config_path=config_path)

        # Set callbacks
        def on_save_config(form_data: dict) -> None:
            print("Configuration saved (Flet):")
            for key, value in form_data.items():
                print(f"  {key}: {value}")

            # Save to file
            output_path = os.path.join(os.path.dirname(__file__), "tabbed_config_flet_data.json")
            success = gui.save_data_to_file(output_path)
            if success:
                print(f"Configuration saved to {output_path}")

            print("✓ Configuration has been saved successfully!")

        gui.set_submit_callback(on_save_config)

        print("✓ Flet tabbed GUI created")
        print("  - Modern Material Design interface")
        print("  - Multiple tabs available - switch between them")
        print("  - Beautiful animations and transitions")
        print("  - Automatically adapts to system theme")
        print("  - Submit to see the form data structure")
        print("✓ Starting Flet application...")

        # Show and run the GUI
        gui.run()

    except ImportError as e:
        print(f"✗ Flet not available: {e}")
        print("  Install Flet support: pip install flet")
    except Exception as e:
        print(f"✗ Error with Flet backend: {e}")
        import traceback
        traceback.print_exc()
        print("  Note: If you encounter issues, try the simpler Flet demo:")
        print("  python examples/demo.py flet")


def demo_backend_comparison() -> None:
    """Demo Qt, wxPython, tkinter, and GTK backends side by side."""
    print("Starting Backend Comparison Demo...")

    # Don't import from vibegui here - it may trigger Qt imports!
    # Just show what backends are typically available
    print("Available backends: ['qt', 'wx', 'tk', 'gtk']")

    backend_choice = input("Choose backend (qt/wx/tk/gtk/all): ").lower()

    if backend_choice == "qt":
        demo_user_registration()  # Existing Qt demo
    elif backend_choice == "wx":
        demo_wxpython_backend()   # wxPython demo
    elif backend_choice == "tk":
        demo_tkinter_backend()    # tkinter demo
    elif backend_choice == "gtk":
        demo_gtk_backend()        # GTK demo
    else:
        print("Invalid choice. Available options: qt, wx, tk, gtk")


def demo_unified_interface() -> None:
    """Demo the unified GuiBuilder interface that auto-selects backend."""
    print("Starting Unified Interface Demo...")

    from vibegui import GuiBuilder, get_backend_info

    # Show current backend info
    info = get_backend_info()
    print(f"Auto-selected backend: {info['backend']}")

    # Create a simple configuration
    config = {
        "window": {
            "title": f"Unified Interface Demo - {info['backend'].upper()} Backend",
            "width": 500,
            "height": 400
        },
        "layout": "form",
        "fields": [
            {
                "name": "backend_test",
                "type": "text",
                "label": "Backend Test",
                "default_value": f"Running on {info['backend']} backend",
                "required": True
            },
            {
                "name": "user_name",
                "type": "text",
                "label": "Your Name",
                "placeholder": "Enter your name"
            },
            {
                "name": "rating",
                "type": "int",
                "label": "Rate this demo (1-10)",
                "min_value": 1,
                "max_value": 10,
                "default_value": 5
            },
            {
                "name": "feedback",
                "type": "textarea",
                "label": "Feedback",
                "placeholder": "How was the cross-platform experience?",
                "height": 100
            }
        ],
        "submit_button": True,
        "cancel_button": True
    }

    def on_submit_unified(form_data: dict) -> None:
        print(f"Unified interface form submitted via {info['backend']} backend:")
        for key, value in form_data.items():
            print(f"  {key}: {value}")

    # Create the appropriate application based on backend
    if info['backend'] == 'qt':
        # Qt backend needs QApplication
        from qtpy.QtWidgets import QApplication
        app = QApplication(sys.argv)
        gui = GuiBuilder(config_dict=config)
        gui.set_submit_callback(on_submit_unified)
        gui.show()
        app.exec()
    elif info['backend'] == 'wx':
        # wxPython backend needs wx.App
        import wx
        app = wx.App()
        gui = GuiBuilder(config_dict=config)
        gui.set_submit_callback(on_submit_unified)
        gui.show()
        app.MainLoop()
    elif info['backend'] == 'tk':
        # tkinter backend manages its own main loop
        gui = GuiBuilder(config_dict=config)
        gui.set_submit_callback(on_submit_unified)
        gui.show()
        gui.run()
    else:
        # Use the create_and_run method as fallback
        gui = GuiBuilder(config_dict=config)
        gui.set_submit_callback(on_submit_unified)
        return GuiBuilder.create_and_run(config_dict=config)


def demo_complex_tabs_tk() -> None:
    """Demo a complex tabbed configuration interface using tkinter backend."""
    print("Starting Complex Tabbed Configuration Demo (tkinter)...")

    try:
        # Force tkinter backend
        from vibegui import set_backend
        set_backend('tk')
        print("✓ tkinter backend selected")

        # Import tkinter
        import tkinter as tk
        from tkinter import messagebox

        # NOW import GuiBuilder after backend is set
        from vibegui import GuiBuilder

        # Create GUI from JSON file
        config_path = os.path.join(os.path.dirname(__file__), "tabbed_config.json")
        gui = GuiBuilder(config_path=config_path)

        # Set callbacks
        def on_save_config(form_data: dict) -> None:
            print("Configuration saved (tkinter):")
            for key, value in form_data.items():
                print(f"  {key}: {value}")

            # Save to file
            output_path = os.path.join(os.path.dirname(__file__), "tabbed_config_output_tk.json")
            success = gui.save_data_to_file(output_path)
            if success:
                print(f"Configuration saved to {output_path}")

            # Show success message
            messagebox.showinfo(
                "Configuration Saved",
                f"Configuration has been saved successfully!\nOutput: {output_path}"
            )

        gui.set_submit_callback(on_save_config)

        print("✓ tkinter tabbed GUI created and shown")
        print("  - Switch between tabs to verify all fields expand properly")
        print("  - Submit to see the form data structure")
        print("✓ GUI created successfully! Close the window to exit.")

        # Show and run the GUI
        gui.show()
        gui.run()

    except ImportError as e:
        print(f"✗ tkinter not available: {e}")
        print("  tkinter should be included with Python by default")
    except Exception as e:
        print(f"✗ Error with tkinter backend: {e}")


def main() -> None:
    """Main function to run demos."""
    if len(sys.argv) > 1:
        demo_type = sys.argv[1].lower()
    else:
        print("Available demos:")
        print("  python demo.py registration    - User registration form (Qt)")
        print("  python demo.py settings        - Application settings form (Qt)")
        print("  python demo.py project         - Project data entry form (Qt)")
        print("  python demo.py contact         - Programmatic contact form (Qt)")
        print("  python demo.py persistence     - Data loading and saving demo (Qt)")
        print("  python demo.py tabs            - Tabbed interface demo (Qt)")
        print("  python demo.py complex_tabs    - Complex tabbed configuration demo (Qt)")
        print("  python demo.py complex_tabs_wx - Complex tabbed configuration demo (wxPython)")
        print("  python demo.py complex_tabs_tk - Complex tabbed configuration demo (tkinter)")
        print("  python demo.py complex_tabs_gtk - Complex tabbed configuration demo (GTK)")
        print("  python demo.py complex_tabs_flet - Complex tabbed configuration demo (Flet)")
        print("  python demo.py nested          - Nested field names demo (Qt)")
        print("  python demo.py float           - Float fields demo (Qt)")
        print("  python demo.py format          - Format strings demo (Qt)")
        print("  python demo.py custom_buttons  - Custom buttons demo (Qt)")
        print()
        print("Backend-specific demos:")
        print("  python demo.py wxpython      - wxPython backend demo")
        print("  python demo.py tkinter       - tkinter backend demo")
        print("  python demo.py gtk           - GTK backend demo")
        print("  python demo.py flet          - Flet backend demo")
        print("  python demo.py compare       - Compare all backends")
        print("  python demo.py unified       - Unified interface (auto-backend)")
        print()
        demo_type = input("Enter demo type: ").lower()

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
    elif demo_type == "complex_tabs_wx":
        demo_complex_tabs_wx()
    elif demo_type == "complex_tabs_tk":
        demo_complex_tabs_tk()
    elif demo_type == "complex_tabs_gtk":
        demo_complex_tabs_gtk()
    elif demo_type == "complex_tabs_flet":
        demo_complex_tabs_flet()
    elif demo_type == "wx" or demo_type == "wxpython":
        demo_wxpython_backend()
    elif demo_type == "tk" or demo_type == "tkinter":
        demo_tkinter_backend()
    elif demo_type == "gtk":
        demo_gtk_backend()
    elif demo_type == "flet":
        demo_flet_backend()
    elif demo_type == "backend_comparison" or demo_type == "compare":
        demo_backend_comparison()
    elif demo_type == "unified":
        demo_unified_interface()
    else:
        print(f"Unknown demo type: {demo_type}")
        print("Available options: registration, settings, project, contact, persistence, tabs, complex_tabs, complex_tabs_wx, complex_tabs_tk, complex_tabs_gtk, complex_tabs_flet, nested, float, format, custom_buttons, wx, wxpython, tk, tkinter, gtk, flet, compare, backend_comparison, unified")


if __name__ == "__main__":
    main()
