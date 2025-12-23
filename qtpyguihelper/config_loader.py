"""
Configuration loader for reading and validating JSON GUI configuration files.

This module provides classes and functions for loading, parsing, and validating
GUI configuration files in JSON format. It supports two-layer validation:
1. JSON Schema validation for structural correctness
2. Semantic validation via ConfigValidator for business logic

The module defines dataclasses for representing different parts of the GUI
configuration (fields, windows, tabs, buttons) and provides a ConfigLoader
class for loading and validating these configurations.

Typical usage example:

    loader = ConfigLoader()
    config = loader.load_from_file('path/to/config.json')
    field = loader.get_field_by_name('username')
"""

import json
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Optional JSON Schema validation
try:
    from jsonschema import validate, ValidationError as JsonSchemaValidationError
    HAS_JSONSCHEMA = True
except ImportError:
    HAS_JSONSCHEMA = False


@dataclass
class FieldConfig:
    """Configuration for a single form field.

    Represents all configuration options for a form field including its type,
    label, default value, constraints, and display options.

    Attributes:
        name (str): Unique identifier for the field.
        type (str): Field type (e.g., 'text', 'number', 'select', 'checkbox').
        label (str): Display label shown to the user.
        default_value (Any, optional): Default value for the field. Defaults to None.
        required (bool, optional): Whether the field is required. Defaults to False.
        min_value (float, optional): Minimum value for numeric fields. Defaults to None.
        max_value (float, optional): Maximum value for numeric fields. Defaults to None.
        options (List[str], optional): Options for select/radio/combo fields. Defaults to None.
        choices (List[str], optional): Alternative to options for combo/select fields. Defaults to None.
        placeholder (str, optional): Placeholder text for input fields. Defaults to None.
        tooltip (str, optional): Tooltip text shown on hover. Defaults to None.
        width (int, optional): Field width in pixels. Defaults to None.
        height (int, optional): Field height in pixels. Defaults to None.
        format_string (str, optional): Python format string for float fields (e.g., '.2f'). Defaults to None.
    """
    name: str
    type: str
    label: str
    default_value: Any = None
    required: bool = False
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    options: Optional[List[str]] = None
    choices: Optional[List[str]] = None  # Alternative to options for combo/select fields
    placeholder: Optional[str] = None
    tooltip: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    format_string: Optional[str] = None  # For float formatting (e.g., ".2f", ".4f", etc.)


@dataclass
class WindowConfig:
    """Configuration for the main application window.

    Defines the appearance and behavior of the main GUI window including
    dimensions, title, and resizability.

    Attributes:
        title (str): Window title text. Defaults to 'GUI Application'.
        width (int): Window width in pixels. Defaults to 800.
        height (int): Window height in pixels. Defaults to 600.
        resizable (bool): Whether the window can be resized. Defaults to True.
        icon (str, optional): Path to window icon file. Defaults to None.
    """
    title: str = "GUI Application"
    width: int = 800
    height: int = 600
    resizable: bool = True
    icon: Optional[str] = None


@dataclass
class TabConfig:
    """Configuration for a single tab in a tabbed interface.

    Represents a tab containing multiple form fields with its own layout
    and display properties.

    Attributes:
        name (str): Unique identifier for the tab.
        title (str): Display title shown on the tab.
        fields (List[FieldConfig]): List of form fields contained in this tab.
        layout (str): Layout style for fields ('vertical', 'horizontal', 'grid', 'form'). Defaults to 'vertical'.
        enabled (bool): Whether the tab is enabled and accessible. Defaults to True.
        tooltip (str, optional): Tooltip text shown on tab hover. Defaults to None.
    """
    name: str
    title: str
    fields: List[FieldConfig]
    layout: str = "vertical"
    enabled: bool = True
    tooltip: Optional[str] = None


@dataclass
class CustomButtonConfig:
    """Configuration for a custom action button.

    Defines a custom button that can trigger application-specific actions
    beyond the standard submit/cancel buttons.

    Attributes:
        name (str): Unique identifier for the button.
        label (str): Display text shown on the button.
        tooltip (str, optional): Tooltip text shown on button hover. Defaults to None.
        enabled (bool): Whether the button is enabled and clickable. Defaults to True.
        icon (str, optional): Path to button icon file. Defaults to None.
        style (str, optional): CSS style string for button styling. Defaults to None.
    """
    name: str
    label: str
    tooltip: Optional[str] = None
    enabled: bool = True
    icon: Optional[str] = None
    style: Optional[str] = None  # CSS style string


