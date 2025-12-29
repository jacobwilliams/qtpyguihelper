API Reference
=============

This section provides detailed documentation for all vibegui modules and classes.

.. toctree::
   :maxdepth: 2

   core
   backends
   config
   utils
   exceptions

Core Functions
--------------

.. autofunction:: vibegui.get_available_backends

Quick Reference
---------------

Main Classes by Backend:

* :class:`vibegui.qt.QtGuiBuilder` - Qt backend (PySide6/PyQt6)
* :class:`vibegui.tk.TkGuiBuilder` - tkinter backend
* :class:`vibegui.wx.WxGuiBuilder` - wxPython backend
* :class:`vibegui.gtk.GtkGuiBuilder` - GTK backend
* :class:`vibegui.flet.FletGuiBuilder` - Flet backend (Material Design)

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
