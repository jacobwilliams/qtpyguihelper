Examples
========

This section provides comprehensive examples showing how to use QtPyGuiHelper in different scenarios.

Basic Examples
--------------

Simple Form
~~~~~~~~~~~

Here's a simple contact form example:

.. code-block:: python

   from qtpyguihelper import create_gui

   config = {
       "window": {
           "title": "Contact Form",
           "width": 400,
           "height": 350
       },
       "fields": [
           {
               "name": "name",
               "label": "Full Name",
               "type": "text",
               "required": True,
               "placeholder": "Enter your full name"
           },
           {
               "name": "email",
               "label": "Email",
               "type": "email",
               "required": True,
               "placeholder": "your.email@example.com"
           },
           {
               "name": "phone",
               "label": "Phone Number",
               "type": "text",
               "placeholder": "+1 (555) 123-4567"
           },
           {
               "name": "message",
               "label": "Message",
               "type": "textarea",
               "required": True,
               "placeholder": "Enter your message here..."
           }
       ],
       "submit_button": True,
       "submit_label": "Send Message",
       "cancel_button": True
   }

   def handle_submit(data):
       print("Contact form submitted:")
       for key, value in data.items():
           print(f"  {key}: {value}")

   gui = create_gui(config)
   gui.set_submit_callback(handle_submit)
   gui.run()

Advanced Form with Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from qtpyguihelper import create_gui

   config = {
       "window": {
           "title": "User Registration",
           "width": 500,
           "height": 600
       },
       "fields": [
           {
               "name": "username",
               "label": "Username",
               "type": "text",
               "required": True,
               "placeholder": "Choose a username",
               "tooltip": "Username must be unique"
           },
           {
               "name": "password",
               "label": "Password",
               "type": "password",
               "required": True,
               "tooltip": "Password must be at least 8 characters"
           },
           {
               "name": "confirm_password",
               "label": "Confirm Password",
               "type": "password",
               "required": True
           },
           {
               "name": "email",
               "label": "Email Address",
               "type": "email",
               "required": True
           },
           {
               "name": "age",
               "label": "Age",
               "type": "number",
               "min": 13,
               "max": 120,
               "required": True
           },
           {
               "name": "country",
               "label": "Country",
               "type": "dropdown",
               "options": ["USA", "Canada", "UK", "Australia", "Germany", "France"],
               "required": True
           },
           {
               "name": "birthdate",
               "label": "Birth Date",
               "type": "date",
               "required": True
           },
           {
               "name": "terms",
               "label": "I agree to the terms and conditions",
               "type": "checkbox",
               "required": True
           }
       ],
       "submit_button": True,
       "submit_label": "Register",
       "cancel_button": True
   }

   def validate_registration(data):
       # Custom validation
       if data.get('password') != data.get('confirm_password'):
           print("Error: Passwords do not match")
           return False
       
       if len(data.get('password', '')) < 8:
           print("Error: Password must be at least 8 characters")
           return False
           
       return True

   def handle_registration(data):
       if validate_registration(data):
           print("Registration successful!")
           print(f"Welcome, {data['username']}!")
       else:
           print("Registration failed. Please check your inputs.")

   gui = create_gui(config)
   gui.set_submit_callback(handle_registration)
   gui.run()

Tabbed Interface Example
------------------------