@dataclass
class GuiConfig:
    """Complete GUI configuration for the entire application.

    Top-level configuration object that contains all settings for the GUI
    including window, fields, tabs, layout, and buttons.

    Attributes:
        window (WindowConfig): Main window configuration.
        fields (List[FieldConfig]): List of form fields (used when not using tabs).
        tabs (List[TabConfig], optional): List of tabs for tabbed interface. Defaults to None.
        layout (str): Default layout style for fields. Defaults to 'vertical'.
        submit_button (bool): Whether to show submit button. Defaults to True.
        submit_label (str): Label for submit button. Defaults to 'Submit'.
        cancel_button (bool): Whether to show cancel button. Defaults to True.
        cancel_label (str): Label for cancel button. Defaults to 'Cancel'.
        use_tabs (bool): Whether to use tabbed interface. Defaults to False.
        custom_buttons (List[CustomButtonConfig], optional): List of custom buttons. Defaults to None.
    """
    window: WindowConfig
    fields: List[FieldConfig]
    tabs: Optional[List[TabConfig]] = None
    layout: str = "vertical"
    submit_button: bool = True
    submit_label: str = "Submit"
    cancel_button: bool = True
    cancel_label: str = "Cancel"
    use_tabs: bool = False
    custom_buttons: Optional[List[CustomButtonConfig]] = None


