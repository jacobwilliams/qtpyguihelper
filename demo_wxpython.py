#!/usr/bin/env python3
"""
Demo script showing how to create a working wxPython GUI using qtpyguihelper.
This demonstrates that the library can create actual functional GUIs with wxPython backend.
"""

import sys
import os
import json
from pathlib import Path

# Add the qtpyguihelper module to the path
sys.path.insert(0, str(Path(__file__).parent))

from qtpyguihelper import GuiBuilder, set_backend
import wx


def on_submit_callback(form_data):
    """Callback function for form submission."""
    print("=== Form Submitted ===")
    for key, value in form_data.items():
        print(f"  {key}: {value}")
    
    # Show success message using wxPython
    wx.MessageBox(
        f"Form submitted successfully!\nName: {form_data.get('name', 'N/A')}\nEmail: {form_data.get('email', 'N/A')}", 
        "Success", 
        wx.OK | wx.ICON_INFORMATION
    )


def on_cancel_callback():
    """Callback function for form cancellation."""
    print("Form cancelled by user")
    
    # Show cancellation message
    result = wx.MessageBox(
        "Are you sure you want to exit?", 
        "Confirm Exit", 
        wx.YES_NO | wx.ICON_QUESTION
    )
    
    if result == wx.YES:
        # Close the application
        wx.GetApp().ExitMainLoop()


def validate_data_callback(form_data):
    """Custom button callback for data validation."""
    print("=== Validating Data ===")
    
    errors = []
    
    # Check required fields
    if not form_data.get('name', '').strip():
        errors.append("Name is required")
    
    if not form_data.get('email', '').strip():
        errors.append("Email is required")
    elif '@' not in form_data.get('email', ''):
        errors.append("Email must contain @ symbol")
    
    age = form_data.get('age', 0)
    if age <= 0:
        errors.append("Age must be greater than 0")
    elif age > 150:
        errors.append("Age seems unrealistic")
    
    # Show validation results
    if errors:
        error_msg = "Validation Errors:\n\n" + "\n".join(f"• {error}" for error in errors)
        wx.MessageBox(error_msg, "Validation Failed", wx.OK | wx.ICON_ERROR)
        print("Validation failed:", errors)
    else:
        wx.MessageBox("All data is valid!", "Validation Passed", wx.OK | wx.ICON_INFORMATION)
        print("Validation passed!")


def load_sample_data_callback(form_data):
    """Custom button callback to load sample data."""
    print("=== Loading Sample Data ===")
    
    # Get the GUI builder instance from the callback context
    # Note: In a real application, you'd store the reference to gui_builder
    # For this demo, we'll show how to access it
    app = wx.GetApp()
    if hasattr(app, 'gui_builder'):
        sample_data = {
            'name': 'Alice Johnson',
            'email': 'alice.johnson@example.com',
            'age': 28,
            'salary': 75000.50,
            'subscribe': True,
            'category': 'Professional',
            'priority': 'High',
            'birth_date': '1995-06-15',
            'notes': 'This is sample data loaded via wxPython custom button callback.'
        }
        
        app.gui_builder.set_form_data(sample_data)
        wx.MessageBox("Sample data loaded successfully!", "Data Loaded", wx.OK | wx.ICON_INFORMATION)
        print("Sample data loaded:", sample_data)
    else:
        wx.MessageBox("Could not access form to load data", "Error", wx.OK | wx.ICON_ERROR)


def clear_form_callback(form_data):
    """Custom button callback to clear the form."""
    print("=== Clearing Form ===")
    
    result = wx.MessageBox(
        "Are you sure you want to clear all form data?", 
        "Confirm Clear", 
        wx.YES_NO | wx.ICON_QUESTION
    )
    
    if result == wx.YES:
        app = wx.GetApp()
        if hasattr(app, 'gui_builder'):
            app.gui_builder.clear_form()
            wx.MessageBox("Form cleared successfully!", "Form Cleared", wx.OK | wx.ICON_INFORMATION)
            print("Form cleared")


def create_sample_config():
    """Create a comprehensive sample configuration for testing wxPython."""
    return {
        "window": {
            "title": "wxPython Demo - QtPyGuiHelper",
            "width": 650,
            "height": 600,
            "resizable": True
        },
        "layout": "form",
        "submit_button": True,
        "cancel_button": True,
        "submit_label": "Submit Form",
        "cancel_label": "Cancel",
        "fields": [
            {
                "name": "name",
                "type": "text",
                "label": "Full Name",
                "placeholder": "Enter your full name",
                "required": True
            },
            {
                "name": "email",
                "type": "email",
                "label": "Email Address",
                "placeholder": "your.email@example.com",
                "required": True
            },
            {
                "name": "age",
                "type": "int",
                "label": "Age",
                "min_value": 1,
                "max_value": 150,
                "default_value": 25
            },
            {
                "name": "salary",
                "type": "float",
                "label": "Annual Salary",
                "format_string": ",.2f",
                "min_value": 0.0,
                "max_value": 1000000.0,
                "default_value": 50000.0
            },
            {
                "name": "subscribe",
                "type": "checkbox",
                "label": "Subscribe to newsletter",
                "default_value": False
            },
            {
                "name": "category",
                "type": "select",
                "label": "Category",
                "options": ["Student", "Professional", "Retired", "Other"],
                "default_value": "Professional"
            },
            {
                "name": "priority",
                "type": "radio",
                "label": "Priority Level",
                "options": ["Low", "Medium", "High"],
                "default_value": "Medium"
            },
            {
                "name": "birth_date",
                "type": "date",
                "label": "Birth Date",
                "default_value": "1995-01-01"
            },
            {
                "name": "availability",
                "type": "range",
                "label": "Availability (%)",
                "min_value": 0,
                "max_value": 100,
                "default_value": 80
            },
            {
                "name": "notes",
                "type": "textarea",
                "label": "Additional Notes",
                "placeholder": "Enter any additional information...",
                "height": 100
            }
        ],
        "custom_buttons": [
            {
                "name": "validate",
                "label": "Validate Data",
                "tooltip": "Check if all form data is valid",
                "style": "background-color: #007bff; color: white;",
                "enabled": True
            },
            {
                "name": "load_sample",
                "label": "Load Sample",
                "tooltip": "Load sample data into the form",
                "style": "background-color: #28a745; color: white;",
                "enabled": True
            },
            {
                "name": "clear_all",
                "label": "Clear All",
                "tooltip": "Clear all form fields",
                "style": "background-color: #dc3545; color: white;",
                "enabled": True
            }
        ]
    }


