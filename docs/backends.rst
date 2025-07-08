GUI Backends
============

QtPyGuiHelper supports multiple GUI backends, each with their own strengths and use cases. This page provides detailed information about each backend.

Overview
--------

+------------+------------------+------------------+-------------------+------------------+
| Backend    | Platform Support | Dependencies     | Performance       | Look & Feel      |
+============+==================+==================+===================+==================+
| Qt         | Excellent        | PySide6/PyQt6    | Excellent         | Native           |
+------------+------------------+------------------+-------------------+------------------+
| tkinter    | Excellent        | Built-in         | Good              | Platform-native  |
+------------+------------------+------------------+-------------------+------------------+
| wxPython   | Excellent        | wxPython         | Very Good         | Native           |
+------------+------------------+------------------+-------------------+------------------+
| GTK        | Linux/macOS      | PyGObject        | Good              | GTK theme        |
+------------+------------------+------------------+-------------------+------------------+

Qt Backend
----------

The Qt backend provides the most feature-rich and polished GUI experience.

**Advantages:**
- Excellent cross-platform support
- Rich widget set with advanced features
- Professional look and feel
- Great performance
- Extensive theming capabilities
- Strong community and documentation

**Requirements:**
- PySide6 6.5.0+ or PyQt6 6.5.0+
- qtpy 2.0.0+ (for backend abstraction)

**Installation:**
.. code-block:: bash

   pip install qtpyguihelper[pyside6]  # Recommended
   # or
   pip install qtpyguihelper[pyqt6]

**Usage:**
.. code-block:: python

   from qtpyguihelper.qt import QtGuiBuilder
   
   gui = QtGuiBuilder(config_path="form.json")
   gui.run()

**Features:**
- Advanced date/time pickers
- Rich text editing
- Drag and drop support
- Custom styling with CSS-like syntax
- Built-in validation indicators
- Tooltips and status tips

tkinter Backend
---------------

The tkinter backend is included with Python and provides good cross-platform support.

**Advantages:**
- No additional dependencies required
- Lightweight and fast startup
- Good platform integration
- Dark mode support (automatic detection)
- Reliable and stable

**Requirements:**
- Python with tkinter (included in most Python distributions)

**Installation:**
.. code-block:: bash

   pip install qtpyguihelper  # tkinter support included

**Usage:**
.. code-block:: python

   from qtpyguihelper.tk import TkGuiBuilder
   
   gui = TkGuiBuilder(config_path="form.json")
   gui.run()

**Features:**
- Automatic dark/light theme detection
- Scrollable forms and tabs
- Field validation with visual feedback
- Custom button styling
- Tooltips
- File dialogs

**Dark Mode Support:**
The tkinter backend automatically detects system dark mode and applies appropriate theming:

- Dark backgrounds with light text
- Proper Entry field coloring for visibility
- Theme-aware button styling
- Automatic placeholder text color adjustment

wxPython Backend
----------------

The wxPython backend provides native look and feel on all platforms.

**Advantages:**
- True native widgets on each platform
- Excellent platform integration
- Rich widget set
- Good performance
- Mature and stable

**Requirements:**
- wxPython 4.2.0+

**Installation:**
.. code-block:: bash

   pip install qtpyguihelper[wxpython]

**Usage:**
.. code-block:: python

   from qtpyguihelper.wx import WxGuiBuilder
   
   gui = WxGuiBuilder(config_path="form.json")
   gui.run()

**Features:**
- Native date/time controls
- Platform-specific file dialogs
- Rich text controls
- Custom validators
- Context menus
- Drag and drop

GTK Backend
-----------

The GTK backend is primarily designed for Linux environments but also works on macOS.

**Advantages:**
- Native GTK theming
- Good integration with GNOME desktop
- Supports both GTK3 and GTK4
- Lightweight
- Accessibility features

**Requirements:**
- PyGObject 3.42.0+
- GTK3 or GTK4 system libraries

**Installation:**
.. code-block:: bash

   pip install qtpyguihelper[gtk]

**System Dependencies:**
On Ubuntu/Debian:
.. code-block:: bash

   sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0

On macOS with Homebrew:
.. code-block:: bash

   brew install pygobject3 gtk+3

**Usage:**
.. code-block:: python

   from qtpyguihelper.gtk import GtkGuiBuilder
   
   gui = GtkGuiBuilder(config_path="form.json")
   gui.run()

**Features:**
- GTK theming support
- Keyboard navigation
- Accessibility support
- Custom CSS styling
- Responsive layouts

Backend Selection
-----------------

