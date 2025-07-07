"""
GTK backend for qtpyguihelper using PyGObject/GTK3.

This module provides GTK-based implementations for creating GUI forms
and widgets using the PyGObject library.
"""

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk

    from .gtk_widget_factory import GtkWidgetFactory
    from .gtk_gui_builder import GtkGuiBuilder

    __all__ = ['GtkWidgetFactory', 'GtkGuiBuilder']

except ImportError as e:
    # GTK not available
    class _GTKNotAvailable:
        def __init__(self, *args, **kwargs):
            raise ImportError(f"GTK not available: {e}")

    GtkWidgetFactory = _GTKNotAvailable
    GtkGuiBuilder = _GTKNotAvailable

    __all__ = []
