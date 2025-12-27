"""
Main GUI builder class that creates Flet applications from JSON configuration.
"""

from __future__ import annotations

import json
from typing import Dict, Any, Callable, Optional, List
import flet as ft

from vibegui.config_loader import ConfigLoader, GuiConfig, FieldConfig, CustomButtonConfig
from vibegui.utils import FileUtils, ValidationUtils, CallbackManagerMixin, ValidationMixin, DataPersistenceMixin, WidgetFactoryMixin, set_nested_value, flatten_nested_dict
from vibegui.flet.flet_widget_factory import FletWidgetFactory


class FletGuiBuilder(CallbackManagerMixin, ValidationMixin, DataPersistenceMixin, WidgetFactoryMixin):
    """Main GUI builder class that creates Flet applications from JSON configuration."""

    def __init__(self, config_path: Optional[str] = None, config_dict: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the GUI builder.

        Args:
            config_path: Path to JSON configuration file
            config_dict: Configuration dictionary (alternative to config_path)
        """
        super().__init__()

        self.config_loader = ConfigLoader()
        self.widget_factory = FletWidgetFactory()
        self.config: Optional[GuiConfig] = None
        self.page: Optional[ft.Page] = None
        self.main_column: Optional[ft.Column] = None

        # Load configuration
        if config_path:
            self.load_config_from_file(config_path)
        elif config_dict:
            self.load_config_from_dict(config_dict)

    def load_config_from_file(self, config_path: str) -> None:
        """Load configuration from a JSON file."""
        self.config = self.config_loader.load_from_file(config_path)

    def load_config_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """Load configuration from a dictionary."""
        self.config = self.config_loader.load_from_dict(config_dict)

    def _build_ui(self, page: ft.Page) -> None:
        """Build the user interface based on the loaded configuration."""
        if not self.config:
            return

        self.page = page

        # Set window properties
        page.title = self.config.window.title or "GUI Application"
        page.window_width = self.config.window.width or 600
        page.window_height = self.config.window.height or 400
        page.window_resizable = self.config.window.resizable

        # Set theme mode (automatically uses system theme by default)
        page.theme_mode = ft.ThemeMode.SYSTEM

        # Build the interface
        if self.config.use_tabs and self.config.tabs:
            content = self._build_tabbed_interface()
        else:
            content = self._build_form_interface()

        # Add buttons
        button_row = self._build_buttons()

        # Create main layout with proper spacing
        if content and button_row:
            # Use a column with tabs expanding and buttons at bottom
            main_content = ft.Column(
                controls=[
                    ft.Container(content=content, expand=True),
                    button_row
                ],
                expand=True,
                spacing=0
            )
            page.add(main_content)
        elif content:
            page.add(content)
        elif button_row:
            page.add(button_row)

    def _build_form_interface(self) -> Optional[ft.Container]:
        """Build a simple form interface."""
        if not self.config or not self.config.fields:
            return None

        form_controls = []

        for field_config in self.config.fields:
            # Create widget
            widget = self.widget_factory.create_widget(field_config)

            # Add to form
            form_controls.append(widget)

            # Set up field change monitoring
            if field_config.name in self.field_change_callbacks:
                for callback in self.field_change_callbacks[field_config.name]:
                    self.widget_factory.add_change_callback(field_config.name, callback)

        # Wrap in container with padding and scrolling
        form_container = ft.Container(
            content=ft.Column(form_controls, spacing=15, scroll=ft.ScrollMode.AUTO, expand=True),
            padding=20,
            expand=True
        )

        return form_container

    def _build_tabbed_interface(self) -> Optional[ft.Tabs]:
        """Build a tabbed interface."""
        if not self.config or not self.config.tabs:
            return None

        tabs = []

        for tab_config in self.config.tabs:
            # Create controls for this tab
            tab_controls = []

            if hasattr(tab_config, 'fields') and tab_config.fields:
                for field_config in tab_config.fields:
                    widget = self.widget_factory.create_widget(field_config)
                    tab_controls.append(widget)

                    # Set up field change monitoring
                    if field_config.name in self.field_change_callbacks:
                        for callback in self.field_change_callbacks[field_config.name]:
                            self.widget_factory.add_change_callback(field_config.name, callback)

            # Create tab
            tab = ft.Tab(
                text=tab_config.title,
                content=ft.Container(
                    content=ft.Column(tab_controls, spacing=15, scroll=ft.ScrollMode.AUTO, expand=True),
                    padding=20,
                    expand=True
                )
            )
            tabs.append(tab)

        # Tabs should expand to fill available space (but buttons will be below in layout)
        return ft.Tabs(tabs=tabs, expand=True)

    def _build_buttons(self) -> Optional[ft.Container]:
        """Build button row with custom and default buttons."""
        if not self.config:
            return None

        buttons = []

        # Add custom buttons on the left
        if self.config.custom_buttons:
            for button_config in self.config.custom_buttons:
                button = ft.ElevatedButton(
                    text=button_config.label,
                    on_click=lambda e, btn=button_config: self._handle_custom_button_click(btn)
                )
                buttons.append(button)

        # Add spacer to push default buttons to the right
        if buttons and (self.config.submit_button or self.config.cancel_button):
            buttons.append(ft.Container(expand=True))

        # Add default buttons on the right
        if self.config.cancel_button:
            cancel_text = self.config.cancel_label or "Cancel"
            cancel_button = ft.OutlinedButton(
                text=cancel_text,
                on_click=lambda e: self._handle_cancel()
            )
            buttons.append(cancel_button)

        if self.config.submit_button:
            submit_text = self.config.submit_label or "Submit"
            submit_button = ft.ElevatedButton(
                text=submit_text,
                on_click=lambda e: self._handle_submit()
            )
            buttons.append(submit_button)

        if not buttons:
            return None

        return ft.Container(
            content=ft.Row(buttons, alignment=ft.MainAxisAlignment.END),
            padding=ft.padding.only(left=20, right=20, bottom=20)
        )

    def _handle_submit(self) -> None:
        """Handle form submission."""
        # Validate required fields first
        if not self._validate_required_fields():
            return

        form_data = self.get_form_data()

        if self.submit_callback:
            self.submit_callback(form_data)
        else:
            # Default behavior: show dialog with form data
            if self.page:
                self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Form submitted successfully!"))
                )

    def _handle_cancel(self) -> None:
        """Handle form cancellation."""
        if self.cancel_callback:
            self.cancel_callback()
        else:
            # Default behavior: close window
            if self.page:
                self.page.window_close()

    def _handle_custom_button_click(self, button_config: CustomButtonConfig) -> None:
        """Handle custom button click."""
        callback = self.custom_button_callbacks.get(button_config.id)
        if callback:
            form_data = self.get_form_data()
            callback(form_data)
        else:
            # Default behavior for custom buttons
            if self.page:
                self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text(f"Custom button '{button_config.label}' clicked"))
                )

    def get_form_data(self) -> Dict[str, Any]:
        """Get all form data as a dictionary with support for nested fields."""
        form_data = {}

        if not self.config:
            return form_data

        # Get data from all fields
        all_fields = []

        if self.config.use_tabs and self.config.tabs:
            for tab in self.config.tabs:
                if hasattr(tab, 'fields') and tab.fields:
                    all_fields.extend(tab.fields)
        elif self.config.fields:
            all_fields = self.config.fields

        for field_config in all_fields:
            value = self.widget_factory.get_value(field_config.name)

            # Convert value based on field type
            if field_config.type in ('int', 'number'):
                try:
                    value = int(value) if value else None
                except (ValueError, TypeError):
                    value = None
            elif field_config.type == 'float':
                try:
                    value = float(value) if value else None
                except (ValueError, TypeError):
                    value = None
            elif field_config.type == 'checkbox':
                value = bool(value)

            # Support nested field names with dot notation
            if '.' in field_config.name:
                set_nested_value(form_data, field_config.name, value)
            else:
                form_data[field_config.name] = value

        return form_data

    def set_form_data(self, data: Dict[str, Any]) -> None:
        """Set form data from a dictionary with support for nested structures."""
        # Flatten nested dictionaries to dot notation for widget setting
        flat_data = flatten_nested_dict(data)
        self.widget_factory.set_all_values(flat_data)

        if self.page:
            self.page.update()

    def clear_form(self) -> None:
        """Clear all form fields."""
        if not self.config:
            return

        # Get all fields from config
        all_fields = []
        if self.config.use_tabs and self.config.tabs:
            for tab in self.config.tabs:
                if hasattr(tab, 'fields') and tab.fields:
                    all_fields.extend(tab.fields)
        elif self.config.fields:
            all_fields = self.config.fields

        # Clear each field
        for field_config in all_fields:
            self.widget_factory.set_value(field_config.name, "")

        if self.page:
            self.page.update()

    def get_field_value(self, field_name: str) -> Any:
        """Get the value of a specific field."""
        return self.widget_factory.get_value(field_name)

    def set_field_value(self, field_name: str, value: Any) -> bool:
        """Set the value of a specific field."""
        try:
            self.widget_factory.set_value(field_name, value)
            if self.page:
                self.page.update()
            return True
        except Exception:
            return False

    def enable_field(self, field_name: str, enabled: bool = True) -> None:
        """Enable or disable a specific field."""
        widget = self.widget_factory.widgets.get(field_name)
        if widget:
            widget.disabled = not enabled
            if self.page:
                self.page.update()

    def show_field(self, field_name: str, visible: bool = True) -> None:
        """Show or hide a specific field."""
        widget = self.widget_factory.widgets.get(field_name)
        if widget:
            widget.visible = visible
            if self.page:
                self.page.update()

    def _show_error(self, message: str) -> None:
        """Display an error message to the user."""
        if self.page:
            # Use an AlertDialog for errors
            dialog = ft.AlertDialog(
                title=ft.Text("Validation Error"),
                content=ft.Text(message),
                actions=[
                    ft.TextButton("OK", on_click=lambda e: self._close_dialog(dialog))
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            self.page.dialog = dialog
            dialog.open = True
            self.page.update()

    def _close_dialog(self, dialog: ft.AlertDialog) -> None:
        """Close an alert dialog."""
        dialog.open = False
        if self.page:
            self.page.update()

    def run(self) -> None:
        """Run the Flet application."""
        ft.app(target=self._build_ui)

    def show(self) -> None:
        """Show the GUI (alias for run in Flet)."""
        self.run()

    def close(self) -> None:
        """Close the GUI application."""
        if self.page:
            self.page.window_close()

    @staticmethod
    def create_and_run(config_path: str | None = None,
                       config_dict: Optional[Dict[str, Any]] = None,
                       submit_callback: Optional[Callable] = None) -> FletGuiBuilder:
        """
        Convenience method to create and run a GUI in one call.

        Args:
            config_path: Path to JSON configuration file
            config_dict: Configuration dictionary (alternative to config_path)
            submit_callback: Optional callback for form submission

        Returns:
            FletGuiBuilder instance
        """
        builder = FletGuiBuilder(config_path=config_path, config_dict=config_dict)
        if submit_callback:
            builder.set_submit_callback(submit_callback)
        builder.run()
        return builder
