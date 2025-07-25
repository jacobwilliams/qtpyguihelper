"""
Main GUI builder class that creates tkinter applications from JSON configuration.
"""

import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, Any, Callable, Optional, List

from qtpyguihelper.config_loader import ConfigLoader, GuiConfig, FieldConfig, CustomButtonConfig
from qtpyguihelper.utils import FileUtils, ValidationUtils, PlatformUtils
from qtpyguihelper.tk.tk_widget_factory import TkWidgetFactory


class TkGuiBuilder:
    """Main GUI builder class that creates tkinter applications from JSON configuration."""

    def __init__(self, config_path: Optional[str] = None, config_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize the GUI builder.

        Args:
            config_path: Path to JSON configuration file
            config_dict: Configuration dictionary (alternative to config_path)
        """
        self.config_loader = ConfigLoader()
        self.widget_factory = TkWidgetFactory()
        self.config: Optional[GuiConfig] = None
        self.root: Optional[tk.Tk] = None
        self.main_frame: Optional[tk.Frame] = None
        self.submit_callback: Optional[Callable] = None
        self.cancel_callback: Optional[Callable] = None
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
        # Note: UI setup is deferred until needed

    def load_config_from_dict(self, config_dict: Dict[str, Any]):
        """Load configuration from a dictionary."""
        self.config = self.config_loader.load_from_dict(config_dict)
        # Note: UI setup is deferred until needed

    def _setup_ui(self):
        """Set up the user interface based on the loaded configuration."""
        if not self.config:
            return

        # Create root window if it doesn't exist
        if self.root is None:
            self.root = tk.Tk()

        # Detect and apply theme before setting up UI
        self._detect_and_apply_theme()

        # Pass theme colors to widget factory after theme detection
        if hasattr(self, '_theme_colors') and self._theme_colors:
            self.widget_factory.set_theme_colors(self._theme_colors)

        # Set window properties
        if self.config.window.title:
            self.root.title(self.config.window.title)
        else:
            self.root.title("GUI Application")

        if self.config.window.width and self.config.window.height:
            self.root.geometry(f"{self.config.window.width}x{self.config.window.height}")
        else:
            self.root.geometry("600x400")

        # Center the window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Configure window to be resizable
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Create main container with scrolling capability
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.main_frame = scrollable_frame

        # Build the interface
        if self.config.use_tabs and self.config.tabs:
            self._build_tabbed_interface()
        else:
            self._build_form_interface()

        # Add custom buttons
        self._add_buttons()

        # Set up field change monitoring
        self._setup_field_change_monitoring()

        # Bind mouse wheel to canvas for scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Apply theme
        self._detect_and_apply_theme()

    def _add_buttons(self):
        """Add all buttons (custom and default) in a single frame for proper alignment."""
        if not self.config:
            return

        # Only create button frame if we have buttons to add
        has_custom_buttons = self.config.custom_buttons and len(self.config.custom_buttons) > 0
        has_default_buttons = self.config.submit_button or self.config.cancel_button

        if not (has_custom_buttons or has_default_buttons):
            return

        # Create single frame for all buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill="x", padx=10, pady=10)

        # Add custom buttons on the left
        if has_custom_buttons:
            for button_config in self.config.custom_buttons:
                button = tk.Button(
                    button_frame,
                    text=button_config.label,
                    command=lambda btn=button_config: self._handle_custom_button_click(btn)
                )

                # Apply button styling if specified
                if hasattr(button_config, 'style') and button_config.style:
                    style = button_config.style
                    if 'background' in style:
                        button.config(bg=style['background'])
                    if 'foreground' in style:
                        button.config(fg=style['foreground'])

                button.pack(side="left", padx=(0, 5))

        # Add default buttons on the right (order matters for pack side="right")
        if has_default_buttons:
            # Submit button (packed first to appear on the far right)
            if self.config.submit_button:
                submit_text = self.config.submit_label or "Submit"
                submit_button = tk.Button(
                    button_frame,
                    text=submit_text,
                    command=self._handle_submit
                )
                submit_button.pack(side="right")

            # Cancel button (packed second to appear to the left of Submit)
            if self.config.cancel_button:
                cancel_text = self.config.cancel_label or "Cancel"
                cancel_button = tk.Button(
                    button_frame,
                    text=cancel_text,
                    command=self._handle_cancel
                )
                cancel_button.pack(side="right", padx=(5, 0))

    def _build_form_interface(self):
        """Build a simple form interface."""
        if not self.config or not self.config.fields:
            return

        # Create form frame
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Configure column weights for proper resizing
        form_frame.columnconfigure(1, weight=1)

        row = 0
        for field_config in self.config.fields:
            self._add_field_to_form(form_frame, field_config, row)
            row += 1

    def _build_tabbed_interface(self):
        """Build a tabbed interface."""
        if not self.config or not self.config.tabs:
            return

        # Create notebook widget for tabs
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        for tab_config in self.config.tabs:
            # Create tab frame
            tab_frame = ttk.Frame(notebook)
            notebook.add(tab_frame, text=tab_config.title)

            # Create scrollable content for the tab
            tab_canvas = tk.Canvas(tab_frame)
            tab_scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=tab_canvas.yview)
            tab_content = ttk.Frame(tab_canvas)

            def on_tab_configure(event, canvas=tab_canvas):
                del event  # Unused but required by bind
                canvas.configure(scrollregion=canvas.bbox("all"))

            tab_content.bind("<Configure>", on_tab_configure)

            tab_canvas.create_window((0, 0), window=tab_content, anchor="nw")
            tab_canvas.configure(yscrollcommand=tab_scrollbar.set)

            tab_canvas.pack(side="left", fill="both", expand=True)
            tab_scrollbar.pack(side="right", fill="y")

            # Configure column weights
            tab_content.columnconfigure(1, weight=1)

            # Add fields to the tab
            row = 0
            for field_config in tab_config.fields:
                self._add_field_to_form(tab_content, field_config, row)
                row += 1

    def _add_field_to_form(self, parent: tk.Widget, field_config: FieldConfig, row: int):
        """Add a field to the form."""
        # Create label
        label = self.widget_factory.create_label(parent, field_config)
        label.grid(row=row, column=0, sticky="nw", padx=(0, 10), pady=5)

        # Create widget
        widget = self.widget_factory.create_widget(parent, field_config)
        if widget:
            widget.grid(row=row, column=1, sticky="ew", pady=5)

            # Add tooltip if specified
            if field_config.tooltip:
                self._add_tooltip(widget, field_config.tooltip)

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
                    messagebox.showerror("Error", f"Error in submit callback: {str(e)}")
            else:
                # Default behavior - show the data
                self._show_form_data(form_data)

        except Exception as e:
            messagebox.showerror("Error", f"Error submitting form: {str(e)}")

    def _handle_cancel(self):
        """Handle cancel button click."""
        if self.cancel_callback:
            try:
                self.cancel_callback()
            except Exception as e:
                messagebox.showerror("Error", f"Error in cancel callback: {str(e)}")
        else:
            # Default behavior - close the window
            if self.root:
                self.root.quit()

    def _handle_custom_button_click(self, button_config: CustomButtonConfig):
        """Handle custom button click."""
        if button_config.name in self.custom_button_callbacks:
            try:
                callback = self.custom_button_callbacks[button_config.name]
                callback(button_config, self.get_form_data())
            except Exception as e:
                messagebox.showerror("Error", f"Error in custom button callback: {str(e)}")
        else:
            # Default behavior
            messagebox.showinfo("Button Clicked", f"Custom button '{button_config.label}' clicked")

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

        # Get required field names
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

            messagebox.showerror(
                "Required Fields Missing",
                f"Please fill in the following required fields:\n\n" + "\n".join(f"• {label}" for label in missing_labels)
            )
            return False

        return True

    def _show_form_data(self, data: Dict[str, Any]):
        """Show form data in a dialog (default submit behavior)."""
        # Create a new window to display the data
        data_window = tk.Toplevel(self.root)
        data_window.title("Form Data")
        data_window.geometry("500x400")

        # Create text widget with scrollbar
        text_frame = tk.Frame(data_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        text_widget = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD)
        text_widget.pack(fill="both", expand=True)

        # Format and display the data
        formatted_data = json.dumps(data, indent=2, default=str)
        text_widget.insert("1.0", formatted_data)
        text_widget.config(state="disabled")

        # Add close button
        close_button = tk.Button(data_window, text="Close", command=data_window.destroy)
        close_button.pack(pady=(0, 10))

    def _add_tooltip(self, widget: tk.Widget, text: str):
        """Add a tooltip to a widget."""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

            label = tk.Label(
                tooltip,
                text=text,
                background="lightyellow",
                relief="solid",
                borderwidth=1,
                wraplength=200
            )
            label.pack()

            # Store reference to prevent garbage collection
            widget._tooltip = tooltip

            def hide_tooltip():
                if hasattr(widget, '_tooltip'):
                    widget._tooltip.destroy()
                    del widget._tooltip

            # Hide tooltip after delay or on leave
            tooltip.after(3000, hide_tooltip)
            widget.bind('<Leave>', lambda e: hide_tooltip(), '+')

        widget.bind('<Enter>', show_tooltip)

    def _apply_dark_theme(self):
        """Apply dark theme colors to tkinter widgets."""
        try:
            # Dark theme colors
            bg_color = '#2d2d2d'
            fg_color = '#ffffff'
            entry_bg = '#404040'
            entry_fg = '#ffffff'
            button_bg = '#404040'
            button_fg = '#ffffff'

            # Configure root window
            if self.root:
                self.root.configure(bg=bg_color)

            # Configure ttk styles for dark theme
            style = ttk.Style()

            # Configure various ttk widget styles
            style.configure('TFrame', background=bg_color)
            style.configure('TLabel', background=bg_color, foreground=fg_color)
            style.configure('TButton', background=button_bg, foreground=button_fg)
            style.configure('TNotebook', background=bg_color)
            style.configure('TNotebook.Tab', background=button_bg, foreground=button_fg)

            # Configure Entry widgets (these need special handling)
            style.configure('TEntry',
                          fieldbackground=entry_bg,
                          foreground=entry_fg,
                          bordercolor='#555555',
                          lightcolor='#555555',
                          darkcolor='#555555')

            # Configure Combobox
            style.configure('TCombobox',
                          fieldbackground=entry_bg,
                          foreground=entry_fg,
                          background=button_bg,
                          bordercolor='#555555')

            # Configure Scrollbar
            style.configure('TScrollbar',
                          background=button_bg,
                          bordercolor='#555555',
                          arrowcolor=fg_color,
                          troughcolor=bg_color)

            # Store theme colors for widget creation
            self._theme_colors = {
                'bg': bg_color,
                'fg': fg_color,
                'entry_bg': entry_bg,
                'entry_fg': entry_fg,
                'button_bg': button_bg,
                'button_fg': button_fg
            }

        except Exception as e:
            print(f"Warning: Could not apply dark theme to tkinter: {e}")
            self._theme_colors = None

    def _apply_light_theme(self):
        """Apply light theme colors to tkinter widgets."""
        try:
            # Light theme colors (tkinter defaults)
            bg_color = '#f0f0f0'
            fg_color = '#000000'
            entry_bg = '#ffffff'
            entry_fg = '#000000'
            button_bg = '#e1e1e1'
            button_fg = '#000000'

            # Configure root window
            if self.root:
                self.root.configure(bg=bg_color)

            # Configure ttk styles for light theme
            style = ttk.Style()

            style.configure('TFrame', background=bg_color)
            style.configure('TLabel', background=bg_color, foreground=fg_color)
            style.configure('TButton', background=button_bg, foreground=button_fg)
            style.configure('TNotebook', background=bg_color)
            style.configure('TNotebook.Tab', background=button_bg, foreground=button_fg)

            style.configure('TEntry',
                          fieldbackground=entry_bg,
                          foreground=entry_fg,
                          bordercolor='#d4d4d4',
                          lightcolor='#d4d4d4',
                          darkcolor='#d4d4d4')

            style.configure('TCombobox',
                          fieldbackground=entry_bg,
                          foreground=entry_fg,
                          background=button_bg,
                          bordercolor='#d4d4d4')

            style.configure('TScrollbar',
                          background=button_bg,
                          bordercolor='#d4d4d4',
                          arrowcolor=fg_color,
                          troughcolor=bg_color)

            # Store theme colors for widget creation
            self._theme_colors = {
                'bg': bg_color,
                'fg': fg_color,
                'entry_bg': entry_bg,
                'entry_fg': entry_fg,
                'button_bg': button_bg,
                'button_fg': button_fg
            }

        except Exception as e:
            print(f"Warning: Could not apply light theme to tkinter: {e}")
            self._theme_colors = None

    def _detect_and_apply_theme(self):
        """Detect system theme and apply appropriate colors."""
        try:
            if PlatformUtils.is_dark_mode():
                self._apply_dark_theme()
            else:
                self._apply_light_theme()
        except Exception as e:
            print(f"Warning: Could not detect system theme: {e}")
            self._apply_light_theme()  # Fallback to light theme

    def run(self):
        """Run the GUI application (start the main loop)."""
        # Ensure UI is set up before running
        if self.root is None:
            self._setup_ui()

        if self.root:
            # Ensure window is properly shown and focused before starting main loop
            self.show()
            self.root.mainloop()

    def show(self):
        """Show the GUI window and bring it to the front."""
        # Ensure UI is set up before showing
        if self.root is None:
            self._setup_ui()

        if self.root:
            self.root.deiconify()
            self.root.lift()
            self.root.attributes('-topmost', True)  # Bring to front
            self.root.attributes('-topmost', False)  # Remove always-on-top
            self.root.focus_force()  # Force focus

    def hide(self):
        """Hide the GUI window."""
        if self.root:
            self.root.withdraw()

    def get_form_data(self) -> Dict[str, Any]:
        """Get all form data as a dictionary."""
        # Ensure UI is set up before trying to get data
        if self.root is None and self.config:
            self._setup_ui()
        return self.widget_factory.get_all_values()

    def set_form_data(self, data: Dict[str, Any]):
        """Set form data from a dictionary."""
        self.widget_factory.set_all_values(data)

    def clear_form(self):
        """Clear all form fields."""
        self.widget_factory.clear_widgets()

    def get_field_value(self, field_name: str) -> Any:
        """Get the value of a specific field."""
        # Ensure UI is set up before trying to get field value
        if self.root is None:
            self._setup_ui()
        return self.widget_factory.get_widget_value(field_name)

    def set_field_value(self, field_name: str, value: Any) -> bool:
        """Set the value of a specific field."""
        # Ensure UI is set up before trying to set field value
        if self.root is None:
            self._setup_ui()
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
                messagebox.showerror("Save Error", f"Failed to save data to file: {data_file_path}")

            return success

        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save data to file: {str(e)}")
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
                messagebox.showerror("Load Error", f"Failed to load data from file: {data_file_path}")
                return False

            self.set_form_data(data)
            return True

        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load data from file: {str(e)}")
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
            messagebox.showerror("Load Error", f"Failed to load data from dictionary: {str(e)}")
            return False

    @classmethod
    def create_and_run(cls, config_path: str = None, config_dict: Dict[str, Any] = None) -> 'TkGuiBuilder':
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
        if self.root:
            self.root.quit()
            self.root.destroy()
            self.root = None

    def __del__(self):
        """Cleanup when the object is destroyed."""
        if self.root:
            try:
                self.root.destroy()
            except (tk.TclError, AttributeError):
                pass  # Window might already be destroyed or Tk might be gone


