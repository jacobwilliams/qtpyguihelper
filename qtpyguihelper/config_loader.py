"""
Configuration loader for reading and validating JSON GUI configuration files.
"""

import json
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass


@dataclass
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

    def load_from_file(self, config_path: str) -> GuiConfig:
        """Load configuration from a JSON file."""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as file:
            config_data = json.load(file)

        return self.load_from_dict(config_data)

    def load_from_dict(self, config_data: Dict[str, Any]) -> GuiConfig:
        """Load configuration from a dictionary."""
        self._validate_config(config_data)

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
        self.config = GuiConfig(
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

        return self.config

    def _validate_config(self, config_data: Dict[str, Any]) -> None:
        """Validate the configuration data."""
        # Initialize field names set for later validation
        field_names = set()

        # First, collect all field names from the main fields list if it exists
        if "fields" in config_data and isinstance(config_data["fields"], list):
            fields = config_data["fields"]

            # Validate each field and collect names
            for i, field in enumerate(fields):
                if not isinstance(field, dict):
                    raise ValueError(f"Field {i} must be a dictionary")

                # Check required field keys
                required_keys = ["name", "type", "label"]
                for key in required_keys:
                    if key not in field:
                        raise ValueError(f"Field {i} missing required key: {key}")

                # Check field name uniqueness
                field_name = field["name"]
                if field_name in field_names:
                    raise ValueError(f"Duplicate field name: {field_name}")
                field_names.add(field_name)

                # Validate field type
                field_type = field["type"]
                if field_type not in self.SUPPORTED_FIELD_TYPES:
                    raise ValueError(f"Unsupported field type: {field_type}")

                # Validate options for select/radio/combo fields
                if field_type in ["select", "radio", "combo"]:
                    if "options" not in field or not field["options"]:
                        # For combo fields, also check for "choices" as an alternative
                        if field_type == "combo" and "choices" in field and field["choices"]:
                            pass  # choices is acceptable for combo fields
                        else:
                            raise ValueError(f"Field {field_name} of type {field_type} must have 'options' or 'choices'")

                # Validate numeric constraints
                if field_type in ["number", "range"]:
                    min_val = field.get("min_value")
                    max_val = field.get("max_value")
                    if min_val is not None and max_val is not None and min_val > max_val:
                        raise ValueError(f"Field {field_name}: min_value cannot be greater than max_value")

        # Check if using tabs
        use_tabs = config_data.get("use_tabs", False)
        has_tabs = "tabs" in config_data and config_data["tabs"]

        if use_tabs or has_tabs:
            # When using tabs or tabs are present, validate them
            if "tabs" not in config_data:
                raise ValueError("Configuration with use_tabs=True must contain 'tabs' key")

            tabs = config_data["tabs"]
            if not isinstance(tabs, list) or len(tabs) == 0:
                raise ValueError("'tabs' must be a non-empty list when use_tabs=True")

            # Track tab names to check for duplicates
            tab_names = set()

            # Validate each tab and its fields
            for i, tab in enumerate(tabs):
                if not isinstance(tab, dict):
                    raise ValueError(f"Tab {i} must be a dictionary")

                required_tab_keys = ["name", "title", "fields"]
                for key in required_tab_keys:
                    if key not in tab:
                        raise ValueError(f"Tab {i} missing required key: {key}")

                # Check for duplicate tab names
                tab_name = tab["name"]
                if tab_name in tab_names:
                    raise ValueError(f"Duplicate tab name: {tab_name}")
                tab_names.add(tab_name)

                # Validate fields within this tab
                tab_fields = tab["fields"]
                if not isinstance(tab_fields, list):
                    raise ValueError(f"Tab {i} 'fields' must be a list")

                # Check if we have a main fields list (field references) or inline field definitions
                has_main_fields = "fields" in config_data and isinstance(config_data["fields"], list)

                for j, field in enumerate(tab_fields):
                    if has_main_fields:
                        # Fields should be strings referencing the main fields list
                        if not isinstance(field, str):
                            raise ValueError(f"Tab {i}, field {j} must be a string (field name) when main fields list exists")
                        # Check that the referenced field actually exists
                        if field not in field_names:
                            raise ValueError(f"Tab '{tab['name']}' references unknown field '{field}'")
                    else:
                        # Fields should be dictionaries (inline field definitions)
                        if not isinstance(field, dict):
                            raise ValueError(f"Tab {i}, field {j} must be a dictionary")

                        # Check required field keys
                        required_keys = ["name", "type", "label"]
                        for key in required_keys:
                            if key not in field:
                                raise ValueError(f"Tab {i}, field {j} missing required key: {key}")
        else:
            # Traditional layout - fields at root level
            if "fields" not in config_data:
                raise ValueError("Configuration must contain 'fields' key")

        # Validate layout
        layout = config_data.get("layout", "vertical")
        if layout not in self.SUPPORTED_LAYOUTS:
            raise ValueError(f"Unsupported layout: {layout}")

        # Validate custom buttons if present
        custom_buttons_data = config_data.get("custom_buttons", [])
        if custom_buttons_data:
            if not isinstance(custom_buttons_data, list):
                raise ValueError("'custom_buttons' must be a list")

            button_names = set()
            for i, button in enumerate(custom_buttons_data):
                if not isinstance(button, dict):
                    raise ValueError(f"Custom button {i} must be a dictionary")

                # Check required button keys
                required_button_keys = ["name", "label"]
                for key in required_button_keys:
                    if key not in button:
                        raise ValueError(f"Custom button {i} missing required key: {key}")

                # Check button name uniqueness
                button_name = button["name"]
                if button_name in button_names:
                    raise ValueError(f"Duplicate custom button name: {button_name}")
                button_names.add(button_name)

    def get_field_by_name(self, name: str) -> Optional[FieldConfig]:
        """Get a field configuration by name."""
        if not self.config:
            return None

        for field in self.config.fields:
            if field.name == name:
                return field
        return None
