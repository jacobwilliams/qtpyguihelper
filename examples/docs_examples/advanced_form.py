"""Advanced form with validation example."""
from vibegui import GuiBuilder
from qtpy.QtWidgets import QApplication
import sys
import os

config = {
    "window": {
        "title": "User Registration",
        "width": 500,
        "height": 600
    },
    "fields": [
        {
            "name": "username",
            "label": "Username",
            "type": "text",
            "required": True,
            "placeholder": "Choose a username",
            "tooltip": "Username must be unique"
        },
        {
            "name": "password",
            "label": "Password",
            "type": "password",
            "required": True,
            "tooltip": "Password must be at least 8 characters"
        },
        {
            "name": "confirm_password",
            "label": "Confirm Password",
            "type": "password",
            "required": True
        },
        {
            "name": "email",
            "label": "Email Address",
            "type": "email",
            "required": True
        },
        {
            "name": "age",
            "label": "Age",
            "type": "number",
            "min_value": 13,
            "max_value": 120,
            "required": True
        },
        {
            "name": "country",
            "label": "Country",
            "type": "select",
            "options": ["USA", "Canada", "UK", "Australia", "Germany", "France"],
            "required": True
        },
        {
            "name": "birthdate",
            "label": "Birth Date",
            "type": "date",
            "required": True
        },
        {
            "name": "terms",
            "label": "I agree to the terms and conditions",
            "type": "checkbox",
            "required": True
        }
    ],
    "submit_button": True,
    "submit_label": "Register",
    "cancel_button": True
}

def validate_registration(data):
    # Custom validation
    if data.get('password') != data.get('confirm_password'):
        print("Error: Passwords do not match")
        return False

    if len(data.get('password', '')) < 8:
        print("Error: Password must be at least 8 characters")
        return False

    return True

def handle_registration(data):
    if validate_registration(data):
        print("Registration successful!")
        print(f"Welcome, {data['username']}!")
    else:
        print("Registration failed. Please check your inputs.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GuiBuilder(config_dict=config, backend='qt')
    gui.set_submit_callback(handle_registration)
    gui.show()

    sys.exit(app.exec())
