"""
JSON Schema Validation Script for vibegui

This script validates all GUI configuration files in the examples directory
against the JSON schema (gui_config_schema.json). It ensures that all example
configuration files conform to the expected structure.

The script excludes *_data.json files as these are form data files, not
GUI configuration files.

Usage:
    python tests/test_schema.py

Requirements:
    jsonschema
"""

import json
import glob
from pathlib import Path
from jsonschema import validate, ValidationError

# Load schema
with open('vibegui/schema/gui_config_schema.json') as f:
    schema = json.load(f)

# Find all JSON files in examples directory, excluding data files
json_files = sorted(glob.glob('examples/*.json'))
json_files = [f for f in json_files if not Path(f).name.endswith('_data.json')]

print(f"Validating {len(json_files)} GUI configuration files...\n")

valid_count = 0
invalid_count = 0
errors = []

for json_file in json_files:
    filename = Path(json_file).name
    try:
        with open(json_file) as f:
            config = json.load(f)

        validate(instance=config, schema=schema)
        print(f"✅ {filename}")
        valid_count += 1
    except ValidationError as e:
        print(f"❌ {filename}")
        print(f"  Error: {e.message}")
        if e.json_path:
            print(f"  Path: {e.json_path}")
        invalid_count += 1
        errors.append((filename, e.message))
    except json.JSONDecodeError as e:
        print(f"✗ {filename}")
        print(f"  JSON Parse Error: {e}")
        invalid_count += 1
        errors.append((filename, f"JSON Parse Error: {e}"))

print(f"\n{'='*60}")
print(f"Results: {valid_count} valid, {invalid_count} invalid")
if errors:
    print(f"\nFailed files:")
    for filename, error in errors:
        print(f"  • {filename}: {error}")