#!/usr/bin/env python3
"""
Test script for vibegui library configuration loading.
"""

import os
import sys
import json

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from vibegui.config_loader import ConfigLoader
from vibegui.exceptions import ConfigurationError


def test_config_loading() -> None:
    """Test loading and validation of example configurations."""
    print("Testing vibegui Configuration Loading...")
    print("=" * 50)

    loader = ConfigLoader()
    # Examples are in the root examples directory, not tests/examples
    examples_dir = os.path.join(os.path.dirname(__file__), "..", "examples")

    # Test each example configuration
    example_files = [
        "user_registration.json",
        "settings_form.json",
        "project_form.json"
    ]

    for filename in example_files:
        file_path = os.path.join(examples_dir, filename)
        print(f"\nTesting {filename}...")

        try:
            # Load configuration
            config = loader.load_from_file(file_path)

            print(f"  ✓ Configuration loaded successfully")
            print(f"  ✓ Window title: {config.window.title}")
            print(f"  ✓ Layout: {config.layout}")
            print(f"  ✓ Number of fields: {len(config.fields)}")

            # Test field validation
            field_types = {field.type for field in config.fields}
            print(f"  ✓ Field types used: {', '.join(sorted(field_types))}")

            # Test required fields
            required_fields = [field.name for field in config.fields if field.required]
            if required_fields:
                print(f"  ✓ Required fields: {', '.join(required_fields)}")

        except Exception as e:
            assert False, f"✗ Error loading {filename}: {e}"

    print("\n" + "=" * 50)
    assert True, "All configuration tests passed!"


def test_programmatic_config() -> None:
    """Test creating configuration programmatically."""
    print("\nTesting Programmatic Configuration...")
    print("-" * 40)

    config_dict = {
        "window": {
            "title": "Test Form",
            "width": 400,
            "height": 300
        },
        "layout": "form",
        "fields": [
            {
                "name": "test_field",
                "type": "text",
                "label": "Test Field",
                "required": True
            },
            {
                "name": "test_number",
                "type": "number",
                "label": "Test Number",
                "min_value": 0,
                "max_value": 100
            }
        ],
        "submit_button": True
    }

    try:
        loader = ConfigLoader()
        config = loader.load_from_dict(config_dict)

        print("  ✓ Programmatic configuration loaded successfully")
        print(f"  ✓ Fields created: {[f.name for f in config.fields]}")
        assert True, "Successfully created programmatic configuration"

    except Exception as e:
        assert False, f"  ✗ Error: {e}"


def test_config_validation() -> None:
    """Test configuration validation."""
    print("\nTesting Configuration Validation...")
    print("-" * 40)

    loader = ConfigLoader()

    # Test invalid configurations that should fail
    invalid_configs = [
        # Missing fields
        {"window": {"title": "Test"}},

        # Invalid field type
        {"fields": [{"name": "test", "type": "invalid", "label": "Test"}]},

        # Missing required field properties
        {"fields": [{"name": "test"}]},

        # Duplicate field names
        {"fields": [
            {"name": "test", "type": "text", "label": "Test 1"},
            {"name": "test", "type": "text", "label": "Test 2"}
        ]},

        # Invalid layout
        {"fields": [{"name": "test", "type": "text", "label": "Test"}], "layout": "invalid"}
    ]

    test_names = [
        "Missing fields",
        "Invalid field type",
        "Missing required properties",
        "Duplicate field names",
        "Invalid layout"
    ]

    for invalid_config, test_name in zip(invalid_configs, test_names):
        try:
            loader.load_from_dict(invalid_config)
            assert False, f"✗ {test_name}: Should have failed but didn't"
        except (ValueError, ConfigurationError):
            print(f"  ✓ {test_name}: Correctly rejected")
        except Exception as e:
            assert False, f"✗ {test_name}: Unexpected error: {e}"

    # Test configurations that should be valid
    valid_configs = [
        # Minimal valid field
        {"fields": [{"name": "test", "type": "text", "label": "Test"}]},
        # Multiple fields with different types
        {"fields": [
            {"name": "text_field", "type": "text", "label": "Text"},
            {"name": "number_field", "type": "number", "label": "Number"}
        ]}
    ]

    valid_test_names = [
        "Minimal valid field",
        "Multiple fields with different types"
    ]

    for valid_config, test_name in zip(valid_configs, valid_test_names):
        try:
            loader.load_from_dict(valid_config)
            print(f"  ✓ {test_name}: Correctly accepted")
        except Exception as e:
            assert False, f"✗ {test_name}: Should have passed but failed: {e}"

    print("\n  ✓ All validation tests passed")
