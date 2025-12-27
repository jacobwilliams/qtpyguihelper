#!/usr/bin/env python3
"""
Test script for nested field names functionality.
"""

import os
import sys
import json

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from vibegui.utils import set_nested_value, flatten_nested_dict, get_nested_value


def test_nested_value_functions() -> None:
    """Test the nested value utility functions."""
    print("Testing nested value utility functions...")

    # Test set_nested_value
    data = {}
    set_nested_value(data, "global.app_name", "My App")
    set_nested_value(data, "database.host", "localhost")
    set_nested_value(data, "database.port", 5432)
    set_nested_value(data, "ui.theme", "dark")

    expected = {
        "global": {"app_name": "My App"},
        "database": {"host": "localhost", "port": 5432},
        "ui": {"theme": "dark"}
    }

    print("Set nested values:", data)
    assert data == expected, f"Expected {expected}, got {data}"

    # Test get_nested_value
    assert get_nested_value(data, "global.app_name") == "My App"
    assert get_nested_value(data, "database.host") == "localhost"
    assert get_nested_value(data, "database.port") == 5432
    assert get_nested_value(data, "ui.theme") == "dark"
    assert get_nested_value(data, "nonexistent.key", "default") == "default"

    print("✓ Get nested values working correctly")

    # Test flatten_nested_dict
    flattened = flatten_nested_dict(data)
    expected_flat = {
        "global.app_name": "My App",
        "database.host": "localhost",
        "database.port": 5432,
        "ui.theme": "dark"
    }

    print("Flattened:", flattened)
    assert flattened == expected_flat, f"Expected {expected_flat}, got {flattened}"

    print("✓ All nested value utility functions working correctly!")


def test_nested_config_loading() -> None:
    """Test loading a config with nested field names."""
    print("\nTesting nested config loading...")

    # Try to load the nested config
    config_path = os.path.join(os.path.dirname(__file__), "examples", "nested_config.json")

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)

        # Check that we have fields with dot notation
        field_names = [field['name'] for field in config['fields']]
        nested_fields = [name for name in field_names if '.' in name]

        print(f"Found {len(nested_fields)} nested field names:")
        for name in nested_fields:
            print(f"  - {name}")

        assert len(nested_fields) > 0, "No nested field names found in config"
        print("✓ Nested config structure is valid!")
    else:
        print("⚠ Nested config file not found, skipping this test")


def test_nested_data_loading() -> None:
    """Test loading nested data."""
    print("\nTesting nested data loading...")

    data_path = os.path.join(os.path.dirname(__file__), "examples", "nested_data.json")

    if os.path.exists(data_path):
        with open(data_path, 'r') as f:
            data = json.load(f)

        # Test that we can access nested values
        app_name = get_nested_value(data, "global.app_name")
        db_host = get_nested_value(data, "database.host")
        ui_theme = get_nested_value(data, "ui.theme")

        print(f"app_name: {app_name}")
        print(f"db_host: {db_host}")
        print(f"ui_theme: {ui_theme}")

        assert app_name is not None, "Could not access global.app_name"
        assert db_host is not None, "Could not access database.host"
        assert ui_theme is not None, "Could not access ui.theme"

        print("✓ Nested data loading working correctly!")
    else:
        print("⚠ Nested data file not found, skipping this test")

