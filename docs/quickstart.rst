Quick Start Guide
=================

This guide will help you get started with vibegui quickly.

Basic Usage
-----------

The simplest way to create a GUI is using a JSON configuration:

.. code-block:: python

   from vibegui import GuiBuilder

   # Define your GUI structure
   config = {
       "window": {
           "title": "My First GUI",
           "width": 400,
           "height": 300
       },
       "fields": [
           {
               "name": "name",
               "label": "Full Name",
               "type": "text",
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
               "min_value": 0,
               "max_value": 120
           }
       ]
   }

   # Create and run the GUI
   gui = GuiBuilder.create_and_run(config_dict=config)

Choosing a Backend
------------------

You can specify which GUI backend to use:

.. code-block:: python

   # Automatically choose the best available backend
   gui = GuiBuilder.create_and_run(config_dict=config)

   # Use specific backends
   gui = GuiBuilder.create_and_run(config_dict=config, backend='qt')      # Qt (PySide6/PyQt6)
   gui = GuiBuilder.create_and_run(config_dict=config, backend='tk')      # tkinter
   gui = GuiBuilder.create_and_run(config_dict=config, backend='wx')      # wxPython
   gui = GuiBuilder.create_and_run(config_dict=config, backend='gtk')     # GTK
   gui = GuiBuilder.create_and_run(config_dict=config, backend='flet')    # Flet (Material Design)

Loading Configuration from File
-------------------------------

You can also load your configuration from a JSON file:

.. code-block:: python

   from vibegui import GuiBuilder

   # Load from file
   gui = GuiBuilder.create_and_run(config_path="my_form.json")

Example JSON Configuration File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a file called ``my_form.json``:

.. code-block:: json

   {
       "window": {
           "title": "User Registration",
           "width": 500,
           "height": 400
       },
       "fields": [
           {
               "name": "username",
               "label": "Username",
               "type": "text",
               "required": true,
               "placeholder": "Enter your username"
           },
           {
               "name": "password",
               "label": "Password",
               "type": "password",
               "required": true
           },
           {
               "name": "country",
               "label": "Country",
               "type": "dropdown",
               "options": ["USA", "Canada", "UK", "Australia"]
           },
           {
               "name": "newsletter",
               "label": "Subscribe to newsletter",
               "type": "checkbox",
               "default": true
           }
       ],
       "submit_button": true,
       "cancel_button": true
   }

Handling Form Submission
------------------------

Add callbacks to handle form submission:

.. code-block:: python

   def on_submit(data):
       print("Form submitted with data:", data)
       # Process the form data here

   def on_cancel():
       print("Form cancelled")

   gui = GuiBuilder(config_dict=config)
   gui.set_submit_callback(on_submit)
   gui.set_cancel_callback(on_cancel)
   gui.run()

Working with Form Data
----------------------

Get and set form data programmatically:

.. code-block:: python

   # Get all form data
   data = gui.get_form_data()
   print(data)  # {'name': 'John Doe', 'email': 'john@example.com', 'age': 30}

   # Set form data
   gui.set_form_data({
       'name': 'Jane Smith',
       'email': 'jane@example.com',
       'age': 25
   })

   # Get/set individual field values
   name = gui.get_field_value('name')
   gui.set_field_value('name', 'New Name')

Saving and Loading Data
-----------------------

Save form data to files and load it back:

.. code-block:: python

   # Save current form data to a JSON file
   gui.save_data_to_file('user_data.json')

   # Load data from a JSON file
   gui.load_data_from_file('user_data.json')

Layout Options
--------------

vibegui supports multiple layout styles for organizing fields:

* ``vertical`` - Stack fields vertically (default)
* ``horizontal`` - Arrange fields horizontally in a row
* ``grid`` - Responsive grid layout (2-column on desktop, single column on mobile)
* ``form`` - Form-style layout with labels and fields

Specify layout in your configuration:

.. code-block:: json

   {
       "window": {"title": "My App"},
       "layout": "grid",
       "fields": [
           {"name": "field1", "label": "Field 1", "type": "text"},
           {"name": "field2", "label": "Field 2", "type": "text"}
       ]
   }

Tabs can also have their own layout:

