"""
wxPython GUI builder class that creates applications from JSON configuration.
"""

from typing import Dict, Any, Optional, List
import wx
import wx.lib.scrolledpanel as scrolled

from ..config_loader import ConfigLoader, GuiConfig, FieldConfig
from ..utils import CallbackManagerMixin, ValidationMixin, DataPersistenceMixin, WidgetFactoryMixin, FieldStateMixin, ButtonHandlerMixin, ConfigLoaderMixin
from .wx_widget_factory import WxWidgetFactory


class WxGuiBuilder(CallbackManagerMixin, ValidationMixin, DataPersistenceMixin, WidgetFactoryMixin, FieldStateMixin, ButtonHandlerMixin, ConfigLoaderMixin, wx.Frame):
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

        # Event IDs for custom buttons
        self._next_button_id = wx.ID_HIGHEST + 1

        # Load configuration
        if config_path:
            self.load_config_from_file(config_path)
        elif config_dict:
            self.load_config_from_dict(config_dict)

    # load_config_from_file and load_config_from_dict provided by ConfigLoaderMixin

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

    def _create_tab_page(self, parent: wx.Notebook, tab_config: GuiConfig) -> wx.Panel:
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

    def _connect_field_events(self) -> None:
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

    def _on_field_changed(self, field_name: str, value: Any) -> None:
        """Handle field value changes."""
        # Emit field change event (similar to Qt signal)
        # For now, we'll just print the change
        print(f"Field '{field_name}' changed to: {value}")

    def _on_submit(self, event: wx.CommandEvent) -> None:
        """Handle submit button click."""
        self._handle_submit_click()

    def _on_form_submitted(self, form_data: Dict[str, Any]) -> None:
        """Wx-specific: print confirmation after submit."""
        print("Form submitted:", form_data)

    def _on_cancel(self, event: wx.CommandEvent) -> None:
        """Handle cancel button click."""
        self._handle_cancel_click()

    def _on_form_cancelled(self) -> None:
        """Wx-specific: close if no callback."""
        # Close the dialog if no custom cancel callback was set
        if not self.cancel_callback:
            self.Close()

    def _on_custom_button_clicked(self, button_name: str) -> None:
        """Handle custom button click."""
        self._handle_custom_button_click_by_name(button_name)

    def _show_error(self, message: str) -> None:
        """Show an error message dialog."""
        wx.MessageBox(message, "Error", wx.OK | wx.ICON_ERROR)

    # get_form_data, set_form_data, clear_form, get_field_value, set_field_value
    # are provided by WidgetFactoryMixin

    # get_custom_button_names is provided by CallbackManagerMixin
    # enable_field and show_field are provided by FieldStateMixin

    def _enable_widget(self, widget: wx.Window, enabled: bool) -> None:
        """Wx-specific widget enable/disable."""
        widget.Enable(enabled)

    def _show_widget(self, widget: wx.Window, visible: bool) -> None:
        """Wx-specific widget show/hide."""
        widget.Show(visible)

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
