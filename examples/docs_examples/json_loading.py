"""JSON configuration loading example."""
from vibegui import GuiBuilder
from qtpy.QtWidgets import QApplication
import sys
import os
from pathlib import Path

# Get the path to the example JSON file
example_json = Path(__file__).parent / "example_config.json"

if __name__ == "__main__":
    # Load from JSON file
    app = QApplication(sys.argv)
    gui = GuiBuilder(config_path=str(example_json), backend='qt')
    gui.show()

    sys.exit(app.exec())
