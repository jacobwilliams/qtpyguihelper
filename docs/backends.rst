GUI Backends
============

vibegui supports multiple GUI backends, each with their own strengths and use cases. This page provides detailed information about each backend.

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
| Flet       | Excellent        | Flet             | Excellent         | Material Design  |
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

   pip install vibegui[pyside6]  # Recommended
   # or
   pip install vibegui[pyqt6]

**Usage:**

.. code-block:: python

   from vibegui.qt import QtGuiBuilder

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

   pip install vibegui  # tkinter support included

**Usage:**

.. code-block:: python

   from vibegui.tk import TkGuiBuilder

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

   pip install vibegui[wxpython]

**Usage:**

.. code-block:: python

   from vibegui.wx import WxGuiBuilder

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

   pip install vibegui[gtk]

**System Dependencies:**
On Ubuntu/Debian:

.. code-block:: bash

   sudo apt-get install python3-gi python3-gi-cairo gir1.2-gtk-3.0

On macOS with Homebrew:

.. code-block:: bash

   brew install pygobject3 gtk+3

**Usage:**

.. code-block:: python

   from vibegui.gtk import GtkGuiBuilder

   gui = GtkGuiBuilder(config_path="form.json")
   gui.run()

**Features:**
- GTK theming support
- Keyboard navigation
- Accessibility support
- Custom CSS styling
- Responsive layouts

Flet Backend
------------

The Flet backend provides a modern Material Design experience with excellent cross-platform support.

**Advantages:**
- Modern Material Design UI
- Excellent cross-platform support (Desktop, Web, Mobile)
- Beautiful animations and transitions
- Automatic theme adaptation (light/dark mode)
- Hot reload during development
- Progressive Web App (PWA) support
- No platform-specific dependencies

**Requirements:**
- Flet 0.24.0+

**Installation:**

.. code-block:: bash

   pip install vibegui[flet]

**Usage:**

.. code-block:: python

   from vibegui.flet import FletGuiBuilder

   gui = FletGuiBuilder(config_path="form.json")
   gui.run()

**Features:**
- Material Design 3 components
- Smooth animations and transitions
- Automatic light/dark theme switching
- Responsive layouts
- Touch-friendly controls
- Built-in form validation with visual feedback
- File upload/download support
- Color picker widget
- Slider controls with visual feedback
- Rich date/time pickers

**Deployment Options:**
Flet applications can be deployed in multiple ways:

- **Desktop**: Native executables for Windows, macOS, and Linux
- **Web**: Progressive Web Apps (PWA) or static websites
- **Mobile**: iOS and Android native apps
- **Server**: Multi-user web applications

**Unique Features:**
- Can run as a desktop app or in a web browser
- Automatic UI updates across all connected clients
- Built-in support for responsive design
- No JavaScript required
- Seamless transition between desktop and web deployment

Backend Selection
-----------------

Automatic Backend Selection
~~~~~~~~~~~~~~~~~~~~~~~~~~~

vibegui can automatically choose the best available backend:

.. code-block:: python

   from vibegui import GuiBuilder

   # Automatically selects the best available backend
   gui = GuiBuilder.create_and_run(config_dict=config)

The selection priority is:
1. Qt (if PySide6 or PyQt6 is available)
2. tkinter (if available)
3. wxPython (if available)
4. GTK (if available on Linux/macOS)
5. Flet (if available)

Manual Backend Selection
~~~~~~~~~~~~~~~~~~~~~~~~

You can explicitly choose a backend:

.. code-block:: python

   # Specific backend selection
   gui = GuiBuilder.create_and_run(config_dict=config, backend='qt')      # Qt backend
   gui = GuiBuilder.create_and_run(config_dict=config, backend='tkinter') # tkinter backend
   gui = GuiBuilder.create_and_run(config_dict=config, backend='wx')      # wxPython backend
   gui = GuiBuilder.create_and_run(config_dict=config, backend='gtk')     # GTK backend
   gui = GuiBuilder.create_and_run(config_dict=config, backend='flet')    # Flet backend

Checking Available Backends
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see which backends are available on your system:

.. code-block:: python

   from vibegui import get_available_backends

   backends = get_available_backends()
   print("Available backends:", backends)

Backend-Specific Features
-------------------------

Widget Support Matrix
~~~~~~~~~~~~~~~~~~~~~

+----------------+-------+----------+----------+-------+-------+
| Widget Type    | Qt    | tkinter  | wxPython | GTK   | Flet  |
+================+=======+==========+==========+=======+=======+
| Text           | ✓     | ✓        | ✓        | ✓     | ✓     |
+----------------+-------+----------+----------+-------+-------+
| Textarea       | ✓     | ✓        | ✓        | ✓     | ✓     |
+----------------+-------+----------+----------+-------+-------+
| Password       | ✓     | ✓        | ✓        | ✓     | ✓     |
+----------------+-------+----------+----------+-------+-------+
| Number         | ✓     | ✓        | ✓        | ✓     | ✓     |
+----------------+-------+----------+----------+-------+-------+
| Float          | ✓     | ✓        | ✓        | ✓     | ✓     |
+----------------+-------+----------+----------+-------+-------+
| Email          | ✓     | ✓        | ✓        | ✓     | ✓     |
+----------------+-------+----------+----------+-------+-------+
| URL            | ✓     | ✓        | ✓        | ✓     | ✓     |
+----------------+-------+----------+----------+-------+-------+
| Date           | ✓     | ✓        | ✓        | ✓     | ✓     |
+----------------+-------+----------+----------+-------+-------+
| Time           | ✓     | ✓        | ✓        | ✓     | ✓     |
+----------------+-------+----------+----------+-------+-------+
| DateTime       | ✓     | ✓        | ✓        | ✓     | ✓     |
+----------------+-------+----------+----------+-------+-------+
| Checkbox       | ✓     | ✓        | ✓        | ✓     | ✓     |
+----------------+-------+----------+----------+-------+-------+
| Dropdown       | ✓     | ✓        | ✓        | ✓     | ✓     |
+----------------+-------+----------+----------+-------+-------+
| Radio          | ✓     | ✓        | ✓        | ✓     | ✓     |
+----------------+-------+----------+----------+-------+-------+
| File           | ✓     | ✓        | ✓        | ✓     | ✓     |
+----------------+-------+----------+----------+-------+-------+

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
| Flet           | ✓       | ✓       | ✓       |
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

**Flet Issues:**
- Flet applications may take a moment to initialize on first launch
- Web deployment requires proper CORS configuration
- Mobile deployment requires additional setup with Flutter SDK

Performance Considerations
~~~~~~~~~~~~~~~~~~~~~~~~~~

- **Qt**: Best overall performance, especially for complex forms
- **Flet**: Excellent performance with modern UI and animations
- **tkinter**: Good performance, fastest startup time
- **wxPython**: Good performance with native feel
- **GTK**: Moderate performance, depends on system GTK version

For applications with many fields or complex layouts, Qt or Flet are recommended for the best user experience.
