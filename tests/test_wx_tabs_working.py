#!/usr/bin/env python3
"""
Test wxPython backend with tabs using existing tabbed_config.json.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_wx_tabs() -> None:
    """Test wxPython backend with tabs using the existing tabbed_config.json."""
    print("Testing wxPython backend with tabs...")

    try:
        # Force wxPython backend
        from vibegui import set_backend
        set_backend('wx')
        print("✓ wxPython backend selected")

        import wx

        # Use the existing tabbed_config.json file
        config_path = os.path.join(os.path.dirname(__file__), "..", "examples", "tabbed_config.json")

        from vibegui import GuiBuilder

        # Create wxPython application
        from .wx_test_utils import create_wx_app
        app = create_wx_app()

        # Create GUI builder with the existing configuration
        gui_builder = GuiBuilder(config_path=config_path)

        def on_submit(form_data: dict) -> None:
            print("wxPython tabs form submitted:")
            for key, value in form_data.items():
                print(f"  {key}: {value}")
            wx.MessageBox("Configuration saved successfully!", "Success", wx.OK | wx.ICON_INFORMATION)

        def on_cancel() -> None:
            print("wxPython tabs form cancelled")

        # Register callbacks
        gui_builder.set_submit_callback(on_submit)
        gui_builder.set_cancel_callback(on_cancel)

        # Show the GUI
        gui_builder.show()

        print("✓ wxPython tabbed GUI created successfully")
        print("  - Check that fields in tabs expand to fit the window width")

        # Use the utility function to handle pytest vs direct execution
        try:
            from .wx_test_utils import run_wx_gui_for_test
        except ImportError:
            from wx_test_utils import run_wx_gui_for_test

        run_wx_gui_for_test(app, gui_builder)

    except ImportError as e:
        print(f"✗ wxPython not available: {e}")
    except Exception as e:
        print(f"✗ Error with wxPython tabs: {e}")
        import traceback
        traceback.print_exc()

