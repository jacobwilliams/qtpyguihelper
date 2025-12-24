# vibegui Examples

This directory contains example files and demonstrations of the vibegui library.

## Demo Files

### Main Demo

**`demo.py`** - Comprehensive demo showcasing all library features:
- User registration, settings, and project forms
- Programmatic configuration creation
- Data persistence (save/load)
- Tabbed interfaces (simple and complex)
- Nested field names
- Float fields with custom formatting
- Custom buttons with callbacks
- Backend-specific demos (Qt, wxPython, and tkinter)
- Backend comparison (supports all three backends)
- Unified interface (auto-backend selection)

### Running the Demo

```bash
# Run interactive demo menu
python examples/demo.py

# Run specific demos directly
python examples/demo.py registration
python examples/demo.py float
python examples/demo.py custom_buttons
python examples/demo.py wxpython
python examples/demo.py tkinter
python examples/demo.py compare
python examples/demo.py unified
```

### Available Demo Types

- `registration` - User registration form (Qt)
- `settings` - Application settings form (Qt)
- `project` - Project data entry form (Qt)
- `contact` - Programmatic contact form (Qt)
- `persistence` - Data loading and saving demo (Qt)
- `tabs` - Tabbed interface demo (Qt)
- `complex_tabs` - Complex tabbed configuration demo (Qt)
- `nested` - Nested field names demo (Qt)
- `float` - Float fields demo (Qt)
- `format` - Format strings demo (Qt)
- `custom_buttons` - Custom buttons demo (Qt)
- `wxpython` - wxPython backend demo
- `tkinter` - tkinter backend demo
- `compare` - Compare all backends (Qt, wxPython, tkinter)
- `unified` - Unified interface (auto-backend)

### Simple Examples

**`simple_example.py`** - Basic getting-started example showing minimal vibegui usage. Perfect for beginners.

**`qt_backend_demo.py`** - Demonstrates how to set specific Qt backends (PySide6, PyQt6, PyQt5, PySide2) using qtpy environment variables. Educational for understanding Qt API compatibility.

## Configuration Files

The directory also contains example JSON configuration files used by the demos:

- `nested_config_output.json` - Example of nested field configuration
- `project_output.json` - Sample project form data
- `project_output_with_metadata.json` - Project data with metadata
- `tabbed_config_output.json` - Example tabbed interface configuration

## Quick Start

For a quick demonstration, run the root `demo.py` which provides simple access to key features:

```bash
python demo.py comprehensive  # Full featured demo
python demo.py quick-qt       # Simple Qt demo
python demo.py quick-wx       # Simple wxPython demo
python demo.py backend        # Backend comparison
```
