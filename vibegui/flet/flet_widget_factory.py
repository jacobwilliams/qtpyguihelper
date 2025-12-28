"""
Widget factory for creating Flet controls based on field configurations.
"""

from __future__ import annotations

from typing import Dict, Any, Callable, Optional, List
import flet as ft

from vibegui.config_loader import FieldConfig
from vibegui.utils import NestedValueMixin


class FletWidgetFactory(NestedValueMixin):
    """Factory class for creating Flet controls based on field configurations."""

    def __init__(self) -> None:
        """Initialize the widget factory."""
        self.widgets: Dict[str, ft.Control] = {}
        self.change_callbacks: Dict[str, List[Callable]] = {}

    def create_widget(self, field_config: FieldConfig) -> ft.Control:
        """Create a Flet control based on the field configuration."""
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

        # Store widget reference
        if widget:
            self.widgets[field_config.name] = widget

        return widget

    def _create_label_text(self, field_config: FieldConfig) -> str:
        """Create label text for a field."""
        text = field_config.label or field_config.name
        if field_config.required:
            text += " *"
        return text

    def _create_text_field(self, field_config: FieldConfig) -> ft.TextField:
        """Create a text input field."""
        text_field = ft.TextField(
            label=self._create_label_text(field_config),
            value=str(field_config.default_value) if field_config.default_value else "",
            hint_text=field_config.placeholder or None,
            tooltip=field_config.tooltip or None,
            multiline=False,
            on_change=lambda e: self._trigger_change_callback(field_config.name, e.control.value)
        )
        return text_field

    def _create_number_field(self, field_config: FieldConfig) -> ft.TextField:
        """Create a number input field."""
        text_field = ft.TextField(
            label=self._create_label_text(field_config),
            value=str(field_config.default_value) if field_config.default_value else "",
            hint_text=field_config.placeholder or None,
            tooltip=field_config.tooltip or None,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=lambda e: self._trigger_change_callback(field_config.name, e.control.value)
        )
        return text_field

    def _create_int_field(self, field_config: FieldConfig) -> ft.TextField:
        """Create an integer input field."""
        text_field = ft.TextField(
            label=self._create_label_text(field_config),
            value=str(field_config.default_value) if field_config.default_value else "",
            hint_text=field_config.placeholder or None,
            tooltip=field_config.tooltip or None,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=lambda e: self._trigger_change_callback(field_config.name, e.control.value)
        )
        return text_field

    def _create_float_field(self, field_config: FieldConfig) -> ft.TextField:
        """Create a float input field."""
        text_field = ft.TextField(
            label=self._create_label_text(field_config),
            value=str(field_config.default_value) if field_config.default_value else "",
            hint_text=field_config.placeholder or None,
            tooltip=field_config.tooltip or None,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=lambda e: self._trigger_change_callback(field_config.name, e.control.value)
        )
        return text_field

    def _create_email_field(self, field_config: FieldConfig) -> ft.TextField:
        """Create an email input field."""
        text_field = ft.TextField(
            label=self._create_label_text(field_config),
            value=str(field_config.default_value) if field_config.default_value else "",
            hint_text=field_config.placeholder or None,
            tooltip=field_config.tooltip or None,
            keyboard_type=ft.KeyboardType.EMAIL,
            on_change=lambda e: self._trigger_change_callback(field_config.name, e.control.value)
        )
        return text_field

    def _create_password_field(self, field_config: FieldConfig) -> ft.TextField:
        """Create a password input field."""
        text_field = ft.TextField(
            label=self._create_label_text(field_config),
            value=str(field_config.default_value) if field_config.default_value else "",
            hint_text=field_config.placeholder or None,
            tooltip=field_config.tooltip or None,
            password=True,
            can_reveal_password=True,
            on_change=lambda e: self._trigger_change_callback(field_config.name, e.control.value)
        )
        return text_field

    def _create_textarea_field(self, field_config: FieldConfig) -> ft.TextField:
        """Create a multiline textarea field."""
        text_field = ft.TextField(
            label=self._create_label_text(field_config),
            value=str(field_config.default_value) if field_config.default_value else "",
            hint_text=field_config.placeholder or None,
            tooltip=field_config.tooltip or None,
            multiline=True,
            min_lines=3,
            max_lines=10,
            on_change=lambda e: self._trigger_change_callback(field_config.name, e.control.value)
        )
        return text_field

    def _create_checkbox_field(self, field_config: FieldConfig) -> ft.Checkbox:
        """Create a checkbox field."""
        checkbox = ft.Checkbox(
            label=self._create_label_text(field_config),
            value=bool(field_config.default_value) if field_config.default_value else False,
            tooltip=field_config.tooltip or None,
            on_change=lambda e: self._trigger_change_callback(field_config.name, e.control.value)
        )
        return checkbox

    def _create_radio_field(self, field_config: FieldConfig) -> ft.RadioGroup:
        """Create a radio button group."""
        radio_buttons = []

        if field_config.options:
            for option in field_config.options:
                radio_buttons.append(
                    ft.Radio(value=option, label=option)
                )

        radio_group = ft.RadioGroup(
            content=ft.Column(radio_buttons),
            value=str(field_config.default_value) if field_config.default_value else None,
            on_change=lambda e: self._trigger_change_callback(field_config.name, e.control.value)
        )

        return radio_group

    def _create_select_field(self, field_config: FieldConfig) -> ft.Dropdown:
        """Create a dropdown/select field."""
        dropdown_options = []

        if field_config.options:
            for option in field_config.options:
                dropdown_options.append(ft.dropdown.Option(option))

        dropdown = ft.Dropdown(
            label=self._create_label_text(field_config),
            options=dropdown_options,
            value=str(field_config.default_value) if field_config.default_value else None,
            tooltip=field_config.tooltip or None,
            on_change=lambda e: self._trigger_change_callback(field_config.name, e.control.value)
        )
        return dropdown

    def _create_date_field(self, field_config: FieldConfig) -> ft.TextField:
        """Create a date input field."""
        # Flet doesn't have native date picker yet, use text field with hint
        text_field = ft.TextField(
            label=self._create_label_text(field_config),
            value=str(field_config.default_value) if field_config.default_value else "",
            hint_text="YYYY-MM-DD",
            tooltip=field_config.tooltip or None,
            on_change=lambda e: self._trigger_change_callback(field_config.name, e.control.value)
        )
        return text_field

    def _create_time_field(self, field_config: FieldConfig) -> ft.TextField:
        """Create a time input field."""
        text_field = ft.TextField(
            label=self._create_label_text(field_config),
            value=str(field_config.default_value) if field_config.default_value else "",
            hint_text="HH:MM",
            tooltip=field_config.tooltip or None,
            on_change=lambda e: self._trigger_change_callback(field_config.name, e.control.value)
        )
        return text_field

    def _create_datetime_field(self, field_config: FieldConfig) -> ft.TextField:
        """Create a datetime input field."""
        text_field = ft.TextField(
            label=self._create_label_text(field_config),
            value=str(field_config.default_value) if field_config.default_value else "",
            hint_text="YYYY-MM-DD HH:MM",
            tooltip=field_config.tooltip or None,
            on_change=lambda e: self._trigger_change_callback(field_config.name, e.control.value)
        )
        return text_field

    def _create_range_field(self, field_config: FieldConfig) -> ft.Column:
        """Create a range/slider field."""
        # Parse min/max from field config if available
        min_val = 0
        max_val = 100

        # Create a text element to display the current value
        initial_value = float(field_config.default_value) if field_config.default_value else min_val
        value_text = ft.Text(
            value=f"{initial_value:.1f}",
            size=14,
            weight=ft.FontWeight.BOLD
        )

        def on_slider_change(e: ft.ControlEvent) -> None:
            """Update the value text when slider changes."""
            value_text.value = f"{e.control.value:.1f}"
            e.page.update()
            self._trigger_change_callback(field_config.name, e.control.value)

        slider = ft.Slider(
            min=min_val,
            max=max_val,
            value=initial_value,
            label="{value}",
            on_change=on_slider_change,
            expand=True
        )

        # Store reference to both slider and value text
        container = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(self._create_label_text(field_config)),
                        value_text
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                slider
            ],
            spacing=5
        )

        # Store the slider in widgets dict, not the container
        self.widgets[field_config.name] = slider

        return container

    def _create_file_field(self, field_config: FieldConfig) -> ft.FilePicker:
        """Create a file picker field."""
        # Flet file picker requires special handling
        file_picker = ft.FilePicker(
            on_result=lambda e: self._trigger_change_callback(
                field_config.name,
                e.files[0].path if e.files else None
            )
        )
        return file_picker

    def _create_color_field(self, field_config: FieldConfig) -> ft.TextField:
        """Create a color input field."""
        text_field = ft.TextField(
            label=self._create_label_text(field_config),
            value=str(field_config.default_value) if field_config.default_value else "#000000",
            hint_text="#RRGGBB",
            tooltip=field_config.tooltip or None,
            on_change=lambda e: self._trigger_change_callback(field_config.name, e.control.value)
        )
        return text_field

    def _create_url_field(self, field_config: FieldConfig) -> ft.TextField:
        """Create a URL input field."""
        text_field = ft.TextField(
            label=self._create_label_text(field_config),
            value=str(field_config.default_value) if field_config.default_value else "",
            hint_text=field_config.placeholder or "https://",
            tooltip=field_config.tooltip or None,
            keyboard_type=ft.KeyboardType.URL,
            on_change=lambda e: self._trigger_change_callback(field_config.name, e.control.value)
        )
        return text_field

    def get_value(self, field_name: str) -> Any:
        """Get the current value of a widget."""
        widget = self.widgets.get(field_name)
        if not widget:
            return None

        if isinstance(widget, ft.TextField):
            return widget.value
        elif isinstance(widget, ft.Checkbox):
            return widget.value
        elif isinstance(widget, ft.Dropdown):
            return widget.value
        elif isinstance(widget, ft.RadioGroup):
            return widget.value
        elif isinstance(widget, ft.Slider):
            return widget.value
        elif isinstance(widget, ft.FilePicker):
            # File pickers don't store values directly
            return None
        else:
            return None

    def set_value(self, field_name: str, value: Any) -> None:
        """Set the value of a widget."""
        widget = self.widgets.get(field_name)
        if not widget:
            return

        if isinstance(widget, ft.TextField):
            widget.value = str(value) if value is not None else ""
        elif isinstance(widget, ft.Checkbox):
            widget.value = bool(value)
        elif isinstance(widget, ft.Dropdown):
            widget.value = str(value) if value is not None else None
        elif isinstance(widget, ft.RadioGroup):
            widget.value = str(value) if value is not None else None
        elif isinstance(widget, ft.Slider):
            widget.value = float(value) if value is not None else 0

    # get_all_values and set_all_values provided by NestedValueMixin (now with nested support!)
    # Note: Renamed get_value/set_value to match mixin expectations
    def get_widget_value(self, field_name: str) -> Any:
        """Alias for get_value to match NestedValueMixin interface."""
        return self.get_value(field_name)

    def set_widget_value(self, field_name: str, value: Any) -> bool:
        """Alias for set_value to match NestedValueMixin interface."""
        try:
            self.set_value(field_name, value)
            return True
        except Exception:
            return False

    def clear_all_widgets(self) -> None:
        """Clear all widget values to their defaults."""
        # Note: Flet doesn't store field_configs, so we just reset to empty values
        for widget in self.widgets.values():
            if isinstance(widget, ft.TextField):
                widget.value = ""
            elif isinstance(widget, ft.Checkbox):
                widget.value = False
            elif isinstance(widget, (ft.Dropdown, ft.RadioGroup)):
                widget.value = None
            elif isinstance(widget, ft.Slider):
                widget.value = 0

    def add_change_callback(self, field_name: str, callback: Callable) -> None:
        """Add a callback to be called when a field's value changes."""
        if field_name not in self.change_callbacks:
            self.change_callbacks[field_name] = []
        self.change_callbacks[field_name].append(callback)

    def _trigger_change_callback(self, field_name: str, value: Any) -> None:
        """Trigger all change callbacks for a field."""
        if field_name in self.change_callbacks:
            for callback in self.change_callbacks[field_name]:
                callback(field_name, value)