Automatic Backend Selection
~~~~~~~~~~~~~~~~~~~~~~~~~~~

QtPyGuiHelper can automatically choose the best available backend:

.. code-block:: python

   from qtpyguihelper import create_gui
   
   # Automatically selects the best available backend
   gui = create_gui(config, backend='auto')

The selection priority is:
1. Qt (if PySide6 or PyQt6 is available)
2. tkinter (if available)
3. wxPython (if available)
4. GTK (if available on Linux/macOS)

Manual Backend Selection
~~~~~~~~~~~~~~~~~~~~~~~~

You can explicitly choose a backend:

.. code-block:: python

   # Specific backend selection
   gui = create_gui(config, backend='qt')      # Qt backend
   gui = create_gui(config, backend='tkinter') # tkinter backend
   gui = create_gui(config, backend='wx')      # wxPython backend
   gui = create_gui(config, backend='gtk')     # GTK backend

Checking Available Backends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see which backends are available on your system:

.. code-block:: python

   from qtpyguihelper import get_available_backends
   
   backends = get_available_backends()
   print("Available backends:", backends)

Backend-Specific Features
-------------------------

Widget Support Matrix
~~~~~~~~~~~~~~~~~~~~~

+----------------+-------+----------+----------+-------+
| Widget Type    | Qt    | tkinter  | wxPython | GTK   |
+================+=======+==========+==========+=======+
| Text           | ✓     | ✓        | ✓        | ✓     |
+----------------+-------+----------+----------+-------+
| Textarea       | ✓     | ✓        | ✓        | ✓     |
+----------------+-------+----------+----------+-------+
| Password       | ✓     | ✓        | ✓        | ✓     |
+----------------+-------+----------+----------+-------+
| Number         | ✓     | ✓        | ✓        | ✓     |
+----------------+-------+----------+----------+-------+
| Float          | ✓     | ✓        | ✓        | ✓     |
+----------------+-------+----------+----------+-------+
| Email          | ✓     | ✓        | ✓        | ✓     |
+----------------+-------+----------+----------+-------+
| URL            | ✓     | ✓        | ✓        | ✓     |
+----------------+-------+----------+----------+-------+
| Date           | ✓     | ✓        | ✓        | ✓     |
+----------------+-------+----------+----------+-------+
| Time           | ✓     | ✓        | ✓        | ✓     |
+----------------+-------+----------+----------+-------+
| DateTime       | ✓     | ✓        | ✓        | ✓     |
+----------------+-------+----------+----------+-------+
| Checkbox       | ✓     | ✓        | ✓        | ✓     |
+----------------+-------+----------+----------+-------+
| Dropdown       | ✓     | ✓        | ✓        | ✓     |
+----------------+-------+----------+----------+-------+
| Radio          | ✓     | ✓        | ✓        | ✓     |
+----------------+-------+----------+----------+-------+
| File           | ✓     | ✓        | ✓        | ✓     |
+----------------+-------+----------+----------+-------+

Platform Compatibility
~~~~~~~~~~~~~~~~~~~~~~~

+----------------+---------+---------+---------+
| Backend        | Windows | macOS   | Linux   |
+================+=========+=========+=========+
| Qt             | ✓       | ✓       | ✓       |
+----------------+---------+---------+---------+
| tkinter        | ✓       | ✓       | ✓       |
+----------------+---------+---------+---------+
| wxPython       | ✓       | ✓       | ✓       |
+----------------+---------+---------+---------+
| GTK            | ✗       | ✓       | ✓       |
+----------------+---------+---------+---------+

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Qt Backend Issues:**
- Make sure either PySide6 or PyQt6 is installed
- Check that qtpy is installed and can detect your Qt installation
- On Linux, you may need to install additional Qt dependencies

**tkinter Issues:**
- tkinter is usually included with Python, but some minimal Python installations may exclude it
- On Linux, install ``python3-tk`` package if tkinter is missing
- Dark mode detection requires platform-specific libraries (automatically handled)

**wxPython Issues:**
- wxPython installation can be complex on some platforms
- Use pre-compiled wheels when available: ``pip install -U wxPython``
- On Linux, you may need additional development libraries

**GTK Issues:**
- GTK backend only works on Linux and macOS
- Requires system GTK libraries to be installed
- PyGObject installation can be complex; use system package manager when possible

Performance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Qt**: Best overall performance, especially for complex forms
- **tkinter**: Good performance, fastest startup time
- **wxPython**: Good performance with native feel
- **GTK**: Moderate performance, depends on system GTK version

For applications with many fields or complex layouts, Qt is recommended for the best user experience.
