"""
Main GUI builder class that creates GTK applications from JSON configuration.
"""

import json
from typing import Dict, Any, Callable, Optional, List

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    from gi.repository import Gtk, GLib, Gdk
    GTK_AVAILABLE = True
except (ImportError, ValueError) as e:
    print(f"GTK backend not available: {e}")
    GTK_AVAILABLE = False
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

        # Create window if it doesn't exist
        if self.window is None:
            self.window = Gtk.Window()

        # Set window properties
        if self.config.window.title:
            self.window.set_title(self.config.window.title)
        else:
            self.window.set_title("GUI Application")

        if self.config.window.width and self.config.window.height:
            self.window.set_default_size(self.config.window.width, self.config.window.height)
        else:
            self.window.set_default_size(600, 400)

        # Center window on screen
        self.window.set_position(Gtk.WindowPosition.CENTER)

        # Make window resizable
        self.window.set_resizable(True)
        
        # Ensure window can receive focus and comes to front
        self.window.set_can_focus(True)
        self.window.set_accept_focus(True)
        
        # Additional window properties to ensure it comes to front
        self.window.set_focus_on_map(True)
        self.window.set_type_hint(Gdk.WindowTypeHint.NORMAL)
        self.window.set_modal(False)  # Ensure it's not modal
        
        # Set window to always be visible when shown
        self.window.set_skip_taskbar_hint(False)
        self.window.set_skip_pager_hint(False)

        # Connect window close event
        self.window.connect("delete-event", self._on_window_close)

        # Create main scrolled window
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_border_width(10)

        # Create main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        scrolled_window.add(main_box)
        self.main_container = main_box

        # Build the interface
        if self.config.use_tabs and self.config.tabs:
            self._build_tabbed_interface()
        else:
            self._build_form_interface()

        # Add custom buttons
        self._add_custom_buttons()

        # Add default buttons (Submit/Cancel)
        self._add_default_buttons()

        # Set up field change monitoring
        self._setup_field_change_monitoring()

        # Add scrolled window to main window
        self.window.add(scrolled_window)

    def _build_form_interface(self):
        """Build a simple form interface."""
        if not self.config or not self.config.fields:
            return

        # Create form grid
        form_grid = Gtk.Grid()
        form_grid.set_column_spacing(10)
        form_grid.set_row_spacing(10)
        form_grid.set_border_width(10)

        self.main_container.pack_start(form_grid, True, True, 0)

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
        notebook.set_border_width(10)
        self.main_container.pack_start(notebook, True, True, 0)

        for tab_config in self.config.tabs:
            # Create tab content
            tab_scrolled = Gtk.ScrolledWindow()
            tab_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

            tab_grid = Gtk.Grid()
            tab_grid.set_column_spacing(10)
            tab_grid.set_row_spacing(10)
            tab_grid.set_border_width(10)

            tab_scrolled.add(tab_grid)

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
        grid.attach(label, 0, row, 1, 1)

        # Create widget
        widget = self.widget_factory.create_widget(grid, field_config)
        if widget:
            grid.attach(widget, 1, row, 1, 1)
            widget.set_hexpand(True)

            # Add tooltip if specified
            if field_config.tooltip:
                widget.set_tooltip_text(field_config.tooltip)

    def _add_custom_buttons(self):
        """Add custom buttons defined in the configuration."""
        if not self.config or not self.config.custom_buttons:
            return

        # Create frame for custom buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        button_box.set_border_width(10)

        for button_config in self.config.custom_buttons:
            button = Gtk.Button(label=button_config.label)
            button.connect("clicked", lambda btn, cfg=button_config: self._handle_custom_button_click(cfg))

            if hasattr(button_config, 'tooltip') and button_config.tooltip:
                button.set_tooltip_text(button_config.tooltip)

            button_box.pack_start(button, False, False, 0)

        self.main_container.pack_start(button_box, False, False, 0)

    def _add_default_buttons(self):
        """Add default Submit and Cancel buttons."""
        if not self.config:
            return

        # Create frame for default buttons
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        button_box.set_border_width(10)
        button_box.set_halign(Gtk.Align.END)

        # Submit button
        if self.config.submit_button:
            submit_text = self.config.submit_label or "Submit"
            submit_button = Gtk.Button(label=submit_text)
            submit_button.connect("clicked", lambda btn: self._handle_submit())
            submit_button.get_style_context().add_class("suggested-action")
            button_box.pack_start(submit_button, False, False, 0)

        # Cancel button
        if self.config.cancel_button:
            cancel_text = self.config.cancel_label or "Cancel"
            cancel_button = Gtk.Button(label=cancel_text)
            cancel_button.connect("clicked", lambda btn: self._handle_cancel())
            button_box.pack_start(cancel_button, False, False, 0)

        self.main_container.pack_start(button_box, False, False, 0)

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
                Gtk.main_quit()

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

        missing_fields = []
        all_fields = []

        # Collect all fields from tabs or main form
        if self.config.use_tabs and self.config.tabs:
            for tab in self.config.tabs:
                all_fields.extend(tab.fields)
        else:
            all_fields = self.config.fields or []

        # Check required fields
        for field_config in all_fields:
            if field_config.required:
                value = self.widget_factory.get_widget_value(field_config.name)
                if value is None or (isinstance(value, str) and not value.strip()):
                    missing_fields.append(field_config.label or field_config.name)

        if missing_fields:
            self._show_error(
                "Required Fields Missing",
                f"Please fill in the following required fields:\n\n" + "\n".join(f"• {field}" for field in missing_fields)
            )
            return False

        return True

    def _show_form_data(self, data: Dict[str, Any]):
        """Show form data in a dialog (default submit behavior)."""
        # Create a dialog to display the data
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

        scrolled.add(text_view)
        dialog.get_content_area().add(scrolled)

        dialog.show_all()
        dialog.run()
        dialog.destroy()

    def _show_error(self, title: str, message: str):
        """Show an error dialog."""
        dialog = Gtk.MessageDialog(
            parent=self.window,
            flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
            type=Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            message_format=message
        )
        dialog.set_title(title)
        dialog.run()
        dialog.destroy()

    def _show_info(self, title: str, message: str):
        """Show an info dialog."""
        dialog = Gtk.MessageDialog(
            parent=self.window,
            flags=Gtk.DialogFlags.MODAL | Gtk.DialogFlags.DESTROY_WITH_PARENT,
            type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            message_format=message
        )
        dialog.set_title(title)
        dialog.run()
        dialog.destroy()

    def _on_window_close(self, widget, event):
        """Handle window close event."""
        Gtk.main_quit()
        return False

    def show(self):
        """Show the GUI window and bring it to the front (cross-platform)."""
        if self.window:
            import platform
            system = platform.system()
            
            # Make sure window is visible
            self.window.show_all()
            
            # Cross-platform window activation
            self.window.present()
            
            # Platform-specific window focusing
            if system == 'Darwin':  # macOS
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
                    
            elif system == 'Windows':  # Windows
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
                    
            else:  # Linux and other Unix systems
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
            Gtk.main()

    def get_form_data(self) -> Dict[str, Any]:
        """Get all form data as a dictionary."""
        return self.widget_factory.get_all_values()

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

    def close(self):
        """Close the GUI application."""
        if self.window:
            Gtk.main_quit()
            self.window.destroy()
            self.window = None

    def __del__(self):
        """Cleanup when the object is destroyed."""
        if hasattr(self, 'window') and self.window:
            try:
                self.window.destroy()
            except Exception:
                pass  # Window might already be destroyed
