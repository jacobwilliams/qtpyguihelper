#!/usr/bin/env python3
"""
Utilities for wxPython testing that work properly with pytest.
"""

import sys
import os


def is_running_under_pytest():
    """Check if we're running under pytest."""
    return "pytest" in sys.modules or "PYTEST_CURRENT_TEST" in os.environ


def run_wx_gui_for_test(app, gui):
    """
    Helper function to run wxPython GUI appropriately for test environment.

    Args:
        app: wx.App instance
        gui: GUI builder instance with a window
    """

    if is_running_under_pytest():
        print("✓ GUI created successfully! (pytest mode - not running MainLoop)")
        # In pytest mode, just verify the GUI was created and close it
        try:
            if hasattr(gui, 'window') and gui.window:
                gui.window.Close()
            elif hasattr(gui, 'Close'):
                gui.Close()
        except (AttributeError, RuntimeError):
            # Window might already be closed or invalid
            pass
    else:
        print("✓ GUI created successfully! Close the window to exit.")
        # Run the application only when not in pytest
        app.MainLoop()


def create_wx_app():
    """
    Create or get existing wx.App instance.

    Returns:
        wx.App instance
    """
    import wx

    # Get existing app or create new one
    if not wx.App.Get():
        app = wx.App()
    else:
        app = wx.App.Get()

    return app


def safe_wx_message_box(message, title="Info", style=None):
    """
    Show a message box safely, handling cases where wx might not be available.

    Args:
        message: Message to show
        title: Title of the message box
        style: wx message box style (e.g., wx.OK | wx.ICON_INFORMATION)
    """
    try:
        import wx
        if style is None:
            style = wx.OK | wx.ICON_INFORMATION

        # Only show message box if not running under pytest
        if not is_running_under_pytest():
            wx.MessageBox(message, title, style)
        else:
            print(f"{title}: {message}")
    except (ImportError, AttributeError, RuntimeError):
        # Fallback to console output
        print(f"{title}: {message}")
