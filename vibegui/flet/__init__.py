"""
Flet backend for vibegui.

Flet is a modern Python framework for building interactive multi-platform
applications with Material Design UI.
"""

from .flet_gui_builder import FletGuiBuilder
from .flet_widget_factory import FletWidgetFactory

__all__ = ['FletGuiBuilder', 'FletWidgetFactory']
