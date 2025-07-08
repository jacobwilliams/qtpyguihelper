"""
Custom exceptions for QtPyGuiHelper library.
"""


class QtPyGuiHelperError(Exception):
    """Base exception for QtPyGuiHelper library."""
    pass


class BackendError(QtPyGuiHelperError):
    """Raised when there's an issue with backend selection or initialization."""
    pass


class ConfigurationError(QtPyGuiHelperError):
    """Raised when there's an issue with configuration loading or validation."""
    pass


class WidgetError(QtPyGuiHelperError):
    """Raised when there's an issue with widget creation or manipulation."""
    pass


class ValidationError(QtPyGuiHelperError):
    """Raised when form validation fails."""

    def __init__(self, message: str, missing_fields: list = None):
        super().__init__(message)
        self.missing_fields = missing_fields or []


class FileOperationError(QtPyGuiHelperError):
    """Raised when file operations (save/load) fail."""
    pass


class UnsupportedOperationError(QtPyGuiHelperError):
    """Raised when an operation is not supported by the current backend."""
    pass
