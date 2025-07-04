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
        print()
        demo_type = input("Enter demo type (registration/settings/project/contact): ").lower()

    if demo_type == "registration":
        demo_user_registration()
    elif demo_type == "settings":
        demo_settings_form()
    elif demo_type == "project":
        demo_project_form()
    elif demo_type == "contact":
        demo_programmatic_config()
    else:
        print(f"Unknown demo type: {demo_type}")
        print("Available options: registration, settings, project, contact")


if __name__ == "__main__":
    main()
