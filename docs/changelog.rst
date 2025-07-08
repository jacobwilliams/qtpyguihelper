Changelog
=========

All notable changes to QtPyGuiHelper will be documented in this file.

The format is based on `Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_,
and this project adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.

Version 1.0.0 (2025-01-08)
---------------------------

**Added**

- Initial release of QtPyGuiHelper
- Support for multiple GUI backends:

  - Qt backend (PySide6/PyQt6) with qtpy abstraction
  - tkinter backend with dark mode support
  - wxPython backend with native widgets
  - GTK backend for Linux/macOS

- Comprehensive widget support:

  - Text input fields (single-line and multi-line)
  - Password fields with hidden input
  - Email and URL fields with validation
  - Number and float fields with range validation
  - Date, time, and datetime pickers
  - Checkboxes and radio button groups
  - Dropdown/combobox selections
  - File selection dialogs

- Advanced form features:

  - JSON-based configuration system
  - Tabbed interface support
  - Required field validation
  - Custom button actions
  - Field change callbacks
  - Tooltips and help text
  - Form data persistence (save/load JSON)

- Dark mode support:

  - Automatic system theme detection
  - Proper text visibility in dark themes
  - Theme-aware widget styling

- Utility modules:

  - ValidationUtils for field validation
  - FileUtils for JSON data persistence
  - PlatformUtils for system detection
  - FormatUtils for data formatting
  - LayoutUtils for UI layout helpers

- Configuration system:

  - ConfigLoader for JSON configuration parsing
  - ConfigValidator for configuration validation
  - Comprehensive error handling

- Backend detection and automatic selection
- Extensive documentation and examples
- Comprehensive test suite

**Technical Details**

- Centralized file I/O operations using FileUtils
- Unified validation system across all backends
- Modular architecture with pluggable backends
- Type hints and comprehensive docstrings
- Cross-platform compatibility (Windows, macOS, Linux)

**Dependencies**

- Core: Python 3.8+
- Qt backend: PySide6 6.5.0+ or PyQt6 6.5.0+ with qtpy 2.0.0+
- wxPython backend: wxPython 4.2.0+
- GTK backend: PyGObject 3.42.0+
- tkinter backend: Included with Python

**Breaking Changes**

- N/A (Initial release)

**Deprecated**

- N/A (Initial release)

**Security**

- Input validation to prevent injection attacks
- Safe JSON parsing with error handling
- File path validation for security

**Performance**

- Lazy UI initialization for faster startup
- Efficient widget creation and management
- Optimized form data handling
- Memory-efficient backend selection

Future Releases
---------------

Planned features for future releases:

**Version 1.1.0 (Planned)**

- Additional widget types (sliders, progress bars)
- Enhanced validation rules and custom validators
- Improved theming and styling options
- Plugin system for custom widgets
- Internationalization (i18n) support

**Version 1.2.0 (Planned)**

- Visual form designer/editor
- REST API integration helpers
- Database connectivity modules
- Advanced layout management
- Performance optimizations

**Version 2.0.0 (Future)**

- Web backend support (HTML/JavaScript generation)
- Mobile app generation capabilities
- Cloud configuration management
- Advanced data binding and MVVM patterns
- Breaking changes for improved architecture

Contributing
------------

We welcome contributions! Please see our contributing guidelines for:

- Bug reports and feature requests
- Code contributions and pull requests
- Documentation improvements
- Testing and quality assurance

License
-------

QtPyGuiHelper is released under the MIT License. See LICENSE file for details.
