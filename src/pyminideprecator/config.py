from typing import Optional, Union

from .version import Version

# Sorry for globals
# TODO: fix it in future release
_CURRENT_VERSION: Optional[Version] = None


def set_current_version(version: Union[str, Version, None]) -> None:
    """Sets the current application version globally.

    This version is used to determine whether to show warnings or raise errors
    for deprecated functionality. The version can be provided as either a string
    (which will be parsed into a Version object) or directly as a Version object.

    Args:
        version: The current version to set. Can be:
            - String representation (e.g., "1.2.3" or "2023.12.31")
            - Version object instance
            - None to clear the current version

    Raises:
        ValueError: If string version has invalid format
        TypeError: If invalid version type is provided
    """
    global _CURRENT_VERSION

    if version is None:
        _CURRENT_VERSION = None
        return

    if isinstance(version, str):
        _CURRENT_VERSION = Version(version)
    else:
        _CURRENT_VERSION = version


def get_current_version() -> Optional[Version]:
    """Retrieves the current application version.

    Returns the version previously set via set_current_version(). If no version
    has been set, returns None.

    Returns:
        The current Version object if set, otherwise None.
    """
    global _CURRENT_VERSION

    if _CURRENT_VERSION:
        return _CURRENT_VERSION

    return None
