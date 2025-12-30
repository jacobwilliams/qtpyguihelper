"""
Main GUI builder class that creates GTK applications from JSON configuration.
"""

import json
from typing import Dict, Any, Callable, Optional
import os

from ..utils import CallbackManagerMixin, ValidationMixin, DataPersistenceMixin, WidgetFactoryMixin, FieldStateMixin, ButtonHandlerMixin, ConfigLoaderMixin, PlatformUtils

try:
    import gi

    # Try to determine GTK version
    GTK_VERSION = None
    GTK_MAJOR_VERSION = None

    # Try GTK4 first
    try:
        gi.require_version('Gtk', '4.0')
        gi.require_version('Gdk', '4.0')
        from gi.repository import Gtk, GLib, Gdk
        GTK_VERSION = '4.0'
        GTK_MAJOR_VERSION = 4
    except (ValueError, ImportError):
        # Fallback to GTK3
        try:
            gi.require_version('Gtk', '3.0')
            gi.require_version('Gdk', '3.0')
            from gi.repository import Gtk, GLib, Gdk
            GTK_VERSION = '3.0'
            GTK_MAJOR_VERSION = 3
        except (ValueError, ImportError):
            raise ImportError("No compatible GTK version found")

    GTK_AVAILABLE = True
except (ImportError, ValueError) as e:
    print(f"GTK backend not available: {e}")
    GTK_AVAILABLE = False
    GTK_VERSION = None
    GTK_MAJOR_VERSION = None
    # Create dummy classes for type hints
    class Gtk:
        class Window: pass
        class Widget: pass
        class Gdk:
            class WindowTypeHint:
                NORMAL = None
    class GLib:
        @staticmethod
        def timeout_add(*args): pass
    class Gdk:
        class WindowTypeHint:
            NORMAL = None

from vibegui.config_loader import ConfigLoader, GuiConfig, FieldConfig, CustomButtonConfig

if GTK_AVAILABLE:
    from vibegui.gtk.gtk_widget_factory import GtkWidgetFactory


