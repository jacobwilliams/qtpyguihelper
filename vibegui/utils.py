"""
Common utilities used across different GUI backends.
"""

import json
import platform
from typing import Dict, Any, Optional, Union, List, Callable


def set_nested_value(data: Dict[str, Any], key_path: str, value: Any) -> None:
    """
    Set a value in a nested dictionary using dot notation.

    Args:
        data: The dictionary to modify
        key_path: Dot-separated key path (e.g., "project.name")
        value: The value to set
    """
    keys = key_path.split('.')
    current = data

    # Navigate to the parent of the target key
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        elif not isinstance(current[key], dict):
            # If the intermediate key exists but isn't a dict, we can't proceed
            return
        current = current[key]

    # Set the final value
    current[keys[-1]] = value


def get_nested_value(data: Dict[str, Any], key_path: str, default: Any = None) -> Any:
    """
    Get a value from a nested dictionary using dot notation.

    Args:
        data: The dictionary to search
        key_path: Dot-separated key path (e.g., "project.name")
        default: Default value if key not found

    Returns:
        The value at the key path, or default if not found
    """
    keys = key_path.split('.')
    current = data

    try:
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current
    except (KeyError, TypeError):
        return default


def flatten_nested_dict(data: Dict[str, Any], parent_key: str = '', separator: str = '.') -> Dict[str, Any]:
    """
    Flatten a nested dictionary into a flat dictionary with dot notation keys.

    Args:
        data: The nested dictionary to flatten
        parent_key: The parent key path (for recursion)
        separator: The separator to use (default: '.')

    Returns:
        Flattened dictionary with dot notation keys
    """
    items = []
    for key, value in data.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_nested_dict(value, new_key, separator).items())
        else:
            items.append((new_key, value))
    return dict(items)


class WidgetFactoryMixin:
    """Mixin providing common widget factory delegation methods.

    Assumes the class has a self.widget_factory attribute.
    Provides standardized methods for form data manipulation and field access.
    """

    def get_form_data(self) -> Dict[str, Any]:
        """Get all form data as a dictionary."""
        return self.widget_factory.get_all_values()

    def set_form_data(self, data: Dict[str, Any]) -> None:
        """Set form data from a dictionary."""
        self.widget_factory.set_all_values(data)

    def clear_form(self) -> None:
        """Clear all form fields."""
        # Handle different method names across widget factories
        if hasattr(self.widget_factory, 'clear_all_widgets'):
            self.widget_factory.clear_all_widgets()
        elif hasattr(self.widget_factory, 'clear_widgets'):
            self.widget_factory.clear_widgets()

    def get_field_value(self, field_name: str) -> Any:
        """Get the value of a specific field."""
        # Handle different method names
        if hasattr(self.widget_factory, 'get_widget_value'):
            return self.widget_factory.get_widget_value(field_name)
        elif hasattr(self.widget_factory, 'get_value'):
            return self.widget_factory.get_value(field_name)
        return None

    def set_field_value(self, field_name: str, value: Any) -> bool:
        """Set the value of a specific field."""
        try:
            # Handle different method names
            if hasattr(self.widget_factory, 'set_widget_value'):
                return self.widget_factory.set_widget_value(field_name, value)
            elif hasattr(self.widget_factory, 'set_value'):
                self.widget_factory.set_value(field_name, value)
                return True
            return False
        except Exception:
            return False


