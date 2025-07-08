"""
Main GUI builder class that creates GTK applications from JSON configuration.
"""

import json
from typing import Dict, Any, Callable, Optional, List
import os

from ..utils import FileUtils, ValidationUtils, PlatformUtils

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

from qtpyguihelper.config_loader import ConfigLoader, GuiConfig, FieldConfig, CustomButtonConfig

if GTK_AVAILABLE:
    from qtpyguihelper.gtk.gtk_widget_factory import GtkWidgetFactory


class GtkGuiBuilder:
    """Main GUI builder class that creates GTK applications from JSON configuration."""

    def __init__(self, config_path: Optional[str] = None, config_dict: Optional[Dict[str, Any]] = None, submit_callback: Optional[Callable] = None, cancel_callback: Optional[Callable] = None):
        """
        Initialize the GUI builder.

        Args:
            config_path: Path to JSON configuration file
            config_dict: Configuration dictionary (alternative to config_path)
            submit_callback: Callback function for form submission
            cancel_callback: Callback function for form cancellation
        """
        self.config_loader = ConfigLoader()
        self.widget_factory = None
        if GTK_AVAILABLE:
            self.widget_factory = GtkWidgetFactory()
        self.config: Optional[GuiConfig] = None
        self.window: Optional[Gtk.Window] = None
        self.main_container: Optional[Gtk.Widget] = None
        self.submit_callback: Optional[Callable] = submit_callback
        self.cancel_callback: Optional[Callable] = cancel_callback
        self.custom_button_callbacks: Dict[str, Callable] = {}
        self.field_change_callbacks: Dict[str, List[Callable]] = {}

        # Load configuration
        if config_path:
            self.load_config_from_file(config_path)
        elif config_dict:
            self.load_config_from_dict(config_dict)

    def load_config_from_file(self, config_path: str):
        """Load configuration from a JSON file."""
        self.config = self.config_loader.load_from_file(config_path)
        if self.config:
            self._setup_ui()

    def load_config_from_dict(self, config_dict: Dict[str, Any]):
        """Load configuration from a dictionary."""
        self.config = self.config_loader.load_from_dict(config_dict)
        if self.config:
            self._setup_ui()

    def _setup_ui(self):
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

        # Add custom buttons
        self._add_custom_buttons()

        # Add a flexible spacer to push buttons to bottom
        spacer = Gtk.Box()
        spacer.set_vexpand(True)  # This will expand to fill available space
        compat = self._gtk_version_compat()
        compat['box_pack_start'](self.main_container, spacer, True, True, 0)

        # Add default buttons (Submit/Cancel) - these will stay at bottom
        self._add_default_buttons()

        # Set up field change monitoring
        self._setup_field_change_monitoring()

        # Add scrolled window to main window
        compat['container_add'](self.window, scrolled_window)

    def _build_form_interface(self):
        """Build a simple form interface."""
        if not self.config or not self.config.fields:
            return

        # Get compatibility helpers
        compat = self._gtk_version_compat()

        # Create form grid
        form_grid = Gtk.Grid()
        form_grid.set_column_spacing(10)
        form_grid.set_row_spacing(10)
        compat['set_border_width'](form_grid, 10)

        compat['box_pack_start'](self.main_container, form_grid, True, True, 0)

        row = 0
        for field_config in self.config.fields:
            self._add_field_to_grid(form_grid, field_config, row)
            row += 1

    def _build_tabbed_interface(self):
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

            tab_grid = Gtk.Grid()
            tab_grid.set_column_spacing(10)
            tab_grid.set_row_spacing(10)
            tab_grid.set_hexpand(True)
            tab_grid.set_vexpand(False)  # Don't expand vertically - align to top
            tab_grid.set_valign(Gtk.Align.START)  # Align content to top of container
            compat['set_border_width'](tab_grid, 10)

            compat['container_add'](tab_scrolled, tab_grid)

            # Create tab label
            tab_label = Gtk.Label(label=tab_config.title)

            # Add tab to notebook
            notebook.append_page(tab_scrolled, tab_label)

            # Add fields to the tab
            row = 0
            for field_config in tab_config.fields:
                self._add_field_to_grid(tab_grid, field_config, row)
                row += 1

    def _add_field_to_grid(self, grid: Gtk.Grid, field_config: FieldConfig, row: int):
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

    def _add_custom_buttons(self):
        """Add custom buttons defined in the configuration."""
        if not self.config or not self.config.custom_buttons:
            return

        # Create frame for custom buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        compat = self._gtk_version_compat()
        compat['set_border_width'](button_box, 10)

        for button_config in self.config.custom_buttons:
            button = Gtk.Button(label=button_config.label)
            button.connect("clicked", lambda btn, cfg=button_config: self._handle_custom_button_click(cfg))

            if hasattr(button_config, 'tooltip') and button_config.tooltip:
                button.set_tooltip_text(button_config.tooltip)

            compat['box_pack_start'](button_box, button, False, False, 0)

        compat['box_pack_start'](self.main_container, button_box, False, False, 0)

    def _add_default_buttons(self):
        """Add default Submit and Cancel buttons."""
        if not self.config:
            return

        # Get compatibility helpers
        compat = self._gtk_version_compat()

        # Create frame for default buttons
        button_box = compat['box_new'](compat['orientation_horizontal'], 5)
        compat['set_border_width'](button_box, 10)
        button_box.set_halign(Gtk.Align.END)

        # Cancel button (added first to match Qt backend order)
        if self.config.cancel_button:
            cancel_text = self.config.cancel_label or "Cancel"
            cancel_button = compat['button_new'](cancel_text)
            cancel_button.connect("clicked", lambda btn: self._handle_cancel())
            compat['box_pack_start'](button_box, cancel_button, False, False, 0)

        # Submit button (added second to match Qt backend order)
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

    def _setup_field_change_monitoring(self):
        """Set up field change monitoring."""
        def on_field_change(field_name: str, value: Any):
            if field_name in self.field_change_callbacks:
                for callback in self.field_change_callbacks[field_name]:
                    try:
                        callback(field_name, value)
                    except Exception as e:
                        print(f"Error in field change callback for {field_name}: {e}")

        # Add change callback to all fields
        for field_name in self.widget_factory.widgets.keys():
            self.widget_factory.add_change_callback(field_name, on_field_change)

    def _handle_submit(self):
        """Handle submit button click."""
        try:
            # Validate required fields
            if not self._validate_required_fields():
                return

            # Get form data
            form_data = self.get_form_data()

            # Call submit callback if set
            if self.submit_callback:
                try:
                    self.submit_callback(form_data)
                except Exception as e:
                    self._show_error("Error", f"Error in submit callback: {str(e)}")
            else:
                # Default behavior - show the data
                self._show_form_data(form_data)

        except Exception as e:
            self._show_error("Error", f"Error submitting form: {str(e)}")

    def _handle_cancel(self):
        """Handle cancel button click."""
        if self.cancel_callback:
            try:
                self.cancel_callback()
            except Exception as e:
                self._show_error("Error", f"Error in cancel callback: {str(e)}")
        else:
            # Default behavior - close the window
            if self.window:
                compat = self._gtk_version_compat()
                compat['main_quit']()

    def _handle_custom_button_click(self, button_config: CustomButtonConfig):
        """Handle custom button click."""
        if button_config.name in self.custom_button_callbacks:
            try:
                callback = self.custom_button_callbacks[button_config.name]
                callback(button_config, self.get_form_data())
            except Exception as e:
                self._show_error("Error", f"Error in custom button callback: {str(e)}")
        else:
            # Default behavior
            self._show_info("Button Clicked", f"Custom button '{button_config.label}' clicked")

    def _validate_required_fields(self) -> bool:
        """Validate that all required fields have values."""
        if not self.config:
            return True

        # Collect all required field names and current form data
        required_field_names = []
        all_fields = []

        # Collect all fields from tabs or main form
        if self.config.use_tabs and self.config.tabs:
            for tab in self.config.tabs:
                all_fields.extend(tab.fields)
        else:
            all_fields = self.config.fields or []

        # Get required field names and current values
        for field_config in all_fields:
            if field_config.required:
                required_field_names.append(field_config.name)

        # Get current form data and validate using utility
        form_data = self.get_form_data()
        missing_field_names = ValidationUtils.validate_required_fields(form_data, required_field_names)

        if missing_field_names:
            # Convert field names back to labels for user-friendly display
            missing_labels = []
            for field_name in missing_field_names:
                field_config = next((f for f in all_fields if f.name == field_name), None)
                label = field_config.label if field_config else field_name
                missing_labels.append(label)

            self._show_error(
                "Required Fields Missing",
                f"Please fill in the following required fields:\n\n" + "\n".join(f"• {label}" for label in missing_labels)
            )
            return False

        return True

    def _show_form_data(self, data: Dict[str, Any]):
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

    def _show_error(self, title: str, message: str):
        """Show an error dialog."""
        try:
            if GTK_MAJOR_VERSION == 4:
                # GTK4 approach
                dialog = Gtk.MessageDialog(
                    transient_for=self.window,
                    modal=True,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text=message
                )
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

    def _show_info(self, title: str, message: str):
        """Show an info dialog."""
        try:
            if GTK_MAJOR_VERSION == 4:
                # GTK4 approach
                dialog = Gtk.MessageDialog(
                    transient_for=self.window,
                    modal=True,
                    message_type=Gtk.MessageType.INFO,
                    buttons=Gtk.ButtonsType.OK,
                    text=message
                )
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

    def _on_window_close(self, widget, event):
        """Handle window close event."""
        compat = self._gtk_version_compat()
        compat['main_quit']()
        return False

    def show(self):
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
                    def reset_macos_hints():
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
                    def reset_windows_hints():
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
                    def reset_linux_hints():
                        if self.window:
                            self.window.set_urgency_hint(False)
                        return False
                    GLib.timeout_add(300, reset_linux_hints)

                except Exception:
                    pass  # Fall back to basic present() if anything fails

    def hide(self):
        """Hide the GUI window."""
        if self.window:
            self.window.hide()

    def run(self):
        """Run the GUI application (start the main loop)."""
        if self.window:
            self.show()
            compat = self._gtk_version_compat()
            compat['main_loop']()

    def get_form_data(self) -> Dict[str, Any]:
        """Get all form data as a dictionary."""
        return self.widget_factory.get_all_values()

    def save_data_to_file(self, data_file_path: str, include_empty: bool = True) -> bool:
        """
        Save current form data to a JSON file.

        Args:
            data_file_path: Path where to save the JSON file
            include_empty: Whether to include fields with empty/None values

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data = self.get_form_data()
            success = FileUtils.save_data_to_json(data, data_file_path, include_empty)

            if not success:
                self._show_error("Save Error", f"Failed to save data to file: {data_file_path}")

            return success

        except Exception as e:
            self._show_error("Save Error", f"Failed to save data to file: {str(e)}")
            return False

    def load_data_from_file(self, data_file_path: str) -> bool:
        """
        Load form data from a JSON file and populate the GUI.

        Args:
            data_file_path: Path to the JSON file to load

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            data = FileUtils.load_data_from_json(data_file_path)

            if data is None:
                self._show_error("Load Error", f"Failed to load data from file: {data_file_path}")
                return False

            self.set_form_data(data)
            return True

        except Exception as e:
            self._show_error("Load Error", f"Failed to load data from file: {str(e)}")
            return False

    def load_data_from_dict(self, data: Dict[str, Any]) -> bool:
        """
        Load form data from a dictionary and populate the GUI.

        Args:
            data: Dictionary containing the form data

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.set_form_data(data)
            return True

        except Exception as e:
            self._show_error("Load Error", f"Failed to load data from dictionary: {str(e)}")
            return False

    def set_form_data(self, data: Dict[str, Any]):
        """Set form data from a dictionary."""
        self.widget_factory.set_all_values(data)

    def clear_form(self):
        """Clear all form fields."""
        self.widget_factory.clear_widgets()

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

    def set_custom_button_callback(self, action_id: str, callback: Callable[[CustomButtonConfig, Dict[str, Any]], None]):
        """Set a callback function for a custom button."""
        self.custom_button_callbacks[action_id] = callback

    def add_field_change_callback(self, field_name: str, callback: Callable[[str, Any], None]):
        """Add a callback function to be called when a field value changes."""
        if field_name not in self.field_change_callbacks:
            self.field_change_callbacks[field_name] = []
        self.field_change_callbacks[field_name].append(callback)

    def get_custom_button_names(self) -> List[str]:
        """Get list of custom button names."""
        if self.config and self.config.custom_buttons:
            return [button.name for button in self.config.custom_buttons]
        return []

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

    def close(self):
        """Close the GUI application."""
        if self.window:
            compat = self._gtk_version_compat()
            compat['main_quit']()
            self.window.destroy()
            self.window = None

    def __del__(self):
        """Cleanup when the object is destroyed."""
        if hasattr(self, 'window') and self.window:
            try:
                self.window.destroy()
            except Exception:
                pass  # Window might already be destroyed

    def _run_gtk4_loop(self):
        """Run GTK4 main loop using GLib.MainLoop."""
        if not hasattr(self, '_main_loop'):
            self._main_loop = GLib.MainLoop()
        self._main_loop.run()

    def _quit_gtk4_loop(self):
        """Quit GTK4 main loop."""
        if hasattr(self, '_main_loop') and self._main_loop.is_running():
            self._main_loop.quit()

    def _gtk_version_compat(self):
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

    def _detect_os_theme(self):
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

    def _apply_dark_theme(self):
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

    def _apply_dark_css_styling(self):
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

    def _apply_light_theme(self):
        """Apply light theme to GTK application."""
        try:
            if GTK_MAJOR_VERSION >= 3:
                settings = Gtk.Settings.get_default()
                if settings:
                    settings.set_property("gtk-application-prefer-dark-theme", False)
                    settings.set_property("gtk-theme-name", "Adwaita")

        except Exception as e:
            print(f"Warning: Could not apply light theme: {e}")
