"""Simple contact form example."""
from vibegui import GuiBuilder
from qtpy.QtWidgets import QApplication
import sys
import os

config = {
    "window": {
        "title": "Contact Form",
        "width": 400,
        "height": 350
    },
    "fields": [
        {
            "name": "name",
            "label": "Full Name",
            "type": "text",
            "required": True,
            "placeholder": "Enter your full name"
        },
        {
            "name": "email",
            "label": "Email",
            "type": "email",
            "required": True,
            "placeholder": "your.email@example.com"
        },
        {
            "name": "phone",
            "label": "Phone Number",
            "type": "text",
            "placeholder": "+1 (555) 123-4567"
        },
        {
            "name": "message",
            "label": "Message",
            "type": "textarea",
            "required": True,
            "placeholder": "Enter your message here..."
        }
    ],
    "submit_button": True,
    "submit_label": "Send Message",
    "cancel_button": True
}

def handle_submit(data):
    print("Contact form submitted:")
    for key, value in data.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GuiBuilder(config_dict=config, backend='qt')
    gui.set_submit_callback(handle_submit)
    gui.show()

    sys.exit(app.exec())
