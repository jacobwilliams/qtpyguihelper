Installation
============

Basic Installation
------------------

Install QtPyGuiHelper using pip:

.. code-block:: bash

   pip install qtpyguihelper

Backend-Specific Installation
-----------------------------

QtPyGuiHelper supports multiple GUI backends. You can install the specific backend you need:

Qt Backend (PySide6)
~~~~~~~~~~~~~~~~~~~~

For Qt support with PySide6 (recommended):

.. code-block:: bash

   pip install qtpyguihelper[pyside6]

Qt Backend (PyQt6)
~~~~~~~~~~~~~~~~~~

For Qt support with PyQt6:

.. code-block:: bash

   pip install qtpyguihelper[pyqt6]

Qt Backend (Generic)
~~~~~~~~~~~~~~~~~~~~

For generic Qt support (requires separate installation of PySide6 or PyQt6):

.. code-block:: bash

   pip install qtpyguihelper[qt]
   # Then install either:
   pip install PySide6  # or PyQt6

wxPython Backend
~~~~~~~~~~~~~~~~

For wxPython support:

.. code-block:: bash

   pip install qtpyguihelper[wxpython]

GTK Backend
~~~~~~~~~~~

For GTK support:

.. code-block:: bash

   pip install qtpyguihelper[gtk]

Note: GTK requires additional system-level dependencies. See the GTK installation guide for your platform.

Tkinter Backend
~~~~~~~~~~~~~~~

Tkinter is included with most Python installations, so no additional installation is required.

All Backends
~~~~~~~~~~~~

To install all supported backends:

.. code-block:: bash

   pip install qtpyguihelper[all]

Development Installation
------------------------

For development, clone the repository and install in editable mode:

.. code-block:: bash

   git clone https://github.com/jacobwilliams/qtpyguihelper.git
   cd qtpyguihelper
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
* **tkinter**: Included with Python (no additional requirements)

Verifying Installation
----------------------

To verify your installation, run:

.. code-block:: python

   import qtpyguihelper
   print(qtpyguihelper.__version__)

   # Test backend availability
   from qtpyguihelper.backend import get_available_backends
   print("Available backends:", get_available_backends())
