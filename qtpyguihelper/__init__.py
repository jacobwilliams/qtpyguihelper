"""
QtPyGuiHelper - A Python library for creating GUI applications from JSON configuration files.

This library allows you to define GUI layouts, widgets, and their properties in JSON format
and automatically generate the corresponding interface using either Qt (PySide6/PyQt6) or wxPython.

Backend Support:
- Qt backend via qtpy (supports PySide6/PyQt6)
- wxPython backend as an alternative
- tkinter backend (built into Python)

Usage:
    # Using the unified interface (auto-detects backend)
    from qtpyguihelper import GuiBuilder
    app = GuiBuilder.create_and_run('config.json')

    # Explicit backend selection
    from qtpyguihelper import set_backend, GuiBuilder
    set_backend('tk')  # or 'qt' or 'wx'
    app = GuiBuilder.create_and_run('config.json')
"""

from .qt.gui_builder import GuiBuilder as QtGuiBuilder
from .qt.widget_factory import WidgetFactory
from .wx.wx_gui_builder import WxGuiBuilder
from .wx.wx_widget_factory import WxWidgetFactory
from .tk.tk_gui_builder import TkGuiBuilder
from .tk.tk_widget_factory import TkWidgetFactory
from .config_loader import ConfigLoader, CustomButtonConfig
from .backend import (
    get_backend, set_backend, get_available_backends,
    get_backend_info, is_backend_available, BackendError
)
from typing import Dict, Any, Optional, Union


class GuiBuilder:
    """
    Unified GUI builder that automatically selects the appropriate backend.

    This class provides a consistent interface that works with Qt, wxPython,
    and tkinter backends, automatically selecting the available backend or using
    the one specified via set_backend().
    """

    def __init__(self, config_path: Optional[str] = None, config_dict: Optional[Dict[str, Any]] = None, backend: Optional[str] = None):
        """
        Initialize the GUI builder with automatic backend selection.

        Args:
            config_path: Path to JSON configuration file
            config_dict: Configuration dictionary (alternative to config_path)
            backend: Force a specific backend ('qt' or 'wx'). If None, auto-detects.
        """
        self._backend = None
        self._builder = None

        # Set backend if specified
        if backend:
            if not is_backend_available(backend):
                raise BackendError(f"Backend '{backend}' is not available")
            set_backend(backend)

        # Get current backend
        self._backend = get_backend()

        # Create appropriate builder
        if self._backend == 'qt':
            self._builder = QtGuiBuilder(config_path, config_dict)
        elif self._backend == 'wx':
            self._builder = WxGuiBuilder(config_path, config_dict)
        elif self._backend == 'tk':
            self._builder = TkGuiBuilder(config_path, config_dict)
        else:
            raise BackendError(f"Unsupported backend: {self._backend}")

    @property
    def backend(self) -> str:
        """Get the current backend being used."""
        return self._backend

    @property
    def builder(self) -> Union[QtGuiBuilder, WxGuiBuilder, TkGuiBuilder]:
        """Get the underlying builder instance."""
        return self._builder

    def show(self):
        """Show the GUI window."""
        if hasattr(self._builder, 'show'):
            self._builder.show()
        elif hasattr(self._builder, 'Show'):
            self._builder.Show()

    def hide(self):
        """Hide the GUI window."""
        if hasattr(self._builder, 'hide'):
            self._builder.hide()
        elif hasattr(self._builder, 'Hide'):
            self._builder.Hide()

    def get_form_data(self) -> Dict[str, Any]:
        """Get all form data as a dictionary."""
        return self._builder.get_form_data()

    def set_form_data(self, data: Dict[str, Any]):
        """Set form data from a dictionary."""
        self._builder.set_form_data(data)

    def clear_form(self):
        """Clear all form fields."""
        self._builder.clear_form()

    def get_field_value(self, field_name: str) -> Any:
        """Get the value of a specific field."""
        return self._builder.get_field_value(field_name)

    def set_field_value(self, field_name: str, value: Any) -> bool:
        """Set the value of a specific field."""
        return self._builder.set_field_value(field_name, value)

    def set_submit_callback(self, callback):
        """Set a callback function to be called when the form is submitted."""
        self._builder.set_submit_callback(callback)

    def set_cancel_callback(self, callback):
        """Set a callback function to be called when the form is cancelled."""
        self._builder.set_cancel_callback(callback)

    def set_custom_button_callback(self, button_name: str, callback):
        """Set a callback function to be called when a custom button is clicked."""
        self._builder.set_custom_button_callback(button_name, callback)

    def remove_custom_button_callback(self, button_name: str):
        """Remove a custom button callback."""
        self._builder.remove_custom_button_callback(button_name)

    def get_custom_button_names(self):
        """Get a list of all custom button names from the configuration."""
        return self._builder.get_custom_button_names()

    def enable_field(self, field_name: str, enabled: bool = True):
        """Enable or disable a specific field."""
        self._builder.enable_field(field_name, enabled)

    def show_field(self, field_name: str, visible: bool = True):
        """Show or hide a specific field."""
        self._builder.show_field(field_name, visible)

    def load_data_from_file(self, data_file_path: str) -> bool:
        """Load form data from a JSON file and populate the GUI."""
        return self._builder.load_data_from_file(data_file_path)

    def load_data_from_dict(self, data: Dict[str, Any]) -> bool:
        """Load form data from a dictionary and populate the GUI."""
        return self._builder.load_data_from_dict(data)

    def save_data_to_file(self, data_file_path: str, include_empty: bool = True) -> bool:
        """Save current form data to a JSON file."""
        return self._builder.save_data_to_file(data_file_path, include_empty)

    def run(self):
        """Run the GUI application (start the main loop)."""
        if hasattr(self._builder, 'run'):
            self._builder.run()
        else:
            # For backends that don't have a run method, try to show and start mainloop
            self.show()
            if hasattr(self._builder, 'mainloop'):
                self._builder.mainloop()

    def close(self):
        """Close the GUI application."""
        if hasattr(self._builder, 'close'):
            self._builder.close()

    @staticmethod
    def create_and_run(config_path: Optional[str] = None,
                      config_dict: Optional[Dict[str, Any]] = None,
                      backend: Optional[str] = None):
        """
        Create and run a GUI application with automatic backend detection.

        Args:
            config_path: Path to JSON configuration file
            config_dict: Configuration dictionary (alternative to config_path)
            backend: Force a specific backend ('qt' or 'wx'). If None, auto-detects.

        Returns:
            GuiBuilder instance
        """
        # Set backend if specified
        if backend:
            set_backend(backend)

        current_backend = get_backend()

        if current_backend == 'qt':
            return QtGuiBuilder.create_and_run(config_path, config_dict)
        elif current_backend == 'wx':
            return WxGuiBuilder.create_and_run(config_path, config_dict)
        elif current_backend == 'tk':
            return TkGuiBuilder.create_and_run(config_path, config_dict)
        else:
            raise BackendError(f"Unsupported backend: {current_backend}")


__version__ = "1.0.0"
__author__ = "QtPyGuiHelper Team"

__all__ = [
    "GuiBuilder", "QtGuiBuilder", "WxGuiBuilder", "TkGuiBuilder",
    "ConfigLoader", "WidgetFactory", "WxWidgetFactory", "TkWidgetFactory", "CustomButtonConfig",
    "get_backend", "set_backend", "get_available_backends",
    "get_backend_info", "is_backend_available", "BackendError"
]
