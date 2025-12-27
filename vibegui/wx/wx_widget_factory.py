"""
wxPython widget factory for creating widgets based on field configurations.
"""

import sys
from typing import Any, Dict, Optional, List
import wx
import wx.lib.scrolledpanel as scrolled
import wx.adv
from datetime import datetime, date, time

from ..config_loader import FieldConfig
from ..utils import NestedValueMixin


class WxCustomColorButton(wx.Button):
    """Custom button widget for color selection in wxPython."""

    def __init__(self, parent: wx.Window, initial_color: wx.Colour = wx.Colour(255, 255, 255)) -> None:
        super().__init__(parent, label="Choose Color")
        self.current_color = initial_color
        self.Bind(wx.EVT_BUTTON, self._on_choose_color)
        self._update_button_appearance()

    def _on_choose_color(self, event: wx.Event) -> None:
        """Open color dialog and update button."""
        dialog = wx.ColourDialog(self)
        dialog.GetColourData().SetColour(self.current_color)

        if dialog.ShowModal() == wx.ID_OK:
            self.current_color = dialog.GetColourData().GetColour()
            self._update_button_appearance()

        dialog.Destroy()

    def _update_button_appearance(self) -> None:
        """Update button appearance to show current color."""
        self.SetBackgroundColour(self.current_color)
        # Set text color based on background brightness
        r, g, b = self.current_color.Red(), self.current_color.Green(), self.current_color.Blue()
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        text_color = wx.Colour(255, 255, 255) if brightness < 128 else wx.Colour(0, 0, 0)
        self.SetForegroundColour(text_color)

    def get_color(self) -> wx.Colour:
        """Get the current selected color."""
        return self.current_color

    def set_color(self, color: wx.Colour) -> None:
        """Set the current color."""
        self.current_color = color
        self._update_button_appearance()


