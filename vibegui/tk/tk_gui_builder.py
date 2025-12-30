"""
Main GUI builder class that creates tkinter applications from JSON configuration.
"""
from __future__ import annotations

import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Dict, Any, Optional

from vibegui.config_loader import ConfigLoader, GuiConfig, FieldConfig, CustomButtonConfig
from vibegui.utils import CallbackManagerMixin, ValidationMixin, DataPersistenceMixin, WidgetFactoryMixin, FieldStateMixin, ButtonHandlerMixin, ConfigLoaderMixin, PlatformUtils
from vibegui.tk.tk_widget_factory import TkWidgetFactory


class TkGuiBuilder(ButtonHandlerMixin, ConfigLoaderMixin, CallbackManagerMixin, ValidationMixin, DataPersistenceMixin, WidgetFactoryMixin, FieldStateMixin):
    """Main GUI builder class that creates tkinter applications from JSON configuration."""

    def __init__(self, config_path: Optional[str] = None, config_dict: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the GUI builder.

        Args:
            config_path: Path to JSON configuration file
            config_dict: Configuration dictionary (alternative to config_path)
        """
        super().__init__()

        self.config_loader = ConfigLoader()
        self.widget_factory = TkWidgetFactory()
        self.config: Optional[GuiConfig] = None
        self.root: Optional[tk.Tk] = None
        self.main_frame: Optional[tk.Frame] = None

        # Load configuration
        if config_path:
            self.load_config_from_file(config_path)
        elif config_dict:
            self.load_config_from_dict(config_dict)

    # load_config_from_file and load_config_from_dict provided by ConfigLoaderMixin
    # Note: Tk defers UI setup until show() is called, so no _build_gui() call needed

    def _should_build_ui_on_config_load(self) -> bool:
        """Override to defer UI building until show() is called."""
        return False

    def _setup_ui(self) -> None:
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

        # For tabbed interfaces, use a simpler layout without scrolling
        if self.config.use_tabs and self.config.tabs:
            # Create main frame directly without canvas scrolling
            main_frame = ttk.Frame(self.root)
            main_frame.pack(fill="both", expand=True)
            main_frame.columnconfigure(0, weight=1)
            main_frame.rowconfigure(0, weight=1)

            self.main_frame = main_frame

            # Build the tabbed interface
            self._build_tabbed_interface()

            # Add buttons in a separate frame at the bottom
            self._add_buttons()

            # Set up field change monitoring
            self._setup_field_change_monitoring()
        else:
            # For non-tabbed forms, use the scrollable canvas
            canvas = tk.Canvas(self.root)
            scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)

            def on_frame_configure(event: tk.Event) -> None:
                canvas.configure(scrollregion=canvas.bbox("all"))

            def on_canvas_configure(event: tk.Event) -> None:
                # Update the window width to match canvas width
                canvas.itemconfig(canvas_window, width=event.width)

            scrollable_frame.bind("<Configure>", on_frame_configure)

            canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.bind("<Configure>", on_canvas_configure)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            self.main_frame = scrollable_frame

            # Build the form interface
            self._build_form_interface()

            # Add custom buttons
            self._add_buttons()

            # Set up field change monitoring
            self._setup_field_change_monitoring()

            # Bind mouse wheel to canvas for scrolling
            def _on_mousewheel(event: tk.Event) -> None:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")

            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Apply theme
        self._detect_and_apply_theme()

    def _add_buttons(self) -> None:
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

    def _build_form_interface(self) -> None:
        """Build a simple form interface."""
        if not self.config or not self.config.fields:
            return

        # Create form frame
        form_frame = ttk.Frame(self.main_frame)
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add fields based on layout type
        self._add_fields_to_container(form_frame, self.config.fields, self.config.layout)

    def _build_tabbed_interface(self) -> None:
        """Build a tabbed interface."""
        if not self.config or not self.config.tabs:
            return

        # Create notebook widget for tabs - it will expand to fill the main_frame
        notebook = ttk.Notebook(self.main_frame)
        notebook.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        for tab_config in self.config.tabs:
            # Create tab frame
            tab_frame = ttk.Frame(notebook)
            notebook.add(tab_frame, text=tab_config.title)

            # Create scrollable content for the tab
            tab_canvas = tk.Canvas(tab_frame)
            tab_scrollbar = ttk.Scrollbar(tab_frame, orient="vertical", command=tab_canvas.yview)
            tab_content = ttk.Frame(tab_canvas)

            def on_tab_content_configure(event: tk.Event, canvas: tk.Canvas = tab_canvas) -> None:
                canvas.configure(scrollregion=canvas.bbox("all"))

            def on_tab_canvas_configure(event: tk.Event, canvas: tk.Canvas = tab_canvas, window_id = None) -> None:
                # Update the window width to match canvas width
                if window_id:
                    canvas.itemconfig(window_id, width=event.width)

            tab_content.bind("<Configure>", on_tab_content_configure)

            tab_window = tab_canvas.create_window((0, 0), window=tab_content, anchor="nw")
            tab_canvas.configure(yscrollcommand=tab_scrollbar.set)

            # Bind canvas resize to update window width
            tab_canvas.bind("<Configure>", lambda e, c=tab_canvas, w=tab_window: on_tab_canvas_configure(e, c, w))

            tab_canvas.pack(side="left", fill="both", expand=True)
            tab_scrollbar.pack(side="right", fill="y")

            # Add fields to the tab based on layout type
            self._add_fields_to_container(tab_content, tab_config.fields, tab_config.layout)

    def _add_fields_to_container(self, parent: tk.Widget, fields: list, layout_type: str = None) -> None:
        """Add fields to a container based on layout type."""
        if layout_type is None:
            layout_type = "form"  # Default to form layout

        if layout_type in ["form", "grid"]:
            # Form/grid layout: use grid manager with label-widget pairs
            parent.columnconfigure(1, weight=1)
            for i, field_config in enumerate(fields):
                if field_config.type == "checkbox":
                    # Checkbox includes its own label
                    widget = self.widget_factory.create_widget(parent, field_config)
                    if widget:
                        widget.grid(row=i, column=0, columnspan=2, sticky="w", pady=5)
                        if field_config.tooltip:
                            self._add_tooltip(widget, field_config.tooltip)
                else:
                    # Regular field with separate label
                    label = self.widget_factory.create_label(parent, field_config)
                    label.grid(row=i, column=0, sticky="nw", padx=(0, 10), pady=5)

                    widget = self.widget_factory.create_widget(parent, field_config)
                    if widget:
                        widget.grid(row=i, column=1, sticky="ew", pady=5)
                        if field_config.tooltip:
                            self._add_tooltip(widget, field_config.tooltip)

        elif layout_type == "horizontal":
            # Horizontal layout: use pack manager with side="left"
            for i, field_config in enumerate(fields):
                # Create a container for each field
                field_frame = ttk.Frame(parent)
                field_frame.pack(side="left", fill="both", expand=True, padx=5)

                if field_config.type != "checkbox":
                    label = self.widget_factory.create_label(field_frame, field_config)
                    label.pack(side="top", anchor="w")

                widget = self.widget_factory.create_widget(field_frame, field_config)
                if widget:
                    widget.pack(side="top", fill="x")
                    if field_config.tooltip:
                        self._add_tooltip(widget, field_config.tooltip)

        else:  # vertical or default
            # Vertical layout: use pack manager with side="top"
            for i, field_config in enumerate(fields):
                if field_config.type != "checkbox":
                    label = self.widget_factory.create_label(parent, field_config)
                    label.pack(side="top", anchor="w", pady=(0, 2))

                widget = self.widget_factory.create_widget(parent, field_config)
                if widget:
                    widget.pack(side="top", fill="x", pady=(0, 10))
                    if field_config.tooltip:
                        self._add_tooltip(widget, field_config.tooltip)

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
            self._show_error(f"Error submitting form: {str(e)}")

    def _on_form_submitted(self, form_data: Dict[str, Any]) -> None:
        """Tk-specific post-submit action - show form data if no callback."""
        if not self.submit_callback:
            self._show_form_data(form_data)

    def _handle_cancel(self) -> None:
        """Handle cancel button click."""
        try:
            self._handle_cancel_click()
        except Exception as e:
            self._show_error(f"Error in cancel callback: {str(e)}")

    def _on_form_cancelled(self) -> None:
        """Tk-specific post-cancel action - quit if no callback."""
        if not self.cancel_callback and self.root:
            self.root.quit()

    def _handle_custom_button_click(self, button_config: CustomButtonConfig) -> None:
        """Handle custom button click."""
        try:
            # Note: Tk custom button callbacks take (button_config, form_data)
            # The mixin uses just button name, so we call callback directly here
            if button_config.name in self.custom_button_callbacks:
                callback = self.custom_button_callbacks[button_config.name]
                callback(button_config, self.get_form_data())
            else:
                # Default behavior
                messagebox.showinfo("Button Clicked", f"Custom button '{button_config.label}' clicked")
        except Exception as e:
            self._show_error(f"Error in custom button callback: {str(e)}")

    def _show_error(self, title: str, message: str = None) -> None:
        """Show an error message dialog.

        Args:
            title: Error title or message if message param is None
            message: Error message (optional for backward compatibility)
        """
        if message is None:
            # Single parameter call - title is actually the message
            messagebox.showerror("Error", title)
        else:
            # Two parameter call
            messagebox.showerror(title, message)

    def _show_form_data(self, data: Dict[str, Any]) -> None:
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

    def _add_tooltip(self, widget: tk.Widget, tooltip_text: str) -> None:
        """Add a tooltip to a widget."""
        def show_tooltip(event: tk.Event) -> None:
            tooltip_window = tk.Toplevel()
            tooltip_window.wm_overrideredirect(True)
            tooltip_window.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")

            label = tk.Label(
                tooltip_window,
                text=tooltip_text,
                background="lightyellow",
                foreground="black",
                relief="solid",
                borderwidth=1,
                padx=5,
                pady=3,
                wraplength=200
            )
            label.pack()

            # Store reference to prevent garbage collection
            widget._tooltip_window = tooltip_window

            def hide_tooltip() -> None:
                if hasattr(widget, '_tooltip_window'):
                    widget._tooltip_window.destroy()
                    delattr(widget, '_tooltip_window')

            # Hide tooltip after delay or on leave
            tooltip_window.after(3000, hide_tooltip)
            widget.bind('<Leave>', lambda e: hide_tooltip(), '+')

        widget.bind('<Enter>', show_tooltip)

    def _apply_dark_theme(self) -> None:
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

    def _apply_light_theme(self) -> None:
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

    def _detect_and_apply_theme(self) -> None:
        """Detect system theme and apply appropriate colors."""
        try:
            # Skip theme detection in test/headless environments
            if not self.root or not self.root.winfo_ismapped():
                # Window not yet mapped, skip theme detection
                return

            if PlatformUtils.is_dark_mode():
                self._apply_dark_theme()
            else:
                self._apply_light_theme()
        except Exception as e:
            # Silently fall back to light theme if detection fails
            try:
                self._apply_light_theme()
            except Exception:
                pass  # Even fallback failed, just use defaults

    def run(self) -> None:
        """Run the GUI application (start the main loop)."""
        # Ensure UI is set up before running
        if self.root is None:
            self._setup_ui()

        if self.root:
            # Ensure window is properly shown and focused before starting main loop
            self.show()
            self.root.mainloop()

    def show(self) -> None:
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

    def hide(self) -> None:
        """Hide the GUI window."""
        if self.root:
            self.root.withdraw()

    # get_form_data, set_form_data, clear_form, get_field_value, set_field_value
    # are provided by WidgetFactoryMixin
    # enable_field and show_field are provided by FieldStateMixin

    def _enable_widget(self, widget: tk.Widget, enabled: bool) -> None:
        """Tk-specific widget enable/disable."""
        state = tk.NORMAL if enabled else tk.DISABLED
        try:
            widget.config(state=state)
        except tk.TclError:
            # Some widgets don't support state configuration
            pass

    def _show_widget(self, widget: tk.Widget, visible: bool) -> None:
        """Tk-specific widget show/hide."""
        if visible:
            widget.grid()
        else:
            widget.grid_remove()

    @classmethod
    def create_and_run(cls, config_path: str | None = None, config_dict: Dict[str, Any] | None = None) -> 'TkGuiBuilder':
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

    def close(self) -> None:
        """Close the GUI application."""
        if self.root:
            self.root.quit()
            self.root.destroy()
            self.root = None

    def __del__(self) -> None:
        """Cleanup when the object is destroyed."""
        if self.root:
            try:
                self.root.destroy()
            except (tk.TclError, AttributeError):
                pass  # Window might already be destroyed or Tk might be gone


