Installation
============

Basic Installation
------------------

Install vibegui using pip:

.. code-block:: bash

   pip install vibegui

Backend-Specific Installation
-----------------------------

vibegui supports multiple GUI backends. You can install the specific backend you need:

Qt Backend (PySide6)
~~~~~~~~~~~~~~~~~~~~

For Qt support with PySide6 (recommended):

.. code-block:: bash

   pip install vibegui[pyside6]

Qt Backend (PyQt6)
~~~~~~~~~~~~~~~~~~

For Qt support with PyQt6:

.. code-block:: bash

   pip install vibegui[pyqt6]

Qt Backend (Generic)
~~~~~~~~~~~~~~~~~~~~

For generic Qt support (requires separate installation of PySide6 or PyQt6):

.. code-block:: bash

   pip install vibegui[qt]
   # Then install either:
   pip install PySide6  # or PyQt6

wxPython Backend
~~~~~~~~~~~~~~~~

For wxPython support:

.. code-block:: bash

   pip install vibegui[wxpython]

GTK Backend
~~~~~~~~~~~

For GTK support:

.. code-block:: bash

   pip install vibegui[gtk]

Note: GTK requires additional system-level dependencies. See the GTK installation guide for your platform.

Flet Backend
~~~~~~~~~~~~

For Flet support (Material Design UI):

.. code-block:: bash

   pip install vibegui[flet]

Flet provides a modern Material Design interface with excellent cross-platform support for desktop, web, and mobile applications.

Tkinter Backend
~~~~~~~~~~~~~~~

Tkinter is included with most Python installations, so no additional installation is required.

All Backends
~~~~~~~~~~~~

To install all supported backends:

.. code-block:: bash

   pip install vibegui[all]

Development Installation
------------------------

For development, clone the repository and install in editable mode:

.. code-block:: bash

   git clone https://github.com/jacobwilliams/vibegui.git
   cd vibegui
   pip install -e .[dev]

This installs all development dependencies including testing tools, code formatters, and documentation tools.

Requirements
------------

* Python 3.8 or higher
* Operating System: Windows, macOS, or Linux

Backend-specific requirements:

* **Qt**: PySide6 6.5.0+ or PyQt6 6.5.0+ with qtpy 2.0.0+
* **wxPython**: wxPython 4.2.0+
* **GTK**: PyGObject 3.42.0+
* **Flet**: Flet 0.24.0+
* **tkinter**: Included with Python (no additional requirements)

Verifying Installation
----------------------

To verify your installation, run:

.. code-block:: python

   import vibegui
   print(vibegui.__version__)

   # Test backend availability
   from vibegui.backend import get_available_backends
   print("Available backends:", get_available_backends())
