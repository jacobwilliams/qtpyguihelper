#!/usr/bin/env python3
"""
Demo script showing backend selection between Qt and wxPython.
"""

import sys
import os

# Add the library to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from qtpyguihelper import (
    GuiBuilder, get_available_backends, get_backend_info, 
    set_backend, BackendError
)


def on_form_submit(form_data):
    """Callback function for form submission."""
    print("Form submitted with data:")
    for key, value in form_data.items():
        print(f"  {key}: {value}")


def on_form_cancel():
    """Callback function for form cancellation."""
    print("Form cancelled by user")


def demo_backend_detection():
    """Demo automatic backend detection."""
    print("=== Backend Detection Demo ===")
    print(f"Available backends: {get_available_backends()}")
    
    backend_info = get_backend_info()
    print(f"Current backend: {backend_info['backend']}")
    
    if backend_info['backend'] == 'qt':
        print(f"Qt API: {backend_info.get('qt_api', 'Unknown')}")
        print(f"Qt Version: {backend_info.get('qt_version', 'Unknown')}")
    elif backend_info['backend'] == 'wx':
        print(f"wxPython Version: {backend_info.get('wx_version', 'Unknown')}")
        print(f"wxPython Platform: {backend_info.get('wx_platform', 'Unknown')}")
    
    print()


def create_sample_config():
    """Create a sample configuration to test both backends."""
    return {
        "window": {
            "title": "Backend Demo - Cross-Platform GUI",
            "width": 600,
            "height": 500,
            "resizable": True
        },
        "layout": "form",
        "submit_button": True,
        "cancel_button": True,
        "submit_label": "Submit Data",
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
                "name": "age",
                "type": "int",
                "label": "Age",
                "min_value": 0,
                "max_value": 120,
                "default_value": 25
            },
            {
                "name": "height",
                "type": "float",
                "label": "Height (m)",
                "format_string": ".2f",
                "min_value": 0.5,
                "max_value": 3.0,
                "default_value": 1.75
            },
            {
                "name": "email",
                "type": "email",
                "label": "Email Address",
                "placeholder": "your.email@example.com",
                "required": True
            },
            {
                "name": "subscribe",
                "type": "checkbox",
                "label": "Subscribe to newsletter",
                "default_value": True
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
                "default_value": "1990-01-01"
            },
            {
                "name": "notes",
                "type": "textarea",
                "label": "Additional Notes",
                "placeholder": "Enter any additional information...",
                "height": 80
            }
        ],
        "custom_buttons": [
            {
                "name": "clear_form",
                "label": "Clear Form",
                "tooltip": "Clear all form fields",
                "style": "background-color: #f0f0f0; color: #333;",
                "enabled": True
            },
            {
                "name": "load_demo",
                "label": "Load Demo Data",
                "tooltip": "Load sample data into the form",
                "style": "background-color: #007acc; color: white;",
                "enabled": True
            }
        ]
    }


def demo_qt_backend():
    """Demo the Qt backend specifically."""
    print("=== Qt Backend Demo ===")
    
    try:
        # Force Qt backend
        set_backend('qt')
        print("Qt backend selected successfully")
        
        # Create configuration
        config = create_sample_config()
        config["window"]["title"] += " (Qt Backend)"
        
        # Create and run GUI
        gui_builder = GuiBuilder(config_dict=config)
        gui_builder.set_submit_callback(on_form_submit)
        gui_builder.set_cancel_callback(on_form_cancel)
        
        # Set up custom button callbacks
        def clear_form(_form_data):
            gui_builder.clear_form()
            print("Form cleared")
        
        def load_demo_data(_form_data):
            demo_data = {
                "name": "John Doe",
                "age": 30,
                "height": 1.80,
                "email": "john.doe@example.com",
                "subscribe": True,
                "category": "Professional",
                "priority": "High",
                "birth_date": "1993-05-15",
                "notes": "This is demo data loaded via custom button."
            }
            gui_builder.set_form_data(demo_data)
            print("Demo data loaded")
        
        gui_builder.set_custom_button_callback("clear_form", clear_form)
        gui_builder.set_custom_button_callback("load_demo", load_demo_data)
        
        # Show the window
        gui_builder.show()
        
        # For Qt, we need to run the application event loop
        try:
            from qtpy.QtWidgets import QApplication
        except ImportError:
            from qtpy.QtGui import QApplication
            
        if not QApplication.instance():
            app = QApplication(sys.argv)
            sys.exit(app.exec())
        
    except BackendError as e:
        print(f"Qt backend not available: {e}")
    except ImportError as e:
        print(f"Qt import error: {e}")
    except RuntimeError as e:
        print(f"Qt runtime error: {e}")


