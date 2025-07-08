"""
Configuration validation utilities for QtPyGuiHelper.
"""

from typing import Dict, Any, List, Optional
from .config_loader import GuiConfig, FieldConfig, TabConfig, WindowConfig, CustomButtonConfig
from .exceptions import ConfigurationError


class ConfigValidator:
    """Validates GUI configuration for correctness and completeness."""

    SUPPORTED_FIELD_TYPES = {
        'text', 'password', 'email', 'textarea', 'number', 'float',
        'combo', 'select', 'checkbox', 'radio', 'slider', 'file', 'color'
    }

    REQUIRED_FIELD_ATTRIBUTES = {'name', 'type', 'label'}

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
            for tab in config.tabs:
                errors.extend(cls._validate_tab_config(tab))
        elif config.fields:
            for field in config.fields:
                errors.extend(cls._validate_field_config(field))
        else:
            errors.append("Configuration must have either fields or tabs defined")

        # Validate custom buttons
        if config.custom_buttons:
            for button in config.custom_buttons:
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

        # Check required attributes
        if not field.name:
            errors.append("Field name cannot be empty")

        if not field.type:
            errors.append(f"Field '{field.name}' must have a type")
        elif field.type not in cls.SUPPORTED_FIELD_TYPES:
            errors.append(f"Field '{field.name}' has unsupported type '{field.type}'. "
                         f"Supported types: {', '.join(sorted(cls.SUPPORTED_FIELD_TYPES))}")

        if not field.label:
            errors.append(f"Field '{field.name}' must have a label")

        # Validate numeric fields
        if field.type in {'number', 'float', 'slider'}:
            if field.min_value is not None and field.max_value is not None:
                if field.min_value >= field.max_value:
                    errors.append(f"Field '{field.name}' min_value must be less than max_value")

        # Validate choice fields
        if field.type in {'combo', 'select', 'radio'}:
            choices = field.options or field.choices
            if not choices:
                errors.append(f"Field '{field.name}' of type '{field.type}' must have options or choices")
            elif not isinstance(choices, list) or len(choices) == 0:
                errors.append(f"Field '{field.name}' options/choices must be a non-empty list")

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
    def validate_field_names_unique(cls, config: GuiConfig) -> List[str]:
        """
        Validate that all field names are unique across the configuration.

        Args:
            config: The GUI configuration to validate

        Returns:
            List of validation error messages for duplicate field names
        """
        errors = []
        seen_names = set()

        # Collect all field names
        all_fields = []
        if config.use_tabs and config.tabs:
            for tab in config.tabs:
                all_fields.extend(tab.fields)
        elif config.fields:
            all_fields = config.fields

        # Check for duplicates
        for field in all_fields:
            if field.name in seen_names:
                errors.append(f"Duplicate field name: '{field.name}'")
            else:
                seen_names.add(field.name)

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
        errors.extend(cls.validate_field_names_unique(config))

        if errors:
            raise ConfigurationError(f"Configuration validation failed:\n" + "\n".join(f"- {error}" for error in errors))
