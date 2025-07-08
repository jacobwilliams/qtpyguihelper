API Reference
=============

This section provides detailed documentation for all QtPyGuiHelper modules and classes.

.. toctree::
   :maxdepth: 2

   core
   backends
   config
   utils
   exceptions

Core Functions
--------------

.. autofunction:: qtpyguihelper.get_available_backends

Quick Reference
---------------

Main Classes by Backend:

* :class:`qtpyguihelper.qt.QtGuiBuilder` - Qt backend (PySide6/PyQt6)
* :class:`qtpyguihelper.tk.TkGuiBuilder` - tkinter backend  
* :class:`qtpyguihelper.wx.WxGuiBuilder` - wxPython backend
* :class:`qtpyguihelper.gtk.GtkGuiBuilder` - GTK backend

Configuration Classes:

* :doc:`config` - Configuration loading and validation
* GuiConfig - Main configuration
* FieldConfig - Field configuration  
* WindowConfig - Window configuration

Utility Classes:

* :doc:`utils` - Utility modules
* ValidationUtils - Field validation utilities
* FileUtils - File I/O utilities
* PlatformUtils - Platform detection utilities
