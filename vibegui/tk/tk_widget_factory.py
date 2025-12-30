"""
Widget factory for creating tkinter widgets based on field configurations.
"""

import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
from typing import Any, Dict, Optional, List, Callable

from vibegui.config_loader import FieldConfig
from vibegui.utils import NestedValueMixin


class CustomColorButton(tk.Button):
    """Custom button widget for color selection."""

    def __init__(self, parent: tk.Widget, initial_color: str = "#ffffff", callback: Optional[Callable] = None) -> None:
        super().__init__(parent)
        self.current_color = initial_color
        self.callback = callback
        self.config(text="Choose Color", command=self._choose_color, bg=initial_color)

    def _choose_color(self) -> None:
        """Open color chooser dialog."""
        color = colorchooser.askcolor(color=self.current_color, title="Choose Color")
        if color[1]:  # color[1] is the hex value
            self.current_color = color[1]
            self.config(bg=self.current_color)
            if self.callback:
                self.callback(self.current_color)

    def get_color(self) -> str:
        """Get the current color."""
        return self.current_color

    def set_color(self, color: str) -> None:
        """Set the current color."""
        self.current_color = color
        self.config(bg=color)


class RadioButtonGroup:
    """Container for radio button groups."""

    def __init__(self, parent: tk.Widget) -> None:
        self.parent = parent
        self.var = tk.StringVar()
        self.buttons: List[tk.Radiobutton] = []

    def add_button(self, text: str, value: str, **kwargs: Any) -> tk.Radiobutton:
        """Add a radio button to the group."""
        button = tk.Radiobutton(
            self.parent,
            text=text,
            variable=self.var,
            value=value,
            **kwargs
        )
        self.buttons.append(button)
        return button

    def get_value(self) -> str:
        """Get the selected value."""
        return self.var.get()

    def set_value(self, value: str) -> None:
        """Set the selected value."""
        self.var.set(value)


