#!/usr/bin/env python3
"""
Example showing how to set the Qt backend for vibegui.
This demonstrates the flexibility of using qtpy for Qt binding compatibility.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def demo_pyside6() -> None:
    """Demo using PySide6 backend."""
    print("Setting Qt backend to PySide6...")
    os.environ['QT_API'] = 'pyside6'

    # Import and run demo
    from vibegui import GuiBuilder
    from qtpy.QtWidgets import QApplication

    print(f"Using Qt backend: {os.environ.get('QT_API', 'default')}")

    # Simple config for demo
    config = {
        "window": {"title": "PySide6 Demo", "width": 400, "height": 200},
        "layout": "form",
        "fields": [
            {"name": "backend_info", "type": "text", "label": "Qt Backend", "default_value": "PySide6"},
            {"name": "version_info", "type": "text", "label": "Info", "default_value": "Using PySide6 via qtpy"}
        ],
        "submit_button": True
    }

    app = QApplication(sys.argv)
    gui = GuiBuilder(config_dict=config)
    gui.show()
    app.exec()


def demo_pyqt6() -> None:
    """Demo using PyQt6 backend."""
    print("Setting Qt backend to PyQt6...")
    os.environ['QT_API'] = 'pyqt6'

    try:
        # Import and run demo
        from vibegui import GuiBuilder
        from qtpy.QtWidgets import QApplication

        print(f"Using Qt backend: {os.environ.get('QT_API', 'default')}")

        # Simple config for demo
        config = {
            "window": {"title": "PyQt6 Demo", "width": 400, "height": 200},
            "layout": "form",
            "fields": [
                {"name": "backend_info", "type": "text", "label": "Qt Backend", "default_value": "PyQt6"},
                {"name": "version_info", "type": "text", "label": "Info", "default_value": "Using PyQt6 via qtpy"}
            ],
            "submit_button": True
        }

        app = QApplication(sys.argv)
        gui = GuiBuilder(config_dict=config)
        gui.show()
        app.exec()

    except ImportError as e:
        print(f"PyQt6 not available: {e}")

def show_current_backend() -> None:
    """Show which Qt backend is currently being used."""
    try:
        import qtpy
        print(f"Current qtpy API: {qtpy.API_NAME}")
        print(f"Qt version: {qtpy.QT_VERSION}")
        print(f"qtpy version: {qtpy.__version__}")

        # Show available APIs
        print("\nAvailable Qt APIs:")
        available_apis = []

        try:
            import PySide6
            available_apis.append(f"PySide6 {PySide6.__version__}")
        except ImportError:
            pass

        try:
            import PyQt6
            available_apis.append(f"PyQt6 {PyQt6.QtCore.QT_VERSION_STR}")
        except ImportError:
            pass

        if available_apis:
            for api in available_apis:
                print(f"  - {api}")
        else:
            print("  - No Qt APIs detected")

    except ImportError:
        print("qtpy not available")


def main() -> None:
    """Main function to demonstrate Qt backend selection."""
    if len(sys.argv) > 1:
        backend = sys.argv[1].lower()
    else:
        print("Qt Backend Demo for vibegui")
        print("Available commands:")
        print("  python qt_backend_demo.py pyside6  - Use PySide6")
        print("  python qt_backend_demo.py pyqt6    - Use PyQt6")
        print("  python qt_backend_demo.py info     - Show current backend info")
        print()
        backend = input("Enter backend (pyside6/pyqt6/info): ").lower()

    if backend == "pyside6":
        demo_pyside6()
    elif backend == "pyqt6":
        demo_pyqt6()
    elif backend == "info":
        show_current_backend()
    else:
        print(f"Unknown backend: {backend}")
        print("Available options: pyside6, pyqt6, info")


if __name__ == "__main__":
    main()
