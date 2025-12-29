"""Custom buttons example."""
from vibegui import GuiBuilder
from qtpy.QtWidgets import QApplication
import sys
import os

config = {
    "window": {"title": "Data Entry Form", "width": 500, "height": 400},
    "fields": [
        {"name": "name", "label": "Name", "type": "text"},
        {"name": "email", "label": "Email", "type": "email"},
        {"name": "notes", "label": "Notes", "type": "textarea"}
    ],
    "custom_buttons": [
        {
            "name": "clear_form",
            "label": "Clear All",
            "style": "background-color: #ff6b6b; color: white;"
        },
        {
            "name": "load_template",
            "label": "Load Template",
            "style": "background-color: #4ecdc4; color: white;"
        },
        {
            "name": "save_draft",
            "label": "Save Draft",
            "style": "background-color: #45b7d1; color: white;"
        }
    ],
    "submit_button": True,
    "cancel_button": True
}

def clear_form(button_config, form_data):
    gui.clear_form()
    print("Form cleared!")

def load_template(button_config, form_data):
    template_data = {
        "name": "John Template",
        "email": "template@example.com",
        "notes": "This is a template entry."
    }
    gui.set_form_data(template_data)
    print("Template loaded!")

def save_draft(button_config, form_data):
    gui.save_data_to_file("draft.json")
    print("Draft saved!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GuiBuilder(config_dict=config, backend='qt')
    gui.set_custom_button_callback('clear_form', clear_form)
    gui.set_custom_button_callback('load_template', load_template)
    gui.set_custom_button_callback('save_draft', save_draft)
    gui.show()

    sys.exit(app.exec())