def demo_wx_backend():
    """Demo the wxPython backend specifically."""
    print("=== wxPython Backend Demo ===")
    
    try:
        # Force wxPython backend
        set_backend('wx')
        print("wxPython backend selected successfully")
        
        # Create configuration
        config = create_sample_config()
        config["window"]["title"] += " (wxPython Backend)"
        
        # Create and run GUI
        gui_builder = GuiBuilder(config_dict=config)
        gui_builder.set_submit_callback(on_form_submit)
        gui_builder.set_cancel_callback(on_form_cancel)
        
        # Set up custom button callbacks
        def clear_form(_form_data):
            gui_builder.clear_form()
            print("Form cleared")
        
        def load_demo_data(_form_data):
            demo_data = {
                "name": "Jane Smith",
                "age": 28,
                "height": 1.65,
                "email": "jane.smith@example.com",
                "subscribe": False,
                "category": "Student",
                "priority": "Medium",
                "birth_date": "1995-03-20",
                "notes": "Demo data for wxPython backend testing."
            }
            gui_builder.set_form_data(demo_data)
            print("Demo data loaded")
        
        gui_builder.set_custom_button_callback("clear_form", clear_form)
        gui_builder.set_custom_button_callback("load_demo", load_demo_data)
        
        # Show the window
        gui_builder.show()
        
        # For wxPython, we need to run the application main loop
        import wx
        if not wx.App.Get():
            app = wx.App()
            app.MainLoop()
        
    except BackendError as e:
        print(f"wxPython backend not available: {e}")
    except ImportError as e:
        print(f"wxPython import error: {e}")
    except RuntimeError as e:
        print(f"wxPython runtime error: {e}")


def demo_auto_backend():
    """Demo automatic backend selection."""
    print("=== Auto Backend Selection Demo ===")
    
    # Create configuration
    config = create_sample_config()
    config["window"]["title"] += " (Auto-Selected Backend)"
    
    # Let the system auto-select backend
    gui_builder = GuiBuilder(config_dict=config)
    print(f"Auto-selected backend: {gui_builder.backend}")
    
    gui_builder.set_submit_callback(on_form_submit)
    gui_builder.set_cancel_callback(on_form_cancel)
    
    # Set up custom button callbacks
    def clear_form(_form_data):
        gui_builder.clear_form()
        print("Form cleared")
    
    def load_demo_data(_form_data):
        demo_data = {
            "name": "Alex Johnson",
            "age": 35,
            "height": 1.75,
            "email": "alex.johnson@example.com",
            "subscribe": True,
            "category": "Professional",
            "priority": "Low",
            "birth_date": "1988-11-10",
            "notes": "Auto-backend selection demo data."
        }
        gui_builder.set_form_data(demo_data)
        print("Demo data loaded")
    
    gui_builder.set_custom_button_callback("clear_form", clear_form)
    gui_builder.set_custom_button_callback("load_demo", load_demo_data)
    
    # Use the unified create_and_run method
    return GuiBuilder.create_and_run(config_dict=config)


def main():
    """Main demo function."""
    print("QtPyGuiHelper Backend Selection Demo")
    print("====================================")
    
    # Show backend detection info
    demo_backend_detection()
    
    # Check command line arguments for specific demo
    if len(sys.argv) > 1:
        backend_choice = sys.argv[1].lower()
        
        if backend_choice == 'qt':
            demo_qt_backend()
        elif backend_choice == 'wx':
            demo_wx_backend()
        elif backend_choice == 'auto':
            demo_auto_backend()
        else:
            print(f"Unknown backend choice: {backend_choice}")
            print("Valid options: qt, wx, auto")
    else:
        print("Usage:")
        print("  python demo_backend_selection.py qt     # Force Qt backend")
        print("  python demo_backend_selection.py wx     # Force wxPython backend")
        print("  python demo_backend_selection.py auto   # Auto-select backend")
        print()
        
        # Default to auto-selection
        print("No backend specified, using auto-selection...")
        demo_auto_backend()


if __name__ == "__main__":
    main()
