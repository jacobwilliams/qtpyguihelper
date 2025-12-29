"""Nested fields example."""
from vibegui import GuiBuilder
from qtpy.QtWidgets import QApplication
import sys
import json
import os

config = {
    "window": {"title": "Application Settings", "width": 600, "height": 500},
    "layout": "form",
    "fields": [
        # Global settings
        {"name": "global.app_name", "label": "Application Name",
         "type": "text", "default_value": "My App"},
        {"name": "global.version", "label": "Version",
         "type": "text", "default_value": "1.0.0"},

        # Database settings
        {"name": "database.host", "label": "Database Host",
         "type": "text", "default_value": "localhost"},
        {"name": "database.port", "label": "Database Port",
         "type": "int", "default_value": 5432},
        {"name": "database.name", "label": "Database Name",
         "type": "text", "required": True},

        # UI settings
        {"name": "ui.theme", "label": "Theme",
         "type": "select", "options": ["light", "dark", "auto"],
         "default_value": "auto"},
        {"name": "ui.font_size", "label": "Font Size",
         "type": "int", "min_value": 8, "max_value": 24, "default_value": 12}
    ],
    "submit_button": True
}

def on_submit(data):
    print("Settings saved:")
    print(json.dumps(data, indent=2))
    # Output will be nested:
    # {
    #   "global": {"app_name": "...", "version": "..."},
    #   "database": {"host": "...", "port": ..., "name": "..."},
    #   "ui": {"theme": "...", "font_size": ...}
    # }

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GuiBuilder(config_dict=config, backend='qt')
    gui.set_submit_callback(on_submit)
    gui.show()

    sys.exit(app.exec())
