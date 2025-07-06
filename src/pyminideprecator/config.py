from contextvars import ContextVar
from typing import Optional, Union
from contextlib import contextmanager

from .version import Version

# Context-local storage for current version
_CURRENT_VERSION: ContextVar[Optional[Version]] = ContextVar(
    '_CURRENT_VERSION',
    default=None
)

def set_current_version(version: Union[str, Version, None]) -> None:
    """Sets the current application version in the current context.

    This version is context-aware and thread-safe. It can be:
    - String representation (e.g., "1.2.3" or "2023.12.31")
    - Version object instance
    - None to clear the current version

    Args:
        version: The current version to set

    Raises:
        ValueError: If string version has invalid format
        TypeError: If invalid version type is provided
    """
    if version is None:
        _CURRENT_VERSION.set(None)
        return

    if isinstance(version, str):
        _CURRENT_VERSION.set(Version(version))
    elif isinstance(version, Version):
        _CURRENT_VERSION.set(version)

def get_current_version() -> Optional[Version]:
    """Retrieves the current application version for the context.

    Returns:
        The current Version object if set, otherwise None.
    """
    return _CURRENT_VERSION.get()


@contextmanager
def scoped_version(version: str):
    """Context manager for creating scoped version.

    Args:
        version: The scoped version
    """
    original = get_current_version()
    set_current_version(version)

    try:
        yield
    finally:
        set_current_version(original)
