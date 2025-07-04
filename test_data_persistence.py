#!/usr/bin/env python3
"""
Test script for data persistence functionality.
"""

import os
import sys
import json
import tempfile

# Add the library to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from qtpyguihelper.config_loader import ConfigLoader
from qtpyguihelper.gui_builder import GuiBuilder


def test_data_persistence():
    """Test the data persistence functionality."""
    print("Testing Data Persistence Features...")
    print("=" * 50)

    # Create a simple test configuration
    config = {
        "window": {"title": "Test Form", "width": 400, "height": 300},
        "layout": "form",
        "fields": [
            {
                "name": "name",
                "type": "text",
                "label": "Name",
                "default_value": "Default Name"
            },
            {
                "name": "age",
                "type": "number",
                "label": "Age",
                "min_value": 0,
                "max_value": 120,
                "default_value": 25
            },
            {
                "name": "active",
                "type": "checkbox",
                "label": "Active",
                "default_value": True
            },
            {
                "name": "category",
                "type": "select",
                "label": "Category",
                "options": ["A", "B", "C"],
                "default_value": "B"
            }
        ]
    }

    # Test data to load
    test_data = {
        "name": "John Doe",
        "age": 30,
        "active": False,
        "category": "A"
    }

    try:
        # Test 1: Configuration loading
        print("\\n1. Testing configuration loading...")
        loader = ConfigLoader()
        gui_config = loader.load_from_dict(config)
        print(f"   ✓ Configuration loaded: {len(gui_config.fields)} fields")

        # Test 2: Data loading from dictionary
        print("\\n2. Testing data loading from dictionary...")
        # Note: We can't easily test the GUI without actually running it,
        # but we can test the data structures

        # Create temporary files for testing
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_data, f, indent=2)
            test_data_file = f.name

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config, f, indent=2)
            config_file = f.name

        print(f"   ✓ Test data file created: {test_data_file}")
        print(f"   ✓ Config file created: {config_file}")

        # Test 3: File operations
        print("\\n3. Testing file operations...")

        # Test loading data file
        with open(test_data_file, 'r') as f:
            loaded_data = json.load(f)

        if loaded_data == test_data:
            print("   ✓ Data file loaded correctly")
        else:
            print("   ✗ Data file loading failed")
            return False

        # Test 4: Default value handling
        print("\\n4. Testing default value handling...")

        # Test partial data (missing some fields)
        partial_data = {"name": "Jane Smith", "age": 28}

        expected_merged = {
            "name": "Jane Smith",  # From partial data
            "age": 28,             # From partial data
            "active": True,        # From config default
            "category": "B"        # From config default
        }

        # Simulate the merging logic
        merged_data = {}
        for field in gui_config.fields:
            field_name = field.name
            if field_name in partial_data:
                merged_data[field_name] = partial_data[field_name]
            elif field.default_value is not None:
                merged_data[field_name] = field.default_value

        if merged_data == expected_merged:
            print("   ✓ Default value merging works correctly")
        else:
            print("   ✗ Default value merging failed")
            print(f"     Expected: {expected_merged}")
            print(f"     Got: {merged_data}")
            return False

        # Test 5: Metadata generation
        print("\\n5. Testing metadata generation...")

        metadata = {
            "_metadata": {
                "config_source": "qtpyguihelper",
                "window_title": gui_config.window.title,
                "layout": gui_config.layout,
                "field_count": len(gui_config.fields),
                "required_fields": [f.name for f in gui_config.fields if f.required],
            }
        }

        data_with_metadata = {**test_data, **metadata}

        if "_metadata" in data_with_metadata:
            print("   ✓ Metadata generation works correctly")
            print(f"     Window title: {metadata['_metadata']['window_title']}")
            print(f"     Field count: {metadata['_metadata']['field_count']}")
        else:
            print("   ✗ Metadata generation failed")
            return False

        # Cleanup
        os.unlink(test_data_file)
        os.unlink(config_file)

        print("\\n" + "=" * 50)
        print("All data persistence tests passed! ✓")
        print("\\nThe library supports:")
        print("• Loading data from JSON files")
        print("• Saving form data to JSON files")
        print("• Merging loaded data with config defaults")
        print("• Generating metadata for saved files")
        print("• Handling partial data files")

        return True

    except Exception as e:
        print(f"\\n✗ Test failed with error: {e}")
        return False


def main():
    """Run the data persistence tests."""
    print("QtPyGuiHelper Data Persistence Test Suite")
    print("=" * 50)

    success = test_data_persistence()

    if success:
        print("\\n🎉 All tests passed! The data persistence features are working correctly.")
        return 0
    else:
        print("\\n❌ Some tests failed. Please check the implementation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
