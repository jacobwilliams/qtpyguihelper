"""
GTK backend for vibegui using PyGObject/GTK3 or GTK4.

This module provides GTK-based implementations for creating GUI forms
and widgets using the PyGObject library. It automatically detects and
supports both GTK3 and GTK4 versions.
"""

import os

# Allow user to force a specific GTK version via environment variable
FORCE_GTK_VERSION = os.environ.get('vibegui_GTK_VERSION')

def _detect_gtk_version() -> tuple[str, object]:
    """Detect available GTK version and return version info."""
    try:
        import gi

        # Try user-specified version first
        if FORCE_GTK_VERSION:
            try:
                gi.require_version('Gtk', FORCE_GTK_VERSION)
                from gi.repository import Gtk
                return FORCE_GTK_VERSION, Gtk
            except (ValueError, ImportError):
                pass

        # Try GTK4 first (newer version)
        try:
            gi.require_version('Gtk', '4.0')
            from gi.repository import Gtk
            return '4.0', Gtk
        except (ValueError, ImportError):
            pass

        # Fallback to GTK3
        try:
            gi.require_version('Gtk', '3.0')
            from gi.repository import Gtk
            return '3.0', Gtk
        except (ValueError, ImportError):
            pass

        raise ImportError("No compatible GTK version found (tried 4.0, 3.0)")

    except ImportError as e:
        raise ImportError(f"PyGObject (gi) not available: {e}")

try:
    GTK_VERSION, Gtk = _detect_gtk_version()

    # Import our GTK widgets with version info
    from .gtk_widget_factory import GtkWidgetFactory
    from .gtk_gui_builder import GtkGuiBuilder

    # Store version info for runtime access
    GTK_MAJOR_VERSION = int(GTK_VERSION.split('.')[0])

    __all__ = ['GtkWidgetFactory', 'GtkGuiBuilder', 'GTK_VERSION', 'GTK_MAJOR_VERSION', 'Gtk']

except ImportError as e:
    # GTK not available
    class _GTKNotAvailable:
        def __init__(self, *args, **kwargs) -> None:
            raise ImportError(f"GTK not available: {e}")

    GtkWidgetFactory = _GTKNotAvailable
    GtkGuiBuilder = _GTKNotAvailable
    GTK_VERSION = None
    GTK_MAJOR_VERSION = None
    Gtk = None

    __all__ = []
