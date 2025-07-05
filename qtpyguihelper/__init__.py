"""
QtPyGuiHelper - A Python library for creating PySide6 GUIs from JSON configuration files.

This library allows you to define GUI layouts, widgets, and their properties in JSON format
and automatically generate the corresponding PySide6 interface.
"""

from .gui_builder import GuiBuilder
from .config_loader import ConfigLoader, CustomButtonConfig
from .widget_factory import WidgetFactory

__version__ = "1.0.0"
__author__ = "QtPyGuiHelper Team"

__all__ = ["GuiBuilder", "ConfigLoader", "WidgetFactory", "CustomButtonConfig"]
