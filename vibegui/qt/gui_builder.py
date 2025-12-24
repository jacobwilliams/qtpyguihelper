"""
Main GUI builder class that creates Qt applications from JSON configuration.
Compatible with both PySide6 and PyQt6 via qtpy.
"""

from __future__ import annotations

import json
import sys
from typing import Dict, Any, Callable, Optional, List
from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QGridLayout, QPushButton, QScrollArea, QMessageBox,
    QTabWidget, QLayout
)
from qtpy.QtCore import Qt, Signal, QDateTime
from qtpy.QtGui import QIcon

from ..config_loader import ConfigLoader, GuiConfig
from ..utils import FileUtils, ValidationUtils
from .widget_factory import WidgetFactory, get_nested_value


class GuiBuilder(QMainWindow):
    """Main GUI builder class that creates Qt applications from JSON configuration."""

    # Signals
    formSubmitted = Signal(dict)  # Emitted when form is submitted with data
    formCancelled = Signal()      # Emitted when form is cancelled
    fieldChanged = Signal(str, object)  # Emitted when a field value changes

    def __init__(self, config_path: Optional[str] = None, config_dict: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the GUI builder.

        Args:
            config_path: Path to JSON configuration file
            config_dict: Configuration dictionary (alternative to config_path)
        """
        super().__init__()

        self.config_loader = ConfigLoader()
        self.widget_factory = WidgetFactory()
        self.config: Optional[GuiConfig] = None
        self.central_widget: Optional[QWidget] = None
        self.submit_callback: Optional[Callable] = None
        self.cancel_callback: Optional[Callable] = None
        self.custom_button_callbacks: Dict[str, Callable] = {}  # Store custom button callbacks

        # Load configuration
        if config_path:
            self.load_config_from_file(config_path)
        elif config_dict:
            self.load_config_from_dict(config_dict)

    def load_config_from_file(self, config_path: str) -> None:
        """Load configuration from a JSON file and build the GUI."""
        try:
            self.config = self.config_loader.load_from_file(config_path)
            self._build_gui()
        except Exception as e:
            self._show_error(f"Failed to load configuration: {str(e)}")

    def load_config_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """Load configuration from a dictionary and build the GUI."""
        try:
            self.config = self.config_loader.load_from_dict(config_dict)
            self._build_gui()
        except Exception as e:
            self._show_error(f"Failed to load configuration: {str(e)}")

    def _build_gui(self) -> None:
        """Build the GUI based on the loaded configuration."""
        if not self.config:
            return

        # Set window properties
        self.setWindowTitle(self.config.window.title)
        self.resize(self.config.window.width, self.config.window.height)

        if self.config.window.icon and self.config.window.icon.strip():
            try:
                self.setWindowIcon(QIcon(self.config.window.icon))
            except (FileNotFoundError, OSError) as e:
                print(f"Warning: Could not load window icon '{self.config.window.icon}': {e}")  # Ignore icon loading errors

        # Set resizable property
        if not self.config.window.resizable:
            self.setFixedSize(self.config.window.width, self.config.window.height)

        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)        # Create main layout
        main_layout = QVBoxLayout(self.central_widget)

        # Check if we should use tabs
        if self.config.use_tabs and self.config.tabs:
            # Create tab widget
            tab_widget = QTabWidget()
            main_layout.addWidget(tab_widget)

            # Create tabs
            for tab_config in self.config.tabs:
                if tab_config.enabled:
                    tab_page = self._create_tab_page(tab_config)
                    tab_widget.addTab(tab_page, tab_config.title)
                    if tab_config.tooltip:
                        tab_widget.setTabToolTip(tab_widget.count() - 1, tab_config.tooltip)
        else:
            # Create scroll area for form fields (original behavior)
            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
            scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

            # Create form widget
            form_widget = QWidget()
            scroll_area.setWidget(form_widget)

            # Create form layout based on configuration
            form_layout = self._create_form_layout(form_widget)

            # Add fields to the form
            self._add_fields_to_layout(form_layout, self.config.fields, self.config.layout)

            # Add scroll area to main layout
            main_layout.addWidget(scroll_area)

        # Add buttons if enabled
        if self.config.submit_button or self.config.cancel_button:
            button_layout = self._create_button_layout()
            main_layout.addLayout(button_layout)

        # Connect field change signals
        self._connect_field_signals()

    def _create_form_layout(self, parent_widget: QWidget) -> QLayout:
        """Create the appropriate layout based on configuration."""
        if self.config.layout == "vertical":
            return QVBoxLayout(parent_widget)
        elif self.config.layout == "horizontal":
            return QHBoxLayout(parent_widget)
        elif self.config.layout == "grid":
            layout = QGridLayout(parent_widget)
            # Set column stretch to make the widget column expand
            layout.setColumnStretch(1, 1)
            return layout
        elif self.config.layout == "form":
            layout = QFormLayout(parent_widget)
            # Set field growth policy to expand fields
            layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
            return layout
        else:
            # Default to vertical
            return QVBoxLayout(parent_widget)

    def _add_fields_to_layout(self, layout: QLayout, fields: list | None = None, layout_type: str | None = None) -> None:
        """Add form fields to the layout."""
        if fields is None:
            fields = self.config.fields

        for i, field_config in enumerate(fields):
            if layout_type == "form":
                # Form layout: add label and widget as pair
                label = self.widget_factory.create_label(field_config)
                widget = self.widget_factory.create_widget(field_config)
                if widget:
                    # Special handling for checkbox (no separate label)
                    if field_config.type == "checkbox":
                        layout.addRow("", widget)
                    else:
                        layout.addRow(label, widget)

            elif layout_type == "grid":
                # Grid layout: arrange in 2 columns (label, widget)
                row = i
                label = self.widget_factory.create_label(field_config)
                widget = self.widget_factory.create_widget(field_config)
                if widget:
                    if field_config.type == "checkbox":
                        layout.addWidget(widget, row, 0, 1, 2)  # Span both columns
                    else:
                        layout.addWidget(label, row, 0)
                        layout.addWidget(widget, row, 1)

            else:
                # Vertical or horizontal layout
                if field_config.type != "checkbox":
                    label = self.widget_factory.create_label(field_config)
                    layout.addWidget(label)

                widget = self.widget_factory.create_widget(field_config)
                if widget:
                    layout.addWidget(widget)

                    # Add some spacing between fields in vertical layout
                    if layout_type == "vertical" and i < len(fields) - 1:
                        layout.addSpacing(10)

    def _create_tab_page(self, tab_config: GuiConfig) -> QWidget:
        """Create a tab page with its content."""
        # Create scroll area for the tab
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Create tab content widget
        tab_widget = QWidget()
        scroll_area.setWidget(tab_widget)

        # Create layout for the tab based on its configuration
        if tab_config.layout == "vertical":
            tab_layout = QVBoxLayout(tab_widget)
        elif tab_config.layout == "horizontal":
            tab_layout = QHBoxLayout(tab_widget)
        elif tab_config.layout == "grid":
            tab_layout = QGridLayout(tab_widget)
        elif tab_config.layout == "form":
            tab_layout = QFormLayout(tab_widget)
            # Set field growth policy to make fields expand horizontally
            tab_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        else:
            tab_layout = QVBoxLayout(tab_widget)

        # Add fields to the tab
        self._add_fields_to_layout(tab_layout, tab_config.fields, tab_config.layout)

        return scroll_area

    def _create_button_layout(self) -> QHBoxLayout:
        """Create the button layout with submit, cancel, and custom buttons."""
        button_layout = QHBoxLayout()

        # Add custom buttons first (on the left)
        if self.config.custom_buttons:
            for button_config in self.config.custom_buttons:
                custom_btn = QPushButton(button_config.label)

                # Set tooltip if provided
                if button_config.tooltip:
                    custom_btn.setToolTip(button_config.tooltip)

                # Set enabled state
                custom_btn.setEnabled(button_config.enabled)

                # Apply custom style if provided
                if button_config.style:
                    custom_btn.setStyleSheet(button_config.style)

                # Set icon if provided
                if button_config.icon:
                    try:
                        icon = QIcon(button_config.icon)
                        custom_btn.setIcon(icon)
                    except (FileNotFoundError, OSError) as e:
                        print(f"Warning: Could not load button icon '{button_config.icon}': {e}")  # Ignore icon loading errors

                # Connect to custom callback handler
                def make_button_handler(button_name: str) -> Callable:
                    return lambda checked: self._on_custom_button_clicked(button_name)

                custom_btn.clicked.connect(make_button_handler(button_config.name))
                button_layout.addWidget(custom_btn)

        button_layout.addStretch()  # Push default buttons to the right

        if self.config.cancel_button:
            cancel_btn = QPushButton(self.config.cancel_label)
            cancel_btn.clicked.connect(self._on_cancel)
            button_layout.addWidget(cancel_btn)

        if self.config.submit_button:
            submit_btn = QPushButton(self.config.submit_label)
            submit_btn.clicked.connect(self._on_submit)
            submit_btn.setDefault(True)  # Make it the default button
            button_layout.addWidget(submit_btn)

        return button_layout

    def _connect_field_signals(self) -> None:
        """Connect field change signals to emit fieldChanged signal."""

        def create_signal_handler(field_name: str, signal_type: str, widget: QWidget = None) -> Callable:
            """Create a proper signal handler for a specific field and signal type."""
            if signal_type == 'text':
                return lambda text: self.fieldChanged.emit(field_name, text)
            elif signal_type == 'text_edit':
                # Special handler for QTextEdit which doesn't pass text in signal
                return lambda: self.fieldChanged.emit(field_name, widget.toPlainText())
            elif signal_type == 'value':
                return lambda value: self.fieldChanged.emit(field_name, value)
            elif signal_type == 'bool':
                return lambda checked: self.fieldChanged.emit(field_name, checked)
            elif signal_type == 'date':
                return lambda date: self.fieldChanged.emit(field_name, date.toString(Qt.ISODate))
            elif signal_type == 'time':
                return lambda time: self.fieldChanged.emit(field_name, time.toString(Qt.ISODate))
            elif signal_type == 'datetime':
                return lambda datetime: self.fieldChanged.emit(field_name, datetime.toString(Qt.ISODate))
            elif signal_type == 'color':
                return lambda color: self.fieldChanged.emit(field_name, color.name())
            elif signal_type == 'file':
                return lambda file_path: self.fieldChanged.emit(field_name, file_path)
            else:
                return lambda value: self.fieldChanged.emit(field_name, value)

        for field_name, widget in self.widget_factory.widgets.items():
            try:
                # Check widget type by class name to handle QTextEdit specially
                widget_class_name = widget.__class__.__name__

                if widget_class_name == 'QTextEdit':
                    # QTextEdit textChanged signal doesn't pass arguments
                    widget.textChanged.connect(create_signal_handler(field_name, 'text_edit', widget))
                elif hasattr(widget, 'textChanged') and callable(getattr(widget, 'textChanged')):
                    # QLineEdit and other text widgets that pass text in signal
                    widget.textChanged.connect(create_signal_handler(field_name, 'text'))
                elif hasattr(widget, 'valueChanged') and callable(getattr(widget, 'valueChanged')):
                    widget.valueChanged.connect(create_signal_handler(field_name, 'value'))
                elif hasattr(widget, 'toggled') and callable(getattr(widget, 'toggled')):
                    widget.toggled.connect(create_signal_handler(field_name, 'bool'))
                elif hasattr(widget, 'currentTextChanged') and callable(getattr(widget, 'currentTextChanged')):
                    widget.currentTextChanged.connect(create_signal_handler(field_name, 'text'))
                elif hasattr(widget, 'dateChanged') and callable(getattr(widget, 'dateChanged')):
                    widget.dateChanged.connect(create_signal_handler(field_name, 'date'))
                elif hasattr(widget, 'timeChanged') and callable(getattr(widget, 'timeChanged')):
                    widget.timeChanged.connect(create_signal_handler(field_name, 'time'))
                elif hasattr(widget, 'dateTimeChanged') and callable(getattr(widget, 'dateTimeChanged')):
                    widget.dateTimeChanged.connect(create_signal_handler(field_name, 'datetime'))
                elif hasattr(widget, 'colorChanged') and callable(getattr(widget, 'colorChanged')):
                    widget.colorChanged.connect(create_signal_handler(field_name, 'color'))
                elif hasattr(widget, 'fileChanged') and callable(getattr(widget, 'fileChanged')):
                    widget.fileChanged.connect(create_signal_handler(field_name, 'file'))
                # If no recognized signal is found, skip this widget

            except Exception as e:
                print(f"Warning: Could not connect signal for field {field_name}: {e}")
                # Continue with other widgets even if one fails

    def _on_submit(self) -> None:
        """Handle submit button click."""
        # Validate required fields
        if not self._validate_required_fields():
            return

        # Get all form data
        form_data = self.get_form_data()

        # Call custom callback if set
        if self.submit_callback:
            try:
                self.submit_callback(form_data)
            except Exception as e:
                self._show_error(f"Submit callback error: {str(e)}")

        # Emit signal
        self.formSubmitted.emit(form_data)

    def _on_cancel(self) -> None:
        """Handle cancel button click."""
        # Call custom callback if set
        if self.cancel_callback:
            try:
                self.cancel_callback()
            except Exception as e:
                self._show_error(f"Cancel callback error: {str(e)}")

        # Emit signal
        self.formCancelled.emit()

    def _on_custom_button_clicked(self, button_name: str) -> None:
        """Handle custom button click."""
        # Call custom callback if registered
        if button_name in self.custom_button_callbacks:
            try:
                # Get current form data to pass to callback
                form_data = self.get_form_data()
                self.custom_button_callbacks[button_name](form_data)
            except Exception as e:
                self._show_error(f"Custom button '{button_name}' callback error: {str(e)}")

    def _validate_required_fields(self) -> bool:
        """Validate that all required fields have values."""
        if not self.config:
            return True

        # Get required field names
        required_field_names = []
        for field_config in self.config.fields:
            if field_config.required:
                required_field_names.append(field_config.name)

        # Get current form data and validate using utility
        form_data = self.get_form_data()
        missing_field_names = ValidationUtils.validate_required_fields(form_data, required_field_names)

        if missing_field_names:
            # Convert field names back to labels for user-friendly display
            missing_labels = []
            for field_name in missing_field_names:
                field_config = next((f for f in self.config.fields if f.name == field_name), None)
                label = field_config.label if field_config else field_name
                missing_labels.append(label)

            fields_text = "\n• ".join(missing_labels)
            self._show_error(f"Please fill in the following required fields:\n• {fields_text}")
            return False

        return True

    def _show_error(self, message: str) -> None:
        """Show an error message dialog."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec()

    def get_form_data(self) -> Dict[str, Any]:
        """Get all form data as a dictionary."""
        return self.widget_factory.get_all_values()

    def set_form_data(self, data: Dict[str, Any]) -> None:
        """Set form data from a dictionary."""
        for field_name, value in data.items():
            self.widget_factory.set_widget_value(field_name, value)

    def clear_form(self) -> None:
        """Clear all form fields."""
        self.widget_factory.clear_all_widgets()

    def get_field_value(self, field_name: str) -> Any:
        """Get the value of a specific field."""
        return self.widget_factory.get_widget_value(field_name)

    def set_field_value(self, field_name: str, value: Any) -> bool:
        """Set the value of a specific field."""
        return self.widget_factory.set_widget_value(field_name, value)

    def set_submit_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Set a callback function to be called when the form is submitted."""
        self.submit_callback = callback

    def set_cancel_callback(self, callback: Callable[[], None]) -> None:
        """Set a callback function to be called when the form is cancelled."""
        self.cancel_callback = callback

    def set_custom_button_callback(self, button_name: str, callback: Callable[[Dict[str, Any]], None]) -> None:
        """
        Set a callback function to be called when a custom button is clicked.

        Args:
            button_name: The name of the custom button as defined in the configuration
            callback: Function to call when button is clicked. Receives form data as parameter.
        """
        self.custom_button_callbacks[button_name] = callback

    def remove_custom_button_callback(self, button_name: str) -> None:
        """Remove a custom button callback."""
        if button_name in self.custom_button_callbacks:
            del self.custom_button_callbacks[button_name]

    def get_custom_button_names(self) -> List[str]:
        """Get a list of all custom button names from the configuration."""
        if self.config and self.config.custom_buttons:
            return [button.name for button in self.config.custom_buttons]
        return []

    def enable_field(self, field_name: str, enabled: bool = True) -> None:
        """Enable or disable a specific field."""
        if field_name in self.widget_factory.widgets:
            self.widget_factory.widgets[field_name].setEnabled(enabled)

    def show_field(self, field_name: str, visible: bool = True) -> None:
        """Show or hide a specific field."""
        if field_name in self.widget_factory.widgets:
            self.widget_factory.widgets[field_name].setVisible(visible)

        if field_name in self.widget_factory.labels:
            self.widget_factory.labels[field_name].setVisible(visible)

    def load_data_from_file(self, data_file_path: str) -> bool:
        """
        Load form data from a JSON file and populate the GUI.

        Args:
            data_file_path: Path to the JSON file containing form data

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data = FileUtils.load_data_from_json(data_file_path)

            if data is None:
                self._show_error(f"Failed to load data from file: {data_file_path}")
                return False

            return self.load_data_from_dict(data)
        except Exception as e:
            self._show_error(f"Failed to load data from file: {str(e)}")
            return False

    def load_data_from_dict(self, data: Dict[str, Any]) -> bool:
        """
        Load form data from a dictionary and populate the GUI.
        Supports nested field names using dot notation.

        Args:
            data: Dictionary containing form field values (can be nested)

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # For each field in the config, check if data exists
            if not self.config:
                return False

            loaded_count = 0
            for field_config in self.config.fields:
                field_name = field_config.name

                # Handle nested field names with dot notation
                if '.' in field_name:
                    # Use get_nested_value to handle dot notation
                    field_value = get_nested_value(data, field_name)
                    if field_value is not None:
                        success = self.widget_factory.set_widget_value(field_name, field_value)
                        if success:
                            loaded_count += 1
                    elif field_config.default_value is not None:
                        # Use default value from config if no data provided
                        success = self.widget_factory.set_widget_value(field_name, field_config.default_value)
                        if success:
                            loaded_count += 1
                else:
                    # Handle regular field names (for backward compatibility)
                    if field_name in data:
                        # Use provided value
                        success = self.widget_factory.set_widget_value(field_name, data[field_name])
                        if success:
                            loaded_count += 1
                    elif field_config.default_value is not None:
                        # Use default value from config if no data provided
                        success = self.widget_factory.set_widget_value(field_name, field_config.default_value)
                        if success:
                            loaded_count += 1

            print(f"Loaded {loaded_count} field values from data")
            return True

        except Exception as e:
            self._show_error(f"Failed to load data: {str(e)}")
            return False

    def save_data_to_file(self, data_file_path: str, include_empty: bool = True) -> bool:
        """
        Save current form data to a JSON file.

        Args:
            data_file_path: Path where to save the JSON file
            include_empty: Whether to include fields with empty/None values

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data = self.get_form_data()
            success = FileUtils.save_data_to_json(data, data_file_path, include_empty)

            if not success:
                self._show_error(f"Failed to save data to file: {data_file_path}")

            return success

        except Exception as e:
            self._show_error(f"Failed to save data to file: {str(e)}")
            return False

    def get_data_with_metadata(self) -> Dict[str, Any]:
        """
        Get form data with additional metadata about the configuration.

        Returns:
            Dict containing form data plus metadata
        """
        if not self.config:
            return {}

        form_data = self.get_form_data()

        metadata = {
            "_metadata": {
                "config_source": "vibegui",
                "window_title": self.config.window.title,
                "layout": self.config.layout,
                "field_count": len(self.config.fields),
                "required_fields": [f.name for f in self.config.fields if f.required],
                "generated_at": QDateTime.currentDateTime().toString(Qt.ISODate)
            }
        }

        # Merge form data with metadata
        return {**form_data, **metadata}

    def save_data_with_metadata_to_file(self, data_file_path: str) -> bool:
        """
        Save form data with metadata to a JSON file.

        Args:
            data_file_path: Path where to save the JSON file

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data = self.get_data_with_metadata()

            with open(data_file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            self._show_error(f"Failed to save data with metadata: {str(e)}")
            return False

    @staticmethod
    def create_and_run(config_path: Optional[str] = None,
                      config_dict: Optional[Dict[str, Any]] = None,
                      app_args: Optional[list] = None) -> 'GuiBuilder':
        """
        Create and run a GUI application.

        Args:
            config_path: Path to JSON configuration file
            config_dict: Configuration dictionary (alternative to config_path)
            app_args: Arguments for QApplication (defaults to sys.argv)

        Returns:
            GuiBuilder instance
        """
        if app_args is None:
            app_args = sys.argv

        app = QApplication(app_args)

        gui_builder = GuiBuilder(config_path=config_path, config_dict=config_dict)
        gui_builder.show()

        # Run the application event loop
        app.exec()

        return gui_builder
