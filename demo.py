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
from PySide6.QtWidgets import QApplication, QMessageBox


def on_registration_submit(form_data):
    """Callback function for registration form submission."""
    print("Registration form submitted with data:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")

    # Show a success message
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Registration Successful")
    msg.setText(f"Welcome, {form_data.get('first_name', 'User')}!\\nYour registration has been processed.")
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
        msg.setText(f"Project data has been saved successfully!\\nOutput: {output_path}")
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
        print()
        demo_type = input("Enter demo type (registration/settings/project/contact/persistence/tabs/complex_tabs/nested): ").lower()

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
    else:
        print(f"Unknown demo type: {demo_type}")
        print("Available options: registration, settings, project, contact, persistence, tabs, complex_tabs, nested")


if __name__ == "__main__":
    main()
