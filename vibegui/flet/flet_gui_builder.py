"""
Main GUI builder class that creates Flet applications from JSON configuration.
"""

from __future__ import annotations

from typing import Dict, Any, Callable, Optional
import flet as ft

from vibegui.config_loader import ConfigLoader, GuiConfig, CustomButtonConfig
from vibegui.utils import CallbackManagerMixin, ValidationMixin, DataPersistenceMixin, WidgetFactoryMixin, FieldStateMixin, ButtonHandlerMixin, ConfigLoaderMixin
from vibegui.flet.flet_widget_factory import FletWidgetFactory


class FletGuiBuilder(CallbackManagerMixin, ValidationMixin, DataPersistenceMixin, WidgetFactoryMixin, FieldStateMixin, ButtonHandlerMixin, ConfigLoaderMixin):
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

    # load_config_from_file and load_config_from_dict provided by ConfigLoaderMixin
    # Note: Flet doesn't build UI immediately, it's deferred until ft.app() calls _build_ui

    def _should_build_ui_on_config_load(self) -> bool:
        """Override to defer UI building until ft.app() is called."""
        return False

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

        # Build fields based on layout type
        form_content = self._create_layout_container(self.config.fields, self.config.layout)

        # Set up field change monitoring
        for field_config in self.config.fields:
            if field_config.name in self.field_change_callbacks:
                for callback in self.field_change_callbacks[field_config.name]:
                    self.widget_factory.add_change_callback(field_config.name, callback)

        # Wrap in container with padding and scrolling
        form_container = ft.Container(
            content=form_content,
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
            # Set up field change monitoring first
            if hasattr(tab_config, 'fields') and tab_config.fields:
                for field_config in tab_config.fields:
                    if field_config.name in self.field_change_callbacks:
                        for callback in self.field_change_callbacks[field_config.name]:
                            self.widget_factory.add_change_callback(field_config.name, callback)

            # Create content based on layout type
            tab_content = self._create_layout_container(
                tab_config.fields if hasattr(tab_config, 'fields') else [],
                tab_config.layout if hasattr(tab_config, 'layout') else 'vertical'
            )

            # Create tab (Note: Flet's Tab widget doesn't support tooltips)
            tab = ft.Tab(
                text=tab_config.title,
                content=ft.Container(
                    content=tab_content,
                    padding=20,
                    expand=True
                )
            )
            tabs.append(tab)

        # Tabs should expand to fill available space (but buttons will be below in layout)
        return ft.Tabs(tabs=tabs, expand=True)

    def _create_layout_container(self, fields: list, layout_type: str = None) -> ft.Control:
        """Create the appropriate container based on layout type."""
        if layout_type == "horizontal":
            # Horizontal layout: Row with fields side by side
            controls = []
            for field_config in fields:
                # Flet widgets already include labels, so just add the widget
                widget = self.widget_factory.create_widget(field_config)
                # Use fixed width containers to ensure horizontal layout
                controls.append(
                    ft.Container(
                        content=widget,
                        width=200,  # Fixed width for horizontal layout
                        padding=5
                    )
                )

            return ft.Row(controls, spacing=15, scroll=ft.ScrollMode.AUTO)

        elif layout_type == "grid":
            # Grid layout: 2-column responsive grid
            controls = []
            for field_config in fields:
                # Widgets already have built-in labels
                widget = self.widget_factory.create_widget(field_config)

                if field_config.type == "checkbox":
                    # Checkbox spans both columns
                    controls.append(
                        ft.Container(
                            content=widget,
                            col={"xs": 12},  # Full width on all screens
                            padding=5
                        )
                    )
                else:
                    # Widget in responsive column
                    controls.append(
                        ft.Container(
                            content=widget,
                            col={"xs": 12, "sm": 6},  # Full width on mobile, half on desktop
                            padding=5
                        )
                    )

            # Wrap ResponsiveRow in a scrollable Column
            return ft.Column(
                [ft.ResponsiveRow(controls, spacing=10, run_spacing=10)],
                scroll=ft.ScrollMode.AUTO,
                expand=True
            )

        elif layout_type == "form":
            # Form layout: vertical layout with widgets that have built-in labels
            controls = []
            for field_config in fields:
                # Widgets already have built-in labels
                widget = self.widget_factory.create_widget(field_config)
                controls.append(widget)

            return ft.Column(controls, spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)

        else:  # vertical or default
            # Vertical layout: Column with fields stacked
            controls = []
            for field_config in fields:
                widget = self.widget_factory.create_widget(field_config)
                controls.append(widget)

            return ft.Column(controls, spacing=15, scroll=ft.ScrollMode.AUTO, expand=True)

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
        self._handle_submit_click()

    def _on_form_submitted(self, form_data: Dict[str, Any]) -> None:
        """Flet-specific post-submit action - show snackbar if no callback."""
        if not self.submit_callback and self.page:
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Form submitted successfully!"))
            )

    def _handle_cancel(self) -> None:
        """Handle form cancellation."""
        self._handle_cancel_click()

    def _on_form_cancelled(self) -> None:
        """Flet-specific post-cancel action - close window if no callback."""
        if not self.cancel_callback and self.page:
            self.page.window_close()

    def _handle_custom_button_click(self, button_config: CustomButtonConfig) -> None:
        """Handle custom button click."""
        callback = self.custom_button_callbacks.get(button_config.name)
        if callback:
            form_data = self.get_form_data()
            # Flet custom callbacks receive just form_data (unlike Tk/GTK which get button_config too)
            callback(form_data)
        else:
            # Default behavior for custom buttons
            if self.page:
                self.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text(f"Custom button '{button_config.label}' clicked"))
                )

    # Override mixin methods to add Flet-specific page.update() calls

    def set_form_data(self, data: Dict[str, Any]) -> None:
        """Set form data - override to add page.update()."""
        super().set_form_data(data)
        if self.page:
            self.page.update()

    def clear_form(self) -> None:
        """Clear form - override to add page.update()."""
        super().clear_form()
        if self.page:
            self.page.update()

    def set_field_value(self, field_name: str, value: Any) -> bool:
        """Set field value - override to add page.update()."""
        result = super().set_field_value(field_name, value)
        if result and self.page:
            self.page.update()
        return result

    # enable_field and show_field are provided by FieldStateMixin

    def _enable_widget(self, widget: ft.Control, enabled: bool) -> None:
        """Flet-specific widget enable/disable."""
        widget.disabled = not enabled
        if self.page:
            self.page.update()

    def _show_widget(self, widget: ft.Control, visible: bool) -> None:
        """Flet-specific widget show/hide."""
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
