#!/usr/bin/env python3
"""
wxPython demo with custom buttons - showing all features work with wxPython backend.
"""

import sys
import os
import json

# Suppress common wxPython warnings
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="wx")

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

try:
    import wx
    if hasattr(wx, 'Log'):
        wx.Log.SetLogLevel(wx.LOG_Warning)  # type: ignore
except ImportError:
    print("wxPython is not installed. Please install it with: pip install wxpython")
    sys.exit(1)

from qtpyguihelper import GuiBuilder, set_backend


def on_form_submit(form_data):
    """Handle main form submission."""
    print("\n=== Form Submitted ===")
    for key, value in form_data.items():
        print(f"{key}: {value}")
    print("=====================\n")


def on_form_cancel():
    """Handle form cancellation."""
    print("Form cancelled by user")


def validate_form(form_data):
    """Custom button: Validate the form data."""
    print("\n=== Validating Form ===")
    
    errors = []
    
    # Check required fields
    if not form_data.get('name', '').strip():
        errors.append("Name is required")
    
    if not form_data.get('email', '').strip():
        errors.append("Email is required")
    elif '@' not in form_data.get('email', ''):
        errors.append("Email must contain @")
    
    if form_data.get('age', 0) < 18:
        errors.append("Age must be 18 or older")
    
    if errors:
        print("❌ Validation failed:")
        for error in errors:
            print(f"  - {error}")
        
        # Show error dialog
        try:
            wx_local = wx  # Work around linting
            wx_local.MessageBox("\n".join(errors), "Validation Errors", 
                               wx_local.OK | wx_local.ICON_ERROR)  # type: ignore
        except (AttributeError, RuntimeError):
            pass
    else:
        print("✓ Validation passed!")
        try:
            wx_local = wx
            wx_local.MessageBox("All form data is valid!", "Validation Success", 
                               wx_local.OK | wx_local.ICON_INFORMATION)  # type: ignore
        except (AttributeError, RuntimeError):
            pass


def clear_form_data(_form_data):
    """Custom button: Clear all form fields."""
    print("Clearing form...")
    # The GUI builder will handle the actual clearing
    gui_builder.clear_form()
    print("✓ Form cleared")


def load_sample_data(_form_data):
    """Custom button: Load sample data into the form."""
    print("Loading sample data...")
    
    sample_data = {
        "name": "Alice Johnson",
        "age": 28,
        "email": "alice.johnson@example.com",
        "department": "Engineering",
        "salary": 75000.50,
        "start_date": "2020-03-15",
        "full_time": True,
        "experience": "Senior",
        "notes": "Experienced software engineer with expertise in Python and web development."
    }
    
    gui_builder.set_form_data(sample_data)
    print("✓ Sample data loaded")


def export_form_data(form_data):
    """Custom button: Export form data to JSON file."""
    print("Exporting form data...")
    
    try:
        filename = "exported_form_data.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(form_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Form data exported to {filename}")
        
        try:
            wx_local = wx
            wx_local.MessageBox(f"Form data exported successfully to:\n{filename}", 
                               "Export Complete", wx_local.OK | wx_local.ICON_INFORMATION)  # type: ignore
        except (AttributeError, RuntimeError):
            pass
            
    except IOError as e:
        print(f"❌ Export failed: {e}")