class WxCustomFileButton(wx.Button):
    """Custom button widget for file selection in wxPython."""

    def __init__(self, parent: wx.Window, file_mode: str = "open") -> None:
        super().__init__(parent, label="Choose File...")
        self.file_mode = file_mode
        self.selected_file = ""
        self.Bind(wx.EVT_BUTTON, self._on_choose_file)

    def _on_choose_file(self, event: wx.Event) -> None:
        """Open file dialog and update button."""
        if self.file_mode == "save":
            dialog = wx.FileDialog(self, "Save File", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        else:
            dialog = wx.FileDialog(self, "Open File", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

        if dialog.ShowModal() == wx.ID_OK:
            self.selected_file = dialog.GetPath()
            filename = dialog.GetFilename()
            self.SetLabel(f"Selected: {filename}")

        dialog.Destroy()

    def get_file_path(self) -> str:
        """Get the selected file path."""
        return self.selected_file

    def set_file_path(self, path: str) -> None:
        """Set the file path."""
        self.selected_file = path
        if path:
            import os
            filename = os.path.basename(path)
            self.SetLabel(f"Selected: {filename}")
        else:
            self.SetLabel("Choose File...")


class WxWidgetFactory(NestedValueMixin):
    """Factory class for creating wxPython widgets from field configurations."""

    def __init__(self) -> None:
        self.widgets: Dict[str, wx.Window] = {}
        self.labels: Dict[str, wx.StaticText] = {}
        self.field_configs: Dict[str, FieldConfig] = {}

    def create_widget(self, parent: wx.Window, field_config: FieldConfig) -> Optional[wx.Window]:
        """Create a widget based on the field configuration."""
        self.field_configs[field_config.name] = field_config
        widget = None

        if field_config.type == "text":
            widget = self._create_text_field(parent, field_config)
        elif field_config.type == "number":
            widget = self._create_number_field(parent, field_config)
        elif field_config.type == "int":
            widget = self._create_int_field(parent, field_config)
        elif field_config.type == "float":
            widget = self._create_float_field(parent, field_config)
        elif field_config.type == "email":
            widget = self._create_email_field(parent, field_config)
        elif field_config.type == "password":
            widget = self._create_password_field(parent, field_config)
        elif field_config.type == "textarea":
            widget = self._create_textarea_field(parent, field_config)
        elif field_config.type == "checkbox":
            widget = self._create_checkbox_field(parent, field_config)
        elif field_config.type == "radio":
            widget = self._create_radio_field(parent, field_config)
        elif field_config.type == "select":
            widget = self._create_select_field(parent, field_config)
        elif field_config.type == "date":
            widget = self._create_date_field(parent, field_config)
        elif field_config.type == "time":
            widget = self._create_time_field(parent, field_config)
        elif field_config.type == "datetime":
            widget = self._create_datetime_field(parent, field_config)
        elif field_config.type == "range":
            widget = self._create_range_field(parent, field_config)
        elif field_config.type == "file":
            widget = self._create_file_field(parent, field_config)
        elif field_config.type == "color":
            widget = self._create_color_field(parent, field_config)
        elif field_config.type == "url":
            widget = self._create_url_field(parent, field_config)
        else:
            # Fallback to text field
            widget = self._create_text_field(parent, field_config)

        # Apply common properties
        if widget and field_config.tooltip:
            widget.SetToolTip(field_config.tooltip)

        if widget and field_config.width:
            size = widget.GetSize()
            widget.SetSize((field_config.width, size.height))

        if widget and field_config.height:
            size = widget.GetSize()
            widget.SetSize((size.width, field_config.height))

        # Store widget reference
        if widget:
            self.widgets[field_config.name] = widget

        return widget

    def create_label(self, parent: wx.Window, field_config: FieldConfig) -> wx.StaticText:
        """Create a label for the field."""
        label_text = field_config.label
        if field_config.required:
            label_text += " *"

        label = wx.StaticText(parent, label=label_text)
        self.labels[field_config.name] = label
        return label

    def _create_text_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.TextCtrl:
        """Create a text input field."""
        style = wx.TE_PROCESS_ENTER
        widget = wx.TextCtrl(parent, style=style)

        if field_config.placeholder:
            widget.SetHint(field_config.placeholder)
        if field_config.default_value:
            widget.SetValue(str(field_config.default_value))

        return widget

    def _create_number_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.Window:
        """Create a number input field."""
        if (field_config.min_value is not None and isinstance(field_config.min_value, int) and
            field_config.max_value is not None and isinstance(field_config.max_value, int)):
            # Use SpinCtrl for integer ranges
            min_val = int(field_config.min_value) if field_config.min_value is not None else -sys.float_info.max
            max_val = int(field_config.max_value) if field_config.max_value is not None else sys.float_info.max
            widget = wx.SpinCtrl(parent, min=min_val, max=max_val)
            if field_config.default_value is not None:
                widget.SetValue(int(field_config.default_value))
        else:
            # Use SpinCtrlDouble for float ranges
            min_val = float(field_config.min_value) if field_config.min_value is not None else -sys.float_info.max
            max_val = float(field_config.max_value) if field_config.max_value is not None else sys.float_info.max
            widget = wx.SpinCtrlDouble(parent, min=min_val, max=max_val)
            if field_config.default_value is not None:
                widget.SetValue(float(field_config.default_value))

        return widget

    def _create_int_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.SpinCtrl:
        """Create an integer input field."""
        min_val = int(field_config.min_value) if field_config.min_value is not None else -2147483648
        max_val = int(field_config.max_value) if field_config.max_value is not None else 2147483647

        widget = wx.SpinCtrl(parent, min=min_val, max=max_val)

        if field_config.default_value is not None:
            widget.SetValue(int(field_config.default_value))

        return widget

    def _create_float_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.Window:
        """Create a float input field."""
        # Check if we need special formatting
        needs_text_field = False
        if field_config.format_string:
            format_str = field_config.format_string.lower()
            if any(char in format_str for char in ['e', '%', 'g']) or ',' in format_str:
                needs_text_field = True

        if needs_text_field:
            return self._create_scientific_float_field(parent, field_config)
        else:
            return self._create_spinctrl_float_field(parent, field_config)

    def _create_spinctrl_float_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.SpinCtrlDouble:
        """Create a float input field using SpinCtrlDouble."""
        min_val = float(field_config.min_value) if field_config.min_value is not None else -sys.float_info.max
        max_val = float(field_config.max_value) if field_config.max_value is not None else sys.float_info.max

        widget = wx.SpinCtrlDouble(parent, min=min_val, max=max_val)

        # Set decimal places from format string
        decimals = 2
        if field_config.format_string:
            try:
                format_str = field_config.format_string.lower()
                if '.' in format_str and 'f' in format_str:
                    decimal_part = format_str.split('.')[1]
                    decimals = int(decimal_part.replace('f', ''))
            except (ValueError, IndexError):
                decimals = 2

        widget.SetDigits(decimals)

        if field_config.default_value is not None:
            widget.SetValue(float(field_config.default_value))

        # Store format string for later use
        if field_config.format_string:
            widget.format_string = field_config.format_string
        widget.field_type = "spinctrl_float"

        return widget

    def _create_scientific_float_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.TextCtrl:
        """Create a float input field using TextCtrl for scientific notation."""
        widget = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)

        # Set default value
        if field_config.default_value is not None:
            if field_config.format_string:
                try:
                    formatted_value = format(float(field_config.default_value), field_config.format_string)
                    widget.SetValue(formatted_value)
                except (ValueError, TypeError):
                    widget.SetValue(str(field_config.default_value))
            else:
                widget.SetValue(str(field_config.default_value))

        # Store format string and field type
        if field_config.format_string:
            widget.format_string = field_config.format_string
        widget.field_type = "scientific_float"

        # Set hint text based on format
        if field_config.format_string:
            format_str = field_config.format_string
            if 'e' in format_str.lower():
                widget.SetHint("e.g., 1.23e+06 or 1.23E-05")
            elif '%' in format_str:
                widget.SetHint("e.g., 0.856 (for 85.6%)")
            elif 'g' in format_str.lower():
                widget.SetHint("e.g., 123.456 or 1.23e+06")

        return widget

    def _create_email_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.TextCtrl:
        """Create an email input field."""
        widget = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
        widget.SetHint(field_config.placeholder or "Enter email address")
        if field_config.default_value:
            widget.SetValue(str(field_config.default_value))
        return widget

    def _create_password_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.TextCtrl:
        """Create a password input field."""
        widget = wx.TextCtrl(parent, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)
        widget.SetHint(field_config.placeholder or "Enter password")
        return widget

    def _create_textarea_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.TextCtrl:
        """Create a textarea field."""
        style = wx.TE_MULTILINE | wx.TE_WORDWRAP
        widget = wx.TextCtrl(parent, style=style)

        if field_config.default_value:
            widget.SetValue(str(field_config.default_value))

        widget.SetHint(field_config.placeholder or "Enter text...")

        # Set default size for multiline text
        if not field_config.height:
            widget.SetSize((-1, 100))

        return widget

    def _create_checkbox_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.CheckBox:
        """Create a checkbox field."""
        widget = wx.CheckBox(parent, label=field_config.label)
        if field_config.default_value:
            widget.SetValue(bool(field_config.default_value))
        return widget

    def _create_radio_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.Panel:
        """Create radio button group."""
        panel = wx.Panel(parent)
        sizer = wx.BoxSizer(wx.VERTICAL)

        radio_buttons = []
        for i, option in enumerate(field_config.options or []):
            style = wx.RB_GROUP if i == 0 else 0
            radio_button = wx.RadioButton(panel, label=option, style=style)
            radio_buttons.append(radio_button)
            sizer.Add(radio_button, 0, wx.ALL, 2)

            # Set default selection
            if field_config.default_value == option:
                radio_button.SetValue(True)

        panel.SetSizer(sizer)
        panel.radio_buttons = radio_buttons  # Store reference for value access
        return panel

    def _create_select_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.Choice:
        """Create a select (choice) field."""
        choices = field_config.options or []
        widget = wx.Choice(parent, choices=choices)

        # Set default selection
        if field_config.default_value and field_config.default_value in choices:
            index = choices.index(field_config.default_value)
            widget.SetSelection(index)

        return widget

    def _create_date_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.adv.DatePickerCtrl:
        """Create a date input field."""
        widget = wx.adv.DatePickerCtrl(parent, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)

        if field_config.default_value:
            try:
                # Parse YYYY-MM-DD format
                year, month, day = map(int, field_config.default_value.split('-'))
                date_val = wx.DateTime(day, month - 1, year)  # wxPython months are 0-based
                widget.SetValue(date_val)
            except (ValueError, AttributeError):
                pass  # Use current date as fallback

        return widget

    def _create_time_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.adv.TimePickerCtrl:
        """Create a time input field."""
        widget = wx.adv.TimePickerCtrl(parent)

        if field_config.default_value:
            try:
                # Parse HH:MM format
                hour, minute = map(int, field_config.default_value.split(':'))
                # Create a valid datetime first, then set the time
                time_val = wx.DateTime.Now()
                time_val.SetHour(hour)
                time_val.SetMinute(minute)
                time_val.SetSecond(0)
                widget.SetValue(time_val)
            except (ValueError, AttributeError):
                pass  # Use current time as fallback

        return widget

    def _create_datetime_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.Panel:
        """Create a datetime input field using separate date and time controls."""
        panel = wx.Panel(parent)
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create date picker
        date_picker = wx.adv.DatePickerCtrl(panel, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY)
        time_picker = wx.adv.TimePickerCtrl(panel)

        sizer.Add(date_picker, 1, wx.EXPAND | wx.RIGHT, 5)
        sizer.Add(time_picker, 1, wx.EXPAND)

        panel.SetSizer(sizer)
        panel.date_picker = date_picker
        panel.time_picker = time_picker

        # Set default value
        if field_config.default_value:
            try:
                # Parse ISO datetime format
                dt = datetime.fromisoformat(field_config.default_value.replace('Z', '+00:00'))

                date_val = wx.DateTime(dt.day, dt.month - 1, dt.year)
                date_picker.SetValue(date_val)

                # Create a valid datetime first, then set the time
                time_val = wx.DateTime.Now()
                time_val.SetHour(dt.hour)
                time_val.SetMinute(dt.minute)
                time_val.SetSecond(0)
                time_picker.SetValue(time_val)
            except (ValueError, AttributeError):
                pass  # Use current datetime as fallback

        return panel

    def _create_range_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.Slider:
        """Create a range (slider) field."""
        min_val = int(field_config.min_value) if field_config.min_value is not None else 0
        max_val = int(field_config.max_value) if field_config.max_value is not None else 100
        default_val = int(field_config.default_value) if field_config.default_value is not None else min_val

        widget = wx.Slider(parent, value=default_val, minValue=min_val, maxValue=max_val,
                          style=wx.SL_HORIZONTAL | wx.SL_LABELS)

        return widget

    def _create_file_field(self, parent: wx.Window, field_config: FieldConfig) -> WxCustomFileButton:
        """Create a file selection field."""
        file_mode = "open"
        if field_config.default_value == "save":
            file_mode = "save"

        widget = WxCustomFileButton(parent, file_mode)
        return widget

    def _create_color_field(self, parent: wx.Window, field_config: FieldConfig) -> WxCustomColorButton:
        """Create a color selection field."""
        initial_color = wx.Colour(255, 255, 255)

        if field_config.default_value:
            try:
                # Parse hex color
                hex_color = field_config.default_value.lstrip('#')
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                initial_color = wx.Colour(r, g, b)
            except (ValueError, IndexError):
                pass  # Use default color

        widget = WxCustomColorButton(parent, initial_color)
        return widget

    def _create_url_field(self, parent: wx.Window, field_config: FieldConfig) -> wx.TextCtrl:
        """Create a URL input field."""
        widget = wx.TextCtrl(parent, style=wx.TE_PROCESS_ENTER)
        widget.SetHint(field_config.placeholder or "Enter URL (http://...)")
        if field_config.default_value:
            widget.SetValue(str(field_config.default_value))
        return widget

    def get_widget_value(self, field_name: str) -> Any:
        """Get the current value of a widget."""
        if field_name not in self.widgets:
            return None

        widget = self.widgets[field_name]

        if isinstance(widget, wx.TextCtrl):
            return widget.GetValue()
        elif isinstance(widget, (wx.SpinCtrl, wx.SpinCtrlDouble)):
            value = widget.GetValue()
            # Handle format string for SpinCtrlDouble
            if isinstance(widget, wx.SpinCtrlDouble) and hasattr(widget, 'format_string'):
                format_string = widget.format_string
                try:
                    if any(char in format_string.lower() for char in ['e', 'g']):
                        return value
                    else:
                        return float(format(value, format_string.replace('%', '')))
                except (ValueError, TypeError):
                    return value
            return value
        elif isinstance(widget, wx.CheckBox):
            return widget.GetValue()
        elif isinstance(widget, wx.Choice):
            selection = widget.GetSelection()
            return widget.GetString(selection) if selection != wx.NOT_FOUND else ""
        elif isinstance(widget, wx.adv.DatePickerCtrl):
            date_val = widget.GetValue()
            return f"{date_val.GetYear():04d}-{date_val.GetMonth()+1:02d}-{date_val.GetDay():02d}"
        elif isinstance(widget, wx.adv.TimePickerCtrl):
            time_val = widget.GetValue()
            return f"{time_val.GetHour():02d}:{time_val.GetMinute():02d}"
        elif isinstance(widget, wx.Slider):
            return widget.GetValue()
        elif isinstance(widget, WxCustomFileButton):
            return widget.get_file_path()
        elif isinstance(widget, WxCustomColorButton):
            color = widget.get_color()
            return f"#{color.Red():02x}{color.Green():02x}{color.Blue():02x}"
        elif isinstance(widget, wx.Panel):
            # Handle radio buttons
            if hasattr(widget, 'radio_buttons'):
                for radio_button in widget.radio_buttons:
                    if radio_button.GetValue():
                        return radio_button.GetLabel()
            # Handle datetime panel
            elif hasattr(widget, 'date_picker') and hasattr(widget, 'time_picker'):
                date_val = widget.date_picker.GetValue()
                time_val = widget.time_picker.GetValue()
                dt = datetime(date_val.GetYear(), date_val.GetMonth()+1, date_val.GetDay(),
                            time_val.GetHour(), time_val.GetMinute())
                return dt.isoformat()

        return None

    def set_widget_value(self, field_name: str, value: Any) -> bool:
        """Set the value of a widget."""
        if field_name not in self.widgets:
            return False

        widget = self.widgets[field_name]

        try:
            if isinstance(widget, wx.TextCtrl):
                widget.SetValue(str(value))
            elif isinstance(widget, (wx.SpinCtrl, wx.SpinCtrlDouble)):
                widget.SetValue(float(value))
            elif isinstance(widget, wx.CheckBox):
                widget.SetValue(bool(value))
            elif isinstance(widget, wx.Choice):
                # Find the item index
                for i in range(widget.GetCount()):
                    if widget.GetString(i) == str(value):
                        widget.SetSelection(i)
                        break
            elif isinstance(widget, wx.adv.DatePickerCtrl):
                # Parse YYYY-MM-DD format
                year, month, day = map(int, str(value).split('-'))
                date_val = wx.DateTime(day, month - 1, year)
                widget.SetValue(date_val)
            elif isinstance(widget, wx.adv.TimePickerCtrl):
                # Parse HH:MM format
                hour, minute = map(int, str(value).split(':'))
                # Create a valid datetime first, then set the time
                time_val = wx.DateTime.Now()
                time_val.SetHour(hour)
                time_val.SetMinute(minute)
                time_val.SetSecond(0)
                widget.SetValue(time_val)
            elif isinstance(widget, wx.Slider):
                widget.SetValue(int(value))
            elif isinstance(widget, WxCustomFileButton):
                widget.set_file_path(str(value))
            elif isinstance(widget, WxCustomColorButton):
                # Parse hex color
                hex_color = str(value).lstrip('#')
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                color = wx.Colour(r, g, b)
                widget.set_color(color)
            elif isinstance(widget, wx.Panel):
                # Handle radio buttons
                if hasattr(widget, 'radio_buttons'):
                    for radio_button in widget.radio_buttons:
                        if radio_button.GetLabel() == str(value):
                            radio_button.SetValue(True)
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
                self.set_widget_value(field_name, "")
