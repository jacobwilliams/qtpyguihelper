vibegui Documentation
=============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   api/index
   examples
   backends
   changelog

Overview
--------

vibegui is a Python library for creating cross-platform GUIs from JSON configuration files.
It supports multiple GUI backends including Qt (PySide6/PyQt6), wxPython, tkinter, GTK3/GTK4, and Flet.

Key Features
~~~~~~~~~~~~

* **JSON-driven configuration**: Define your GUI structure using simple JSON files
* **Multiple backend support**: Choose from Qt, wxPython, tkinter, GTK, or Flet
* **Cross-platform compatibility**: Works on Windows, macOS, and Linux
* **Rich widget support**: Text fields, numbers, dates, dropdowns, checkboxes, and more
* **Form validation**: Built-in validation for required fields and data types
* **Data persistence**: Save and load form data to/from JSON files
* **Dark mode support**: Automatic theme detection and application
* **Material Design UI**: Modern look with the Flet backend
* **Extensible architecture**: Easy to add custom widgets and validation rules

Quick Example
~~~~~~~~~~~~~

.. code-block:: python

   from vibegui import GuiBuilder

   config = {
       "window": {"title": "My App", "width": 400, "height": 300},
       "fields": [
           {"name": "username", "label": "Username", "type": "text", "required": True},
           {"name": "email", "label": "Email", "type": "email", "required": True},
           {"name": "age", "label": "Age", "type": "number"}
       ]
   }

   # Create and run the GUI
   gui = GuiBuilder.create_and_run(config_dict=config)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