def create_advanced_config():
    """Create an advanced form configuration with custom buttons."""
    return {
        "window": {
            "title": "wxPython Advanced Demo - Employee Form",
            "width": 600,
            "height": 550,
            "resizable": True
        },
        "layout": "form",
        "submit_button": True,
        "cancel_button": True,
        "submit_label": "Save Employee",
        "cancel_label": "Cancel",
        "fields": [
            {
                "name": "name",
                "type": "text",
                "label": "Full Name",
                "placeholder": "Enter employee name",
                "required": True
            },
            {
                "name": "age",
                "type": "int",
                "label": "Age",
                "min_value": 16,
                "max_value": 70,
                "default_value": 25
            },
            {
                "name": "email",
                "type": "email",
                "label": "Email Address",
                "placeholder": "employee@company.com",
                "required": True
            },
            {
                "name": "department",
                "type": "select",
                "label": "Department",
                "options": ["Engineering", "Marketing", "Sales", "HR", "Finance"],
                "default_value": "Engineering"
            },
            {
                "name": "salary",
                "type": "float",
                "label": "Annual Salary",
                "format_string": ",.2f",
                "min_value": 20000.0,
                "max_value": 200000.0,
                "default_value": 50000.0
            },
            {
                "name": "start_date",
                "type": "date",
                "label": "Start Date",
                "default_value": "2024-01-01"
            },
            {
                "name": "full_time",
                "type": "checkbox",
                "label": "Full-time employee",
                "default_value": True
            },
            {
                "name": "experience",
                "type": "radio",
                "label": "Experience Level",
                "options": ["Junior", "Mid-level", "Senior", "Lead"],
                "default_value": "Mid-level"
            },
            {
                "name": "notes",
                "type": "textarea",
                "label": "Additional Notes",
                "placeholder": "Enter any additional information about the employee...",
                "height": 80
            }
        ],
        "custom_buttons": [
            {
                "name": "validate",
                "label": "Validate Form",
                "tooltip": "Check if all form data is valid",
                "style": "background-color: #007bff; color: white;",
                "enabled": True
            },
            {
                "name": "clear",
                "label": "Clear All",
                "tooltip": "Clear all form fields",
                "style": "background-color: #6c757d; color: white;",
                "enabled": True
            },
            {
                "name": "load_sample",
                "label": "Load Sample",
                "tooltip": "Load sample employee data",
                "style": "background-color: #28a745; color: white;",
                "enabled": True
            },
            {
                "name": "export",
                "label": "Export JSON",
                "tooltip": "Export form data to JSON file",
                "style": "background-color: #fd7e14; color: white;",
                "enabled": True
            }
        ]
    }


def main():
    """Main function to run the advanced wxPython demo."""
    global gui_builder
    
    print("QtPyGuiHelper Advanced wxPython Demo")
    print("====================================")
    
    try:
        # Force wxPython backend
        set_backend('wx')
        print("✓ wxPython backend selected")
        
        # Create the advanced GUI configuration
        config = create_advanced_config()
        
        # Create the GUI builder
        gui_builder = GuiBuilder(config_dict=config)
        print("✓ GUI builder created")
        
        # Set main callbacks
        gui_builder.set_submit_callback(on_form_submit)
        gui_builder.set_cancel_callback(on_form_cancel)
        
        # Set custom button callbacks
        gui_builder.set_custom_button_callback("validate", validate_form)
        gui_builder.set_custom_button_callback("clear", clear_form_data)
        gui_builder.set_custom_button_callback("load_sample", load_sample_data)
        gui_builder.set_custom_button_callback("export", export_form_data)
        
        print("✓ All callbacks set")
        
        # Show available custom buttons
        button_names = gui_builder.get_custom_button_names()
        print(f"✓ Custom buttons available: {', '.join(button_names)}")
        
        # Show the window
        print("✓ Showing window...")
        gui_builder.show()
        
        # Start the wxPython event loop
        print("✓ Starting wxPython application...")
        
        app = wx.GetApp()  # type: ignore
        if not app:
            app = wx.App()  # type: ignore
        
        print("\n=== Advanced GUI Demo is now running ===")
        print("Try the following features:")
        print("1. Fill out the form fields")
        print("2. Click 'Validate Form' to check data")
        print("3. Click 'Load Sample' to load test data")
        print("4. Click 'Clear All' to clear the form")
        print("5. Click 'Export JSON' to save data")
        print("6. Click 'Save Employee' to submit")
        print("==========================================")
        
        app.MainLoop()  # type: ignore
        
    except (ImportError, RuntimeError, AttributeError) as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("\n✓ Advanced demo completed successfully!")
    return 0


if __name__ == "__main__":
    # Global variable for GUI builder (needed for custom button callbacks)
    gui_builder = None
    sys.exit(main())