.. code-block:: python

   from qtpyguihelper import create_gui

   config = {
       "window": {
           "title": "Employee Management",
           "width": 600,
           "height": 500
       },
       "use_tabs": True,
       "tabs": [
           {
               "title": "Personal Information",
               "fields": [
                   {"name": "first_name", "label": "First Name", "type": "text", "required": True},
                   {"name": "last_name", "label": "Last Name", "type": "text", "required": True},
                   {"name": "employee_id", "label": "Employee ID", "type": "text", "required": True},
                   {"name": "department", "label": "Department", "type": "dropdown", 
                    "options": ["Engineering", "Sales", "Marketing", "HR", "Finance"]},
                   {"name": "hire_date", "label": "Hire Date", "type": "date", "required": True}
               ]
           },
           {
               "title": "Contact Details",
               "fields": [
                   {"name": "email", "label": "Work Email", "type": "email", "required": True},
                   {"name": "phone", "label": "Phone Number", "type": "text"},
                   {"name": "emergency_contact", "label": "Emergency Contact", "type": "text"},
                   {"name": "address", "label": "Address", "type": "textarea"}
               ]
           },
           {
               "title": "Job Details",
               "fields": [
                   {"name": "position", "label": "Position", "type": "text", "required": True},
                   {"name": "salary", "label": "Salary", "type": "number", "min": 0},
                   {"name": "full_time", "label": "Full-time Employee", "type": "checkbox", "default": True},
                   {"name": "start_time", "label": "Start Time", "type": "time"},
                   {"name": "benefits", "label": "Benefits Package", "type": "dropdown",
                    "options": ["Basic", "Standard", "Premium"]}
               ]
           }
       ],
       "submit_button": True,
       "submit_label": "Save Employee",
       "cancel_button": True
   }

   gui = create_gui(config)
   gui.run()

Custom Buttons Example
----------------------

.. code-block:: python

   from qtpyguihelper import create_gui

   config = {
       "window": {"title": "Data Entry Form", "width": 500, "height": 400},
       "fields": [
           {"name": "name", "label": "Name", "type": "text"},
           {"name": "email", "label": "Email", "type": "email"},
           {"name": "notes", "label": "Notes", "type": "textarea"}
       ],
       "custom_buttons": [
           {
               "name": "clear_form",
               "label": "Clear All",
               "style": {"background": "#ff6b6b", "foreground": "white"}
           },
           {
               "name": "load_template",
               "label": "Load Template",
               "style": {"background": "#4ecdc4", "foreground": "white"}
           },
           {
               "name": "save_draft",
               "label": "Save Draft",
               "style": {"background": "#45b7d1", "foreground": "white"}
           }
       ],
       "submit_button": True,
       "cancel_button": True
   }

   def clear_form(button_config, form_data):
       gui.clear_form()
       print("Form cleared!")

   def load_template(button_config, form_data):
       template_data = {
           "name": "John Template",
           "email": "template@example.com",
           "notes": "This is a template entry."
       }
       gui.set_form_data(template_data)
       print("Template loaded!")

   def save_draft(button_config, form_data):
       gui.save_data_to_file("draft.json")
       print("Draft saved!")

   gui = create_gui(config)
   gui.set_custom_button_callback('clear_form', clear_form)
   gui.set_custom_button_callback('load_template', load_template)
   gui.set_custom_button_callback('save_draft', save_draft)
   gui.run()

Data Persistence Example
------------------------

.. code-block:: python

   from qtpyguihelper import create_gui
   import os

   config = {
       "window": {"title": "Settings Manager", "width": 450, "height": 350},
       "fields": [
           {"name": "theme", "label": "Theme", "type": "dropdown", 
            "options": ["Light", "Dark", "Auto"], "default": "Auto"},
           {"name": "language", "label": "Language", "type": "dropdown",
            "options": ["English", "Spanish", "French", "German"]},
           {"name": "auto_save", "label": "Auto-save", "type": "checkbox", "default": True},
           {"name": "backup_interval", "label": "Backup Interval (hours)", "type": "number", 
            "min": 1, "max": 24, "default": 6}
       ],
       "custom_buttons": [
           {"name": "load_settings", "label": "Load Settings"},
           {"name": "save_settings", "label": "Save Settings"},
           {"name": "reset_defaults", "label": "Reset to Defaults"}
       ]
   }

   settings_file = "user_settings.json"

   def load_settings(button_config, form_data):
       if os.path.exists(settings_file):
           if gui.load_data_from_file(settings_file):
               print("Settings loaded successfully!")
           else:
               print("Failed to load settings.")
       else:
           print("No saved settings found.")

   def save_settings(button_config, form_data):
       if gui.save_data_to_file(settings_file):
           print("Settings saved successfully!")
       else:
           print("Failed to save settings.")

   def reset_defaults(button_config, form_data):
       defaults = {
           "theme": "Auto",
           "language": "English", 
           "auto_save": True,
           "backup_interval": 6
       }
       gui.set_form_data(defaults)
       print("Settings reset to defaults!")

   gui = create_gui(config)
   gui.set_custom_button_callback('load_settings', load_settings)
   gui.set_custom_button_callback('save_settings', save_settings)
   gui.set_custom_button_callback('reset_defaults', reset_defaults)

   # Auto-load settings on startup
   if os.path.exists(settings_file):
       gui.load_data_from_file(settings_file)

   gui.run()