class TkWidgetFactory(NestedValueMixin):
    """Factory class for creating tkinter widgets based on field configurations."""

    def __init__(self) -> None:
        """Initialize the widget factory."""
        self.widgets: Dict[str, tk.Widget] = {}
        self.radio_groups: Dict[str, RadioButtonGroup] = {}
        self.change_callbacks: Dict[str, List[Callable]] = {}
        self.theme_colors: Optional[Dict[str, str]] = None
        self.field_configs: Dict[str, FieldConfig] = {}

    def set_theme_colors(self, theme_colors: Dict[str, str]) -> None:
        """Set theme colors for widgets."""
        self.theme_colors = theme_colors

    def create_widget(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Widget:
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

        # Store widget reference
        if widget:
            self.widgets[field_config.name] = widget

        return widget

    def create_label(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Label:
        """Create a label for the field."""
        text = field_config.label or field_config.name
        if field_config.required:
            text += " *"

        label = tk.Label(parent, text=text)
        return label

    def _create_text_field(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Entry:
        """Create a text input field."""
        entry = tk.Entry(parent)

        # Apply theme colors if available
        if self.theme_colors:
            entry.configure(
                bg=self.theme_colors['entry_bg'],
                fg=self.theme_colors['entry_fg'],
                insertbackground=self.theme_colors['entry_fg']  # Cursor color
            )

        if field_config.default_value:
            entry.insert(0, str(field_config.default_value))

        if field_config.placeholder:
            # Simple placeholder implementation
            self._add_placeholder(entry, field_config.placeholder)

        self._setup_change_callback(entry, field_config.name, lambda: entry.get())
        return entry

    def _create_number_field(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Entry:
        """Create a number input field."""
        entry = tk.Entry(parent)

        # Apply theme colors if available
        if self.theme_colors:
            entry.configure(
                bg=self.theme_colors['entry_bg'],
                fg=self.theme_colors['entry_fg'],
                insertbackground=self.theme_colors['entry_fg']  # Cursor color
            )

        # Validation for numbers
        vcmd = (parent.register(self._validate_number), '%P')
        entry.config(validate='key', validatecommand=vcmd)

        if field_config.default_value is not None:
            entry.insert(0, str(field_config.default_value))

        self._setup_change_callback(entry, field_config.name, lambda: self._get_number_value(entry))
        return entry

    def _create_int_field(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Spinbox:
        """Create an integer input field."""
        min_val = field_config.min_value if field_config.min_value is not None else -2147483648
        max_val = field_config.max_value if field_config.max_value is not None else 2147483647

        spinbox = tk.Spinbox(
            parent,
            from_=min_val,
            to=max_val,
            increment=1
        )

        if field_config.default_value is not None:
            default_val = str(int(field_config.default_value))
            spinbox.delete(0, tk.END)  # Clear any existing content
            spinbox.insert(0, default_val)

        self._setup_change_callback(spinbox, field_config.name, lambda: self._get_int_value(spinbox))
        return spinbox

    def _create_float_field(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Entry:
        """Create a float input field."""
        entry = tk.Entry(parent)

        # Apply theme colors if available
        if self.theme_colors:
            entry.configure(
                bg=self.theme_colors['entry_bg'],
                fg=self.theme_colors['entry_fg'],
                insertbackground=self.theme_colors['entry_fg']  # Cursor color
            )

        # Validation for floats
        vcmd = (parent.register(self._validate_float), '%P')
        entry.config(validate='key', validatecommand=vcmd)

        if field_config.default_value is not None:
            entry.insert(0, str(float(field_config.default_value)))

        self._setup_change_callback(entry, field_config.name, lambda: self._get_float_value(entry))
        return entry

    def _create_email_field(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Entry:
        """Create an email input field."""
        entry = tk.Entry(parent)

        # Apply theme colors if available
        if self.theme_colors:
            entry.configure(
                bg=self.theme_colors['entry_bg'],
                fg=self.theme_colors['entry_fg'],
                insertbackground=self.theme_colors['entry_fg']  # Cursor color
            )

        if field_config.default_value:
            entry.insert(0, str(field_config.default_value))

        if field_config.placeholder:
            self._add_placeholder(entry, field_config.placeholder)

        self._setup_change_callback(entry, field_config.name, lambda: entry.get())
        return entry

    def _create_password_field(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Entry:
        """Create a password input field."""
        entry = tk.Entry(parent, show="*")

        # Apply theme colors if available
        if self.theme_colors:
            entry.configure(
                bg=self.theme_colors['entry_bg'],
                fg=self.theme_colors['entry_fg'],
                insertbackground=self.theme_colors['entry_fg']  # Cursor color
            )

        if field_config.placeholder:
            self._add_placeholder(entry, field_config.placeholder)

        self._setup_change_callback(entry, field_config.name, lambda: entry.get())
        return entry

    def _create_textarea_field(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Text:
        """Create a textarea input field."""
        height = 4  # Default rows
        if field_config.height:
            height = max(1, field_config.height // 20)  # Approximate conversion

        text_widget = tk.Text(parent, height=height, wrap=tk.WORD)

        # Apply theme colors if available
        if self.theme_colors:
            text_widget.configure(
                bg=self.theme_colors['entry_bg'],
                fg=self.theme_colors['entry_fg'],
                insertbackground=self.theme_colors['entry_fg']  # Cursor color
            )

        if field_config.default_value:
            text_widget.insert("1.0", str(field_config.default_value))

        self._setup_change_callback(text_widget, field_config.name,
                                   lambda: text_widget.get("1.0", tk.END).rstrip('\n'))
        return text_widget

    def _create_checkbox_field(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Checkbutton:
        """Create a checkbox field."""
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(
            parent,
            text=field_config.label or field_config.name,
            variable=var
        )

        if field_config.default_value:
            var.set(bool(field_config.default_value))

        # Store the variable for value retrieval
        checkbox._tk_var = var

        self._setup_change_callback(checkbox, field_config.name, lambda: var.get())
        return checkbox

    def _create_radio_field(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Frame:
        """Create a radio button group."""
        frame = tk.Frame(parent)
        group = RadioButtonGroup(frame)

        options = field_config.options or []
        for option in options:
            if isinstance(option, dict):
                text = option.get('label', option.get('value', ''))
                value = option.get('value', '')
            else:
                text = value = str(option)

            button = group.add_button(text, value)
            button.pack(anchor='w')

        # Set default value
        if field_config.default_value:
            group.set_value(str(field_config.default_value))

        # Store the group for value retrieval
        frame._radio_group = group
        self.radio_groups[field_config.name] = group

        self._setup_change_callback(frame, field_config.name, lambda: group.get_value())
        return frame

    def _create_select_field(self, parent: tk.Widget, field_config: FieldConfig) -> ttk.Combobox:
        """Create a select/dropdown field."""
        values = []
        options = field_config.options or []

        for option in options:
            if isinstance(option, dict):
                values.append(option.get('label', option.get('value', '')))
            else:
                values.append(str(option))

        combobox = ttk.Combobox(parent, values=values, state="readonly")

        if field_config.default_value:
            default_str = str(field_config.default_value)
            # Try to find the default in the options by value first
            for i, option in enumerate(options):
                if isinstance(option, dict):
                    if option.get('value') == default_str:
                        combobox.current(i)
                        break
                elif str(option) == default_str:
                    combobox.current(i)
                    break

        # Store options for value mapping
        combobox._field_options = options

        self._setup_change_callback(combobox, field_config.name,
                                   lambda: self._get_select_value(combobox))
        return combobox

    def _create_date_field(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Entry:
        """Create a date input field."""
        entry = tk.Entry(parent)

        # Apply theme colors if available
        if self.theme_colors:
            entry.configure(
                bg=self.theme_colors['entry_bg'],
                fg=self.theme_colors['entry_fg'],
                insertbackground=self.theme_colors['entry_fg']  # Cursor color
            )

        # Add format hint
        entry.insert(0, "YYYY-MM-DD")
        self._add_placeholder(entry, "YYYY-MM-DD")

        if field_config.default_value:
            entry.delete(0, tk.END)
            if isinstance(field_config.default_value, str):
                entry.insert(0, field_config.default_value)
            else:
                entry.insert(0, str(field_config.default_value))

        self._setup_change_callback(entry, field_config.name, lambda: entry.get())
        return entry

    def _create_time_field(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Entry:
        """Create a time input field."""
        entry = tk.Entry(parent)

        # Apply theme colors if available
        if self.theme_colors:
            entry.configure(
                bg=self.theme_colors['entry_bg'],
                fg=self.theme_colors['entry_fg'],
                insertbackground=self.theme_colors['entry_fg']  # Cursor color
            )

        # Add format hint
        self._add_placeholder(entry, "HH:MM:SS")

        if field_config.default_value:
            entry.delete(0, tk.END)
            entry.insert(0, str(field_config.default_value))

        self._setup_change_callback(entry, field_config.name, lambda: entry.get())
        return entry

    def _create_datetime_field(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Entry:
        """Create a datetime input field."""
        entry = tk.Entry(parent)

        # Apply theme colors if available
        if self.theme_colors:
            entry.configure(
                bg=self.theme_colors['entry_bg'],
                fg=self.theme_colors['entry_fg'],
                insertbackground=self.theme_colors['entry_fg']  # Cursor color
            )

        # Add format hint
        self._add_placeholder(entry, "YYYY-MM-DD HH:MM:SS")

        if field_config.default_value:
            entry.delete(0, tk.END)
            entry.insert(0, str(field_config.default_value))

        self._setup_change_callback(entry, field_config.name, lambda: entry.get())
        return entry

    def _create_range_field(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Frame:
        """Create a range/slider field."""
        frame = tk.Frame(parent)

        min_val = field_config.min_value if field_config.min_value is not None else 0
        max_val = field_config.max_value if field_config.max_value is not None else 100

        # Create a scale widget
        scale = tk.Scale(
            frame,
            from_=min_val,
            to=max_val,
            orient=tk.HORIZONTAL,
            length=200
        )

        if field_config.default_value is not None:
            scale.set(field_config.default_value)

        # Add label to show current value
        value_label = tk.Label(frame, text=str(scale.get()))

        def update_label(*args) -> None:
            value_label.config(text=str(scale.get()))

        scale.config(command=update_label)

        scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        value_label.pack(side=tk.RIGHT, padx=(5, 0))

        # Store scale for value retrieval
        frame._scale = scale

        self._setup_change_callback(frame, field_config.name, lambda: scale.get())
        return frame

    def _create_file_field(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Frame:
        """Create a file input field."""
        frame = tk.Frame(parent)

        entry = tk.Entry(frame)

        # Apply theme colors if available
        if self.theme_colors:
            entry.configure(
                bg=self.theme_colors['entry_bg'],
                fg=self.theme_colors['entry_fg'],
                insertbackground=self.theme_colors['entry_fg']  # Cursor color
            )

        entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        def browse_file() -> None:
            filename = filedialog.askopenfilename()
            if filename:
                entry.delete(0, tk.END)
                entry.insert(0, filename)

        button = tk.Button(frame, text="Browse...", command=browse_file)
        button.pack(side=tk.RIGHT, padx=(5, 0))

        if field_config.default_value:
            entry.insert(0, str(field_config.default_value))

        # Store entry for value retrieval
        frame._entry = entry

        self._setup_change_callback(frame, field_config.name, lambda: entry.get())
        return frame

    def _create_color_field(self, parent: tk.Widget, field_config: FieldConfig) -> CustomColorButton:
        """Create a color input field."""
        initial_color = "#ffffff"
        if field_config.default_value:
            initial_color = str(field_config.default_value)

        color_button = CustomColorButton(parent, initial_color)

        self._setup_change_callback(color_button, field_config.name,
                                   lambda: color_button.get_color())
        return color_button

    def _create_url_field(self, parent: tk.Widget, field_config: FieldConfig) -> tk.Entry:
        """Create a URL input field."""
        entry = tk.Entry(parent)

        # Apply theme colors if available
        if self.theme_colors:
            entry.configure(
                bg=self.theme_colors['entry_bg'],
                fg=self.theme_colors['entry_fg'],
                insertbackground=self.theme_colors['entry_fg']  # Cursor color
            )

        if field_config.default_value:
            entry.insert(0, str(field_config.default_value))

        if field_config.placeholder:
            self._add_placeholder(entry, field_config.placeholder)

        self._setup_change_callback(entry, field_config.name, lambda: entry.get())
        return entry

    def _validate_number(self, value: str) -> bool:
        """Validate number input."""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _validate_float(self, value: str) -> bool:
        """Validate float input."""
        if value == "":
            return True
        if value in ["-", ".", "-."]:
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _get_number_value(self, entry: tk.Entry) -> Optional[float]:
        """Get numeric value from entry."""
        try:
            text = entry.get()
            return float(text) if text else None
        except ValueError:
            return None

    def _get_int_value(self, spinbox: tk.Spinbox) -> Optional[int]:
        """Get integer value from spinbox."""
        try:
            text = spinbox.get()
            return int(text) if text else None
        except ValueError:
            return None

    def _get_float_value(self, entry: tk.Entry) -> Optional[float]:
        """Get float value from entry."""
        try:
            text = entry.get()
            return float(text) if text else None
        except ValueError:
            return None

    def _get_select_value(self, combobox: ttk.Combobox) -> Optional[str]:
        """Get value from combobox, mapping back to original option value."""
        current_text = combobox.get()
        if not current_text:
            return None

        options = getattr(combobox, '_field_options', [])
        for option in options:
            if isinstance(option, dict):
                if option.get('label') == current_text:
                    return option.get('value')
            elif str(option) == current_text:
                return str(option)

        return current_text

    def _add_placeholder(self, entry: tk.Entry, placeholder: str) -> None:
        """Add placeholder text to an entry widget."""
        entry.insert(0, placeholder)

        # Use theme-aware colors for placeholder
        placeholder_color = 'grey'
        normal_color = 'black'

        if self.theme_colors:
            placeholder_color = '#999999' if self.theme_colors['entry_fg'] == '#ffffff' else '#666666'
            normal_color = self.theme_colors['entry_fg']

        entry.config(fg=placeholder_color)

        def on_focus_in(event: tk.Event) -> None:
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=normal_color)

        def on_focus_out(event: tk.Event) -> None:
            if not entry.get():
                entry.insert(0, placeholder)
                entry.config(fg=placeholder_color)

        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

    def _setup_change_callback(self, widget: tk.Widget, field_name: str, value_getter: Callable) -> None:
        """Setup change callback for a widget."""
        if field_name not in self.change_callbacks:
            self.change_callbacks[field_name] = []

        def on_change(*args) -> None:
            for callback in self.change_callbacks[field_name]:
                try:
                    callback(field_name, value_getter())
                except Exception as e:
                    print(f"Error in change callback for {field_name}: {e}")

        # Bind appropriate events based on widget type
        if isinstance(widget, tk.Entry):
            widget.bind('<KeyRelease>', on_change)
        elif isinstance(widget, tk.Text):
            widget.bind('<KeyRelease>', on_change)
        elif isinstance(widget, (tk.Checkbutton, tk.Radiobutton)):
            widget.config(command=on_change)
        elif isinstance(widget, ttk.Combobox):
            widget.bind('<<ComboboxSelected>>', on_change)
        elif isinstance(widget, tk.Scale):
            widget.config(command=on_change)
        elif isinstance(widget, tk.Spinbox):
            widget.bind('<KeyRelease>', on_change)

    def add_change_callback(self, field_name: str, callback: Callable) -> None:
        """Add a change callback for a field."""
        if field_name not in self.change_callbacks:
            self.change_callbacks[field_name] = []
        self.change_callbacks[field_name].append(callback)

    def get_widget_value(self, field_name: str) -> Any:
        """Get the current value of a widget."""
        if field_name not in self.widgets:
            return None

        widget = self.widgets[field_name]

        # Check more specific types first
        if isinstance(widget, ttk.Combobox):
            return self._get_select_value(widget)
        elif isinstance(widget, tk.Spinbox):
            return self._get_int_value(widget)
        elif isinstance(widget, CustomColorButton):
            return widget.get_color()
        elif isinstance(widget, tk.Entry):
            value = widget.get()
            # Handle placeholder text (only for tk.Entry, not ttk widgets)
            try:
                if widget.cget('fg') == 'grey':
                    return None
            except tk.TclError:
                # Widget doesn't support fg attribute, just return the value
                pass
            return value
        elif isinstance(widget, tk.Text):
            return widget.get("1.0", tk.END).rstrip('\n')
        elif isinstance(widget, tk.Checkbutton):
            return widget._tk_var.get()
        elif isinstance(widget, tk.Frame):
            if hasattr(widget, '_radio_group'):
                return widget._radio_group.get_value()
            elif hasattr(widget, '_scale'):
                return widget._scale.get()
            elif hasattr(widget, '_entry'):
                return widget._entry.get()

        return None

    def set_widget_value(self, field_name: str, value: Any) -> bool:
        """Set the value of a widget."""
        if field_name not in self.widgets:
            return False

        widget = self.widgets[field_name]

        try:
            if isinstance(widget, ttk.Combobox):
                if value is not None:
                    # Try to find and set the value
                    options = getattr(widget, '_field_options', [])
                    found = False
                    for i, option in enumerate(options):
                        if isinstance(option, dict):
                            if option.get('value') == str(value) or option.get('label') == str(value):
                                widget.current(i)
                                found = True
                                break
                        elif str(option) == str(value):
                            widget.current(i)
                            found = True
                            break
                    # If not found by value/label, try setting the text directly
                    if not found:
                        widget.set(str(value))
            elif isinstance(widget, tk.Entry):
                # Handle placeholder removal
                try:
                    if widget.cget('fg') == 'grey':
                        widget.config(fg='black')
                except tk.TclError:
                    # Widget doesn't support fg attribute (like ttk widgets)
                    pass
                widget.delete(0, tk.END)
                if value is not None:
                    widget.insert(0, str(value))
            elif isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
                if value is not None:
                    widget.insert("1.0", str(value))
            elif isinstance(widget, tk.Checkbutton):
                widget._tk_var.set(bool(value))
            elif isinstance(widget, tk.Frame):
                if hasattr(widget, '_radio_group'):
                    widget._radio_group.set_value(str(value) if value is not None else "")
                elif hasattr(widget, '_scale'):
                    widget._scale.set(value if value is not None else 0)
                elif hasattr(widget, '_entry'):
                    widget._entry.delete(0, tk.END)
                    if value is not None:
                        widget._entry.insert(0, str(value))
            elif isinstance(widget, tk.Spinbox):
                widget.delete(0, tk.END)
                if value is not None:
                    widget.insert(0, str(value))
            elif isinstance(widget, CustomColorButton):
                if value is not None:
                    widget.set_color(str(value))

            return True
        except Exception as e:
            print(f"Error setting value for {field_name}: {e}")
            return False

    def clear_all_widgets(self) -> None:
        """Clear all widget values to their defaults."""
        for field_name in self.widgets.keys():
            field_config = self.field_configs.get(field_name)
            if field_config and field_config.default_value is not None:
                self.set_widget_value(field_name, field_config.default_value)
            else:
                self.set_widget_value(field_name, "")

    # get_all_values and set_all_values provided by NestedValueMixin
