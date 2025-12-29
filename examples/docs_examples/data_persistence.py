"""Data persistence example."""
from vibegui import GuiBuilder
from qtpy.QtWidgets import QApplication
import sys
import os

config = {
    "window": {"title": "Settings Manager", "width": 450, "height": 350},
    "fields": [
        {"name": "theme", "label": "Theme", "type": "select",
         "options": ["Light", "Dark", "Auto"], "default_value": "Auto"},
        {"name": "language", "label": "Language", "type": "select",
         "options": ["English", "Spanish", "French", "German"]},
        {"name": "auto_save", "label": "Auto-save", "type": "checkbox", "default_value": True},
        {"name": "backup_interval", "label": "Backup Interval (hours)", "type": "number",
         "min_value": 1, "max_value": 24, "default_value": 6}
    ],
    "custom_buttons": [
        {"name": "load_settings", "label": "Load Settings"},
        {"name": "save_settings", "label": "Save Settings"},
        {"name": "reset_defaults", "label": "Reset to Defaults"}
    ]
}

settings_file = "user_settings.json"

def load_settings(button_config, form_data):
    if os.path.exists(settings_file):
        if gui.load_data_from_file(settings_file):
            print("Settings loaded successfully!")
        else:
            print("Failed to load settings.")
    else:
        print("No saved settings found.")

def save_settings(button_config, form_data):
    if gui.save_data_to_file(settings_file):
        print("Settings saved successfully!")
    else:
        print("Failed to save settings.")

def reset_defaults(button_config, form_data):
    defaults = {
        "theme": "Auto",
        "language": "English",
        "auto_save": True,
        "backup_interval": 6
    }
    gui.set_form_data(defaults)
    print("Settings reset to defaults!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GuiBuilder(config_dict=config, backend='qt')
    gui.set_custom_button_callback('load_settings', load_settings)
    gui.set_custom_button_callback('save_settings', save_settings)
    gui.set_custom_button_callback('reset_defaults', reset_defaults)

    # Auto-load settings on startup
    if os.path.exists(settings_file):
        gui.load_data_from_file(settings_file)

    gui.show()

    sys.exit(app.exec())
