"""Float formatting example."""
from vibegui import GuiBuilder
from qtpy.QtWidgets import QApplication
import sys
import os

config = {
    "window": {"title": "Measurements", "width": 500, "height": 500},
    "layout": "form",
    "fields": [
        {"name": "price", "label": "Price ($)", "type": "float",
         "format_string": ".2f", "default_value": 99.99},

        {"name": "temperature", "label": "Temperature (°C)", "type": "float",
         "format_string": ".1f", "default_value": 23.5},

        {"name": "precision", "label": "High Precision", "type": "float",
         "format_string": ".4f", "default_value": 3.1416},

        {"name": "scientific", "label": "Large Number", "type": "float",
         "format_string": ".2e", "default_value": 1234567.89},

        {"name": "percentage", "label": "Completion", "type": "float",
         "format_string": ".1%", "default_value": 0.856},

        {"name": "currency", "label": "Revenue", "type": "float",
         "format_string": ",.2f", "default_value": 12345.67}
    ],
    "submit_button": True
}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GuiBuilder(config_dict=config, backend='qt')
    gui.show()

    sys.exit(app.exec())
