QtPyGuiHelper Documentation
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

QtPyGuiHelper is a Python library for creating cross-platform GUIs from JSON configuration files. 
It supports multiple GUI backends including Qt (PySide6/PyQt6), wxPython, tkinter, and GTK3/GTK4.

Key Features
~~~~~~~~~~~~

* **JSON-driven configuration**: Define your GUI structure using simple JSON files
* **Multiple backend support**: Choose from Qt, wxPython, tkinter, or GTK
* **Cross-platform compatibility**: Works on Windows, macOS, and Linux
* **Rich widget support**: Text fields, numbers, dates, dropdowns, checkboxes, and more
* **Form validation**: Built-in validation for required fields and data types
* **Data persistence**: Save and load form data to/from JSON files
* **Dark mode support**: Automatic theme detection and application
* **Extensible architecture**: Easy to add custom widgets and validation rules

Quick Example
~~~~~~~~~~~~~

.. code-block:: python

   from qtpyguihelper import create_gui

   config = {
       "window": {"title": "My App", "width": 400, "height": 300},
       "fields": [
           {"name": "username", "label": "Username", "type": "text", "required": True},
           {"name": "email", "label": "Email", "type": "email", "required": True},
           {"name": "age", "label": "Age", "type": "number"}
       ]
   }

   # Create and run the GUI
   gui = create_gui(config, backend='auto')
   gui.run()

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
