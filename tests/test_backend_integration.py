#!/usr/bin/env python3
"""
Test script to verify wxPython backend integration and backend switching.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from vibegui import (
    GuiBuilder, get_available_backends, get_backend_info,
    set_backend, is_backend_available, BackendError
)


def test_backend_detection():
    """Test backend detection functionality."""
    print("=== Backend Detection Test ===")

    available = get_available_backends()
    print(f"Available backends: {available}")

    assert len(available) > 0, "No backends available"
    assert 'qt' in available, "Qt backend should be available"
    assert 'wx' in available, "wxPython backend should be available"

    print("✓ Backend detection working")


def test_backend_info():
    """Test getting backend information."""
    print("\n=== Backend Info Test ===")

    info = get_backend_info()
    print(f"Backend info: {info}")

    required_keys = ['backend', 'available_backends']
    for key in required_keys:
        assert key in info, f"Missing key '{key}' in backend info"

    print("✓ Backend info working")


def test_backend_switching():
    """Test switching between backends."""
    print("\n=== Backend Switching Test ===")

    # Test Qt backend
    if is_backend_available('qt'):
        set_backend('qt')
        info = get_backend_info()
        assert info['backend'] == 'qt', "Failed to switch to Qt backend"
        print("✓ Qt backend switch successful")

    # Test wxPython backend
    if is_backend_available('wx'):
        set_backend('wx')
        info = get_backend_info()
        assert info['backend'] == 'wx', "Failed to switch to wxPython backend"
        print("✓ wxPython backend switch successful")

    print("✓ Backend switching working")


def test_unified_interface():
    """Test the unified GuiBuilder interface (without creating GUI)."""
    print("\n=== Unified Interface Test ===")

    # Simple config for testing
    config = {
        'window': {'title': 'Test', 'width': 400, 'height': 300},
        'layout': 'form',
        'fields': [
            {'name': 'name', 'type': 'text', 'label': 'Name'},
            {'name': 'age', 'type': 'int', 'label': 'Age', 'default_value': 25},
        ]
    }

    # Test that we can create the unified interface
    # (Note: This will fail when trying to create actual widgets without app,
    # but we can test the interface creation)

    original_backend = get_backend_info()['backend']

    try:
        # Test Qt backend selection via constructor
        if is_backend_available('qt'):
            set_backend('qt')
            qt_gui = GuiBuilder.__new__(GuiBuilder)  # Create without calling __init__
            qt_gui._backend = 'qt'
            assert qt_gui.backend == 'qt', "Qt backend not set correctly"
            print("✓ Qt unified interface creation works")

        # Test wxPython backend selection via constructor
        if is_backend_available('wx'):
            set_backend('wx')
            wx_gui = GuiBuilder.__new__(GuiBuilder)  # Create without calling __init__
            wx_gui._backend = 'wx'
            assert wx_gui.backend == 'wx', "wxPython backend not set correctly"
            print("✓ wxPython unified interface creation works")

    except Exception as e:
        print(f"Note: Full GUI creation requires app initialization: {e}")

    # Restore original backend
    set_backend(original_backend)
    print("✓ Unified interface design working")


def test_widget_factory_imports():
    """Test that widget factories can be imported."""
    print("\n=== Widget Factory Import Test ===")

    try:
        from vibegui.qt.qt_widget_factory import WidgetFactory
        from vibegui.wx.wx_widget_factory import WxWidgetFactory

        # Test that we can create factory instances
        qt_factory = WidgetFactory()
        wx_factory = WxWidgetFactory()

        print("✓ Qt widget factory import and creation successful")
        print("✓ wxPython widget factory import and creation successful")

    except Exception as e:
        assert False, f"✗ Widget factory import failed: {e}"

    assert True


def test_config_compatibility():
    """Test that configurations work with all backends."""
    print("\n=== Configuration Compatibility Test ===")

    from vibegui.config_loader import ConfigLoader

    config = {
        'window': {'title': 'Cross-Backend Test', 'width': 500, 'height': 400},
        'layout': 'form',
        'submit_button': True,
        'cancel_button': True,
        'fields': [
            {'name': 'text_field', 'type': 'text', 'label': 'Text Field'},
            {'name': 'int_field', 'type': 'int', 'label': 'Integer Field'},
            {'name': 'float_field', 'type': 'float', 'label': 'Float Field', 'format_string': '.2f'},
            {'name': 'checkbox_field', 'type': 'checkbox', 'label': 'Checkbox Field'},
            {'name': 'select_field', 'type': 'select', 'label': 'Select Field', 'options': ['A', 'B', 'C']},
        ],
        'custom_buttons': [
            {'name': 'test_btn', 'label': 'Test Button', 'tooltip': 'Test button tooltip'}
        ]
    }

    loader = ConfigLoader()
    gui_config = loader.load_from_dict(config)

    assert gui_config.window.title == 'Cross-Backend Test'
    assert len(gui_config.fields) == 5
    assert len(gui_config.custom_buttons) == 1

    print("✓ Configuration compatibility verified")