class CallbackManagerMixin:
    """Mixin providing common callback management functionality for GUI builders.

    Provides standardized callback storage and setter methods for:
    - submit_callback: Called when form is submitted
    - cancel_callback: Called when form is cancelled
    - custom_button_callbacks: Dictionary of callbacks for custom buttons
    - field_change_callbacks: Dictionary of callbacks for field changes
    """

    def __init__(self, *args, **kwargs) -> None:
        """Initialize callback storage."""
        # Pass all args/kwargs to super() to properly initialize base classes (especially wx.Frame)
        super().__init__(*args, **kwargs)
        self.submit_callback: Optional[Callable] = None
        self.cancel_callback: Optional[Callable] = None
        self.custom_button_callbacks: Dict[str, Callable] = {}
        self.field_change_callbacks: Dict[str, List[Callable]] = {}

    def set_submit_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Set a callback function to be called when the form is submitted.

        Args:
            callback: Function that takes form data dict as argument
        """
        self.submit_callback = callback

    def set_cancel_callback(self, callback: Callable[[], None]) -> None:
        """Set a callback function to be called when the form is cancelled.

        Args:
            callback: Function with no arguments
        """
        self.cancel_callback = callback

    def set_custom_button_callback(self, button_id: str, callback: Callable) -> None:
        """Set a callback function for a custom button.

        Args:
            button_id: ID/name of the custom button
            callback: Callback function (signature may vary by backend)
        """
        self.custom_button_callbacks[button_id] = callback

    def remove_custom_button_callback(self, button_id: str) -> None:
        """Remove a custom button callback.

        Args:
            button_id: ID/name of the custom button
        """
        if button_id in self.custom_button_callbacks:
            del self.custom_button_callbacks[button_id]

    def get_custom_button_names(self) -> List[str]:
        """Get list of custom button IDs/names.

        Returns:
            List of button IDs that have been configured
        """
        if hasattr(self, 'config') and self.config and hasattr(self.config, 'custom_buttons') and self.config.custom_buttons:
            return [button.name if hasattr(button, 'name') else button.id for button in self.config.custom_buttons]
        return []

    def add_field_change_callback(self, field_name: str, callback: Callable[[str, Any], None]) -> None:
        """Add a callback function to be called when a field value changes.

        Args:
            field_name: Name of the field to monitor
            callback: Function that takes (field_name, value) as arguments
        """
        if field_name not in self.field_change_callbacks:
            self.field_change_callbacks[field_name] = []
        self.field_change_callbacks[field_name].append(callback)


class ValidationMixin:
    """Mixin providing common validation functionality for GUI builders.

    Classes using this mixin must implement:
    - get_form_data() -> Dict[str, Any]: Get current form data
    - _show_error(*args, **kwargs) -> None: Show error dialog
    """

    def _get_all_fields(self) -> List[Any]:
        """Get all fields from config (handling tabs if present)."""
        if not hasattr(self, 'config') or not self.config:
            return []

        all_fields = []
        if hasattr(self.config, 'use_tabs') and self.config.use_tabs and hasattr(self.config, 'tabs') and self.config.tabs:
            for tab in self.config.tabs:
                if hasattr(tab, 'fields') and tab.fields:
                    all_fields.extend(tab.fields)
        elif hasattr(self.config, 'fields') and self.config.fields:
            all_fields = self.config.fields

        return all_fields

    def _validate_required_fields(self) -> bool:
        """
        Validate that all required fields have values.

        Returns:
            True if all required fields are filled, False otherwise
        """
        if not hasattr(self, 'config') or not self.config:
            return True

        # Get all fields from config (handling tabs if present)
        all_fields = self._get_all_fields()

        # Get required field names
        required_field_names = []
        for field_config in all_fields:
            if hasattr(field_config, 'required') and field_config.required:
                required_field_names.append(field_config.name)

        # Get current form data and validate using utility
        form_data = self.get_form_data()
        missing_field_names = ValidationUtils.validate_required_fields(form_data, required_field_names)

        if missing_field_names:
            # Convert field names back to labels for user-friendly display
            missing_labels = []
            for field_name in missing_field_names:
                field_config = next((f for f in all_fields if f.name == field_name), None)
                label = field_config.label if field_config and hasattr(field_config, 'label') else field_name
                missing_labels.append(label)

            # Format the error message
            fields_text = "\n• ".join(missing_labels)
            error_message = f"Please fill in the following required fields:\n• {fields_text}"

            # Call the backend-specific error display
            # Different backends have different signatures, so we try to handle both
            try:
                # Try two-argument form (GTK, Tk with title)
                self._show_error("Required Fields Missing", error_message)
            except TypeError:
                # Fallback to one-argument form (Qt, Flet, Wx)
                self._show_error(error_message)

            return False

        return True


class DataPersistenceMixin:
    """Mixin providing common data loading/saving functionality for GUI builders.

    Classes using this mixin must implement:
    - get_form_data() -> Dict[str, Any]: Get current form data
    - set_form_data(data: Dict[str, Any]) -> None: Set form data
    - _show_error(*args, **kwargs) -> None: Show error dialog (optional, for error handling)
    """

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

            if not success and hasattr(self, '_show_error'):
                try:
                    self._show_error("Save Error", f"Failed to save data to file: {data_file_path}")
                except TypeError:
                    self._show_error(f"Failed to save data to file: {data_file_path}")

            return success

        except Exception as e:
            if hasattr(self, '_show_error'):
                try:
                    self._show_error("Save Error", f"Failed to save data to file: {str(e)}")
                except TypeError:
                    self._show_error(f"Failed to save data to file: {str(e)}")
            else:
                print(f"Error saving data to file: {e}")
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
                if hasattr(self, '_show_error'):
                    try:
                        self._show_error("Load Error", f"Failed to load data from file: {data_file_path}")
                    except TypeError:
                        self._show_error(f"Failed to load data from file: {data_file_path}")
                else:
                    print(f"Error loading data from file: {data_file_path}")
                return False

            self.set_form_data(data)
            return True

        except Exception as e:
            if hasattr(self, '_show_error'):
                try:
                    self._show_error("Load Error", f"Failed to load data from file: {str(e)}")
                except TypeError:
                    self._show_error(f"Failed to load data from file: {str(e)}")
            else:
                print(f"Error loading data from file: {e}")
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
            if data:
                self.set_form_data(data)
                return True
            return False
        except Exception as e:
            if hasattr(self, '_show_error'):
                try:
                    self._show_error("Load Error", f"Failed to load data from dictionary: {str(e)}")
                except TypeError:
                    self._show_error(f"Failed to load data from dictionary: {str(e)}")
            else:
                print(f"Error loading data from dict: {e}")
            return False


class ValidationUtils:
    """Utilities for validating form data and configurations."""

    @staticmethod
    def _get_nested_value(data: Dict[str, Any], key_path: str) -> Any:
        """
        Get a value from a nested dictionary using dot notation.

        Args:
            data: The dictionary to search
            key_path: Dot-separated key path (e.g., "project.name")

        Returns:
            The value at the key path, or None if not found
        """
        if '.' not in key_path:
            return data.get(key_path)

        keys = key_path.split('.')
        current = data

        try:
            for key in keys:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return None
            return current
        except (KeyError, TypeError):
            return None

    @staticmethod
    def validate_required_fields(form_data: Dict[str, Any], required_fields: List[str]) -> List[str]:
        """
        Validate that all required fields have values.

        Args:
            form_data: Dictionary of form field values (may be nested)
            required_fields: List of field names that are required (may use dot notation)

        Returns:
            List of missing field names (empty if all valid)
        """
        missing_fields = []

        for field_name in required_fields:
            # Handle both flat and nested field names
            value = ValidationUtils._get_nested_value(form_data, field_name)
            if value is None or (isinstance(value, str) and not value.strip()):
                missing_fields.append(field_name)

        return missing_fields

    @staticmethod
    def validate_numeric_range(value: Union[int, float], min_val: Optional[float] = None, max_val: Optional[float] = None) -> bool:
        """
        Validate that a numeric value is within the specified range.

        Args:
            value: The numeric value to validate
            min_val: Minimum allowed value (inclusive)
            max_val: Maximum allowed value (inclusive)

        Returns:
            True if value is within range, False otherwise
        """
        if min_val is not None and value < min_val:
            return False
        if max_val is not None and value > max_val:
            return False
        return True


class FileUtils:
    """Utilities for file operations."""

    @staticmethod
    def save_data_to_json(data: Dict[str, Any], file_path: str, include_empty: bool = True) -> bool:
        """
        Save data to a JSON file.

        Args:
            data: Data to save
            file_path: Path to save the file
            include_empty: Whether to include empty/None values

        Returns:
            True if successful, False otherwise
        """
        try:
            if not include_empty:
                data = {k: v for k, v in data.items()
                       if v is not None and (not isinstance(v, str) or v.strip())}

            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"Error saving data to {file_path}: {e}")
            return False

    @staticmethod
    def load_data_from_json(file_path: str) -> Optional[Dict[str, Any]]:
        """
        Load data from a JSON file.

        Args:
            file_path: Path to the JSON file

        Returns:
            Loaded data dictionary, or None if failed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)

        except Exception as e:
            print(f"Error loading data from {file_path}: {e}")
            return None