Field Change Callbacks
----------------------

.. code-block:: python

   from qtpyguihelper import create_gui

   config = {
       "window": {"title": "Dynamic Form", "width": 400, "height": 300},
       "fields": [
           {"name": "user_type", "label": "User Type", "type": "dropdown",
            "options": ["Student", "Teacher", "Administrator"], "required": True},
           {"name": "student_id", "label": "Student ID", "type": "text"},
           {"name": "grade_level", "label": "Grade Level", "type": "number", "min": 1, "max": 12},
           {"name": "department", "label": "Department", "type": "text"},
           {"name": "admin_level", "label": "Admin Level", "type": "dropdown",
            "options": ["Level 1", "Level 2", "Level 3"]}
       ]
   }

   def on_user_type_change(field_name, value):
       print(f"User type changed to: {value}")
       
       # Enable/disable fields based on user type
       if value == "Student":
           gui.set_field_value("student_id", "")
           gui.set_field_value("grade_level", "")
           # In a real implementation, you would show/hide fields here
           print("Showing student-specific fields")
       elif value == "Teacher":
           gui.set_field_value("department", "")
           print("Showing teacher-specific fields")
       elif value == "Administrator":
           gui.set_field_value("admin_level", "")
           print("Showing administrator-specific fields")

   gui = create_gui(config)
   gui.add_field_change_callback('user_type', on_user_type_change)
   gui.run()

Backend-Specific Examples
-------------------------

Using Specific Backends
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from qtpyguihelper.tk import TkGuiBuilder
   from qtpyguihelper.qt import QtGuiBuilder
   from qtpyguihelper.wx import WxGuiBuilder
   from qtpyguihelper.gtk import GtkGuiBuilder

   config = {"window": {"title": "Backend Test"}, "fields": []}

   # Use tkinter specifically
   tk_gui = TkGuiBuilder(config_dict=config)
   
   # Use Qt specifically  
   qt_gui = QtGuiBuilder(config_dict=config)
   
   # Use wxPython specifically
   wx_gui = WxGuiBuilder(config_dict=config)
   
   # Use GTK specifically
   gtk_gui = GtkGuiBuilder(config_dict=config)

Loading from JSON Files
~~~~~~~~~~~~~~~~~~~~~~~

Create a JSON configuration file and load it:

.. code-block:: json

   {
       "window": {
           "title": "My Application",
           "width": 500,
           "height": 400
       },
       "fields": [
           {
               "name": "title",
               "label": "Title",
               "type": "dropdown",
               "options": ["Mr.", "Ms.", "Dr.", "Prof."],
               "required": true
           },
           {
               "name": "name",
               "label": "Full Name", 
               "type": "text",
               "required": true
           }
       ],
       "submit_button": true,
       "cancel_button": true
   }

.. code-block:: python

   from qtpyguihelper import create_gui

   # Load from JSON file
   gui = create_gui(config_path="my_form.json")
   gui.run()

For more examples, check the ``examples/`` directory in the QtPyGuiHelper repository.
