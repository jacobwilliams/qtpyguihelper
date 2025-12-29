Examples
========

This section provides comprehensive examples showing how to use vibegui in different scenarios.

Basic Examples
--------------

Simple Form
~~~~~~~~~~~

Here's a simple contact form example:

.. literalinclude:: ../examples/docs_examples/simple_form.py
   :language: python
   :linenos:


Advanced Form with Validation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: ../examples/docs_examples/advanced_form.py
   :language: python
   :linenos:

Tabbed Interface Example
------------------------

.. literalinclude:: ../examples/docs_examples/tabbed_interface.py
   :language: python
   :linenos:

Custom Buttons Example
----------------------

.. literalinclude:: ../examples/docs_examples/custom_buttons.py
   :language: python
   :linenos:

Data Persistence Example
------------------------

.. literalinclude:: ../examples/docs_examples/data_persistence.py
   :language: python
   :linenos:

Field Change Callbacks
----------------------

.. literalinclude:: ../examples/docs_examples/field_change_callbacks.py
   :language: python
   :linenos:

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

.. literalinclude:: ../examples/docs_examples/nested_fields.py
   :language: python
   :linenos:

Float Formatting Example
~~~~~~~~~~~~~~~~~~~~~~~~~

Controlling decimal precision for float fields:

.. literalinclude:: ../examples/docs_examples/float_formatting.py
   :language: python
   :linenos:

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
   from qtpy.QtWidgets import QApplication
   import sys

   # Load from JSON file
   app = QApplication(sys.argv)
   gui = GuiBuilder(config_path="my_form.json", backend='qt')
   gui.show()
   sys.exit(app.exec())

For more examples, check the ``examples/`` directory in the vibegui repository.
