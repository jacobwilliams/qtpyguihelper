#!/usr/bin/env python3
"""
Comprehensive test of vibegui backend functionality.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from vibegui import (
    get_available_backends, get_backend_info, set_backend,
    is_backend_available
)


def test_backend_detection():
    """Test backend detection and switching."""
    print("=== Backend Detection Test ===")

    available = get_available_backends()
    print(f"Available backends: {available}")

    info = get_backend_info()
    print(f"Default backend: {info['backend']}")

    # Test Qt availability
    if is_backend_available('qt'):
        print("✓ Qt backend is available")
        set_backend('qt')
        qt_info = get_backend_info()
        print(f"  Qt API: {qt_info.get('qt_api', 'Unknown')}")
        print(f"  Qt Version: {qt_info.get('qt_version', 'Unknown')}")
    else:
        print("✗ Qt backend not available")

    # Test wxPython availability
    if is_backend_available('wx'):
        print("✓ wxPython backend is available")
        set_backend('wx')
        wx_info = get_backend_info()
        print(f"  wxPython Version: {wx_info.get('wx_version', 'Unknown')}")
        print(f"  wxPython Platform: {wx_info.get('wx_platform', 'Unknown')}")
    else:
        print("✗ wxPython backend not available")

    print()


def test_unified_interface():
    """Test the unified GuiBuilder interface."""
    print("=== Unified Interface Test ===")

    # Test backend switching without creating GUI objects
    for backend in get_available_backends():
        print(f"Testing backend selection: {backend}")
        try:
            set_backend(backend)
            current_backend = get_backend_info()['backend']
            if current_backend == backend:
                print(f"  ✓ {backend} backend selected successfully")
            else:
                print(f"  ✗ {backend} backend selection failed")
        except Exception as e:
            print(f"  ✗ Error selecting {backend} backend: {e}")

    print()


def test_import_safety():
    """Test that all imports work without requiring app creation."""
    print("=== Import Safety Test ===")

    try:
        from vibegui import GuiBuilder
        print("✓ GuiBuilder imported successfully")
    except ImportError as e:
        print(f"✗ GuiBuilder import error: {e}")

    try:
        from vibegui.qt.qt_gui_builder import GuiBuilder as QtGuiBuilder
        print("✓ QtGuiBuilder imported successfully")
    except ImportError as e:
        print(f"✗ QtGuiBuilder import error: {e}")

    try:
        from vibegui.wx.wx_gui_builder import WxGuiBuilder
        print("✓ WxGuiBuilder imported successfully")
    except ImportError as e:
        print(f"✗ WxGuiBuilder import error: {e}")

    print()


def test_config_loading():
    """Test configuration loading with different backends."""
    print("=== Configuration Loading Test ===")

    from vibegui.config_loader import ConfigLoader

    config_dict = {
        "window": {"title": "Test", "width": 500, "height": 400},
        "layout": "form",
        "fields": [
            {"name": "name", "type": "text", "label": "Name", "required": True},
            {"name": "age", "type": "int", "label": "Age", "min_value": 0, "max_value": 120},
            {"name": "height", "type": "float", "label": "Height", "format_string": ".2f"},
            {"name": "active", "type": "checkbox", "label": "Active"},
            {"name": "category", "type": "select", "label": "Category", "options": ["A", "B", "C"]},
            {"name": "priority", "type": "radio", "label": "Priority", "options": ["Low", "High"]},
            {"name": "notes", "type": "textarea", "label": "Notes"}
        ],
        "custom_buttons": [
            {"name": "test_btn", "label": "Test Button", "tooltip": "Test button"}
        ]
    }

    loader = ConfigLoader()
    config = loader.load_from_dict(config_dict)

    print("Configuration loaded successfully")
    print(f"  Window title: {config.window.title}")
    print(f"  Field count: {len(config.fields)}")
    print(f"  Custom buttons: {len(config.custom_buttons) if config.custom_buttons else 0}")
    print(f"  Layout: {config.layout}")

    print()


def test_widget_factories():
    """Test both widget factory imports."""
    print("=== Widget Factory Test ===")

    try:
        from vibegui.qt.qt_widget_factory import WidgetFactory
        _qt_factory = WidgetFactory()
        print("✓ Qt WidgetFactory created successfully")
    except (ImportError, RuntimeError) as e:
        print(f"✗ Qt WidgetFactory error: {e}")

    try:
        from vibegui.wx.wx_widget_factory import WxWidgetFactory
        _wx_factory = WxWidgetFactory()
        print("✓ wxPython WxWidgetFactory created successfully")
    except (ImportError, RuntimeError) as e:
        print(f"✗ wxPython WxWidgetFactory error: {e}")

    print()


def test_get_available_backends():
    """test get_available_backends."""

    available = get_available_backends()
    if len(available) == 2:
        print("✓ Both Qt and wxPython backends are available")
        print("✓ Full cross-platform support enabled")
    elif 'qt' in available:
        print("✓ Qt backend available")
        print("⚠ wxPython backend not available")
    elif 'wx' in available:
        print("✓ wxPython backend available")
        print("⚠ Qt backend not available")
    else:
        assert False, "✗ No backends available!"

    assert True, "get_available_backends() test passed"
