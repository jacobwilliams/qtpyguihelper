"""
Common utilities used across different GUI backends.
"""

import json
import platform
from typing import Dict, Any, Optional, Union, List


class ValidationUtils:
    """Utilities for validating form data and configurations."""

    @staticmethod
    def validate_required_fields(form_data: Dict[str, Any], required_fields: List[str]) -> List[str]:
        """
        Validate that all required fields have values.

        Args:
            form_data: Dictionary of form field values
            required_fields: List of field names that are required

        Returns:
            List of missing field names (empty if all valid)
        """
        missing_fields = []

        for field_name in required_fields:
            value = form_data.get(field_name)
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
