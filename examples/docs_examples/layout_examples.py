"""Layout examples showing different field organization styles."""
from vibegui import GuiBuilder
from qtpy.QtWidgets import QApplication
import sys
import os

# Vertical layout (default - stacks fields vertically)
vertical_config = {
    "window": {"title": "Vertical Layout", "width": 400, "height": 400},
    "layout": "vertical",
    "fields": [
        {"name": "field1", "label": "Field 1", "type": "text"},
        {"name": "field2", "label": "Field 2", "type": "text"},
        {"name": "field3", "label": "Field 3", "type": "number"}
    ]
}

# Horizontal layout (arranges fields in a row)
horizontal_config = {
    "window": {"title": "Horizontal Layout", "width": 600, "height": 200},
    "layout": "horizontal",
    "fields": [
        {"name": "first", "label": "First", "type": "text"},
        {"name": "middle", "label": "Middle", "type": "text"},
        {"name": "last", "label": "Last", "type": "text"}
    ]
}

# Grid layout (responsive 2-column grid)
grid_config = {
    "window": {"title": "Grid Layout", "width": 600, "height": 400},
    "layout": "grid",
    "fields": [
        {"name": "fname", "label": "First Name", "type": "text"},
        {"name": "lname", "label": "Last Name", "type": "text"},
        {"name": "email", "label": "Email", "type": "email"},
        {"name": "phone", "label": "Phone", "type": "text"},
        {"name": "city", "label": "City", "type": "text"},
        {"name": "state", "label": "State", "type": "text"}
    ]
}

# Form layout (label-field pairs)
form_config = {
    "window": {"title": "Form Layout", "width": 500, "height": 400},
    "layout": "form",
    "fields": [
        {"name": "username", "label": "Username", "type": "text"},
        {"name": "password", "label": "Password", "type": "password"},
        {"name": "remember", "label": "Remember me", "type": "checkbox"}
    ]
}

# Use different layouts in tabs
tabbed_layout_config = {
    "window": {"title": "Mixed Layouts", "width": 600, "height": 500},
    "fields": [
        {"name": "v1", "label": "Field 1", "type": "text"},
        {"name": "v2", "label": "Field 2", "type": "text"},
        {"name": "g1", "label": "Field 1", "type": "text"},
        {"name": "g2", "label": "Field 2", "type": "text"},
        {"name": "g3", "label": "Field 3", "type": "text"},
        {"name": "g4", "label": "Field 4", "type": "text"}
    ],
    "use_tabs": True,
    "tabs": [
        {
            "name": "vertical_tab",
            "title": "Vertical Tab",
            "layout": "vertical",
            "fields": ["v1", "v2"]
        },
        {
            "name": "grid_tab",
            "title": "Grid Tab",
            "layout": "grid",
            "fields": ["g1", "g2", "g3", "g4"]
        }
    ]
}

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = GuiBuilder(config_dict=grid_config, backend='qt')
    gui.show()

    sys.exit(app.exec())
