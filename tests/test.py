import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from vibegui import GuiBuilder

def test_create_and_run() -> None:
    """Test creating and running a GUI with the Qt backend."""

    print("Testing GUI creation and run with Qt backend...")

    # Simple configuration
    config = {
        "window": {"title": "My App", "width": 400, "height": 300},
        "fields": [
            {"name": "username", "label": "Username", "type": "text", "required": True},
            {"name": "email", "label": "Email", "type": "email", "required": True},
            {"name": "age", "label": "Age", "type": "number"}
        ]
    }

    # Create and run the GUI
    gui = GuiBuilder.create_and_run(config_dict=config, backend='qt')