class PlatformUtils:
    """Utilities for platform-specific operations."""

    @staticmethod
    def get_system() -> str:
        """Get the current operating system."""
        return platform.system()

    @staticmethod
    def is_macos() -> bool:
        """Check if running on macOS."""
        return platform.system() == 'Darwin'

    @staticmethod
    def is_windows() -> bool:
        """Check if running on Windows."""
        return platform.system() == 'Windows'

    @staticmethod
    def is_linux() -> bool:
        """Check if running on Linux."""
        return platform.system() == 'Linux'

    @staticmethod
    def is_dark_mode() -> bool:
        """
        Detect if the system is using dark mode.

        Returns:
            True if dark mode is detected, False otherwise
        """
        try:
            import os
            import subprocess

            if PlatformUtils.is_macos():
                # macOS dark mode detection
                try:
                    result = subprocess.run(
                        ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
                        capture_output=True, text=True, timeout=2
                    )
                    return result.stdout.strip() == 'Dark'
                except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                    return False

            elif PlatformUtils.is_windows():
                # Windows dark mode detection
                try:
                    import winreg
                    registry = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                    key = winreg.OpenKey(registry, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                    value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                    return value == 0  # 0 = dark mode, 1 = light mode
                except (ImportError, OSError, FileNotFoundError):
                    return False

            elif PlatformUtils.is_linux():
                # Linux dark mode detection
                try:
                    # Try gsettings first (GNOME/GTK)
                    result = subprocess.run(
                        ['gsettings', 'get', 'org.gnome.desktop.interface', 'gtk-theme'],
                        capture_output=True, text=True, timeout=2
                    )
                    theme_name = result.stdout.strip().strip("'\"").lower()
                    if 'dark' in theme_name:
                        return True

                    # Try color-scheme setting (newer GNOME)
                    result = subprocess.run(
                        ['gsettings', 'get', 'org.gnome.desktop.interface', 'color-scheme'],
                        capture_output=True, text=True, timeout=2
                    )
                    color_scheme = result.stdout.strip().strip("'\"").lower()
                    return 'dark' in color_scheme or 'prefer-dark' in color_scheme

                except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                    # Fallback: check environment variables
                    return (os.environ.get('GTK_THEME', '').lower().find('dark') >= 0 or
                           os.environ.get('QT_STYLE_OVERRIDE', '').lower().find('dark') >= 0)

            # Default to light mode if detection fails
            return False

        except Exception:
            return False


class FormatUtils:
    """Utilities for formatting values."""

    @staticmethod
    def format_float(value: float, format_string: Optional[str] = None) -> str:
        """
        Format a float value according to the specified format string.

        Args:
            value: The float value to format
            format_string: Format string (e.g., ".2f", ".4f")

        Returns:
            Formatted string representation
        """
        if format_string:
            try:
                return f"{value:{format_string}}"
            except (ValueError, TypeError):
                # Fallback to default formatting if format string is invalid
                pass

        return str(value)

    @staticmethod
    def parse_float(value_str: str) -> Optional[float]:
        """
        Parse a string to float, returning None if invalid.

        Args:
            value_str: String to parse

        Returns:
            Parsed float value or None
        """
        try:
            return float(value_str)
        except (ValueError, TypeError):
            return None

    @staticmethod
    def parse_int(value_str: str) -> Optional[int]:
        """
        Parse a string to int, returning None if invalid.

        Args:
            value_str: String to parse

        Returns:
            Parsed int value or None
        """
        try:
            return int(value_str)
        except (ValueError, TypeError):
            return None


class LayoutUtils:
    """Utilities for layout calculations and adjustments."""

    @staticmethod
    def calculate_window_center(window_width: int, window_height: int, screen_width: int, screen_height: int) -> tuple:
        """
        Calculate the center position for a window.

        Args:
            window_width: Width of the window
            window_height: Height of the window
            screen_width: Width of the screen
            screen_height: Height of the screen

        Returns:
            Tuple of (x, y) coordinates for centering
        """
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        return max(0, x), max(0, y)

    @staticmethod
    def get_recommended_widget_sizes() -> Dict[str, Dict[str, int]]:
        """
        Get recommended widget sizes for different field types.

        Returns:
            Dictionary mapping field types to size recommendations
        """
        return {
            'text': {'width': 200, 'height': 25},
            'password': {'width': 200, 'height': 25},
            'email': {'width': 200, 'height': 25},
            'textarea': {'width': 300, 'height': 100},
            'number': {'width': 100, 'height': 25},
            'float': {'width': 100, 'height': 25},
            'combo': {'width': 150, 'height': 25},
            'select': {'width': 150, 'height': 25},
            'checkbox': {'width': 20, 'height': 20},
            'radio': {'width': 20, 'height': 20},
            'slider': {'width': 200, 'height': 25},
        }
