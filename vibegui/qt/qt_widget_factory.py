"""
Widget factory for creating Qt widgets based on field configurations.
Compatible with both PySide6 and PyQt6 via qtpy.
"""

import sys
from typing import Any, Dict, Optional, List
from qtpy.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox,
    QCheckBox, QRadioButton, QButtonGroup, QComboBox, QDateEdit,
    QTimeEdit, QDateTimeEdit, QSlider, QProgressBar, QPushButton,
    QFileDialog, QColorDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QGridLayout, QFrame, QGroupBox, QSizePolicy
)
from qtpy.QtCore import Qt, QDate, QTime, QDateTime, Signal
from qtpy.QtGui import QColor, QPixmap, QIcon, QDoubleValidator

from ..config_loader import FieldConfig
from ..utils import NestedValueMixin


def flatten_nested_dict(data: Dict[str, Any], parent_key: str = '', separator: str = '.') -> Dict[str, Any]:
    """
    Flatten a nested dictionary into a flat dictionary with dot notation keys.

    Args:
        data: The nested dictionary to flatten
        parent_key: The parent key path (for recursion)
        separator: The separator to use (default: '.')

    Returns:
        Flattened dictionary with dot notation keys
    """
    items = []
    for key, value in data.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_nested_dict(value, new_key, separator).items())
        else:
            items.append((new_key, value))
    return dict(items)


