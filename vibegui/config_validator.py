"""
Configuration validation utilities for vibegui.
"""

from typing import Dict, Any, List, Optional
from .config_loader import GuiConfig, FieldConfig, TabConfig, WindowConfig, CustomButtonConfig
from .exceptions import ConfigurationError


class ConfigValidator:
    """Validates GUI configuration for correctness and completeness."""

    SUPPORTED_FIELD_TYPES = {
        "text", "number", "int", "float", "email", "password", "textarea",
        "checkbox", "check", "radio", "select", "combo", "date", "time",
        "datetime", "file", "color", "range", "spin", "url"
    }

    @classmethod
    def validate_config(cls, config: GuiConfig) -> List[str]:
        """
        Validate a complete GUI configuration.

        Args:
            config: The GUI configuration to validate

        Returns:
            List of validation error messages (empty if valid)
        """
        errors = []

        # Validate window configuration
        errors.extend(cls._validate_window_config(config.window))

        # Validate fields or tabs
        if config.use_tabs and config.tabs:
            # Validate tabs and uniqueness
            tab_names = set()
            for tab in config.tabs:
                if tab.name in tab_names:
                    errors.append(f"Duplicate tab name: '{tab.name}'")
                else:
                    tab_names.add(tab.name)
                errors.extend(cls._validate_tab_config(tab))
        elif config.fields:
            # Validate field uniqueness
            field_names = set()
            for field in config.fields:
                if field.name in field_names:
                    errors.append(f"Duplicate field name: '{field.name}'")
                else:
                    field_names.add(field.name)
                errors.extend(cls._validate_field_config(field))
        else:
            errors.append("Configuration must have either fields or tabs defined")

        # Validate custom buttons and uniqueness
        if config.custom_buttons:
            button_names = set()
            for button in config.custom_buttons:
                if button.name in button_names:
                    errors.append(f"Duplicate custom button name: '{button.name}'")
                else:
                    button_names.add(button.name)
                errors.extend(cls._validate_custom_button_config(button))

        return errors

    @classmethod
    def _validate_window_config(cls, window: WindowConfig) -> List[str]:
        """Validate window configuration."""
        errors = []

        if not window.title:
            errors.append("Window title cannot be empty")

        if window.width <= 0:
            errors.append("Window width must be positive")

        if window.height <= 0:
            errors.append("Window height must be positive")

        return errors

    @classmethod
    def _validate_field_config(cls, field: FieldConfig) -> List[str]:
        """Validate a single field configuration."""
        errors = []

        # Check required attributes (schema already validates these exist, but check for empty)
        if not field.name:
            errors.append("Field name cannot be empty")

        if not field.type:
            errors.append(f"Field '{field.name}' must have a type")
        elif field.type not in cls.SUPPORTED_FIELD_TYPES:
            errors.append(f"Field '{field.name}' has unsupported type '{field.type}'. "
                         f"Supported types: {', '.join(sorted(cls.SUPPORTED_FIELD_TYPES))}")

        if not field.label:
            errors.append(f"Field '{field.name}' must have a label")

        # Validate numeric fields - min_value must be less than max_value
        if field.type in {"number", "int", "float", "range", "spin"}:
            if field.min_value is not None and field.max_value is not None:
                if field.min_value >= field.max_value:
                    errors.append(f"Field '{field.name}' min_value must be less than max_value")

        # Validate choice fields - for select/radio, require non-empty options
        if field.type in {"select", "radio"}:
            choices = field.options or field.choices
            if not choices:
                errors.append(f"Field '{field.name}' of type '{field.type}' must have options or choices")
            elif not isinstance(choices, list) or len(choices) == 0:
                errors.append(f"Field '{field.name}' options/choices must be a non-empty list")
        # For combo, options/choices are optional but if provided must be non-empty
        elif field.type == "combo":
            choices = field.options or field.choices
            if choices is not None and (not isinstance(choices, list) or len(choices) == 0):
                errors.append(f"Field '{field.name}' options/choices, if provided, must be a non-empty list")

        # Validate dimensions
        if field.width is not None and field.width <= 0:
            errors.append(f"Field '{field.name}' width must be positive")

        if field.height is not None and field.height <= 0:
            errors.append(f"Field '{field.name}' height must be positive")

        return errors

    @classmethod
    def _validate_tab_config(cls, tab: TabConfig) -> List[str]:
        """Validate a tab configuration."""
        errors = []

        if not tab.name:
            errors.append("Tab name cannot be empty")

        if not tab.title:
            errors.append(f"Tab '{tab.name}' must have a title")

        if not tab.fields:
            errors.append(f"Tab '{tab.name}' must have at least one field")

        # Validate all fields in the tab
        for field in tab.fields:
            field_errors = cls._validate_field_config(field)
            errors.extend(field_errors)

        return errors

    @classmethod
    def _validate_custom_button_config(cls, button: CustomButtonConfig) -> List[str]:
        """Validate a custom button configuration."""
        errors = []

        if not button.name:
            errors.append("Custom button name cannot be empty")

        if not button.label:
            errors.append(f"Custom button '{button.name}' must have a label")

        return errors

    @classmethod
    def validate_and_raise(cls, config: GuiConfig) -> None:
        """
        Validate configuration and raise ConfigurationError if invalid.

        Args:
            config: The GUI configuration to validate

        Raises:
            ConfigurationError: If the configuration is invalid
        """
        errors = cls.validate_config(config)

        if errors:
            raise ConfigurationError(f"Configuration validation failed:\n" + "\n".join(f"- {error}" for error in errors))
