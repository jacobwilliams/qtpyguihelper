"""
Backend detection and selection for qtpyguihelper.
Supports both Qt (via qtpy) and wxPython backends.
"""

import os
import sys
from typing import Optional, Dict, Any


class BackendError(Exception):
    """Exception raised when backend operations fail."""
    pass


class BackendManager:
    """Manages GUI backend selection and availability."""

    SUPPORTED_BACKENDS = ['qt', 'wx']
    DEFAULT_BACKEND = 'qt'

    def __init__(self):
        self._current_backend: Optional[str] = None
        self._backend_available: Dict[str, bool] = {}
        self._check_backend_availability()

    def _check_backend_availability(self):
        """Check which backends are available."""
        # Check Qt availability
        try:
            import qtpy
            self._backend_available['qt'] = True
        except ImportError:
            self._backend_available['qt'] = False

        # Check wxPython availability
        try:
            import wx
            self._backend_available['wx'] = True
        except ImportError:
            self._backend_available['wx'] = False

    def get_available_backends(self) -> list:
        """Get list of available backends."""
        return [backend for backend, available in self._backend_available.items() if available]

    def is_backend_available(self, backend: str) -> bool:
        """Check if a specific backend is available."""
        return self._backend_available.get(backend.lower(), False)

    def get_backend(self) -> str:
        """Get the current backend, detecting automatically if not set."""
        if self._current_backend is None:
            self._current_backend = self._detect_backend()
        return self._current_backend

    def set_backend(self, backend: str) -> bool:
        """
        Set the backend to use.

        Args:
            backend: Backend name ('qt' or 'wx')

        Returns:
            True if successfully set, False otherwise
        """
        backend = backend.lower()

        if backend not in self.SUPPORTED_BACKENDS:
            raise BackendError(f"Unsupported backend: {backend}. Supported: {self.SUPPORTED_BACKENDS}")

        if not self.is_backend_available(backend):
            raise BackendError(f"Backend '{backend}' is not available. Please install the required dependencies.")

        self._current_backend = backend
        return True

    def _detect_backend(self) -> str:
        """Automatically detect which backend to use."""
        # Check environment variable first
        env_backend = os.environ.get('GUI_BACKEND', '').lower()
        if env_backend in self.SUPPORTED_BACKENDS and self.is_backend_available(env_backend):
            return env_backend

        # Check for Qt API environment variable (for backward compatibility)
        qt_api = os.environ.get('QT_API', '').lower()
        if qt_api and self.is_backend_available('qt'):
            return 'qt'

        # Use default backend if available
        if self.is_backend_available(self.DEFAULT_BACKEND):
            return self.DEFAULT_BACKEND

        # Fall back to any available backend
        available = self.get_available_backends()
        if available:
            return available[0]

        raise BackendError("No GUI backends are available. Please install qtpy+PySide6/PyQt6 or wxPython.")

    def get_backend_info(self) -> Dict[str, Any]:
        """Get information about the current backend."""
        backend = self.get_backend()

        info = {
            'backend': backend,
            'available_backends': self.get_available_backends(),
        }

        if backend == 'qt':
            try:
                import qtpy
                info['qt_api'] = qtpy.API_NAME
                info['qt_version'] = qtpy.QT_VERSION
            except ImportError:
                pass
        elif backend == 'wx':
            try:
                import wx
                info['wx_version'] = wx.version()
                info['wx_platform'] = wx.Platform
            except ImportError:
                pass

        return info


# Global backend manager instance
_backend_manager = BackendManager()


def get_backend() -> str:
    """Get the current GUI backend."""
    return _backend_manager.get_backend()


def set_backend(backend: str) -> bool:
    """Set the GUI backend to use."""
    return _backend_manager.set_backend(backend)


def get_available_backends() -> list:
    """Get list of available GUI backends."""
    return _backend_manager.get_available_backends()


def get_backend_info() -> Dict[str, Any]:
    """Get information about the current backend."""
    return _backend_manager.get_backend_info()


def is_backend_available(backend: str) -> bool:
    """Check if a specific backend is available."""
    return _backend_manager.is_backend_available(backend)
