#!/usr/bin/env python3
"""
Test script for QtPyGuiHelper library configuration loading.
"""

import os
import sys
import json

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from qtpyguihelper.config_loader import ConfigLoader


def test_config_loading():
    """Test loading and validation of example configurations."""
    print("Testing QtPyGuiHelper Configuration Loading...")
    print("=" * 50)

    loader = ConfigLoader()
    examples_dir = os.path.join(os.path.dirname(__file__), "examples")

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
            print(f"  ✗ Error loading {filename}: {e}")
            return False

    print("\n" + "=" * 50)
    print("All configuration tests passed! ✓")
    return True


def test_programmatic_config():
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
        return True

    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False


def test_config_validation():
    """Test configuration validation."""
    print("\nTesting Configuration Validation...")
    print("-" * 40)

    loader = ConfigLoader()

    # Test invalid configurations
    invalid_configs = [
        # Missing fields
        {"window": {"title": "Test"}},

        # Empty fields array
        {"fields": []},

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
        "Empty fields array",
        "Invalid field type",
        "Missing required properties",
        "Duplicate field names",
        "Invalid layout"
    ]

    for i, (invalid_config, test_name) in enumerate(zip(invalid_configs, test_names)):
        try:
            config = loader.load_from_dict(invalid_config)
            print(f"  ✗ {test_name}: Should have failed but didn't")
            return False
        except ValueError:
            print(f"  ✓ {test_name}: Correctly rejected")
        except Exception as e:
            print(f"  ✗ {test_name}: Unexpected error: {e}")
            return False

    print("  ✓ All validation tests passed")
    return True


def main():
    """Run all tests."""
    print("QtPyGuiHelper Library Test Suite")
    print("=" * 50)

    tests = [
        test_config_loading,
        test_programmatic_config,
        test_config_validation
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"Test failed with exception: {e}")
            results.append(False)

    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)

    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"ALL TESTS PASSED! ({passed}/{total})")
        print("The QtPyGuiHelper library is ready to use.")
        return 0
    else:
        print(f"SOME TESTS FAILED! ({passed}/{total})")
        return 1


if __name__ == "__main__":
    sys.exit(main())
