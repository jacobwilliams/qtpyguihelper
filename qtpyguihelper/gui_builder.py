"""
Main GUI builder class that creates PySide6 applications from JSON configuration.
"""

import sys
from typing import Dict, Any, Callable, Optional
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QFormLayout, QGridLayout, QPushButton, QScrollArea, QMessageBox,
    QSplitter, QFrame
)
from PySide6.QtCore import Qt, Signal, QObject
from PySide6.QtGui import QIcon

from .config_loader import ConfigLoader, GuiConfig, FieldConfig
from .widget_factory import WidgetFactory


class GuiBuilder(QMainWindow):
    """Main GUI builder class that creates a PySide6 application from JSON configuration."""

    # Signals
    formSubmitted = Signal(dict)  # Emitted when form is submitted with data
    formCancelled = Signal()      # Emitted when form is cancelled
    fieldChanged = Signal(str, object)  # Emitted when a field value changes

    def __init__(self, config_path: Optional[str] = None, config_dict: Optional[Dict[str, Any]] = None):
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

        # Load configuration
        if config_path:
            self.load_config_from_file(config_path)
        elif config_dict:
            self.load_config_from_dict(config_dict)

    def load_config_from_file(self, config_path: str):
        """Load configuration from a JSON file and build the GUI."""
        try:
            self.config = self.config_loader.load_from_file(config_path)
            self._build_gui()
        except Exception as e:
            self._show_error(f"Failed to load configuration: {str(e)}")

    def load_config_from_dict(self, config_dict: Dict[str, Any]):
        """Load configuration from a dictionary and build the GUI."""
        try:
            self.config = self.config_loader.load_from_dict(config_dict)
            self._build_gui()
        except Exception as e:
            self._show_error(f"Failed to load configuration: {str(e)}")

    def _build_gui(self):
        """Build the GUI based on the loaded configuration."""
        if not self.config:
            return

        # Set window properties
        self.setWindowTitle(self.config.window.title)
        self.resize(self.config.window.width, self.config.window.height)

        if self.config.window.icon and self.config.window.icon.strip():
            try:
                self.setWindowIcon(QIcon(self.config.window.icon))
            except:
                pass  # Ignore icon loading errors

        # Set resizable property
        if not self.config.window.resizable:
            self.setFixedSize(self.config.window.width, self.config.window.height)

        # Create central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create main layout
        main_layout = QVBoxLayout(self.central_widget)

        # Create scroll area for form fields
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
        self._add_fields_to_layout(form_layout)

        # Add scroll area to main layout
        main_layout.addWidget(scroll_area)

        # Add buttons if enabled
        if self.config.submit_button or self.config.cancel_button:
            button_layout = self._create_button_layout()
            main_layout.addLayout(button_layout)

        # Connect field change signals
        self._connect_field_signals()

    def _create_form_layout(self, parent_widget: QWidget):
        """Create the appropriate layout based on configuration."""
        if self.config.layout == "vertical":
            return QVBoxLayout(parent_widget)
        elif self.config.layout == "horizontal":
            return QHBoxLayout(parent_widget)
        elif self.config.layout == "grid":
            return QGridLayout(parent_widget)
        elif self.config.layout == "form":
            return QFormLayout(parent_widget)
        else:
            # Default to vertical
            return QVBoxLayout(parent_widget)

    def _add_fields_to_layout(self, layout):
        """Add form fields to the layout."""
        for i, field_config in enumerate(self.config.fields):
            if self.config.layout == "form":
                # Form layout: add label and widget as pair
                label = self.widget_factory.create_label(field_config)
                widget = self.widget_factory.create_widget(field_config)
                if widget:
                    # Special handling for checkbox (no separate label)
                    if field_config.type == "checkbox":
                        layout.addRow("", widget)
                    else:
                        layout.addRow(label, widget)

            elif self.config.layout == "grid":
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
                    if self.config.layout == "vertical" and i < len(self.config.fields) - 1:
                        layout.addSpacing(10)

    def _create_button_layout(self) -> QHBoxLayout:
        """Create the button layout with submit and cancel buttons."""
        button_layout = QHBoxLayout()
        button_layout.addStretch()  # Push buttons to the right

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

    def _connect_field_signals(self):
        """Connect field change signals to emit fieldChanged signal."""
        for field_name, widget in self.widget_factory.widgets.items():
            # Connect appropriate signal based on widget type
            try:
                if hasattr(widget, 'textChanged'):
                    widget.textChanged.connect(lambda text, name=field_name: self.fieldChanged.emit(name, text))
                elif hasattr(widget, 'valueChanged'):
                    widget.valueChanged.connect(lambda value, name=field_name: self.fieldChanged.emit(name, value))
                elif hasattr(widget, 'toggled'):
                    widget.toggled.connect(lambda checked, name=field_name: self.fieldChanged.emit(name, checked))
                elif hasattr(widget, 'currentTextChanged'):
                    widget.currentTextChanged.connect(lambda text, name=field_name: self.fieldChanged.emit(name, text))
                elif hasattr(widget, 'dateChanged'):
                    widget.dateChanged.connect(lambda date, name=field_name: self.fieldChanged.emit(name, date.toString(Qt.ISODate)))
                elif hasattr(widget, 'timeChanged'):
                    widget.timeChanged.connect(lambda time, name=field_name: self.fieldChanged.emit(name, time.toString(Qt.ISODate)))
                elif hasattr(widget, 'dateTimeChanged'):
                    widget.dateTimeChanged.connect(lambda datetime, name=field_name: self.fieldChanged.emit(name, datetime.toString(Qt.ISODate)))
                elif hasattr(widget, 'colorChanged'):
                    widget.colorChanged.connect(lambda color, name=field_name: self.fieldChanged.emit(name, color.name()))
                elif hasattr(widget, 'fileChanged'):
                    widget.fileChanged.connect(lambda file_path, name=field_name: self.fieldChanged.emit(name, file_path))
            except Exception as e:
                print(f"Warning: Could not connect signal for field {field_name}: {e}")

    def _on_submit(self):
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

    def _on_cancel(self):
        """Handle cancel button click."""
        # Call custom callback if set
        if self.cancel_callback:
            try:
                self.cancel_callback()
            except Exception as e:
                self._show_error(f"Cancel callback error: {str(e)}")

        # Emit signal
        self.formCancelled.emit()

    def _validate_required_fields(self) -> bool:
        """Validate that all required fields have values."""
        if not self.config:
            return True

        missing_fields = []

        for field_config in self.config.fields:
            if field_config.required:
                value = self.widget_factory.get_widget_value(field_config.name)

                # Check if value is empty/None
                if value is None or (isinstance(value, str) and not value.strip()):
                    missing_fields.append(field_config.label)

        if missing_fields:
            fields_text = "\\n• ".join(missing_fields)
            self._show_error(f"Please fill in the following required fields:\\n• {fields_text}")
            return False

        return True

    def _show_error(self, message: str):
        """Show an error message dialog."""
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec()

    def get_form_data(self) -> Dict[str, Any]:
        """Get all form data as a dictionary."""
        return self.widget_factory.get_all_values()

    def set_form_data(self, data: Dict[str, Any]):
        """Set form data from a dictionary."""
        for field_name, value in data.items():
            self.widget_factory.set_widget_value(field_name, value)

    def clear_form(self):
        """Clear all form fields."""
        self.widget_factory.clear_all_widgets()

    def get_field_value(self, field_name: str) -> Any:
        """Get the value of a specific field."""
        return self.widget_factory.get_widget_value(field_name)

    def set_field_value(self, field_name: str, value: Any) -> bool:
        """Set the value of a specific field."""
        return self.widget_factory.set_widget_value(field_name, value)

    def set_submit_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Set a callback function to be called when the form is submitted."""
        self.submit_callback = callback

    def set_cancel_callback(self, callback: Callable[[], None]):
        """Set a callback function to be called when the form is cancelled."""
        self.cancel_callback = callback

    def enable_field(self, field_name: str, enabled: bool = True):
        """Enable or disable a specific field."""
        if field_name in self.widget_factory.widgets:
            self.widget_factory.widgets[field_name].setEnabled(enabled)

    def show_field(self, field_name: str, visible: bool = True):
        """Show or hide a specific field."""
        if field_name in self.widget_factory.widgets:
            self.widget_factory.widgets[field_name].setVisible(visible)

        if field_name in self.widget_factory.labels:
            self.widget_factory.labels[field_name].setVisible(visible)

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
