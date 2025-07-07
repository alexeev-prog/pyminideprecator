"""
Fast and minimalistic library for marking methods and classes as deprecated.

`pyminideprecator` is a lightweight yet powerful decorator-based solution for managing
code deprecation in Python libraries and applications. It provides a robust mechanism
to mark deprecated code with automatic warnings that escalate to errors at specified
version thresholds, supporting both semantic versioning and date-based versioning.
The library is designed with thread safety and asynchronous execution in mind, making
it suitable for all types of Python projects.
"""

from .config import get_current_version, scoped_version, set_current_version
from .deprecator import deprecate
from .exc import DeprecatedError
from .version import Version

__all__ = [
    "DeprecatedError",
    "Version",
    "deprecate",
    "get_current_version",
    "scoped_version",
    "set_current_version",
]