def demo_wxpython_gui():
    """Create and run a complete wxPython GUI demo."""
    print("=== Starting wxPython GUI Demo ===")
    print("This demo shows a fully functional GUI created with wxPython backend")
    print()
    
    # Force wxPython backend
    try:
        set_backend('wx')
        print("✓ wxPython backend selected successfully")
    except Exception as e:
        print(f"❌ Failed to set wxPython backend: {e}")
        return
    
    # Create wxPython application
    app = wx.App()
    
    try:
        # Create the GUI configuration
        config = create_sample_config()
        
        # Create the GUI builder
        gui_builder = GuiBuilder(config_dict=config)
        print("✓ GUI builder created successfully")
        
        # Store reference in app for custom button callbacks
        app.gui_builder = gui_builder
        
        # Set up callbacks
        gui_builder.set_submit_callback(on_submit_callback)
        gui_builder.set_cancel_callback(on_cancel_callback)
        
        # Set up custom button callbacks
        gui_builder.set_custom_button_callback("validate", validate_data_callback)
        gui_builder.set_custom_button_callback("load_sample", load_sample_data_callback)
        gui_builder.set_custom_button_callback("clear_all", clear_form_callback)
        
        print("✓ All callbacks registered successfully")
        
        # Show the GUI window
        gui_builder.show()
        print("✓ GUI window shown")
        
        print()
        print("=== GUI Demo Features ===")
        print("• Text input fields with validation")
        print("• Integer and float number inputs")
        print("• Checkbox and radio button groups")
        print("• Date picker and range slider")
        print("• Dropdown selection")
        print("• Multi-line text area")
        print("• Custom buttons with callbacks")
        print("• Form validation and data handling")
        print()
        print("Try the custom buttons:")
        print("• 'Validate Data' - Check form validation")
        print("• 'Load Sample' - Load demo data")
        print("• 'Clear All' - Clear all fields")
        print("• 'Submit Form' - Submit the form")
        print("• 'Cancel' - Close the application")
        print()
        print("Close the window or click Cancel to exit...")
        
        # Run the wxPython event loop
        app.MainLoop()
        
        print("=== Demo completed successfully! ===")
        
    except Exception as e:
        print(f"❌ Error during GUI demo: {e}")
        import traceback
        traceback.print_exc()


def demo_file_based_config():
    """Demo loading configuration from a JSON file."""
    print("\n=== File-Based Configuration Demo ===")
    
    # Create a sample config file
    config_file = "demo_wx_config.json"
    config = create_sample_config()
    config["window"]["title"] = "wxPython Demo - From JSON File"
    
    try:
        # Save config to file
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        print(f"✓ Created config file: {config_file}")
        
        # Force wxPython backend
        set_backend('wx')
        
        # Create wxPython app
        app = wx.App()
        
        # Load GUI from file
        gui_builder = GuiBuilder(config_path=config_file)
        app.gui_builder = gui_builder
        
        # Set up callbacks (simplified)
        gui_builder.set_submit_callback(lambda data: print("File-based config submitted:", data))
        gui_builder.set_cancel_callback(lambda: app.ExitMainLoop())
        
        print("✓ Loaded GUI from JSON file")
        
        # Show and run
        gui_builder.show()
        app.MainLoop()
        
        # Clean up
        os.remove(config_file)
        print(f"✓ Cleaned up config file: {config_file}")
        
    except Exception as e:
        print(f"❌ Error in file-based demo: {e}")
        # Clean up on error
        if os.path.exists(config_file):
            os.remove(config_file)


def main():
    """Main demo function."""
    print("QtPyGuiHelper - wxPython Backend Demo")
    print("=====================================")
    print()
    
    # Check if wxPython is available
    try:
        import wx
        print("✓ wxPython is available")
    except ImportError:
        print("❌ wxPython is not installed. Please install it with:")
        print("   pip install wxPython")
        return
    
    # Check command line arguments
    if len(sys.argv) > 1:
        demo_type = sys.argv[1].lower()
        
        if demo_type == "dict":
            demo_wxpython_gui()
        elif demo_type == "file":
            demo_file_based_config()
        else:
            print(f"Unknown demo type: {demo_type}")
            print("Valid options: dict, file")
    else:
        print("Usage:")
        print("  python demo_wxpython.py dict    # Demo with dictionary config")
        print("  python demo_wxpython.py file    # Demo with JSON file config")
        print()
        print("Running default demo (dictionary config)...")
        print()
        demo_wxpython_gui()


if __name__ == "__main__":
    main()