class GtkGuiBuilder(CallbackManagerMixin, ValidationMixin, DataPersistenceMixin, WidgetFactoryMixin, FieldStateMixin, ButtonHandlerMixin, ConfigLoaderMixin):
    """Main GUI builder class that creates GTK applications from JSON configuration."""

    def __init__(self, config_path: Optional[str] = None, config_dict: Optional[Dict[str, Any]] = None, submit_callback: Optional[Callable] = None, cancel_callback: Optional[Callable] = None) -> None:
        """
        Initialize the GUI builder.

        Args:
            config_path: Path to JSON configuration file
            config_dict: Configuration dictionary (alternative to config_path)
            submit_callback: Callback function for form submission
            cancel_callback: Callback function for form cancellation
        """
        super().__init__()

        self.config_loader = ConfigLoader()
        self.widget_factory = None
        if GTK_AVAILABLE:
            self.widget_factory = GtkWidgetFactory()
        self.config: Optional[GuiConfig] = None
        self.window: Optional[Gtk.Window] = None
        self.main_container: Optional[Gtk.Widget] = None

        # Set callbacks from constructor if provided
        if submit_callback:
            self.submit_callback = submit_callback
        if cancel_callback:
            self.cancel_callback = cancel_callback

        # Load configuration
        if config_path:
            self.load_config_from_file(config_path)
        elif config_dict:
            self.load_config_from_dict(config_dict)

    # load_config_from_file and load_config_from_dict provided by ConfigLoaderMixin
    # GTK uses _setup_ui instead of _build_gui

    def _build_gui(self) -> None:
        """Alias for _setup_ui to match ConfigLoaderMixin expectations."""
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Set up the user interface based on the loaded configuration."""
        if not self.config:
            return

        # Get compatibility helpers
        compat = self._gtk_version_compat()

        # Create window if it doesn't exist
        if self.window is None:
            self.window = compat['window_new']()

        # Detect and apply OS theme early
        self._detect_os_theme()

        # Set window properties
        if self.config.window.title:
            self.window.set_title(self.config.window.title)
        else:
            self.window.set_title("GUI Application")

        if self.config.window.width and self.config.window.height:
            self.window.set_default_size(self.config.window.width, self.config.window.height)
        else:
            # Use larger default size for tabbed interfaces
            if self.config.tabs:
                self.window.set_default_size(800, 600)
            else:
                self.window.set_default_size(600, 400)

        # Center window on screen (GTK3 only)
        compat['set_window_position'](self.window)

        # Make window resizable
        self.window.set_resizable(True)

        # Version-specific window setup
        if GTK_MAJOR_VERSION == 3:
            # GTK3-specific window properties
            self.window.set_can_focus(True)
            self.window.set_accept_focus(True)
            self.window.set_focus_on_map(True)
            if compat['window_type_hint']:
                self.window.set_type_hint(compat['window_type_hint'])
            self.window.set_modal(False)
            self.window.set_skip_taskbar_hint(False)
            self.window.set_skip_pager_hint(False)
        # GTK4 handles many of these automatically

        # Connect window close event using compatibility helper
        compat['connect_delete_event'](self.window, self._on_window_close)

        # Create main scrolled window
        scrolled_window = compat['scrolled_new']()
        compat['set_scrolled_policy'](scrolled_window, Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        compat['set_border_width'](scrolled_window, 10)

        # Create main container
        main_box = compat['box_new'](compat['orientation_vertical'], 10)
        compat['container_add'](scrolled_window, main_box)
        self.main_container = main_box

        # Build the interface
        if self.config.use_tabs and self.config.tabs:
            self._build_tabbed_interface()
        else:
            self._build_form_interface()

        # Add a flexible spacer to push buttons to bottom
        spacer = Gtk.Box()
        spacer.set_vexpand(True)  # This will expand to fill available space
        compat = self._gtk_version_compat()
        compat['box_pack_start'](self.main_container, spacer, True, True, 0)

        # Add all buttons (custom + submit/cancel) on the same line
        self._add_all_buttons()

        # Set up field change monitoring
        self._setup_field_change_monitoring()

        # Add scrolled window to main window
        compat['container_add'](self.window, scrolled_window)

    def _build_form_interface(self) -> None:
        """Build a simple form interface."""
        if not self.config or not self.config.fields:
            return

        # Get compatibility helpers
        compat = self._gtk_version_compat()

        # Create container based on layout type
        form_container = self._create_layout_container(self.config.layout)
        compat['set_border_width'](form_container, 10)
        compat['box_pack_start'](self.main_container, form_container, True, True, 0)

        # Add fields based on layout type
        self._add_fields_to_container(form_container, self.config.fields, self.config.layout)

    def _build_tabbed_interface(self) -> None:
        """Build a tabbed interface."""
        if not self.config or not self.config.tabs:
            return

        # Create notebook widget for tabs
        notebook = Gtk.Notebook()
        compat = self._gtk_version_compat()
        compat['set_border_width'](notebook, 10)

        # Allow notebook to expand with window
        notebook.set_hexpand(True)  # Expand horizontally
        notebook.set_vexpand(True)  # Expand vertically to fill available space
        notebook.set_valign(Gtk.Align.FILL)  # Fill available vertical space

        # Pack notebook with expansion
        compat['box_pack_start'](self.main_container, notebook, True, True, 0)

        for tab_config in self.config.tabs:
            # Create tab content
            tab_scrolled = Gtk.ScrolledWindow()
            tab_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
            tab_scrolled.set_hexpand(True)
            tab_scrolled.set_vexpand(True)  # Allow vertical expansion to fill available space

            # Set reasonable minimum size and allow expansion
            try:
                # GTK4 method - set minimum content size but allow expansion
                tab_scrolled.set_min_content_height(300)  # Reasonable minimum height
                tab_scrolled.set_min_content_width(500)   # Minimum width
                # Don't set max_content_height to allow expansion with window size
            except AttributeError:
                # GTK3 fallback - set minimum size only
                tab_scrolled.set_size_request(500, 300)

            # Create container based on tab layout type
            tab_container = self._create_layout_container(tab_config.layout)
            tab_container.set_hexpand(True)
            tab_container.set_vexpand(False)
            tab_container.set_valign(Gtk.Align.START)
            compat['set_border_width'](tab_container, 10)

            compat['container_add'](tab_scrolled, tab_container)

            # Create tab label
            tab_label = Gtk.Label(label=tab_config.title)

            # Add tab to notebook
            notebook.append_page(tab_scrolled, tab_label)

            # Add tooltip to tab if provided
            if tab_config.tooltip:
                tab_label.set_tooltip_text(tab_config.tooltip)

            # Add fields to the tab based on layout type
            self._add_fields_to_container(tab_container, tab_config.fields, tab_config.layout)

    def _create_layout_container(self, layout_type: str = None) -> Gtk.Widget:
        """Create the appropriate container based on layout type."""
        compat = self._gtk_version_compat()

        if layout_type == "vertical":
            box = compat['box_new'](compat['orientation_vertical'], 10)
            return box
        elif layout_type == "horizontal":
            box = compat['box_new'](compat['orientation_horizontal'], 10)
            return box
        elif layout_type in ["grid", "form", None]:
            # Default to grid for form and grid layouts
            grid = Gtk.Grid()
            grid.set_column_spacing(10)
            grid.set_row_spacing(10)
            return grid
        else:
            # Fallback to vertical box
            return compat['box_new'](compat['orientation_vertical'], 10)

    def _add_fields_to_container(self, container: Gtk.Widget, fields: list, layout_type: str = None) -> None:
        """Add fields to a container based on layout type."""
        compat = self._gtk_version_compat()

        if layout_type in ["form", "grid", None]:
            # Grid layout: label and widget in columns
            for i, field_config in enumerate(fields):
                if field_config.type == "checkbox":
                    # Checkbox includes its own label
                    widget = self.widget_factory.create_widget(container, field_config)
                    if widget:
                        widget.set_hexpand(True)
                        widget.set_halign(Gtk.Align.FILL)
                        container.attach(widget, 0, i, 2, 1)
                        if field_config.tooltip:
                            widget.set_tooltip_text(field_config.tooltip)
                else:
                    # Regular field with separate label
                    label = self.widget_factory.create_label(container, field_config)
                    label.set_halign(Gtk.Align.START)
                    label.set_valign(Gtk.Align.START)
                    container.attach(label, 0, i, 1, 1)

                    widget = self.widget_factory.create_widget(container, field_config)
                    if widget:
                        widget.set_hexpand(True)
                        widget.set_halign(Gtk.Align.FILL)
                        if isinstance(widget, Gtk.ScrolledWindow):
                            widget.set_vexpand(False)
                            widget.set_valign(Gtk.Align.START)
                        container.attach(widget, 1, i, 1, 1)
                        if field_config.tooltip:
                            widget.set_tooltip_text(field_config.tooltip)

        elif layout_type == "horizontal":
            # Horizontal box: fields side by side
            for field_config in fields:
                # Create a vertical box for each field (label on top, widget below)
                field_box = compat['box_new'](compat['orientation_vertical'], 5)

                if field_config.type != "checkbox":
                    label = self.widget_factory.create_label(field_box, field_config)
                    label.set_halign(Gtk.Align.START)
                    compat['box_pack_start'](field_box, label, False, False, 0)

                widget = self.widget_factory.create_widget(field_box, field_config)
                if widget:
                    widget.set_hexpand(True)
                    compat['box_pack_start'](field_box, widget, True, True, 0)
                    if field_config.tooltip:
                        widget.set_tooltip_text(field_config.tooltip)

                compat['box_pack_start'](container, field_box, True, True, 0)

        else:  # vertical
            # Vertical box: fields stacked
            for field_config in fields:
                if field_config.type != "checkbox":
                    label = self.widget_factory.create_label(container, field_config)
                    label.set_halign(Gtk.Align.START)
                    compat['box_pack_start'](container, label, False, False, 0)

                widget = self.widget_factory.create_widget(container, field_config)
                if widget:
                    widget.set_hexpand(True)
                    compat['box_pack_start'](container, widget, False, False, 0)
                    if field_config.tooltip:
                        widget.set_tooltip_text(field_config.tooltip)

    def _add_field_to_grid(self, grid: Gtk.Grid, field_config: FieldConfig, row: int) -> None:
        """Add a field to the grid."""
        # Create label
        label = self.widget_factory.create_label(grid, field_config)
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.START)
        grid.attach(label, 0, row, 1, 1)

        # Create widget
        widget = self.widget_factory.create_widget(grid, field_config)
        if widget:
            widget.set_hexpand(True)
            widget.set_halign(Gtk.Align.FILL)

            # For textarea widgets, don't expand vertically to avoid taking too much space
            if isinstance(widget, Gtk.ScrolledWindow):
                widget.set_vexpand(False)  # Don't expand vertically
                widget.set_valign(Gtk.Align.START)  # Align to top

            grid.attach(widget, 1, row, 1, 1)

            # Add tooltip if specified
            if field_config.tooltip:
                widget.set_tooltip_text(field_config.tooltip)

    def _add_all_buttons(self) -> None:
        """Add all buttons (custom + submit/cancel) on the same line."""
        if not self.config:
            return

        # Get compatibility helpers
        compat = self._gtk_version_compat()

        # Create button box for all buttons
        button_box = compat['box_new'](compat['orientation_horizontal'], 5)
        compat['set_border_width'](button_box, 10)

        # Add custom buttons first (on the left)
        if self.config.custom_buttons:
            for button_config in self.config.custom_buttons:
                button = Gtk.Button(label=button_config.label)
                button.connect("clicked", lambda btn, cfg=button_config: self._handle_custom_button_click(cfg))

                if hasattr(button_config, 'tooltip') and button_config.tooltip:
                    button.set_tooltip_text(button_config.tooltip)

                compat['box_pack_start'](button_box, button, False, False, 0)

        # Add a spacer to push default buttons to the right
        spacer = Gtk.Box()
        spacer.set_hexpand(True)
        compat['box_pack_start'](button_box, spacer, True, True, 0)

        # Cancel button (added to the right)
        if self.config.cancel_button:
            cancel_text = self.config.cancel_label or "Cancel"
            cancel_button = compat['button_new'](cancel_text)
            cancel_button.connect("clicked", lambda btn: self._handle_cancel())
            compat['box_pack_start'](button_box, cancel_button, False, False, 0)

        # Submit button (added to the right, after cancel)
        if self.config.submit_button:
            submit_text = self.config.submit_label or "Submit"
            submit_button = compat['button_new'](submit_text)
            submit_button.connect("clicked", lambda btn: self._handle_submit())

            # Apply suggested-action style using the appropriate GTK version method
            if GTK_MAJOR_VERSION == 4:
                submit_button.add_css_class("suggested-action")
            else:
                # GTK3 - use the older method but suppress deprecation warnings
                submit_button.get_style_context().add_class("suggested-action")

            compat['box_pack_start'](button_box, submit_button, False, False, 0)

        compat['box_pack_start'](self.main_container, button_box, False, False, 0)

    def _setup_field_change_monitoring(self) -> None:
        """Set up field change monitoring."""

        def on_field_change(field_name: str, value: Any) -> None:
            if field_name in self.field_change_callbacks:
                for callback in self.field_change_callbacks[field_name]:
                    try:
                        callback(field_name, value)
                    except Exception as e:
                        print(f"Error in field change callback for {field_name}: {e}")

        # Add change callback to all fields
        for field_name in self.widget_factory.widgets.keys():
            self.widget_factory.add_change_callback(field_name, on_field_change)

    def _handle_submit(self) -> None:
        """Handle submit button click."""
        try:
            self._handle_submit_click()
        except Exception as e:
            self._show_error("Submit Error", f"Error submitting form: {str(e)}")

    def _on_form_submitted(self, form_data: Dict[str, Any]) -> None:
        """GTK-specific post-submit action - show form data if no callback."""
        if not self.submit_callback:
            self._show_form_data(form_data)

    def _handle_cancel(self) -> None:
        """Handle cancel button click."""
        try:
            self._handle_cancel_click()
        except Exception as e:
            self._show_error("Cancel Error", f"Error in cancel callback: {str(e)}")

    def _on_form_cancelled(self) -> None:
        """GTK-specific post-cancel action - quit if no callback."""
        if not self.cancel_callback and self.window:
            compat = self._gtk_version_compat()
            compat['main_quit']()

    def _handle_custom_button_click(self, button_config: CustomButtonConfig) -> None:
        """Handle custom button click."""
        try:
            # Note: GTK custom button callbacks take (button_config, form_data)
            # The mixin uses just button name, so we call callback directly here
            if button_config.name in self.custom_button_callbacks:
                callback = self.custom_button_callbacks[button_config.name]
                callback(button_config, self.get_form_data())
            else:
                # Default behavior
                self._show_info("Button Clicked", f"Custom button '{button_config.label}' clicked")
        except Exception as e:
            self._show_error("Button Error", f"Error in custom button callback: {str(e)}")

    def _show_form_data(self, data: Dict[str, Any]) -> None:
        """Show form data in a dialog (default submit behavior)."""
        try:
            # Create a dialog to display the data
            if GTK_MAJOR_VERSION == 4:
                # GTK4 approach
                dialog = Gtk.Dialog()
                dialog.set_transient_for(self.window)
                dialog.set_modal(True)
                dialog.set_title("Form Data")
                dialog.add_button("Close", Gtk.ResponseType.CLOSE)
            else:
                # GTK3 approach
                dialog = Gtk.Dialog(
                    title="Form Data",
                    parent=self.window,
                    flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT
                )
                dialog.add_button("Close", Gtk.ResponseType.CLOSE)

            dialog.set_default_size(500, 400)

            # Create scrolled window for content
            scrolled = Gtk.ScrolledWindow()
            scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

            # Create text view
            text_view = Gtk.TextView()
            text_view.set_editable(False)
            text_view.set_cursor_visible(False)

            # Format and display the data
            formatted_data = json.dumps(data, indent=2, default=str)
            buffer = text_view.get_buffer()
            buffer.set_text(formatted_data)

            # Get compatibility helpers
            compat = self._gtk_version_compat()
            compat['container_add'](scrolled, text_view)
            compat['container_add'](dialog.get_content_area(), scrolled)

            # Show dialog
            compat['show_all'](dialog)
            dialog.run()
            dialog.destroy()

        except Exception as e:
            # Fallback: print to console if dialog creation fails
            print("Form Data:")
            print(json.dumps(data, indent=2, default=str))

    def _show_error(self, title: str, message: str) -> None:
        """Show an error dialog."""
        try:
            if GTK_MAJOR_VERSION == 4:
                # GTK4 approach - use show() instead of run()
                dialog = Gtk.MessageDialog(
                    transient_for=self.window,
                    modal=True,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text=message
                )
                if title:
                    dialog.set_title(title)
                dialog.connect("response", lambda d, r: d.destroy())
                dialog.show()
            else:
                # GTK3 approach
                dialog = Gtk.MessageDialog(
                    parent=self.window,
                    flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                    type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    message_format=message
                )
                if title:
                    dialog.set_title(title)
                dialog.run()
                dialog.destroy()
        except Exception as e:
            # Fallback: print to console if dialog creation fails
            print(f"Error: {title}: {message}")
            print(f"Dialog creation failed: {e}")

    def _show_info(self, title: str, message: str) -> None:
        """Show an info dialog."""
        try:
            if GTK_MAJOR_VERSION == 4:
                # GTK4 approach - use show() instead of run()
                dialog = Gtk.MessageDialog(
                    transient_for=self.window,
                    modal=True,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text=message
                )
                if title:
                    dialog.set_title(title)
                dialog.connect("response", lambda d, r: d.destroy())
                dialog.show()
            else:
                # GTK3 approach
                dialog = Gtk.MessageDialog(
                    parent=self.window,
                    flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
                    type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    message_format=message
                )
                if title:
                    dialog.set_title(title)
                dialog.run()
                dialog.destroy()
        except Exception as e:
            # Fallback: print to console if dialog creation fails
            print(f"Info: {title}: {message}")
            print(f"Dialog creation failed: {e}")

    def _on_window_close(self, widget: Gtk.Widget, event: Gdk.Event) -> bool:
        """Handle window close event."""
        compat = self._gtk_version_compat()
        compat['main_quit']()
        return False

    def show(self) -> None:
        """Show the GUI window and bring it to the front (cross-platform)."""
        if self.window:
            # Get compatibility helpers
            compat = self._gtk_version_compat()

            # Make sure window is visible
            compat['show_all'](self.window)

            # Cross-platform window activation
            self.window.present()

            # Platform-specific window focusing
            if PlatformUtils.is_macos():  # macOS
                try:
                    # macOS-specific activation
                    self.window.set_urgency_hint(True)
                    self.window.present_with_time(0)
                    self.window.set_keep_above(True)
                    self.window.grab_focus()

                    # Try AppleScript to bring app to front
                    try:
                        import subprocess
                        subprocess.run(['osascript', '-e', 'tell application "System Events" to set frontmost of every process whose unix id is {} to true'.format(os.getpid())],
                                     capture_output=True, timeout=1, check=False)
                    except (subprocess.SubprocessError, FileNotFoundError):
                        pass  # AppleScript not available or failed

                    # Reset keep_above after a short delay
                    def reset_macos_hints() -> bool:
                        if self.window:
                            self.window.set_keep_above(False)
                            self.window.set_urgency_hint(False)
                        return False
                    GLib.timeout_add(500, reset_macos_hints)

                except Exception:
                    pass  # Fall back to basic present() if anything fails

            elif PlatformUtils.is_windows():  # Windows
                try:
                    # Windows-specific activation
                    self.window.set_urgency_hint(True)
                    self.window.present_with_time(0)
                    self.window.grab_focus()

                    # Reset urgency hint after a delay
                    def reset_windows_hints() -> bool:
                        if self.window:
                            self.window.set_urgency_hint(False)
                        return False
                    GLib.timeout_add(200, reset_windows_hints)

                except Exception:
                    pass  # Fall back to basic present() if anything fails

            elif PlatformUtils.is_linux():  # Linux and other Unix systems
                try:
                    # Linux-specific activation
                    self.window.set_urgency_hint(True)
                    self.window.present_with_time(0)

                    # On some Linux desktop environments, grab_focus might help
                    try:
                        self.window.grab_focus()
                    except Exception:
                        pass  # Some WMs don't support this

                    # Reset urgency hint after a delay
                    def reset_linux_hints() -> bool:
                        if self.window:
                            self.window.set_urgency_hint(False)
                        return False
                    GLib.timeout_add(300, reset_linux_hints)

                except Exception:
                    pass  # Fall back to basic present() if anything fails

    def hide(self) -> None:
        """Hide the GUI window."""
        if self.window:
            self.window.hide()

    def run(self) -> None:
        """Run the GUI application (start the main loop)."""
        if self.window:
            self.show()
            compat = self._gtk_version_compat()
            compat['main_loop']()

    # get_form_data, set_form_data, clear_form, get_field_value, set_field_value
    # are provided by WidgetFactoryMixin
    # enable_field and show_field are provided by FieldStateMixin

    def _enable_widget(self, widget: Gtk.Widget, enabled: bool) -> None:
        """GTK-specific widget enable/disable."""
        widget.set_sensitive(enabled)

    def _show_widget(self, widget: Gtk.Widget, visible: bool) -> None:
        """GTK-specific widget show/hide."""
        widget.set_visible(visible)

    @classmethod
    def create_and_run(cls, config_path: str = None, config_dict: Dict[str, Any] = None) -> 'GtkGuiBuilder':
        """
        Create a GUI builder and run it immediately.

        Args:
            config_path: Path to JSON configuration file
            config_dict: Configuration dictionary (alternative to config_path)

        Returns:
            The created GUI builder instance
        """
        builder = cls(config_path, config_dict)
        builder.run()
        return builder

    # ...existing code...

    def close(self) -> None:
        """Close the GUI application."""
        if self.window:
            compat = self._gtk_version_compat()
            compat['main_quit']()
            self.window.destroy()
            self.window = None

    def __del__(self) -> None:
        """Cleanup when the object is destroyed."""
        if hasattr(self, 'window') and self.window:
            try:
                self.window.destroy()
            except Exception:
                pass  # Window might already be destroyed

    def _run_gtk4_loop(self) -> None:
        """Run GTK4 main loop using GLib.MainLoop."""
        if not hasattr(self, '_main_loop'):
            self._main_loop = GLib.MainLoop()
        self._main_loop.run()

    def _quit_gtk4_loop(self) -> None:
        """Quit GTK4 main loop."""
        if hasattr(self, '_main_loop') and self._main_loop.is_running():
            self._main_loop.quit()

    def _gtk_version_compat(self) -> Dict[str, Any]:
        """Return compatibility helpers for different GTK versions."""
        if GTK_MAJOR_VERSION == 4:
            return {
                'window_new': lambda: Gtk.Window(),
                'set_window_position': lambda window: None,  # GTK4 doesn't have set_position
                'orientation_horizontal': Gtk.Orientation.HORIZONTAL,
                'orientation_vertical': Gtk.Orientation.VERTICAL,
                'box_new': lambda orientation, spacing: Gtk.Box(orientation=orientation, spacing=spacing),
                'button_new': lambda text: Gtk.Button(label=text),
                'window_type_hint': None,  # GTK4 doesn't have type hints
                'connect_delete_event': lambda window, callback: window.connect('close-request', lambda w: callback(w, None) or True),
                'scrolled_new': lambda: Gtk.ScrolledWindow(),
                'set_scrolled_policy': lambda sw, h, v: sw.set_policy(h, v),
                'set_border_width': lambda widget, width: None,  # GTK4 doesn't have border_width
                'container_add': lambda container, child: container.set_child(child),
                'box_pack_start': lambda box, child, expand, fill, padding: box.append(child),
                'box_pack_end': lambda box, child, expand, fill, padding: box.append(child),
                'show_all': lambda window: window.show(),
                'main_loop': lambda: self._run_gtk4_loop(),
                'main_quit': lambda: self._quit_gtk4_loop(),
            }
        else:  # GTK3
            return {
                'window_new': lambda: Gtk.Window(),
                'set_window_position': lambda window: window.set_position(Gtk.WindowPosition.CENTER),
                'orientation_horizontal': Gtk.Orientation.HORIZONTAL,
                'orientation_vertical': Gtk.Orientation.VERTICAL,
                'box_new': lambda orientation, spacing: Gtk.Box(orientation=orientation, spacing=spacing),
                'button_new': lambda text: Gtk.Button(label=text),
                'window_type_hint': Gdk.WindowTypeHint.NORMAL,
                'connect_delete_event': lambda window, callback: window.connect('delete-event', callback),
                'scrolled_new': lambda: Gtk.ScrolledWindow(),
                'set_scrolled_policy': lambda sw, h, v: sw.set_policy(h, v),
                'set_border_width': lambda widget, width: widget.set_border_width(width),
                'container_add': lambda container, child: container.add(child),
                'box_pack_start': lambda box, child, expand, fill, padding: box.pack_start(child, expand, fill, padding),
                'box_pack_end': lambda box, child, expand, fill, padding: box.pack_end(child, expand, fill, padding),
                'show_all': lambda window: window.show_all(),
                'main_loop': lambda: Gtk.main(),
                'main_quit': lambda: Gtk.main_quit(),
            }

    @property
    def backend(self) -> str:
        """Return the backend name with version info."""
        return f"gtk{GTK_MAJOR_VERSION}" if GTK_MAJOR_VERSION else "gtk"

    def _detect_os_theme(self) -> None:
        """Detect if the OS is using dark mode and configure GTK accordingly."""
        try:
            import platform

            # Check environment variables first
            if os.environ.get('GTK_THEME'):
                return  # User has manually set GTK_THEME, respect it

            dark_mode = False

            # macOS dark mode detection
            if PlatformUtils.is_macos():
                try:
                    import subprocess
                    result = subprocess.run(['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                                            capture_output=True, text=True, timeout=2)
                    dark_mode = result.stdout.strip() == 'Dark'
                except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                    pass

            # Linux/Unix dark mode detection
            elif PlatformUtils.is_linux():
                # Check GNOME/GTK settings
                try:
                    import subprocess
                    # Try gsettings first (GNOME/GTK)
                    result = subprocess.run(['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'],
                                            capture_output=True, text=True, timeout=2)
                    theme_name = result.stdout.strip().strip("'\"").lower()
                    dark_mode = 'dark' in theme_name or 'adwaita-dark' in theme_name

                    if not dark_mode:
                        # Try color-scheme setting (newer GNOME)
                        result = subprocess.run(['gsettings', 'get', 'org.gnome.desktop.interface', 'color-scheme'],
                                              capture_output=True, text=True, timeout=2)
                        color_scheme = result.stdout.strip().strip("'\"").lower()
                        dark_mode = 'dark' in color_scheme or 'prefer-dark' in color_scheme

                except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                    # Fallback: check environment variables
                    dark_mode = (os.environ.get('GTK_THEME', '').lower().find('dark') >= 0 or
                               os.environ.get('QT_STYLE_OVERRIDE', '').lower().find('dark') >= 0)

            # Windows dark mode detection
            elif PlatformUtils.is_windows():
                try:
                    import winreg
                    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                    key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                    value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                    dark_mode = value == 0  # 0 = dark mode, 1 = light mode
                    winreg.CloseKey(key)
                except (ImportError, OSError, FileNotFoundError):
                    pass

            # Apply theme based on detection
            if dark_mode:
                self._apply_dark_theme()
            else:
                self._apply_light_theme()

        except Exception as e:
            print(f"Warning: Could not detect OS theme: {e}")
            # Fallback to default theme
            pass

    def _apply_dark_theme(self) -> None:
        """Apply dark theme to GTK application."""
        try:
            if GTK_MAJOR_VERSION == 4:
                # GTK4: Use Adwaita-dark
                settings = Gtk.Settings.get_default()
                if settings:
                    settings.set_property("gtk-application-prefer-dark-theme", True)
                    settings.set_property("gtk-theme-name", "Adwaita-dark")
            elif GTK_MAJOR_VERSION == 3:
                # GTK3: More comprehensive dark theme setup
                settings = Gtk.Settings.get_default()
                if settings:
                    # First try to enable dark variant of current theme
                    settings.set_property("gtk-application-prefer-dark-theme", True)

                    # Get current theme and try dark variants
                    current_theme = settings.get_property("gtk-theme-name")

                    # Try dark variants in order of preference
                    dark_themes = [
                        "Adwaita-dark",
                        f"{current_theme}-dark" if current_theme else None,
                        f"{current_theme}:dark" if current_theme else None,
                        "Yaru-dark",
                        "Arc-Dark",
                        "Breeze-Dark",
                        "Materia-dark",
                        "Adwaita"  # Fallback with prefer-dark-theme=True
                    ]

                    theme_applied = False
                    for theme in dark_themes:
                        if theme:
                            try:
                                settings.set_property("gtk-theme-name", theme)
                                theme_applied = True
                                print(f"Applied GTK3 dark theme: {theme}")
                                break
                            except Exception as e:
                                continue

                    # If theme setting didn't work, try CSS styling approach
                    if not theme_applied or current_theme == "Adwaita":
                        self._apply_dark_css_styling()

        except Exception as e:
            print(f"Warning: Could not apply dark theme: {e}")

    def _apply_dark_css_styling(self) -> None:
        """Apply dark styling via CSS for GTK3 when theme switching doesn't work."""
        try:
            if GTK_MAJOR_VERSION == 3:
                # Apply CSS styling for dark theme
                css_provider = Gtk.CssProvider()
                dark_css = """
                * {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }

                window {
                    background-color: #2d2d2d;
                    color: #ffffff;
                }

                entry {
                    background-color: #404040;
                    color: #ffffff;
                    border: 1px solid #555555;
                }

                entry:focus {
                    border-color: #0066cc;
                }

                button {
                    background-color: #404040;
                    color: #ffffff;
                    border: 1px solid #555555;
                    border-radius: 3px;
                    padding: 6px 12px;
                    min-height: 24px;
                }

                button:hover {
                    background-color: #505050;
                    border-color: #666666;
                }

                button:active {
                    background-color: #353535;
                    border-color: #444444;
                }

                button:focus {
                    border-color: #0066cc;
                    outline: none;
                }

                checkbutton {
                    color: #ffffff;
                }

                checkbutton check {
                    background-color: #404040;
                    border: 1px solid #555555;
                }

                checkbutton check:checked {
                    background-color: #0066cc;
                    border-color: #0066cc;
                }

                radiobutton {
                    color: #ffffff;
                }

                radiobutton radio {
                    background-color: #404040;
                    border: 1px solid #555555;
                }

                radiobutton radio:checked {
                    background-color: #0066cc;
                    border-color: #0066cc;
                }

                combobox {
                    background-color: #404040;
                    color: #ffffff;
                    border: 1px solid #555555;
                    border-radius: 3px;
                    padding: 4px 8px;
                }

                combobox button {
                    background-color: #404040;
                    border: none;
                    border-left: 1px solid #555555;
                    color: #ffffff;
                    padding: 4px 8px;
                }

                combobox button:hover {
                    background-color: #505050;
                }

                combobox entry {
                    background-color: #404040;
                    color: #ffffff;
                    border: none;
                }

                combobox arrow {
                    color: #ffffff;
                    min-height: 16px;
                    min-width: 16px;
                }

                combobox popover {
                    background-color: #404040;
                    border: 1px solid #555555;
                }

                combobox popover listview {
                    background-color: #404040;
                    color: #ffffff;
                }

                combobox popover row {
                    background-color: #404040;
                    color: #ffffff;
                    padding: 4px 8px;
                }

                combobox popover row:hover {
                    background-color: #505050;
                }

                combobox popover row:selected {
                    background-color: #0066cc;
                }

                textview {
                    background-color: #404040;
                    color: #ffffff;
                }

                textview text {
                    background-color: #404040;
                    color: #ffffff;
                }

                label {
                    color: #ffffff;
                }

                scale {
                    color: #ffffff;
                }

                scale trough {
                    background-color: #404040;
                    border: 1px solid #555555;
                }

                scale highlight {
                    background-color: #0066cc;
                }

                scale slider {
                    background-color: #606060;
                    border: 1px solid #555555;
                }

                scrolledwindow {
                    background-color: #2d2d2d;
                }

                scrollbar {
                    background-color: #2d2d2d;
                }

                scrollbar slider {
                    background-color: #505050;
                    border-radius: 3px;
                }

                scrollbar slider:hover {
                    background-color: #606060;
                }
                """

                css_provider.load_from_data(dark_css.encode('utf-8'))

                # Apply CSS to default screen
                screen = Gdk.Screen.get_default()
                style_context = Gtk.StyleContext()
                style_context.add_provider_for_screen(
                    screen,
                    css_provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                )
                print("Applied custom dark CSS styling for GTK3")

        except Exception as e:
            print(f"Warning: Could not apply dark CSS styling: {e}")

    def _apply_light_theme(self) -> None:
        """Apply light theme to GTK application."""
        try:
            if GTK_MAJOR_VERSION >= 3:
                settings = Gtk.Settings.get_default()
                if settings:
                    settings.set_property("gtk-application-prefer-dark-theme", False)
                    settings.set_property("gtk-theme-name", "Adwaita")

        except Exception as e:
            print(f"Warning: Could not apply light theme: {e}")
