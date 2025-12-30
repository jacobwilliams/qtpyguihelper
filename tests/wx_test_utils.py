#!/usr/bin/env python3
"""
Utilities for wxPython testing that work properly with pytest.
"""

import sys
import os


def run_wx_gui_for_test(app: object, gui: object) -> None:
    """
    Helper function to run wxPython GUI appropriately for test environment.

    Args:
        app: wx.App instance
        gui: GUI builder instance with a window
    """

    print("✓ GUI created successfully! Close the window to exit.")
    # Run the application only when not in pytest
    app.MainLoop()


def is_running_under_pytest() -> bool:
    """Check if we're running under pytest."""
    # More reliable way - check for pytest-specific environment variables
    # or if we're being called by pytest
    return (
        "PYTEST_CURRENT_TEST" in os.environ or
        hasattr(sys, '_called_from_test') or
        any('pytest' in arg for arg in sys.argv) or
        any('py.test' in arg for arg in sys.argv)
    )

def create_wx_app() -> object:
    """
    Create or get existing wx.App instance.
    Properly handles multiple test scenarios and Qt/wx conflicts.

    Returns:
        wx.App instance
    """
    import wx

    # If we're running under pytest and there might be Qt apps running,
    # we need to be more careful about app creation
    if is_running_under_pytest():
        # Check for existing Qt applications that might conflict
        try:
            # Try to import qtpy and check for QApplication
            from qtpy.QtWidgets import QApplication
            qt_app = QApplication.instance()
            if qt_app:
                # There's a Qt application running - this might cause conflicts
                print("Warning: Qt application detected, ensuring wxPython compatibility...")
        except ImportError:
            # qtpy not available, no conflict
            pass

    # Check if there's already a wx app instance
    existing_app = wx.App.Get()
    if existing_app:
        return existing_app

    # Create new app only if none exists
    # Use False parameter to avoid redirecting stdout/stderr in tests
    try:
        app = wx.App(False)
        return app
    except Exception as e:
        # If app creation fails (possibly due to Qt conflicts), try to handle it
        print(f"Warning: Failed to create wx.App: {e}")
        # Try to get existing app or create with different parameters
        existing_app = wx.App.Get()
        if existing_app:
            return existing_app
        raise


def safe_wx_message_box(message: str, title: str = "Info", style: object = None) -> None:
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


def cleanup_wx_test() -> None:
    """
    Clean up after wxPython test to prevent conflicts between tests.
    """
    try:
        import wx

        # Close all top-level windows
        for window in wx.GetTopLevelWindows():
            try:
                if window and not window.IsBeingDeleted():
                    window.Close(True)
            except (AttributeError, RuntimeError):
                pass

        # Process pending events
        app = wx.App.Get()
        if app:
            try:
                app.ProcessPendingEvents()
                wx.SafeYield()
            except (AttributeError, RuntimeError):
                pass

    except (ImportError, RuntimeError):
        pass

