#!/usr/bin/env python3
"""
Test script for GTK version compatibility.
"""

import os
import sys

def test_gtk_detection():
    """Test GTK version detection."""
    print("Testing GTK version detection...")

    try:
        # Test with no forced version
        if 'vibegui_GTK_VERSION' in os.environ:
            del os.environ['vibegui_GTK_VERSION']

        # Import our GTK module
        from vibegui.gtk import GTK_VERSION, GTK_MAJOR_VERSION, Gtk

        print(f"Detected GTK version: {GTK_VERSION}")
        print(f"GTK major version: {GTK_MAJOR_VERSION}")
        print(f"GTK module: {Gtk}")

        # Test creating a simple window
        print("\nTesting window creation...")
        import vibegui
        vibegui.set_backend('gtk')

        config = {
            'window': {'title': 'GTK Version Test', 'width': 400, 'height': 300},
            'fields': [
                {'type': 'text', 'key': 'test', 'name': 'test', 'label': 'Test Field'}
            ]
        }

        gui = vibegui.GuiBuilder(config_dict=config)
        print(f"GUI backend: {gui.backend}")
        print("GTK GUI created successfully!")

        assert True, "GTK version detection and GUI creation successful"

    except ImportError as e:
        print(f"GTK not available: {e}")
        assert False, "GTK not available. Ensure GTK is installed and accessible."
    except Exception as e:
        print(f"Error: {e}")
        assert False, f"Unexpected error during GTK version detection: {e}"
