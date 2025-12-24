"""
Custom exceptions for vibegui library.
"""


class VibeGuiError(Exception):
    """Base exception for vibegui library."""
    pass


class BackendError(VibeGuiError):
    """Raised when there's an issue with backend selection or initialization."""
    pass


class ConfigurationError(VibeGuiError):
    """Raised when there's an issue with configuration loading or validation."""
    pass
