#!/usr/bin/env python3
"""
Comprehensive test suite for vibegui library.
Run with: python -m pytest tests/test_comprehensive.py -v
"""

import sys
import os
import tempfile
import json
from pathlib import Path
import pytest

# Add the library to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

from vibegui.config_loader import ConfigLoader, FieldConfig
from vibegui.backend import get_available_backends, set_backend, get_backend_info


class TestConfigLoader:
    """Test the configuration loader."""

    def test_valid_config_loading(self) -> None:
        """Test loading a valid configuration."""
        config_data = {
            "window": {"title": "Test App", "width": 500, "height": 400},
            "fields": [
                {"name": "test_field", "type": "text", "label": "Test Field"}
            ],
            "submit_button": True
        }

        loader = ConfigLoader()
        config = loader.load_from_dict(config_data)

        assert config.window.title == "Test App"
        assert config.window.width == 500
        assert len(config.fields) == 1
        assert config.fields[0].name == "test_field"

    def test_invalid_config_validation(self) -> None:
        """Test validation of invalid configurations."""
        loader = ConfigLoader()

        # Missing required fields key - should fail schema validation
        with pytest.raises(ValueError, match="Schema validation failed|Configuration must contain 'fields' key"):
            loader.load_from_dict({"window": {"title": "Test"}})

        # Invalid field type - should fail schema validation
        config_data = {
            "fields": [
                {"name": "test", "type": "invalid_type", "label": "Test"}
            ]
        }
        with pytest.raises(ValueError, match="Schema validation failed|'invalid_type' is not one of"):
            loader.load_from_dict(config_data)

    def test_tab_configuration(self) -> None:
        """Test tab configuration loading."""
        config_data = {
            "use_tabs": True,
            "fields": [
                {"name": "field1", "type": "text", "label": "Field 1"},
                {"name": "field2", "type": "text", "label": "Field 2"}
            ],
            "tabs": [
                {"name": "tab1", "title": "Tab 1", "fields": ["field1"], "layout": "form"},
                {"name": "tab2", "title": "Tab 2", "fields": ["field2"], "layout": "form"}
            ]
        }

        loader = ConfigLoader()
        config = loader.load_from_dict(config_data)

        assert config.use_tabs is True
        assert len(config.tabs) == 2
        assert config.tabs[0].name == "tab1"
        assert len(config.tabs[0].fields) == 1


class TestBackendSystem:
    """Test the backend selection system."""

    def test_backend_detection(self) -> None:
        """Test backend detection."""
        backends = get_available_backends()
        assert isinstance(backends, list)
        assert len(backends) > 0  # At least one backend should be available

    def test_backend_switching(self) -> None:
        """Test backend switching."""
        # Test setting Qt backend
        set_backend('qt')
        info = get_backend_info()
        assert info['backend'] == 'qt'

        # Test setting wx backend (if available)
        available = get_available_backends()
        if 'wx' in available:
            set_backend('wx')
            info = get_backend_info()
            assert info['backend'] == 'wx'


class TestFieldTypes:
    """Test different field types."""

    @pytest.fixture
    def basic_config(self) -> dict:
        """Basic configuration template."""
        return {
            "window": {"title": "Test", "width": 400, "height": 300},
            "submit_button": True,
            "fields": []
        }

    def test_text_field(self, basic_config: dict) -> None:
        """Test text field configuration."""
        basic_config["fields"] = [
            {
                "name": "text_field",
                "type": "text",
                "label": "Text Field",
                "placeholder": "Enter text",
                "required": True
            }
        ]

        loader = ConfigLoader()
        config = loader.load_from_dict(basic_config)
        field = config.fields[0]

        assert field.type == "text"
        assert field.placeholder == "Enter text"
        assert field.required is True

    def test_numeric_fields(self, basic_config: dict) -> None:
        """Test numeric field types."""
        basic_config["fields"] = [
            {
                "name": "int_field",
                "type": "int",
                "label": "Integer",
                "min_value": 0,
                "max_value": 100,
                "default_value": 50
            },
            {
                "name": "float_field",
                "type": "float",
                "label": "Float",
                "format_string": ".2f",
                "default_value": 3.14
            }
        ]

        loader = ConfigLoader()
        config = loader.load_from_dict(basic_config)

        int_field = config.fields[0]
        float_field = config.fields[1]

        assert int_field.type == "int"
        assert int_field.min_value == 0
        assert int_field.max_value == 100

        assert float_field.type == "float"
        assert float_field.format_string == ".2f"

    def test_choice_fields(self, basic_config: dict) -> None:
        """Test choice field types (select, radio)."""
        basic_config["fields"] = [
            {
                "name": "select_field",
                "type": "select",
                "label": "Select Option",
                "options": ["Option 1", "Option 2", "Option 3"],
                "default_value": "Option 1"
            },
            {
                "name": "radio_field",
                "type": "radio",
                "label": "Radio Options",
                "options": ["Choice A", "Choice B"],
                "default_value": "Choice A"
            }
        ]

        loader = ConfigLoader()
        config = loader.load_from_dict(basic_config)

        select_field = config.fields[0]
        radio_field = config.fields[1]

        assert select_field.type == "select"
        assert select_field.options == ["Option 1", "Option 2", "Option 3"]

        assert radio_field.type == "radio"
        assert radio_field.options == ["Choice A", "Choice B"]


class TestFileOperations:
    """Test file operations."""

    def test_config_file_loading(self) -> None:
        """Test loading configuration from file."""
        config_data = {
            "window": {"title": "File Test"},
            "fields": [
                {"name": "test", "type": "text", "label": "Test"}
            ]
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_path = f.name

        try:
            loader = ConfigLoader()
            config = loader.load_from_file(temp_path)
            assert config.window.title == "File Test"
        finally:
            os.unlink(temp_path)

    def test_nonexistent_file(self) -> None:
        """Test loading from nonexistent file."""
        loader = ConfigLoader()
        with pytest.raises(FileNotFoundError):
            loader.load_from_file("/nonexistent/file.json")

