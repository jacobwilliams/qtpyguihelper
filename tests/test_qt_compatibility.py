#!/usr/bin/env python3
"""
Test script to verify Qt backend compatibility.
"""

import os
import sys

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def test_qtpy_imports() -> None:
    """Test that qtpy imports work correctly."""
    print("Testing qtpy imports...")

    try:
        # Test core qtpy functionality
        import qtpy
        print(f"✓ qtpy version: {qtpy.__version__}")
        print(f"✓ Current API: {qtpy.API_NAME}")
        print(f"✓ Qt version: {qtpy.QT_VERSION}")

        # Test widget imports
        from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout
        from qtpy.QtCore import Qt, Signal
        from qtpy.QtGui import QIcon
        print("✓ Qt widget imports successful")

        # Test library imports
        from vibegui import GuiBuilder
        from vibegui.qt.qt_widget_factory import WidgetFactory
        from vibegui.config_loader import ConfigLoader
        print("✓ vibegui imports successful")
        assert True, "All qtpy imports successful"

    except ImportError as e:
        print(f"❌ Import error: {e}")
        assert False, "Import error occurred"


def test_simple_gui_creation() -> None:
    """Test creating a simple GUI without showing it."""
    print("\nTesting GUI creation...")

    try:
        from vibegui import GuiBuilder
        from qtpy.QtWidgets import QApplication
        import sys

        # Create QApplication if needed
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)

        # Simple test config
        config = {
            "window": {"title": "Test", "width": 300, "height": 200},
            "fields": [
                {"name": "test_field", "type": "text", "label": "Test Field"}
            ]
        }

        # Create GUI (don't show it)
        gui = GuiBuilder(config_dict=config)

        # Test basic functionality
        assert gui.builder.config is not None
        assert gui.builder.config.window.title == "Test"
        assert len(gui.builder.config.fields) == 1

        print("✓ GUI creation successful")
        assert True, "GUI created successfully"

    except Exception as e:
        print(f"❌ GUI creation error: {e}")
        assert False, "GUI creation failed"


def test_available_backends() -> None:
    """Test which Qt backends are available."""
    print("\nTesting available Qt backends...")

    backends = []

    # Test PySide6
    try:
        import PySide6
        backends.append(f"PySide6 {PySide6.__version__}")
        print(f"✓ PySide6 available: {PySide6.__version__}")
    except ImportError:
        print("⚠ PySide6 not available")

    # Test PyQt6
    try:
        import PyQt6
        backends.append(f"PyQt6 {PyQt6.QtCore.QT_VERSION_STR}")
        print(f"✓ PyQt6 available: {PyQt6.QtCore.QT_VERSION_STR}")
    except ImportError:
        print("⚠ PyQt6 not available")

    if not backends:
        print("❌ No Qt backends available!")
        assert False, "No Qt backends available"

    print(f"✓ Found {len(backends)} Qt backend(s)")
    assert True, "Qt backends available"
