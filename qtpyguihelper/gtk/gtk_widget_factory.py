"""
Widget factory for creating GTK widgets from field configurations.
"""

from typing import Dict, Any, Optional, List, Callable
import datetime

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from qtpyguihelper.config_loader import FieldConfig

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, GLib
    GTK_AVAILABLE = True
except (ImportError, ValueError) as e:
    print(f"GTK widgets not available: {e}")
    GTK_AVAILABLE = False
    # Create dummy classes for type hints
    class Gtk:
        class Widget: pass
        class Label: pass
        class Entry: pass
        class SpinButton: pass
        class ScrolledWindow: pass
        class CheckButton: pass
        class Box: pass
        class ComboBoxText: pass
        class Scale: pass
        class ColorButton: pass


class GtkWidgetFactory:
    """Factory for creating GTK widgets from field configurations."""

    def __init__(self):
        """Initialize the widget factory."""
        if not GTK_AVAILABLE:
            raise ImportError("GTK backend is not available. Please install PyGObject and GTK development files.")

        self.widgets: Dict[str, Gtk.Widget] = {}
        self.labels: Dict[str, Gtk.Label] = {}
        self.field_configs: Dict[str, FieldConfig] = {}
        self.change_callbacks: Dict[str, List[Callable]] = {}

    def create_label(self, parent: Gtk.Widget, field_config: FieldConfig) -> Gtk.Label:
        """Create a label for a field."""
        label_text = field_config.label or field_config.name.replace('_', ' ').title()
        if field_config.required:
            label_text += " *"

        label = Gtk.Label(label=label_text)
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.CENTER)

        self.labels[field_config.name] = label
        return label

    def create_widget(self, parent: Gtk.Widget, field_config: FieldConfig) -> Optional[Gtk.Widget]:
        """Create a widget based on the field configuration."""
        self.field_configs[field_config.name] = field_config

        widget = None
        field_type = field_config.type.lower()

        if field_type in ['text', 'email', 'url', 'password']:
            widget = self._create_text_widget(field_config)
        elif field_type in ['int', 'number']:
            widget = self._create_int_widget(field_config)
        elif field_type == 'float':
            widget = self._create_float_widget(field_config)
        elif field_type == 'textarea':
            widget = self._create_textarea_widget(field_config)
        elif field_type in ['checkbox', 'check']:
            widget = self._create_checkbox_widget(field_config)
        elif field_type == 'radio':
            widget = self._create_radio_widget(field_config)
        elif field_type in ['select', 'combo']:
            widget = self._create_select_widget(field_config)
        elif field_type == 'date':
            widget = self._create_date_widget(field_config)
        elif field_type == 'time':
            widget = self._create_time_widget(field_config)
        elif field_type in ['range', 'spin']:
            widget = self._create_range_widget(field_config)
        elif field_type == 'file':
            widget = self._create_file_widget(field_config)
        elif field_type == 'color':
            widget = self._create_color_widget(field_config)
        else:
            # Default to text entry
            widget = self._create_text_widget(field_config)

        if widget:
            self.widgets[field_config.name] = widget
            self._setup_change_callback(field_config.name, widget)

        return widget

    def _create_text_widget(self, field_config: FieldConfig) -> Gtk.Entry:
        """Create a text entry widget."""
        entry = Gtk.Entry()

        if field_config.placeholder:
            entry.set_placeholder_text(field_config.placeholder)

        if field_config.default_value:
            entry.set_text(str(field_config.default_value))

        if field_config.type == 'password':
            entry.set_visibility(False)

        return entry

    def _create_int_widget(self, field_config: FieldConfig) -> Gtk.SpinButton:
        """Create an integer spin button widget."""
        min_val = field_config.min_value if field_config.min_value is not None else -2147483648
        max_val = field_config.max_value if field_config.max_value is not None else 2147483647

        adjustment = Gtk.Adjustment(
            value=field_config.default_value or 0,
            lower=min_val,
            upper=max_val,
            step_increment=1,
            page_increment=10
        )

        spin_button = Gtk.SpinButton(adjustment=adjustment)
        spin_button.set_digits(0)

        return spin_button

    def _create_float_widget(self, field_config: FieldConfig) -> Gtk.SpinButton:
        """Create a float spin button widget."""
        min_val = field_config.min_value if field_config.min_value is not None else -1e6
        max_val = field_config.max_value if field_config.max_value is not None else 1e6

        # Determine decimal places from format string
        digits = 2  # default
        if hasattr(field_config, 'format_string') and field_config.format_string:
            format_str = field_config.format_string
            if '.f' in format_str:
                try:
                    digits = int(format_str.split('.')[1].split('f')[0])
                except (ValueError, IndexError):
                    digits = 2

        adjustment = Gtk.Adjustment(
            value=field_config.default_value or 0.0,
            lower=min_val,
            upper=max_val,
            step_increment=10 ** (-digits),
            page_increment=1.0
        )

        spin_button = Gtk.SpinButton(adjustment=adjustment)
        spin_button.set_digits(digits)

        return spin_button

    def _create_textarea_widget(self, field_config: FieldConfig) -> Gtk.ScrolledWindow:
        """Create a multi-line text widget."""
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        text_view = Gtk.TextView()
        text_view.set_wrap_mode(Gtk.WrapMode.WORD)

        if field_config.default_value:
            buffer = text_view.get_buffer()
            buffer.set_text(str(field_config.default_value))

        # Set minimum height if specified
        if hasattr(field_config, 'height') and field_config.height:
            text_view.set_size_request(-1, field_config.height)

        scrolled_window.add(text_view)

        # Store reference to text_view for value retrieval
        scrolled_window._text_view = text_view

        return scrolled_window

    def _create_checkbox_widget(self, field_config: FieldConfig) -> Gtk.CheckButton:
        """Create a checkbox widget."""
        checkbox = Gtk.CheckButton(label=field_config.label or field_config.name)

        if field_config.default_value:
            checkbox.set_active(bool(field_config.default_value))

        return checkbox

    def _create_radio_widget(self, field_config: FieldConfig) -> Gtk.Box:
        """Create a radio button group widget."""
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)

        if not field_config.options:
            return box

        radio_group = None
        box._radio_buttons = []  # Store radio buttons for value retrieval

        for option in field_config.options:
            if radio_group is None:
                radio_button = Gtk.RadioButton(label=str(option))
                radio_group = radio_button
            else:
                radio_button = Gtk.RadioButton.new_from_widget(radio_group)
                radio_button.set_label(str(option))

            if field_config.default_value and str(field_config.default_value) == str(option):
                radio_button.set_active(True)

            box._radio_buttons.append((radio_button, option))
            box.pack_start(radio_button, False, False, 0)

        return box

    def _create_select_widget(self, field_config: FieldConfig) -> Gtk.ComboBoxText:
        """Create a combobox widget."""
        combo = Gtk.ComboBoxText()

        # Support both "options" and "choices" attributes
        options = field_config.options or getattr(field_config, 'choices', None)

        if options:
            for option in options:
                combo.append_text(str(option))

            if field_config.default_value:
                try:
                    index = options.index(field_config.default_value)
                    combo.set_active(index)
                except ValueError:
                    pass

        return combo

    def _create_date_widget(self, field_config: FieldConfig) -> Gtk.Entry:
        """Create a date entry widget."""
        entry = Gtk.Entry()
        entry.set_placeholder_text("YYYY-MM-DD")

        if field_config.default_value:
            entry.set_text(str(field_config.default_value))

        return entry

    def _create_time_widget(self, field_config: FieldConfig) -> Gtk.Entry:
        """Create a time entry widget."""
        entry = Gtk.Entry()
        entry.set_placeholder_text("HH:MM")

        if field_config.default_value:
            entry.set_text(str(field_config.default_value))

        return entry

    def _create_range_widget(self, field_config: FieldConfig) -> Gtk.Scale:
        """Create a range/slider widget."""
        min_val = field_config.min_value or 0
        max_val = field_config.max_value or 100

        adjustment = Gtk.Adjustment(
            value=field_config.default_value or min_val,
            lower=min_val,
            upper=max_val,
            step_increment=1,
            page_increment=10
        )

        scale = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=adjustment)
        scale.set_draw_value(True)
        scale.set_value_pos(Gtk.PositionType.BOTTOM)

        return scale

    def _create_file_widget(self, field_config: FieldConfig) -> Gtk.Box:
        """Create a file chooser widget."""
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        entry = Gtk.Entry()
        entry.set_placeholder_text("No file selected")
        if field_config.default_value:
            entry.set_text(str(field_config.default_value))

        button = Gtk.Button(label="Browse...")

        def on_browse_clicked(widget):
            dialog = Gtk.FileChooserDialog(
                title="Select File",
                parent=None,
                action=Gtk.FileChooserAction.OPEN
            )
            dialog.add_buttons(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN, Gtk.ResponseType.OK
            )

            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                filename = dialog.get_filename()
                entry.set_text(filename)

            dialog.destroy()

        button.connect("clicked", on_browse_clicked)

        box.pack_start(entry, True, True, 0)
        box.pack_start(button, False, False, 0)

        # Store reference to entry for value retrieval
        box._entry = entry

        return box

    def _create_color_widget(self, field_config: FieldConfig) -> Gtk.ColorButton:
        """Create a color chooser widget."""
        color_button = Gtk.ColorButton()

        if field_config.default_value:
            try:
                # Parse hex color
                color_str = field_config.default_value.lstrip('#')
                if len(color_str) == 6:
                    r = int(color_str[0:2], 16) / 255.0
                    g = int(color_str[2:4], 16) / 255.0
                    b = int(color_str[4:6], 16) / 255.0
                    color = Gtk.Gdk.RGBA(r, g, b, 1.0)
                    color_button.set_rgba(color)
            except (ValueError, AttributeError):
                pass

        return color_button

    def _setup_change_callback(self, field_name: str, widget: Gtk.Widget):
        """Set up change callback for a widget."""
        def on_change(*args):
            if field_name in self.change_callbacks:
                value = self.get_widget_value(field_name)
                for callback in self.change_callbacks[field_name]:
                    try:
                        callback(field_name, value)
                    except Exception as e:
                        print(f"Error in change callback for {field_name}: {e}")

        # Connect appropriate signal based on widget type
        if isinstance(widget, Gtk.Entry):
            widget.connect("changed", on_change)
        elif isinstance(widget, Gtk.SpinButton):
            widget.connect("value-changed", on_change)
        elif isinstance(widget, Gtk.CheckButton):
            widget.connect("toggled", on_change)
        elif isinstance(widget, Gtk.ComboBoxText):
            widget.connect("changed", on_change)
        elif isinstance(widget, Gtk.Scale):
            widget.connect("value-changed", on_change)
        elif isinstance(widget, Gtk.ColorButton):
            widget.connect("color-set", on_change)
        elif isinstance(widget, Gtk.ScrolledWindow) and hasattr(widget, '_text_view'):
            buffer = widget._text_view.get_buffer()
            buffer.connect("changed", on_change)
        elif isinstance(widget, Gtk.Box) and hasattr(widget, '_radio_buttons'):
            for radio_button, _ in widget._radio_buttons:
                radio_button.connect("toggled", on_change)

    def get_widget_value(self, field_name: str) -> Any:
        """Get the current value of a widget."""
        if field_name not in self.widgets:
            return None

        widget = self.widgets[field_name]
        field_config = self.field_configs.get(field_name)

        if isinstance(widget, Gtk.Entry):
            text = widget.get_text()
            if field_config and field_config.type in ['int', 'number']:
                try:
                    return int(text) if text else 0
                except ValueError:
                    return 0
            elif field_config and field_config.type == 'float':
                try:
                    return float(text) if text else 0.0
                except ValueError:
                    return 0.0
            return text

        elif isinstance(widget, Gtk.SpinButton):
            if field_config and field_config.type in ['int', 'number']:
                return int(widget.get_value())
            else:
                return widget.get_value()

        elif isinstance(widget, Gtk.CheckButton):
            return widget.get_active()

        elif isinstance(widget, Gtk.ComboBoxText):
            return widget.get_active_text()

        elif isinstance(widget, Gtk.Scale):
            return widget.get_value()

        elif isinstance(widget, Gtk.ColorButton):
            color = widget.get_rgba()
            # Convert to hex
            r = int(color.red * 255)
            g = int(color.green * 255)
            b = int(color.blue * 255)
            return f"#{r:02x}{g:02x}{b:02x}"

        elif isinstance(widget, Gtk.ScrolledWindow) and hasattr(widget, '_text_view'):
            buffer = widget._text_view.get_buffer()
            start_iter = buffer.get_start_iter()
            end_iter = buffer.get_end_iter()
            return buffer.get_text(start_iter, end_iter, True)

        elif isinstance(widget, Gtk.Box):
            if hasattr(widget, '_radio_buttons'):
                for radio_button, option in widget._radio_buttons:
                    if radio_button.get_active():
                        return option
                return None
            elif hasattr(widget, '_entry'):  # File widget
                return widget._entry.get_text()

        return None

    def set_widget_value(self, field_name: str, value: Any) -> bool:
        """Set the value of a widget."""
        if field_name not in self.widgets:
            return False

        widget = self.widgets[field_name]

        try:
            if isinstance(widget, Gtk.Entry):
                widget.set_text(str(value) if value is not None else "")

            elif isinstance(widget, Gtk.SpinButton):
                widget.set_value(float(value) if value is not None else 0)

            elif isinstance(widget, Gtk.CheckButton):
                widget.set_active(bool(value))

            elif isinstance(widget, Gtk.ComboBoxText):
                # Find and select the matching option
                model = widget.get_model()
                for i, row in enumerate(model):
                    if row[0] == str(value):
                        widget.set_active(i)
                        break

            elif isinstance(widget, Gtk.Scale):
                widget.set_value(float(value) if value is not None else 0)

            elif isinstance(widget, Gtk.ColorButton):
                if isinstance(value, str) and value.startswith('#'):
                    try:
                        color_str = value.lstrip('#')
                        r = int(color_str[0:2], 16) / 255.0
                        g = int(color_str[2:4], 16) / 255.0
                        b = int(color_str[4:6], 16) / 255.0
                        color = Gtk.Gdk.RGBA(r, g, b, 1.0)
                        widget.set_rgba(color)
                    except ValueError:
                        pass

            elif isinstance(widget, Gtk.ScrolledWindow) and hasattr(widget, '_text_view'):
                buffer = widget._text_view.get_buffer()
                buffer.set_text(str(value) if value is not None else "")

            elif isinstance(widget, Gtk.Box):
                if hasattr(widget, '_radio_buttons'):
                    for radio_button, option in widget._radio_buttons:
                        radio_button.set_active(str(option) == str(value))
                elif hasattr(widget, '_entry'):  # File widget
                    widget._entry.set_text(str(value) if value is not None else "")

            return True

        except Exception as e:
            print(f"Error setting value for {field_name}: {e}")
            return False

    def get_all_values(self) -> Dict[str, Any]:
        """Get values from all widgets."""
        values = {}
        for field_name in self.widgets.keys():
            value = self.get_widget_value(field_name)
            if value is not None:
                values[field_name] = value
        return values

    def set_all_values(self, values: Dict[str, Any]):
        """Set values for all widgets from a dictionary."""
        for field_name, value in values.items():
            self.set_widget_value(field_name, value)

    def clear_widgets(self):
        """Clear all widget values."""
        for field_name in self.widgets.keys():
            field_config = self.field_configs.get(field_name)
            if field_config and field_config.default_value is not None:
                self.set_widget_value(field_name, field_config.default_value)
            else:
                self.set_widget_value(field_name, "")

    def add_change_callback(self, field_name: str, callback: Callable[[str, Any], None]):
        """Add a change callback for a field."""
        if field_name not in self.change_callbacks:
            self.change_callbacks[field_name] = []
        self.change_callbacks[field_name].append(callback)