.. code-block:: json

   {
       "window": {"title": "Tabbed App"},
       "use_tabs": true,
       "tabs": [
           {
               "title": "Tab 1",
               "layout": "form",
               "fields": [...]
           }
       ]
   }

Field Types
-----------

vibegui supports various field types:

* ``text`` - Single-line text input
* ``textarea`` - Multi-line text input
* ``password`` - Password input (hidden text)
* ``email`` - Email input with validation
* ``number`` - Numeric input
* ``int`` - Integer input
* ``float`` - Floating-point number input with precision control
* ``date`` - Date picker
* ``time`` - Time picker
* ``datetime`` - Date and time picker
* ``checkbox`` - Boolean checkbox
* ``dropdown`` - Dropdown/combobox selection
* ``select`` - Alternative to dropdown
* ``radio`` - Radio button group
* ``file`` - File selection
* ``color`` - Color picker
* ``url`` - URL input with validation
* ``range`` - Slider/range input

Advanced Field Features
-----------------------

Float Formatting
~~~~~~~~~~~~~~~~

For ``float`` fields, you can control the display format using the ``format_string`` parameter:

.. code-block:: json

   {
       "name": "price",
       "label": "Price",
       "type": "float",
       "format_string": ".2f",
       "default_value": 99.99
   }

Common format strings:

* ``.2f`` - Two decimal places (e.g., 99.99)
* ``.1f`` - One decimal place (e.g., 95.5)
* ``.4f`` - Four decimal places (e.g., 0.1234)
* ``,.2f`` - Thousands separator (e.g., 12,345.67)
* ``.2e`` - Scientific notation (e.g., 1.23e+06)
* ``.1%`` - Percentage format (e.g., 85.6%)

Nested Field Names
~~~~~~~~~~~~~~~~~~

vibegui supports hierarchical data structures using dot notation in field names:

.. code-block:: json

   {
       "window": {"title": "App Settings", "width": 500, "height": 400},
       "fields": [
           {"name": "global.app_name", "label": "Application Name", "type": "text"},
           {"name": "global.version", "label": "Version", "type": "text"},
           {"name": "database.host", "label": "Database Host", "type": "text"},
           {"name": "database.port", "label": "Database Port", "type": "int"},
           {"name": "ui.theme", "label": "Theme", "type": "dropdown",
            "options": ["light", "dark", "auto"]}
       ]
   }

When saving data, this creates a nested JSON structure:

.. code-block:: json

   {
       "global": {
           "app_name": "My Application",
           "version": "1.0.0"
       },
       "database": {
           "host": "localhost",
           "port": 5432
       },
       "ui": {
           "theme": "dark"
       }
   }

The library automatically handles loading nested data structures back into the form.

Validation
----------

Add validation to your fields:

.. code-block:: json

   {
       "name": "age",
       "label": "Age",
       "type": "number",
       "required": true,
       "min_value": 18,
       "max_value": 65,
       "tooltip": "Age must be between 18 and 65"
   }

Tabbed Interface
----------------

Create tabbed interfaces for complex forms:

.. code-block:: json

   {
       "window": {"title": "Complex Form", "width": 600, "height": 500},
       "use_tabs": true,
       "tabs": [
           {
               "title": "Personal Info",
               "fields": [
                   {"name": "name", "label": "Name", "type": "text"},
                   {"name": "email", "label": "Email", "type": "email"}
               ]
           },
           {
               "title": "Address",
               "fields": [
                   {"name": "street", "label": "Street", "type": "text"},
                   {"name": "city", "label": "City", "type": "text"}
               ]
           }
       ]
   }

Custom Buttons
--------------

Add custom buttons with your own actions:

.. code-block:: json

   {
       "custom_buttons": [
           {
               "name": "clear_form",
               "label": "Clear All",
               "style": {"background": "#ff6b6b", "foreground": "white"}
           }
       ]
   }

.. code-block:: python

   def clear_form_callback(button_config, form_data):
       gui.clear_form()
       print("Form cleared!")

   gui.set_custom_button_callback('clear_form', clear_form_callback)

Next Steps
----------

* Read the :doc:`api/index` for detailed API documentation
* Check out :doc:`examples` for more complex use cases
* Learn about different :doc:`backends` and their features
