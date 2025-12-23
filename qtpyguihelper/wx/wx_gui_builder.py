"""
wxPython GUI builder class that creates applications from JSON configuration.
"""

import json
from typing import Dict, Any, Callable, Optional, List
import wx
import wx.lib.scrolledpanel as scrolled

from ..config_loader import ConfigLoader, GuiConfig, FieldConfig, CustomButtonConfig
from ..utils import FileUtils, ValidationUtils
from .wx_widget_factory import WxWidgetFactory, get_nested_value


class WxGuiBuilder(wx.Frame):
    """wxPython GUI builder class that creates applications from JSON configuration."""

    def __init__(self, config_path: Optional[str] = None, config_dict: Optional[Dict[str, Any]] = None, parent: Optional[wx.Window] = None) -> None:
        """
        Initialize the wxPython GUI builder.

        Args:
            config_path: Path to JSON configuration file
            config_dict: Configuration dictionary (alternative to config_path)
            parent: Parent window (optional)
        """
        super().__init__(parent, title="GUI Application")

        self.config_loader = ConfigLoader()
        self.widget_factory = WxWidgetFactory()
        self.config: Optional[GuiConfig] = None
        self.submit_callback: Optional[Callable] = None
        self.cancel_callback: Optional[Callable] = None
        self.custom_button_callbacks: Dict[str, Callable] = {}

        # Event IDs for custom buttons
        self._next_button_id = wx.ID_HIGHEST + 1

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
        self.SetTitle(self.config.window.title)
        self.SetSize((self.config.window.width, self.config.window.height))

        # Set resizable property
        if not self.config.window.resizable:
            self.SetMaxSize((self.config.window.width, self.config.window.height))
            self.SetMinSize((self.config.window.width, self.config.window.height))

        # Create main panel
        main_panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Check if we should use tabs
        if self.config.use_tabs and self.config.tabs:
            # Create notebook (tab control)
            notebook = wx.Notebook(main_panel)

            # Create tabs
            for tab_config in self.config.tabs:
                if tab_config.enabled:
                    tab_page = self._create_tab_page(notebook, tab_config)
                    notebook.AddPage(tab_page, tab_config.title)
                    if tab_config.tooltip:
                        # wxPython doesn't have built-in tab tooltips, but we can add them to the page
                        tab_page.SetToolTip(tab_config.tooltip)

            main_sizer.Add(notebook, 1, wx.EXPAND | wx.ALL, 5)
        else:
            # Create scrolled panel for form fields
            scroll_panel = scrolled.ScrolledPanel(main_panel)
            scroll_panel.SetupScrolling()

            # Create form layout based on configuration
            form_sizer = self._create_form_sizer()

            # Add fields to the form
            self._add_fields_to_sizer(scroll_panel, form_sizer, self.config.fields, self.config.layout)

            scroll_panel.SetSizer(form_sizer)
            main_sizer.Add(scroll_panel, 1, wx.EXPAND | wx.ALL, 5)

        # Add buttons if enabled
        if self.config.submit_button or self.config.cancel_button or self.config.custom_buttons:
            button_sizer = self._create_button_sizer(main_panel)
            main_sizer.Add(button_sizer, 0, wx.EXPAND | wx.ALL, 5)

        main_panel.SetSizer(main_sizer)

        # Connect field change events
        self._connect_field_events()

    def _create_form_sizer(self) -> wx.Sizer:
        """Create the appropriate sizer based on configuration."""
        if self.config.layout == "vertical":
            return wx.BoxSizer(wx.VERTICAL)
        elif self.config.layout == "horizontal":
            return wx.BoxSizer(wx.HORIZONTAL)
        elif self.config.layout == "grid":
            # Create a flexible grid with 2 columns
            sizer = wx.FlexGridSizer(cols=2, hgap=10, vgap=5)
            sizer.AddGrowableCol(1)  # Make the second column (widgets) growable
            return sizer
        elif self.config.layout == "form":
            # Use FlexGridSizer for form layout (similar to QFormLayout)
            sizer = wx.FlexGridSizer(cols=2, hgap=10, vgap=5)
            sizer.AddGrowableCol(1)
            return sizer
        else:
            return wx.BoxSizer(wx.VERTICAL)

    def _add_fields_to_sizer(self, parent: wx.Window, sizer: wx.Sizer, fields: Optional[List[FieldConfig]] = None, layout_type: Optional[str] = None) -> None:
        """Add form fields to the sizer."""
        if fields is None:
            fields = self.config.fields

        for i, field_config in enumerate(fields):
            if layout_type in ["form", "grid"]:
                # Form/grid layout: add label and widget in pairs
                if field_config.type == "checkbox":
                    # For checkboxes, add empty space then the checkbox
                    sizer.Add((0, 0), 0)  # Empty space for label column
                    widget = self.widget_factory.create_widget(parent, field_config)
                    if widget:
                        sizer.Add(widget, 0, wx.EXPAND | wx.ALL, 2)
                else:
                    # Regular field with label
                    label = self.widget_factory.create_label(parent, field_config)
                    widget = self.widget_factory.create_widget(parent, field_config)

                    sizer.Add(label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 2)
                    if widget:
                        sizer.Add(widget, 1, wx.EXPAND | wx.ALL, 2)

            else:
                # Vertical or horizontal layout
                if field_config.type != "checkbox":
                    label = self.widget_factory.create_label(parent, field_config)
                    sizer.Add(label, 0, wx.ALL, 2)

                widget = self.widget_factory.create_widget(parent, field_config)
                if widget:
                    if layout_type == "horizontal":
                        sizer.Add(widget, 1, wx.EXPAND | wx.ALL, 2)
                    else:
                        sizer.Add(widget, 0, wx.EXPAND | wx.ALL, 2)

                    # Add spacing between fields in vertical layout
                    if layout_type == "vertical" and i < len(fields) - 1:
                        sizer.Add((0, 10), 0)

    def _create_tab_page(self, parent: wx.Notebook, tab_config) -> wx.Panel:
        """Create a tab page with its content."""
        # Create scrolled panel for the tab
        tab_panel = scrolled.ScrolledPanel(parent)
        tab_panel.SetupScrolling()

        # Create layout for the tab based on its configuration
        if tab_config.layout == "vertical":
            tab_sizer = wx.BoxSizer(wx.VERTICAL)
        elif tab_config.layout == "horizontal":
            tab_sizer = wx.BoxSizer(wx.HORIZONTAL)
        elif tab_config.layout == "grid":
            tab_sizer = wx.FlexGridSizer(cols=2, hgap=10, vgap=5)
            tab_sizer.AddGrowableCol(1)
        elif tab_config.layout == "form":
            tab_sizer = wx.FlexGridSizer(cols=2, hgap=10, vgap=5)
            tab_sizer.AddGrowableCol(1)
        else:
            tab_sizer = wx.BoxSizer(wx.VERTICAL)

        # Add fields to the tab
        self._add_fields_to_sizer(tab_panel, tab_sizer, tab_config.fields, tab_config.layout)

        tab_panel.SetSizer(tab_sizer)
        return tab_panel

    def _create_button_sizer(self, parent: wx.Window) -> wx.BoxSizer:
        """Create the button sizer with submit, cancel, and custom buttons."""
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Add custom buttons first (on the left)
        if self.config.custom_buttons:
            for button_config in self.config.custom_buttons:
                button_id = self._next_button_id
                self._next_button_id += 1

                custom_btn = wx.Button(parent, id=button_id, label=button_config.label)

                # Set tooltip if provided
                if button_config.tooltip:
                    custom_btn.SetToolTip(button_config.tooltip)

                # Set enabled state
                custom_btn.Enable(button_config.enabled)

                # Apply custom style if provided (limited support in wxPython)
                if button_config.style:
                    # Parse simple background-color and color styles
                    try:
                        import re
                        bg_match = re.search(r'background-color:\s*([^;]+)', button_config.style)
                        fg_match = re.search(r'color:\s*([^;]+)', button_config.style)

                        if bg_match:
                            bg_color = bg_match.group(1).strip()
                            if bg_color.startswith('#'):
                                # Parse hex color
                                hex_color = bg_color[1:]
                                r = int(hex_color[0:2], 16)
                                g = int(hex_color[2:4], 16)
                                b = int(hex_color[4:6], 16)
                                custom_btn.SetBackgroundColour(wx.Colour(r, g, b))

                        if fg_match:
                            fg_color = fg_match.group(1).strip()
                            if fg_color.startswith('#'):
                                hex_color = fg_color[1:]
                                r = int(hex_color[0:2], 16)
                                g = int(hex_color[2:4], 16)
                                b = int(hex_color[4:6], 16)
                                custom_btn.SetForegroundColour(wx.Colour(r, g, b))
                            elif fg_color == 'white':
                                custom_btn.SetForegroundColour(wx.Colour(255, 255, 255))
                            elif fg_color == 'black':
                                custom_btn.SetForegroundColour(wx.Colour(0, 0, 0))
                    except (ValueError, AttributeError) as e:
                        print(f"Warning: Could not parse button style '{button_config.style}': {e}")  # Ignore style parsing errors

                # Bind event
                self.Bind(wx.EVT_BUTTON,
                         lambda evt, name=button_config.name: self._on_custom_button_clicked(name),
                         custom_btn)

                button_sizer.Add(custom_btn, 0, wx.ALL, 5)

        button_sizer.AddStretchSpacer()  # Push standard buttons to the right

        if self.config.cancel_button:
            cancel_btn = wx.Button(parent, wx.ID_CANCEL, self.config.cancel_label)
            self.Bind(wx.EVT_BUTTON, self._on_cancel, cancel_btn)
            button_sizer.Add(cancel_btn, 0, wx.ALL, 5)

        if self.config.submit_button:
            submit_btn = wx.Button(parent, wx.ID_OK, self.config.submit_label)
            self.Bind(wx.EVT_BUTTON, self._on_submit, submit_btn)
            submit_btn.SetDefault()  # Make it the default button
            button_sizer.Add(submit_btn, 0, wx.ALL, 5)

        return button_sizer

    def _connect_field_events(self):
        """Connect field change events."""
        for field_name, widget in self.widget_factory.widgets.items():
            if isinstance(widget, wx.TextCtrl):
                # Connect text change event
                widget.Bind(wx.EVT_TEXT,
                           lambda evt, name=field_name: self._on_field_changed(name, evt.GetString()))
            elif isinstance(widget, (wx.SpinCtrl, wx.SpinCtrlDouble)):
                # Connect spin control change event
                widget.Bind(wx.EVT_SPINCTRL,
                           lambda evt, name=field_name: self._on_field_changed(name, evt.GetEventObject().GetValue()))
            elif isinstance(widget, wx.CheckBox):
                # Connect checkbox change event
                widget.Bind(wx.EVT_CHECKBOX,
                           lambda evt, name=field_name: self._on_field_changed(name, evt.IsChecked()))
            elif isinstance(widget, wx.Choice):
                # Connect choice change event
                widget.Bind(wx.EVT_CHOICE,
                           lambda evt, name=field_name: self._on_field_changed(name,
                               evt.GetEventObject().GetString(evt.GetSelection()) if evt.GetSelection() != wx.NOT_FOUND else ""))
            elif isinstance(widget, (wx.adv.DatePickerCtrl, wx.adv.TimePickerCtrl)):
                # Connect date/time picker change events
                if isinstance(widget, wx.adv.DatePickerCtrl):
                    widget.Bind(wx.adv.EVT_DATE_CHANGED,
                               lambda evt, name=field_name: self._on_field_changed(name, self.widget_factory.get_widget_value(field_name)))
                else:  # TimePickerCtrl
                    widget.Bind(wx.adv.EVT_TIME_CHANGED,
                               lambda evt, name=field_name: self._on_field_changed(name, self.widget_factory.get_widget_value(field_name)))
            elif isinstance(widget, wx.Slider):
                # Connect slider change event
                widget.Bind(wx.EVT_SLIDER,
                           lambda evt, name=field_name: self._on_field_changed(name, evt.GetInt()))
            elif isinstance(widget, wx.Panel):
                # Handle radio buttons
                if hasattr(widget, 'radio_buttons'):
                    for radio_button in widget.radio_buttons:
                        radio_button.Bind(wx.EVT_RADIOBUTTON,
                                         lambda evt, name=field_name: self._on_field_changed(name, evt.GetEventObject().GetLabel()))

    def _on_field_changed(self, field_name: str, value: Any):
        """Handle field value changes."""
        # Emit field change event (similar to Qt signal)
        # For now, we'll just print the change
        print(f"Field '{field_name}' changed to: {value}")

    def _on_submit(self, event):
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

        # For wxPython, we can post a custom event or call EndModal for dialogs
        # This is a basic implementation
        print("Form submitted:", form_data)

    def _on_cancel(self, event):
        """Handle cancel button click."""
        # Call custom callback if set
        if self.cancel_callback:
            try:
                self.cancel_callback()
            except Exception as e:
                self._show_error(f"Cancel callback error: {str(e)}")

        print("Form cancelled")

    def _on_custom_button_clicked(self, button_name: str):
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

    def _show_error(self, message: str):
        """Show an error message dialog."""
        wx.MessageBox(message, "Error", wx.OK | wx.ICON_ERROR)

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

    def set_custom_button_callback(self, button_name: str, callback: Callable[[Dict[str, Any]], None]):
        """
        Set a callback function to be called when a custom button is clicked.

        Args:
            button_name: The name of the custom button as defined in the configuration
            callback: Function to call when button is clicked. Receives form data as parameter.
        """
        self.custom_button_callbacks[button_name] = callback

    def remove_custom_button_callback(self, button_name: str):
        """Remove a custom button callback."""
        if button_name in self.custom_button_callbacks:
            del self.custom_button_callbacks[button_name]

    def get_custom_button_names(self) -> List[str]:
        """Get a list of all custom button names from the configuration."""
        if self.config and self.config.custom_buttons:
            return [button.name for button in self.config.custom_buttons]
        return []

    def enable_field(self, field_name: str, enabled: bool = True):
        """Enable or disable a specific field."""
        if field_name in self.widget_factory.widgets:
            self.widget_factory.widgets[field_name].Enable(enabled)

    def show_field(self, field_name: str, visible: bool = True):
        """Show or hide a specific field."""
        if field_name in self.widget_factory.widgets:
            self.widget_factory.widgets[field_name].Show(visible)

        if field_name in self.widget_factory.labels:
            self.widget_factory.labels[field_name].Show(visible)

    def load_data_from_file(self, data_file_path: str) -> bool:
        """
        Load form data from a JSON file and populate the GUI.
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
        """
        try:
            if not self.config:
                return False

            loaded_count = 0
            for field_config in self.config.fields:
                field_name = field_config.name

                if '.' in field_name:
                    field_value = get_nested_value(data, field_name)
                    if field_value is not None:
                        success = self.widget_factory.set_widget_value(field_name, field_value)
                        if success:
                            loaded_count += 1
                    elif field_config.default_value is not None:
                        success = self.widget_factory.set_widget_value(field_name, field_config.default_value)
                        if success:
                            loaded_count += 1
                else:
                    if field_name in data:
                        success = self.widget_factory.set_widget_value(field_name, data[field_name])
                        if success:
                            loaded_count += 1
                    elif field_config.default_value is not None:
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

    @staticmethod
    def create_and_run(config_path: Optional[str] = None,
                      config_dict: Optional[Dict[str, Any]] = None) -> 'WxGuiBuilder':
        """
        Create and run a wxPython GUI application.
        """
        app = wx.App()

        gui_builder = WxGuiBuilder(config_path=config_path, config_dict=config_dict)
        gui_builder.Show()

        app.MainLoop()
        return gui_builder
