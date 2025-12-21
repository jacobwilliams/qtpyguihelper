"""
Configuration loader for reading and validating JSON GUI configuration files.
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
    """Configuration for a single form field."""
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
    """Configuration for the main window."""
    title: str = "GUI Application"
    width: int = 800
    height: int = 600
    resizable: bool = True
    icon: Optional[str] = None


@dataclass
class TabConfig:
    """Configuration for a single tab."""
    name: str
    title: str
    fields: List[FieldConfig]
    layout: str = "vertical"
    enabled: bool = True
    tooltip: Optional[str] = None


@dataclass
class CustomButtonConfig:
    """Configuration for a custom button."""
    name: str
    label: str
    tooltip: Optional[str] = None
    enabled: bool = True
    icon: Optional[str] = None
    style: Optional[str] = None  # CSS style string


@dataclass
class GuiConfig:
    """Complete GUI configuration."""
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
    """Loads and validates GUI configuration from JSON files."""

    SUPPORTED_FIELD_TYPES = {
        "text", "number", "int", "float", "email", "password", "textarea",
        "checkbox", "check", "radio", "select", "combo", "date", "time",
        "datetime", "file", "color", "range", "spin", "url"
    }

    SUPPORTED_LAYOUTS = {"vertical", "horizontal", "grid", "form"}

    def __init__(self):
        self.config: Optional[GuiConfig] = None
        self._schema_cache: Optional[Dict[str, Any]] = None

    def _load_schema(self) -> Dict[str, Any]:
        """Load the JSON schema from the package."""
        if self._schema_cache is not None:
            return self._schema_cache

        # Get the directory where this module is located
        module_dir = os.path.dirname(os.path.abspath(__file__))
        schema_path = os.path.join(module_dir, 'schema', 'gui_config_schema.json')

        with open(schema_path, 'r', encoding='utf-8') as f:
            self._schema_cache = json.load(f)

        return self._schema_cache

    def load_from_file(self, config_path: str) -> GuiConfig:
        """Load configuration from a JSON file."""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as file:
            config_data = json.load(file)

        return self.load_from_dict(config_data)

    def load_from_dict(self, config_data: Dict[str, Any]) -> GuiConfig:
        """Load configuration from a dictionary."""
        # Validate structure with JSON schema
        self._validate_config(config_data)

        # Parse into GuiConfig object
        config = self._create_gui_config_from_dict(config_data)

        # Validate semantics with ConfigValidator
        from .config_validator import ConfigValidator
        ConfigValidator.validate_and_raise(config)

        return config

    def _create_gui_config_from_dict(self, config_data: Dict[str, Any]) -> GuiConfig:
        """Create GuiConfig object from dictionary (without validation)."""
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
        """Validate the configuration data using JSON schema."""
        # Validate against JSON schema if jsonschema is available
        if HAS_JSONSCHEMA:
            try:
                schema = self._load_schema()
                validate(instance=config_data, schema=schema)
            except JsonSchemaValidationError as e:
                raise ValueError(f"Schema validation failed: {e.message}") from e

    def get_field_by_name(self, name: str) -> Optional[FieldConfig]:
        """Get a field configuration by name."""
        if not self.config:
            return None

        for field in self.config.fields:
            if field.name == name:
                return field
        return None
