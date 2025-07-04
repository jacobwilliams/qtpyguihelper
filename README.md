# QtPyGuiHelper

A Python library for creating PySide6 GUIs from JSON configuration files. This library allows you to define GUI layouts, widgets, and their properties in JSON format and automatically generate the corresponding PySide6 interface.

## Features

- 🎯 **JSON-Driven**: Define your entire GUI in JSON configuration files
- 🎨 **Multiple Layouts**: Support for vertical, horizontal, grid, and form layouts
- 🧩 **Rich Widget Set**: Text fields, numbers, dates, checkboxes, radio buttons, file pickers, color pickers, and more
- ✅ **Form Validation**: Built-in validation for required fields and data types
- 🎛️ **Customizable**: Extensive configuration options for each widget
- 📡 **Event Handling**: Built-in callbacks and signals for form submission and field changes
- 🔧 **Programmatic Control**: Runtime manipulation of form fields and values

## Installation

1. Clone or download this repository
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Create a JSON Configuration File

Create a JSON file defining your GUI structure:

```json
{
  "window": {
    "title": "My Application",
    "width": 500,
    "height": 400
  },
  "layout": "form",
  "fields": [
    {
      "name": "username",
      "type": "text",
      "label": "Username",
      "required": true,
      "placeholder": "Enter username"
    },
    {
      "name": "email",
      "type": "email",
      "label": "Email Address",
      "required": true
    },
    {
      "name": "age",
      "type": "number",
      "label": "Age",
      "min_value": 0,
      "max_value": 120
    },
    {
      "name": "subscribe",
      "type": "checkbox",
      "label": "Subscribe to newsletter"
    }
  ],
  "submit_button": true,
  "submit_label": "Submit",
  "cancel_button": true
}
```

### 2. Create the GUI Application

```python
import sys
from qtpyguihelper import GuiBuilder
from PySide6.QtWidgets import QApplication

def on_submit(form_data):
    print("Form submitted:", form_data)

# Create application
app = QApplication(sys.argv)

# Create GUI from JSON file
gui = GuiBuilder(config_path="my_form.json")

# Set submit callback
gui.set_submit_callback(on_submit)

# Show and run
gui.show()
app.exec()
```

## Supported Field Types

| Type | Description | Supported Properties |
|------|-------------|---------------------|
| `text` | Single-line text input | `placeholder`, `default_value` |
| `email` | Email input field | `placeholder`, `default_value` |
| `password` | Password input (masked) | `placeholder` |
| `number` | Numeric input | `min_value`, `max_value`, `default_value` |
| `textarea` | Multi-line text input | `placeholder`, `default_value`, `height` |
| `checkbox` | Checkbox input | `default_value` (boolean) |
| `radio` | Radio button group | `options` (array), `default_value` |
| `select` | Dropdown selection | `options` (array), `default_value` |
| `date` | Date picker | `default_value` (YYYY-MM-DD) |
| `time` | Time picker | `default_value` (HH:MM) |
| `datetime` | Date and time picker | `default_value` (ISO format) |
| `range` | Slider input | `min_value`, `max_value`, `default_value` |
| `file` | File selection button | `default_value` ("open"/"save") |
| `color` | Color picker button | `default_value` (hex color) |
| `url` | URL input field | `placeholder`, `default_value` |

## Layout Types

- **`vertical`**: Fields stacked vertically
- **`horizontal`**: Fields arranged horizontally
- **`grid`**: Fields in a 2-column grid (label, widget)
- **`form`**: Qt's form layout (automatic label-widget pairing)

## Configuration Reference

### Window Configuration

```json
{
  "window": {
    "title": "Window Title",
    "width": 800,
    "height": 600,
    "resizable": true,
    "icon": "path/to/icon.png"
  }
}
```

### Field Configuration

```jsonc
{
  "name": "field_name",           // Unique identifier (required)
  "type": "text",                 // Field type (required)
  "label": "Field Label",         // Display label (required)
  "required": false,              // Whether field is required
  "default_value": "default",     // Default value
  "placeholder": "Enter text...", // Placeholder text
  "tooltip": "Helpful tip",       // Tooltip text
  "width": 200,                   // Fixed width in pixels
  "height": 100,                  // Fixed height in pixels
  "min_value": 0,                 // Minimum value (numbers/ranges)
  "max_value": 100,               // Maximum value (numbers/ranges)
  "options": ["A", "B", "C"]      // Options for select/radio fields
}
```

### Form Configuration

```json
{
  "layout": "form",               // Layout type
  "submit_button": true,          // Show submit button
  "submit_label": "Submit",       // Submit button text
  "cancel_button": true,          // Show cancel button
  "cancel_label": "Cancel"        // Cancel button text
}
```

## Programming Interface

### Creating a GUI

```python
from qtpyguihelper import GuiBuilder

# From JSON file
gui = GuiBuilder(config_path="form.json")

# From dictionary
config = {"window": {...}, "fields": [...]}
gui = GuiBuilder(config_dict=config)
```

### Event Handling

```python
# Form submission
def on_submit(form_data):
    print("Submitted:", form_data)
gui.set_submit_callback(on_submit)

# Form cancellation
def on_cancel():
    print("Cancelled")
gui.set_cancel_callback(on_cancel)

# Field changes
def on_field_change(field_name, value):
    print(f"{field_name} changed to {value}")
gui.fieldChanged.connect(on_field_change)
```

### Runtime Control

```python
# Get/set form data
form_data = gui.get_form_data()
gui.set_form_data({"username": "john", "age": 25})

# Get/set individual fields
value = gui.get_field_value("username")
gui.set_field_value("username", "jane")

# Control field visibility/state
gui.show_field("username", False)  # Hide field
gui.enable_field("submit_btn", False)  # Disable field

# Clear all fields
gui.clear_form()
```

## Examples

The library includes several example configurations in the `examples/` directory:

- `user_registration.json` - Complete user registration form
- `settings_form.json` - Application settings with various widget types
- `project_form.json` - Project data entry form with grid layout

Run the demo script to see these examples in action:

```bash
python demo.py registration
python demo.py settings
python demo.py project
python demo.py contact
```

## Advanced Usage

### Custom Validation

```python
def custom_validator(form_data):
    if form_data['password'] != form_data['confirm_password']:
        raise ValueError("Passwords don't match")
    return True

gui.set_submit_callback(lambda data: custom_validator(data) and save_data(data))
```

### Dynamic Form Updates

```python
def on_country_change(field_name, value):
    if field_name == 'country' and value == 'USA':
        gui.show_field('state', True)
    else:
        gui.show_field('state', False)

gui.fieldChanged.connect(on_country_change)
```

### Integration with Data Models

```python
class User:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

def on_submit(form_data):
    user = User(**form_data)
    user.save()  # Save to database

gui.set_submit_callback(on_submit)
```

## Requirements

- Python 3.7+
- PySide6 6.5.0+

## License

This project is open source. Feel free to use and modify as needed.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure PySide6 is installed: `pip install PySide6`
2. **Configuration validation errors**: Check that all required fields in your JSON are present
3. **Widget not displaying**: Verify the field type is supported and properly configured

### Getting Help

- Check the example configurations in `examples/`
- Run the demo script to see working examples
- Review the configuration reference above
- Open an issue on the project repository
