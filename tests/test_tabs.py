#!/usr/bin/env python3
"""
Test script for tab functionality.
"""

import os
import sys
import json

# Add the library to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from vibegui.config_loader import ConfigLoader
from vibegui.exceptions import ConfigurationError


def test_tab_configuration() -> None:
    """Test loading and validation of tab configurations."""
    print("Testing Tab Configuration Features...")
    print("=" * 50)

    loader = ConfigLoader()

    # Test 1: Simple tab configuration
    print("\n1. Testing simple tab configuration...")

    simple_tab_config = {
        "window": {"title": "Simple Tabs", "width": 600, "height": 400},
        "use_tabs": True,
        "fields": [
            {"name": "field1", "type": "text", "label": "Field 1"},
            {"name": "field2", "type": "text", "label": "Field 2"},
            {"name": "field3", "type": "number", "label": "Field 3"}
        ],
        "tabs": [
            {
                "name": "tab1",
                "title": "Tab 1",
                "fields": ["field1", "field2"],
                "layout": "form"
            },
            {
                "name": "tab2",
                "title": "Tab 2",
                "fields": ["field3"],
                "layout": "vertical"
            }
        ]
    }

    try:
        config = loader.load_from_dict(simple_tab_config)
        print("   ✓ Simple tab configuration loaded successfully")
        print(f"   ✓ Use tabs: {config.use_tabs}")
        print(f"   ✓ Number of tabs: {len(config.tabs) if config.tabs else 0}")
        print(f"   ✓ Tab names: {[tab.name for tab in config.tabs] if config.tabs else []}")

        # Check tab field assignments
        if config.tabs:
            for tab in config.tabs:
                print(f"   ✓ Tab '{tab.name}' has {len(tab.fields)} fields: {[f.name for f in tab.fields]}")

    except Exception as e:
        print(f"   ✗ Error loading simple tab config: {e}")
        assert False, "Failed to load simple tab config"

    # Test 2: Load example tab files
    print("\n2. Testing example tab configuration files...")

    example_files = [
        "simple_tabs.json",
        "tabbed_config.json"
    ]

    for filename in example_files:
        # Look in the main examples directory
        file_path = os.path.join(os.path.dirname(__file__), "..", "examples", filename)
        if os.path.exists(file_path):
            try:
                config = loader.load_from_file(file_path)
                print(f"   ✓ {filename} loaded successfully")
                print(f"     - Use tabs: {config.use_tabs}")
                print(f"     - Number of tabs: {len(config.tabs) if config.tabs else 0}")
                if config.tabs:
                    for tab in config.tabs:
                        print(f"     - Tab '{tab.title}': {len(tab.fields)} fields, layout: {tab.layout}")
            except Exception as e:
                print(f"   ✗ Error loading {filename}: {e}")
                assert False, f"Failed to load {filename}"
        else:
            print(f"   ! {filename} not found, skipping")

    # Test 3: Tab validation
    print("\n3. Testing tab validation...")

    invalid_configs = [
        # Tab with invalid field reference
        {
            "fields": [{"name": "field1", "type": "text", "label": "Field 1"}],
            "tabs": [{"name": "tab1", "title": "Tab 1", "fields": ["nonexistent_field"]}]
        },

        # Missing required tab properties
        {
            "fields": [{"name": "field1", "type": "text", "label": "Field 1"}],
            "tabs": [{"name": "tab1"}]  # Missing title and fields
        },

        # Duplicate tab names
        {
            "fields": [{"name": "field1", "type": "text", "label": "Field 1"}],
            "tabs": [
                {"name": "tab1", "title": "Tab 1", "fields": ["field1"]},
                {"name": "tab1", "title": "Tab 1 Duplicate", "fields": ["field1"]}
            ]
        }
    ]

    test_names = [
        "Invalid field reference",
        "Missing required tab properties",
        "Duplicate tab names"
    ]

    for i, (invalid_config, test_name) in enumerate(zip(invalid_configs, test_names)):
        try:
            config = loader.load_from_dict(invalid_config)
            print(f"   ✗ {test_name}: Should have failed but didn't")
            assert False, f"Test {i+1} failed to raise expected exception"
        except (ValueError, ConfigurationError):
            print(f"   ✓ {test_name}: Correctly rejected")
        except Exception as e:
            print(f"   ✗ {test_name}: Unexpected error: {e}")
            assert False, f"Test {i+1} raised unexpected exception"

    # Test 4: Mixed tab and non-tab configuration
    print("\n4. Testing mixed configurations...")

    # Configuration without tabs (should work normally)
    no_tab_config = {
        "window": {"title": "No Tabs", "width": 400, "height": 300},
        "fields": [{"name": "field1", "type": "text", "label": "Field 1"}],
        "use_tabs": False
    }

    try:
        config = loader.load_from_dict(no_tab_config)
        print("   ✓ Non-tab configuration works correctly")
        print(f"   ✓ Use tabs: {config.use_tabs}")
        print(f"   ✓ Number of fields: {len(config.fields)}")
    except Exception as e:
        print(f"   ✗ Error with non-tab config: {e}")
        assert False, "Non-tab configuration failed"

    print("\n" + "=" * 50)
    print("All tab configuration tests passed! ✓")
    print("\nThe library now supports:")
    print("• Tab-based form organization")
    print("• Multiple layout types per tab")
    print("• Tab tooltips and enablement")
    print("• Mixed tab and non-tab configurations")
    print("• Comprehensive tab validation")

    assert True, "All tab configuration tests passed successfully"

