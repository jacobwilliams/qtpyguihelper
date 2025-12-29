Examples
========

This section provides comprehensive examples showing how to use vibegui in different scenarios.

Basic Examples
--------------

Simple Form
~~~~~~~~~~~

Here's a simple contact form example:

.. code-block:: python

   from vibegui import GuiBuilder

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

   gui = GuiBuilder(config_dict=config)
   gui.set_submit_callback(handle_submit)
   gui.run()

Advanced Form with Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from vibegui import GuiBuilder

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
               "min_value": 13,
               "max_value": 120,
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

   gui = GuiBuilder(config_dict=config)
   gui.set_submit_callback(handle_registration)
   gui.run()

Tabbed Interface Example
------------------------

.. code-block:: python

   from vibegui import GuiBuilder

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

   gui = GuiBuilder(config_dict=config)
   gui.run()
   gui.run()

Custom Buttons Example
----------------------

.. code-block:: python

   from vibegui import GuiBuilder

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

   gui = GuiBuilder(config_dict=config)
   gui.run()
   gui.set_custom_button_callback('clear_form', clear_form)
   gui.set_custom_button_callback('load_template', load_template)
   gui.set_custom_button_callback('save_draft', save_draft)
   gui.run()

Data Persistence Example
------------------------

.. code-block:: python

   from vibegui import GuiBuilder
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
            "min_value": 1, "max_value": 24, "default": 6}
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

   gui = GuiBuilder(config_dict=config)
   gui.run()
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

   from vibegui import GuiBuilder

   config = {
       "window": {"title": "Dynamic Form", "width": 400, "height": 300},
       "fields": [
           {"name": "user_type", "label": "User Type", "type": "dropdown",
            "options": ["Student", "Teacher", "Administrator"], "required": True},
           {"name": "student_id", "label": "Student ID", "type": "text"},
           {"name": "grade_level", "label": "Grade Level", "type": "number", "min_value": 1, "max_value": 12},
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

   gui = GuiBuilder(config_dict=config)
   gui.run()
   gui.add_field_change_callback('user_type', on_user_type_change)
   gui.run()

Backend-Specific Examples
-------------------------

Using Specific Backends
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from vibegui.tk import TkGuiBuilder
   from vibegui.qt import QtGuiBuilder
   from vibegui.wx import WxGuiBuilder
   from vibegui.gtk import GtkGuiBuilder
   from vibegui.flet import FletGuiBuilder

   config = {"window": {"title": "Backend Test"}, "fields": []}

   # Use tkinter specifically
   tk_gui = TkGuiBuilder(config_dict=config)

   # Use Qt specifically
   qt_gui = QtGuiBuilder(config_dict=config)

   # Use wxPython specifically
   wx_gui = WxGuiBuilder(config_dict=config)

   # Use GTK specifically
   gtk_gui = GtkGuiBuilder(config_dict=config)

   # Use Flet specifically (Material Design)
   flet_gui = FletGuiBuilder(config_dict=config)

Layout Examples
~~~~~~~~~~~~~~~

Different layout styles for organizing fields:

.. code-block:: python

   from vibegui import GuiBuilder

   # Vertical layout (default - stacks fields vertically)
   vertical_config = {
       "window": {"title": "Vertical Layout", "width": 400, "height": 400},
       "layout": "vertical",
       "fields": [
           {"name": "field1", "label": "Field 1", "type": "text"},
           {"name": "field2", "label": "Field 2", "type": "text"},
           {"name": "field3", "label": "Field 3", "type": "number"}
       ]
   }

   # Horizontal layout (arranges fields in a row)
   horizontal_config = {
       "window": {"title": "Horizontal Layout", "width": 600, "height": 200},
       "layout": "horizontal",
       "fields": [
           {"name": "first", "label": "First", "type": "text"},
           {"name": "middle", "label": "Middle", "type": "text"},
           {"name": "last", "label": "Last", "type": "text"}
       ]
   }

   # Grid layout (responsive 2-column grid)
   grid_config = {
       "window": {"title": "Grid Layout", "width": 600, "height": 400},
       "layout": "grid",
       "fields": [
           {"name": "fname", "label": "First Name", "type": "text"},
           {"name": "lname", "label": "Last Name", "type": "text"},
           {"name": "email", "label": "Email", "type": "email"},
           {"name": "phone", "label": "Phone", "type": "text"},
           {"name": "city", "label": "City", "type": "text"},
           {"name": "state", "label": "State", "type": "text"}
       ]
   }

   # Form layout (label-field pairs)
   form_config = {
       "window": {"title": "Form Layout", "width": 500, "height": 400},
       "layout": "form",
       "fields": [
           {"name": "username", "label": "Username", "type": "text"},
           {"name": "password", "label": "Password", "type": "password"},
           {"name": "remember", "label": "Remember me", "type": "checkbox"}
       ]
   }

   # Use different layouts in tabs
   tabbed_layout_config = {
       "window": {"title": "Mixed Layouts", "width": 600, "height": 500},
       "use_tabs": True,
       "tabs": [
           {
               "title": "Vertical Tab",
               "layout": "vertical",
               "fields": [
                   {"name": "v1", "label": "Field 1", "type": "text"},
                   {"name": "v2", "label": "Field 2", "type": "text"}
               ]
           },
           {
               "title": "Grid Tab",
               "layout": "grid",
               "fields": [
                   {"name": "g1", "label": "Field 1", "type": "text"},
                   {"name": "g2", "label": "Field 2", "type": "text"},
                   {"name": "g3", "label": "Field 3", "type": "text"},
                   {"name": "g4", "label": "Field 4", "type": "text"}
               ]
           }
       ]
   }

   gui = GuiBuilder.create_and_run(config_dict=grid_config)

Nested Fields Example
~~~~~~~~~~~~~~~~~~~~~~

Using dot notation for hierarchical data structures:

.. code-block:: python

   from vibegui import GuiBuilder

   config = {
       "window": {"title": "Application Settings", "width": 600, "height": 500},
       "layout": "form",
       "fields": [
           # Global settings
           {"name": "global.app_name", "label": "Application Name",
            "type": "text", "default_value": "My App"},
           {"name": "global.version", "label": "Version",
            "type": "text", "default_value": "1.0.0"},

           # Database settings
           {"name": "database.host", "label": "Database Host",
            "type": "text", "default_value": "localhost"},
           {"name": "database.port", "label": "Database Port",
            "type": "int", "default_value": 5432},
           {"name": "database.name", "label": "Database Name",
            "type": "text", "required": True},

           # UI settings
           {"name": "ui.theme", "label": "Theme",
            "type": "dropdown", "options": ["light", "dark", "auto"],
            "default_value": "auto"},
           {"name": "ui.font_size", "label": "Font Size",
            "type": "int", "min_value": 8, "max_value": 24, "default_value": 12}
       ],
       "submit_button": True
   }

   def on_submit(data):
       print("Settings saved:")
       print(json.dumps(data, indent=2))
       # Output will be nested:
       # {
       #   "global": {"app_name": "...", "version": "..."},
       #   "database": {"host": "...", "port": ..., "name": "..."},
       #   "ui": {"theme": "...", "font_size": ...}
       # }

   gui = GuiBuilder(config_dict=config)
   gui.set_submit_callback(on_submit)
   gui.run()

Float Formatting Example
~~~~~~~~~~~~~~~~~~~~~~~~~

Controlling decimal precision for float fields:

.. code-block:: python

   from vibegui import GuiBuilder

   config = {
       "window": {"title": "Measurements", "width": 500, "height": 500},
       "layout": "form",
       "fields": [
           {"name": "price", "label": "Price ($)", "type": "float",
            "format_string": ".2f", "default_value": 99.99},

           {"name": "temperature", "label": "Temperature (°C)", "type": "float",
            "format_string": ".1f", "default_value": 23.5},

           {"name": "precision", "label": "High Precision", "type": "float",
            "format_string": ".4f", "default_value": 3.1416},

           {"name": "scientific", "label": "Large Number", "type": "float",
            "format_string": ".2e", "default_value": 1234567.89},

           {"name": "percentage", "label": "Completion", "type": "float",
            "format_string": ".1%", "default_value": 0.856},

           {"name": "currency", "label": "Revenue", "type": "float",
            "format_string": ",.2f", "default_value": 12345.67}
       ],
       "submit_button": True
   }

   gui = GuiBuilder.create_and_run(config_dict=config)

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

   from vibegui import GuiBuilder

   # Load from JSON file
   gui = GuiBuilder.create_and_run(config_path="my_form.json")
   gui.run()

For more examples, check the ``examples/`` directory in the vibegui repository.
