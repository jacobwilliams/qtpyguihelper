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