class ConfigLoader:
    """Loads and validates GUI configuration from JSON files.

    Provides functionality to load GUI configurations from JSON files or
    dictionaries, validate them against JSON Schema and semantic rules,
    and parse them into GuiConfig objects.

    The loader performs two-layer validation:
    1. JSON Schema validation (if jsonschema package is available)
    2. Semantic validation via ConfigValidator

    Attributes:
        config (GuiConfig, optional): Most recently loaded configuration.
        SUPPORTED_FIELD_TYPES (set): Set of supported field type strings.
        SUPPORTED_LAYOUTS (set): Set of supported layout type strings.

    Example:
        >>> loader = ConfigLoader()
        >>> config = loader.load_from_file('my_form.json')
        >>> username_field = loader.get_field_by_name('username')
    """

    SUPPORTED_FIELD_TYPES = {
        "text", "number", "int", "float", "email", "password", "textarea",
        "checkbox", "check", "radio", "select", "combo", "date", "time",
        "datetime", "file", "color", "range", "spin", "url"
    }

    SUPPORTED_LAYOUTS = {"vertical", "horizontal", "grid", "form"}

    def __init__(self) -> None:
        """Initialize a new ConfigLoader instance.

        Creates a new loader with empty config and schema cache.
        """
        self.config: Optional[GuiConfig] = None
        self._schema_cache: Optional[Dict[str, Any]] = None

    def _load_schema(self) -> Dict[str, Any]:
        """Load the JSON schema from the package.

        Loads the gui_config_schema.json file from the package's schema directory.
        The schema is cached after first load for performance.

        Returns:
            Dict[str, Any]: The parsed JSON schema as a dictionary.

        Raises:
            FileNotFoundError: If the schema file cannot be found.
            json.JSONDecodeError: If the schema file contains invalid JSON.
        """
        if self._schema_cache is not None:
            return self._schema_cache

        # Get the directory where this module is located
        module_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(module_dir, 'schema', 'gui_config_schema.json')

        with open(schema_path, 'r', encoding='utf-8') as f:
            self._schema_cache = json.load(f)

        return self._schema_cache

    def load_from_file(self, config_path: str) -> GuiConfig:
        """Load configuration from a JSON file.

        Reads a JSON configuration file, validates it, and returns a GuiConfig object.

        Args:
            config_path (str): Path to the JSON configuration file.

        Returns:
            GuiConfig: Validated GUI configuration object.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON.
            ValueError: If schema validation fails.
            ConfigurationError: If semantic validation fails.
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as file:
            config_data = json.load(file)

        return self.load_from_dict(config_data)

    def load_from_dict(self, config_data: Dict[str, Any]) -> GuiConfig:
        """Load configuration from a dictionary.

        Validates and parses a configuration dictionary into a GuiConfig object.
        Performs both JSON schema and semantic validation.

        Args:
            config_data (Dict[str, Any]): Configuration data as a dictionary.

        Returns:
            GuiConfig: Validated GUI configuration object.

        Raises:
            ValueError: If schema validation fails.
            ConfigurationError: If semantic validation fails.
        """
        # Validate structure with JSON schema
        self._validate_config(config_data)

        # Parse into GuiConfig object
        config = self._create_gui_config_from_dict(config_data)

        # Validate semantics with ConfigValidator
        from .config_validator import ConfigValidator
        ConfigValidator.validate_and_raise(config)

        return config

    def _create_gui_config_from_dict(self, config_data: Dict[str, Any]) -> GuiConfig:
        """Create GuiConfig object from dictionary without validation.

        Parses raw configuration dictionary into structured GuiConfig object
        with all nested dataclasses. Does not perform validation - assumes
        the data has already been validated.

        Args:
            config_data (Dict[str, Any]): Raw configuration dictionary.

        Returns:
            GuiConfig: Parsed GUI configuration object.

        Raises:
            ValueError: If tab references unknown field.
            KeyError: If required keys are missing from field/tab definitions.
        """
        # Parse window configuration
        window_data = config_data.get("window", {})
        window_config = WindowConfig(
            title=window_data.get("title", "GUI Application"),
            width=window_data.get("width", 800),
            height=window_data.get("height", 600),
            resizable=window_data.get("resizable", True),
            icon=window_data.get("icon")
        )

        # Parse field configurations
        fields_data = config_data.get("fields", [])
        fields = []
        for field_data in fields_data:
            field_config = FieldConfig(
                name=field_data["name"],
                type=field_data["type"],
                label=field_data["label"],
                default_value=field_data.get("default_value"),
                required=field_data.get("required", False),
                min_value=field_data.get("min_value"),
                max_value=field_data.get("max_value"),
                options=field_data.get("options"),
                choices=field_data.get("choices"),  # Add support for choices
                placeholder=field_data.get("placeholder"),
                tooltip=field_data.get("tooltip"),
                width=field_data.get("width"),
                height=field_data.get("height"),
                format_string=field_data.get("format_string")
            )
            fields.append(field_config)

        # Parse tab configurations
        tabs_data = config_data.get("tabs", [])
        tabs = []
        for tab_data in tabs_data:
            # Parse fields for this tab
            tab_fields = []
            for field_name in tab_data.get("fields", []):
                # Find the field in the main fields list
                field_found = False
                for field_config in fields:
                    if field_config.name == field_name:
                        tab_fields.append(field_config)
                        field_found = True
                        break
                if not field_found:
                    raise ValueError(f"Tab '{tab_data['name']}' references unknown field '{field_name}'")

            tab_config = TabConfig(
                name=tab_data["name"],
                title=tab_data["title"],
                fields=tab_fields,
                layout=tab_data.get("layout", "vertical"),
                enabled=tab_data.get("enabled", True),
                tooltip=tab_data.get("tooltip")
            )
            tabs.append(tab_config)

        # Parse custom button configurations
        custom_buttons_data = config_data.get("custom_buttons", [])
        custom_buttons = []
        for button_data in custom_buttons_data:
            custom_button = CustomButtonConfig(
                name=button_data["name"],
                label=button_data["label"],
                tooltip=button_data.get("tooltip"),
                enabled=button_data.get("enabled", True),
                icon=button_data.get("icon"),
                style=button_data.get("style")
            )
            custom_buttons.append(custom_button)

        # Create complete configuration
        use_tabs = len(tabs) > 0 or config_data.get("use_tabs", False)
        config = GuiConfig(
            window=window_config,
            fields=fields,
            tabs=tabs if tabs else None,
            layout=config_data.get("layout", "vertical"),
            submit_button=config_data.get("submit_button", True),
            submit_label=config_data.get("submit_label", "Submit"),
            cancel_button=config_data.get("cancel_button", True),
            cancel_label=config_data.get("cancel_label", "Cancel"),
            use_tabs=use_tabs,
            custom_buttons=custom_buttons if custom_buttons else None
        )

        self.config = config
        return config

    def _validate_config(self, config_data: Dict[str, Any]) -> None:
        """Validate the configuration data using JSON schema.

        Performs structural validation of configuration data against the
        gui_config_schema.json schema. Only validates if jsonschema package
        is installed; otherwise silently skips schema validation.

        Args:
            config_data (Dict[str, Any]): Configuration data to validate.

        Raises:
            ValueError: If schema validation fails with details of the validation error.
        """
        # Validate against JSON schema if jsonschema is available
        if HAS_JSONSCHEMA:
            try:
                schema = self._load_schema()
                validate(instance=config_data, schema=schema)
            except JsonSchemaValidationError as e:
                raise ValueError(f"Schema validation failed: {e.message}") from e

    def get_field_by_name(self, name: str) -> Optional[FieldConfig]:
        """Get a field configuration by name.

        Searches for a field with the given name in the currently loaded
        configuration.

        Args:
            name (str): Name of the field to retrieve.

        Returns:
            FieldConfig: The field configuration if found.
            None: If no config is loaded or field is not found.
        """
        if not self.config:
            return None

        for field in self.config.fields:
            if field.name == name:
                return field
        return None
