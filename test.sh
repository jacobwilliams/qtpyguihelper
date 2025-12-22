#!/bin/bash

#
# Run all the tests.
#

# Exit immediately if any command fails
set -e
# Optionally show commands as they execute
# set -x

# validate JSON schema
python tests/test_schema.py

python -m pytest tests/test_backend_comprehensive.py -v
python -m pytest tests/test_backend_integration.py -v
python -m pytest tests/test_comprehensive.py -v
python -m pytest tests/test_config.py -v
python -m pytest tests/test_custom_buttons.py -v
python -m pytest tests/test_data_persistence.py -v
python -m pytest tests/test_float_fields.py -v
python -m pytest tests/test_format_strings.py -v
python -m pytest tests/test_int_vs_float.py -v
python -m pytest tests/test_nested_fields.py -v
python -m pytest tests/test_qt_backend.py -v
python -m pytest tests/test_qt_compatibility.py -v
python -m pytest tests/test_qt_tabs.py -v
python -m pytest tests/test_tab_field_expansion.py -v
python -m pytest tests/test_tabs.py -v
# python -m pytest tests/test_tkinter_backend.py -v  # Temporarily disabled - requires display
python -m pytest tests/test_wx_backend.py -v
python -m pytest tests/test_wx_tabs_simple.py -v
python -m pytest tests/test_wx_tabs_working.py -v
python -m pytest tests/test_wx_tabs.py -v
python -m pytest tests/test_wxpython_backend.py -v
python -m pytest tests/test_wxpython_integration.py -v
python -m pytest tests/test_wxpython_tabs.py -v
python -m pytest tests/test_tkinter_gui.py -v
python -m pytest tests/test_tk_simple.py -v
python -m pytest tests/test_gtk_versions.py -v