class CustomColorButton(QPushButton):
    """Custom button widget for color selection."""

    colorChanged = Signal(QColor)

    def __init__(self, initial_color: QColor = QColor(255, 255, 255)) -> None:
        super().__init__()
        self.current_color = initial_color
        self.setText("Choose Color")
        self.clicked.connect(self._choose_color)
        self._update_button_style()

    def _choose_color(self) -> None:
        """Open color dialog and update button."""
        color = QColorDialog.getColor(self.current_color, self, "Choose Color")
        if color.isValid():
            self.current_color = color
            self._update_button_style()
            self.colorChanged.emit(color)

    def _update_button_style(self) -> None:
        """Update button appearance to show current color."""
        rgb = self.current_color.rgb()
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: rgb({self.current_color.red()},
                                    {self.current_color.green()},
                                    {self.current_color.blue()});
                color: {'white' if self.current_color.lightness() < 128 else 'black'};
                border: 2px solid #333;
                padding: 5px;
                border-radius: 3px;
            }}
        """)

    def get_color(self) -> QColor:
        """Get the current selected color."""
        return self.current_color

    def set_color(self, color: QColor) -> None:
        """Set the current color."""
        self.current_color = color
        self._update_button_style()


class CustomFileButton(QPushButton):
    """Custom button widget for file selection."""

    fileChanged = Signal(str)

    def __init__(self, file_mode: str = "open") -> None:
        super().__init__()
        self.file_mode = file_mode
        self.selected_file = ""
        self.setText("Choose File...")
        self.clicked.connect(self._choose_file)

    def _choose_file(self) -> None:
        """Open file dialog and update button."""
        if self.file_mode == "save":
            file_path, _ = QFileDialog.getSaveFileName(self, "Save File")
        else:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open File")

        if file_path:
            self.selected_file = file_path
            # Show only filename in button
            filename = file_path.split('/')[-1]
            self.setText(f"Selected: {filename}")
            self.fileChanged.emit(file_path)

    def get_file_path(self) -> str:
        """Get the selected file path."""
        return self.selected_file

    def set_file_path(self, path: str) -> None:
        """Set the file path."""
        self.selected_file = path
        if path:
            filename = path.split('/')[-1]
            self.setText(f"Selected: {filename}")
        else:
            self.setText("Choose File...")


class WidgetFactory(NestedValueMixin):
    """Factory class for creating PySide6 widgets from field configurations."""

    def __init__(self) -> None:
        self.widgets: Dict[str, QWidget] = {}
        self.labels: Dict[str, QLabel] = {}
        self.radio_groups: Dict[str, QButtonGroup] = {}
        self.field_configs: Dict[str, FieldConfig] = {}

    def _set_expanding_size_policy(self, widget: QWidget) -> None:
        """Set size policy to make widget expand horizontally to fill available space."""
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        widget.setSizePolicy(size_policy)

    def create_widget(self, field_config: FieldConfig) -> QWidget:
        """Create a widget based on the field configuration."""
        self.field_configs[field_config.name] = field_config
        widget = None

        if field_config.type == "text":
            widget = self._create_text_field(field_config)
        elif field_config.type == "number":
            widget = self._create_number_field(field_config)
        elif field_config.type == "int":
            widget = self._create_int_field(field_config)
        elif field_config.type == "float":
            widget = self._create_float_field(field_config)
        elif field_config.type == "email":
            widget = self._create_email_field(field_config)
        elif field_config.type == "password":
            widget = self._create_password_field(field_config)
        elif field_config.type == "textarea":
            widget = self._create_textarea_field(field_config)
        elif field_config.type == "checkbox":
            widget = self._create_checkbox_field(field_config)
        elif field_config.type == "radio":
            widget = self._create_radio_field(field_config)
        elif field_config.type == "select":
            widget = self._create_select_field(field_config)
        elif field_config.type == "date":
            widget = self._create_date_field(field_config)
        elif field_config.type == "time":
            widget = self._create_time_field(field_config)
        elif field_config.type == "datetime":
            widget = self._create_datetime_field(field_config)
        elif field_config.type == "range":
            widget = self._create_range_field(field_config)
        elif field_config.type == "file":
            widget = self._create_file_field(field_config)
        elif field_config.type == "color":
            widget = self._create_color_field(field_config)
        elif field_config.type == "url":
            widget = self._create_url_field(field_config)
        else:
            # Fallback to text field
            widget = self._create_text_field(field_config)

        # Apply common properties
        if widget and field_config.tooltip:
            widget.setToolTip(field_config.tooltip)

        if widget and field_config.width:
            widget.setFixedWidth(field_config.width)

        if widget and field_config.height:
            widget.setFixedHeight(field_config.height)

        # Set size policy to make most widgets expand horizontally
        if widget:
            # Special handling for textarea - expand both directions
            if field_config.type == "textarea":
                size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                widget.setSizePolicy(size_policy)
            # For radio buttons and checkboxes, don't force expansion
            elif field_config.type not in ["radio", "checkbox"]:
                self._set_expanding_size_policy(widget)

        # Store widget reference
        if widget:
            self.widgets[field_config.name] = widget

        return widget

    def create_label(self, field_config: FieldConfig) -> QLabel:
        """Create a label for the field."""
        label_text = field_config.label
        if field_config.required:
            label_text += " *"

        label = QLabel(label_text)
        label.setObjectName(f"label_{field_config.name}")

        # Store label reference
        self.labels[field_config.name] = label

        return label

    def _create_text_field(self, field_config: FieldConfig) -> QLineEdit:
        """Create a text input field."""
        widget = QLineEdit()
        if field_config.placeholder:
            widget.setPlaceholderText(field_config.placeholder)
        if field_config.default_value:
            widget.setText(str(field_config.default_value))
        return widget

    def _create_number_field(self, field_config: FieldConfig) -> QWidget:
        """Create a number input field."""
        if field_config.min_value is not None and isinstance(field_config.min_value, int) and \
           field_config.max_value is not None and isinstance(field_config.max_value, int):
            widget = QSpinBox()
            widget.setMinimum(int(field_config.min_value))
            widget.setMaximum(int(field_config.max_value))
            if field_config.default_value is not None:
                widget.setValue(int(field_config.default_value))
        else:
            widget = QDoubleSpinBox()
            if field_config.min_value is not None:
                widget.setMinimum(float(field_config.min_value))
            if field_config.max_value is not None:
                widget.setMaximum(float(field_config.max_value))
            if field_config.default_value is not None:
                widget.setValue(float(field_config.default_value))
        return widget

    def _create_int_field(self, field_config: FieldConfig) -> QSpinBox:
        """Create an integer input field."""
        widget = QSpinBox()

        # Set range
        if field_config.min_value is not None:
            widget.setMinimum(int(field_config.min_value))
        else:
            widget.setMinimum(-2147483648)  # Default minimum for 32-bit int

        if field_config.max_value is not None:
            widget.setMaximum(int(field_config.max_value))
        else:
            widget.setMaximum(2147483647)  # Default maximum for 32-bit int

        # Set default value
        if field_config.default_value is not None:
            widget.setValue(int(field_config.default_value))

        return widget

    def _create_float_field(self, field_config: FieldConfig) -> QWidget:
        """Create a float input field with optional format enforcement."""

        # Check if we need scientific notation or special formatting
        needs_line_edit = False
        if field_config.format_string:
            format_str = field_config.format_string.lower()
            # Use QLineEdit for scientific notation, percentage, or other special formats
            if any(char in format_str for char in ['e', '%', 'g']) or ',' in format_str:
                needs_line_edit = True

        if needs_line_edit:
            return self._create_scientific_float_field(field_config)
        else:
            return self._create_spinbox_float_field(field_config)

    def _create_spinbox_float_field(self, field_config: FieldConfig) -> QDoubleSpinBox:
        """Create a float input field using QDoubleSpinBox for simple decimal formatting."""
        widget = QDoubleSpinBox()

        # Set range
        if field_config.min_value is not None:
            widget.setMinimum(float(field_config.min_value))
        else:
            widget.setMinimum(-sys.float_info.max)  # Default minimum

        if field_config.max_value is not None:
            widget.setMaximum(float(field_config.max_value))
        else:
            widget.setMaximum(sys.float_info.max)  # Default maximum

        # Extract decimal places from format string
        decimals = 2  # Default to 2 decimal places
        if field_config.format_string:
            try:
                format_str = field_config.format_string.lower()
                if '.' in format_str and 'f' in format_str:
                    # Fixed-point notation: ".2f" -> 2
                    decimal_part = format_str.split('.')[1]
                    decimals = int(decimal_part.replace('f', ''))
            except (ValueError, IndexError):
                decimals = 2  # Default to 2 decimal places

        widget.setDecimals(decimals)

        # Set step size based on decimal places
        step = 1.0 / (10 ** decimals)
        widget.setSingleStep(step)

        # Set default value
        if field_config.default_value is not None:
            widget.setValue(float(field_config.default_value))

        # Store format string for later use in value retrieval
        if field_config.format_string:
            widget.setProperty("format_string", field_config.format_string)
        widget.setProperty("field_type", "spinbox_float")

        return widget

    def _create_scientific_float_field(self, field_config: FieldConfig) -> QLineEdit:
        """Create a float input field using QLineEdit for scientific notation and special formatting."""

        widget = QLineEdit()

        # Set up validator for floating point numbers (including scientific notation)
        validator = QDoubleValidator()
        if field_config.min_value is not None:
            validator.setBottom(float(field_config.min_value))
        if field_config.max_value is not None:
            validator.setTop(float(field_config.max_value))
        validator.setNotation(QDoubleValidator.ScientificNotation)
        widget.setValidator(validator)

        # Set default value
        if field_config.default_value is not None:
            if field_config.format_string:
                try:
                    # Format the default value according to the format string
                    formatted_value = format(float(field_config.default_value), field_config.format_string)
                    widget.setText(formatted_value)
                except (ValueError, TypeError):
                    widget.setText(str(field_config.default_value))
            else:
                widget.setText(str(field_config.default_value))

        # Store format string and field type for later use
        if field_config.format_string:
            widget.setProperty("format_string", field_config.format_string)
        widget.setProperty("field_type", "scientific_float")

        # Set placeholder text to show expected format
        if field_config.format_string:
            format_str = field_config.format_string
            if 'e' in format_str.lower():
                widget.setPlaceholderText("e.g., 1.23e+06 or 1.23E-05")
            elif '%' in format_str:
                widget.setPlaceholderText("e.g., 0.856 (for 85.6%)")
            elif 'g' in format_str.lower():
                widget.setPlaceholderText("e.g., 123.456 or 1.23e+06")

        return widget

    def _create_email_field(self, field_config: FieldConfig) -> QLineEdit:
        """Create an email input field."""
        widget = QLineEdit()
        widget.setPlaceholderText(field_config.placeholder or "Enter email address")
        if field_config.default_value:
            widget.setText(str(field_config.default_value))

        return widget

    def _create_password_field(self, field_config: FieldConfig) -> QLineEdit:
        """Create a password input field."""
        widget = QLineEdit()
        widget.setEchoMode(QLineEdit.Password)
        widget.setPlaceholderText(field_config.placeholder or "Enter password")

        return widget

    def _create_textarea_field(self, field_config: FieldConfig) -> QTextEdit:
        """Create a textarea field."""
        widget = QTextEdit()
        if field_config.default_value:
            widget.setPlainText(str(field_config.default_value))
        widget.setPlaceholderText(field_config.placeholder or "Enter text...")
        return widget

    def _create_checkbox_field(self, field_config: FieldConfig) -> QCheckBox:
        """Create a checkbox field."""
        widget = QCheckBox(field_config.label)
        if field_config.default_value:
            widget.setChecked(bool(field_config.default_value))
        return widget

    def _create_radio_field(self, field_config: FieldConfig) -> QWidget:
        """Create radio button group."""
        container = QWidget()
        layout = QVBoxLayout(container)

        button_group = QButtonGroup()
        self.radio_groups[field_config.name] = button_group

        for i, option in enumerate(field_config.options or []):
            radio_button = QRadioButton(option)
            button_group.addButton(radio_button, i)
            layout.addWidget(radio_button)

            # Set default selection
            if field_config.default_value == option:
                radio_button.setChecked(True)

        return container

    def _create_select_field(self, field_config: FieldConfig) -> QComboBox:
        """Create a select (combobox) field."""
        widget = QComboBox()

        if field_config.options:
            widget.addItems(field_config.options)

            # Set default selection
            if field_config.default_value in field_config.options:
                index = field_config.options.index(field_config.default_value)
                widget.setCurrentIndex(index)

        return widget

    def _create_date_field(self, field_config: FieldConfig) -> QDateEdit:
        """Create a date input field."""
        widget = QDateEdit()
        widget.setCalendarPopup(True)
        widget.setDate(QDate.currentDate())

        if field_config.default_value:
            # Assume default_value is in YYYY-MM-DD format
            try:
                date_parts = field_config.default_value.split('-')
                date = QDate(int(date_parts[0]), int(date_parts[1]), int(date_parts[2]))
                widget.setDate(date)
            except (ValueError, IndexError):
                pass  # Use current date as fallback

        return widget

    def _create_time_field(self, field_config: FieldConfig) -> QTimeEdit:
        """Create a time input field."""
        widget = QTimeEdit()
        widget.setTime(QTime.currentTime())

        if field_config.default_value:
            # Assume default_value is in HH:MM format
            try:
                time_parts = field_config.default_value.split(':')
                time = QTime(int(time_parts[0]), int(time_parts[1]))
                widget.setTime(time)
            except (ValueError, IndexError):
                pass  # Use current time as fallback

        return widget

    def _create_datetime_field(self, field_config: FieldConfig) -> QDateTimeEdit:
        """Create a datetime input field."""
        widget = QDateTimeEdit()
        widget.setCalendarPopup(True)
        widget.setDateTime(QDateTime.currentDateTime())

        if field_config.default_value:
            # Assume default_value is in ISO format
            try:
                datetime = QDateTime.fromString(field_config.default_value, Qt.ISODate)
                if datetime.isValid():
                    widget.setDateTime(datetime)
            except (ValueError, TypeError):
                pass  # Use current datetime as fallback

        return widget

    def _create_range_field(self, field_config: FieldConfig) -> QWidget:
        """Create a range (slider) field with value display."""
        # Create container widget to hold slider and value label
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        # Create the slider
        slider = QSlider(Qt.Horizontal)

        if field_config.min_value is not None:
            slider.setMinimum(int(field_config.min_value))
        if field_config.max_value is not None:
            slider.setMaximum(int(field_config.max_value))
        if field_config.default_value is not None:
            slider.setValue(int(field_config.default_value))

        # Create value label
        value_label = QLabel(str(slider.value()))
        value_label.setMinimumWidth(50)
        value_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        # Update label when slider value changes
        slider.valueChanged.connect(lambda v: value_label.setText(str(v)))

        # Add slider and label to layout
        layout.addWidget(slider, 1)  # Slider takes most space
        layout.addWidget(value_label, 0)  # Label has fixed width

        # Store the slider as the main widget for value retrieval
        container.setProperty("slider_widget", slider)

        return container

    def _create_file_field(self, field_config: FieldConfig) -> CustomFileButton:
        """Create a file selection field."""
        file_mode = "open"  # Default to open mode
        if field_config.default_value == "save":
            file_mode = "save"

        widget = CustomFileButton(file_mode)
        return widget

    def _create_color_field(self, field_config: FieldConfig) -> CustomColorButton:
        """Create a color selection field."""
        initial_color = QColor(255, 255, 255)  # Default to white

        if field_config.default_value:
            try:
                initial_color = QColor(field_config.default_value)
            except (ValueError, TypeError):
                pass  # Use default color

        widget = CustomColorButton(initial_color)
        return widget

    def _create_url_field(self, field_config: FieldConfig) -> QLineEdit:
        """Create a URL input field."""
        widget = QLineEdit()
        widget.setPlaceholderText(field_config.placeholder or "Enter URL (http://...)")
        if field_config.default_value:
            widget.setText(str(field_config.default_value))

        return widget

    def get_widget_value(self, field_name: str) -> Any:
        """Get the current value of a widget."""
        if field_name not in self.widgets:
            return None

        widget = self.widgets[field_name]

        if isinstance(widget, QLineEdit):
            text = widget.text()
            # Check if this is a scientific float field
            if widget.property("field_type") == "scientific_float":
                try:
                    # Parse the text as a float (handles scientific notation)
                    return float(text)
                except (ValueError, TypeError):
                    return 0.0  # Default fallback
            return text
        elif isinstance(widget, QTextEdit):
            return widget.toPlainText()
        elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
            value = widget.value()
            # Check if this is a float field with format string
            if isinstance(widget, QDoubleSpinBox) and widget.property("format_string"):
                format_string = widget.property("format_string")
                try:
                    # For scientific notation and other formats, return the raw value
                    # The formatting is primarily for display/input validation
                    if any(char in format_string.lower() for char in ['e', 'g']):
                        # Scientific or general notation - return raw float
                        return value
                    else:
                        # Fixed-point notation - apply precision
                        return float(format(value, format_string.replace('%', '')))
                except (ValueError, TypeError):
                    return value
            return value
        elif isinstance(widget, QCheckBox):
            return widget.isChecked()
        elif isinstance(widget, QComboBox):
            return widget.currentText()
        elif isinstance(widget, QDateEdit):
            return widget.date().toString(Qt.ISODate)
        elif isinstance(widget, QTimeEdit):
            return widget.time().toString(Qt.ISODate)
        elif isinstance(widget, QDateTimeEdit):
            return widget.dateTime().toString(Qt.ISODate)
        elif isinstance(widget, QSlider):
            return widget.value()
        elif isinstance(widget, QWidget) and widget.property("slider_widget"):
            # Handle slider container widget
            slider = widget.property("slider_widget")
            return slider.value()
        elif isinstance(widget, CustomFileButton):
            return widget.get_file_path()
        elif isinstance(widget, CustomColorButton):
            return widget.get_color().name()
        elif field_name in self.radio_groups:
            # Handle radio button groups
            button_group = self.radio_groups[field_name]
            checked_button = button_group.checkedButton()
            if checked_button:
                return checked_button.text()

        return None

    def set_widget_value(self, field_name: str, value: Any) -> bool:
        """Set the value of a widget."""
        if field_name not in self.widgets:
            return False

        widget = self.widgets[field_name]

        try:
            if isinstance(widget, QLineEdit):
                # Check if this is a scientific float field
                if widget.property("field_type") == "scientific_float":
                    try:
                        float_value = float(value)
                        format_string = widget.property("format_string")
                        if format_string:
                            # Format the value according to the format string
                            formatted_value = format(float_value, format_string)
                            widget.setText(formatted_value)
                        else:
                            widget.setText(str(float_value))
                    except (ValueError, TypeError):
                        widget.setText(str(value))
                else:
                    widget.setText(str(value))
            elif isinstance(widget, QTextEdit):
                widget.setPlainText(str(value))
            elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                widget.setValue(float(value))
            elif isinstance(widget, QCheckBox):
                widget.setChecked(bool(value))
            elif isinstance(widget, QComboBox):
                index = widget.findText(str(value))
                if index >= 0:
                    widget.setCurrentIndex(index)
            elif isinstance(widget, QDateEdit):
                date = QDate.fromString(str(value), Qt.ISODate)
                if date.isValid():
                    widget.setDate(date)
            elif isinstance(widget, QTimeEdit):
                time = QTime.fromString(str(value), Qt.ISODate)
                if time.isValid():
                    widget.setTime(time)
            elif isinstance(widget, QDateTimeEdit):
                datetime = QDateTime.fromString(str(value), Qt.ISODate)
                if datetime.isValid():
                    widget.setDateTime(datetime)
            elif isinstance(widget, QSlider):
                widget.setValue(int(value))
            elif isinstance(widget, QWidget) and widget.property("slider_widget"):
                # Handle slider container widget
                slider = widget.property("slider_widget")
                slider.setValue(int(value))
            elif isinstance(widget, CustomFileButton):
                widget.set_file_path(str(value))
            elif isinstance(widget, CustomColorButton):
                color = QColor(str(value))
                if color.isValid():
                    widget.set_color(color)
            elif field_name in self.radio_groups:
                # Handle radio button groups
                button_group = self.radio_groups[field_name]
                for button in button_group.buttons():
                    if button.text() == str(value):
                        button.setChecked(True)
                        break

            return True
        except (ValueError, TypeError, AttributeError):
            return False

    # get_all_values and set_all_values provided by NestedValueMixin

    def clear_all_widgets(self) -> None:
        """Clear all widget values to their defaults."""
        for field_name in self.widgets.keys():
            field_config = self.field_configs.get(field_name)
            if field_config and field_config.default_value is not None:
                self.set_widget_value(field_name, field_config.default_value)
            else:
                # No default, clear to appropriate empty value
                widget = self.widgets[field_name]
                if isinstance(widget, (QLineEdit, QTextEdit)):
                    self.set_widget_value(field_name, "")
                elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                    self.set_widget_value(field_name, 0)
                elif isinstance(widget, QCheckBox):
                    self.set_widget_value(field_name, False)
                elif isinstance(widget, CustomFileButton):
                    widget.set_file_path("")
                elif isinstance(widget, CustomColorButton):
                    widget.set_color(QColor(255, 255, 255))
                elif field_name in self.radio_groups:
                    button_group = self.radio_groups[field_name]
                    if button_group.buttons():
                        button_group.buttons()[0].setChecked(True)
                else:
                    self.set_widget_value(field_name, "")
