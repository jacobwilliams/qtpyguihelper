"""
Backend detection and selection for vibegui.
Supports Qt (via qtpy), wxPython, tkinter, and GTK backends.
"""

import os
import sys
from typing import Optional, Dict, Any, List

from .exceptions import BackendError


class BackendManager:
    """Manages GUI backend selection and availability."""

    SUPPORTED_BACKENDS = ['qt', 'wx', 'tk', 'gtk', 'flet']
    DEFAULT_BACKEND = 'qt'

    def __init__(self) -> None:
        self._current_backend: Optional[str] = None
        self._backend_available: Dict[str, Optional[bool]] = {}

    def _check_backend_availability(self, backend: str) -> bool:
        """Check if a specific backend is available (lazy loading)."""
        if backend in self._backend_available:
            return self._backend_available[backend]

        # Check Qt availability
        if backend == 'qt':
            try:
                import qtpy  # noqa: F401
                self._backend_available['qt'] = True
                return True
            except ImportError:
                self._backend_available['qt'] = False
                return False

        # Check wxPython availability
        elif backend == 'wx':
            try:
                import wx  # noqa: F401
                self._backend_available['wx'] = True
                return True
            except ImportError:
                self._backend_available['wx'] = False
                return False

        # Check tkinter availability
        elif backend == 'tk':
            try:
                import tkinter  # noqa: F401
                self._backend_available['tk'] = True
                return True
            except ImportError:
                self._backend_available['tk'] = False
                return False

        # Check GTK availability
        elif backend == 'gtk':
            try:
                from .gtk import GTK_VERSION, GTK_MAJOR_VERSION, Gtk
                if GTK_VERSION and Gtk:
                    self._backend_available['gtk'] = True
                    return True
                else:
                    self._backend_available['gtk'] = False
                    return False
            except (ImportError, ValueError):
                self._backend_available['gtk'] = False
                return False

        # Check Flet availability
        elif backend == 'flet':
            try:
                import flet  # noqa: F401
                self._backend_available['flet'] = True
                return True
            except ImportError:
                self._backend_available['flet'] = False
                return False

        else:
            self._backend_available[backend] = False
            return False

    def get_available_backends(self) -> List[str]:
        """Get list of available backends."""
        available = []
        for backend in self.SUPPORTED_BACKENDS:
            if self._check_backend_availability(backend):
                available.append(backend)
        return available

    def is_backend_available(self, backend: str) -> bool:
        """Check if a specific backend is available."""
        return self._check_backend_availability(backend.lower())

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
        elif backend == 'tk':
            try:
                import tkinter
                info['tk_version'] = tkinter.TkVersion
                info['tcl_version'] = tkinter.TclVersion
            except ImportError:
                pass
        elif backend == 'gtk':
            try:
                import gi
                gi.require_version('Gtk', '3.0')
                from gi.repository import Gtk
                info['gtk_version'] = f"{Gtk.get_major_version()}.{Gtk.get_minor_version()}.{Gtk.get_micro_version()}"
                info['glib_version'] = gi.version_info
            except (ImportError, ValueError):
                pass
        elif backend == 'flet':
            try:
                import flet
                info['flet_version'] = flet.version.version
            except (ImportError, AttributeError):
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


def get_available_backends() -> List[str]:
    """Get list of available GUI backends."""
    return _backend_manager.get_available_backends()


def get_backend_info() -> Dict[str, Any]:
    """Get information about the current backend."""
    return _backend_manager.get_backend_info()


def is_backend_available(backend: str) -> bool:
    """Check if a specific backend is available."""
    return _backend_manager.is_backend_available(backend)
