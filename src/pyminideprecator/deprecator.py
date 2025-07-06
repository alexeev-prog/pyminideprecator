import inspect
import warnings
from functools import wraps
from typing import Any, Callable, Optional, Type, TypeVar, Union, cast

from .config import get_current_version
from .exc import DeprecatedError
from .version import Version

F = TypeVar("F", bound=Callable[..., Any])
C = TypeVar("C", bound=Type[Any])


def _generate_message(
    message: str,
    remove_version: str,
    since: Optional[str] = None,
    instead: Optional[str] = None,
) -> str:
    """Constructs a standardized deprecation message.

    Formats the deprecation notice according to Google-style deprecation
    messaging conventions.

    Args:
        message: Core deprecation description
        remove_version: Version when functionality will be removed
        since: Optional version when deprecation was introduced
        instead: Optional recommended replacement functionality

    Returns:
        Formatted deprecation message string
    """
    parts = []

    if since:
        parts.append(f"Deprecated since {since}.")

    parts.append(message)

    if instead:
        parts.append(f"Use {instead} instead.")

    parts.append(f"Will be removed in {remove_version}.")
    return " ".join(parts)


def _decorate_callable(
    func: F,
    remove_ver: Version,
    error_ver: Version,
    full_message: str,
    category: Type[Warning],
    stacklevel: int,
) -> F:
    """Decorator implementation for callable objects.

    Wraps a function or method to add deprecation behavior. Modifies the
    function to check current version and either:
    - Raise DeprecatedError if current version >= error_version
    - Emit warning if current version < error_version

    Args:
        func: The target function to decorate
        remove_ver: Version when functionality will be removed
        error_ver: Version when functionality starts raising errors
        full_message: Complete deprecation message
        category: Warning category to emit
        stacklevel: Warning stack level adjustment

    Returns:
        The decorated function with deprecation behavior

    Raises:
        DeprecatedError: When current version >= error_version
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        current_ver = get_current_version()
        if current_ver and current_ver >= error_ver:
            raise DeprecatedError(full_message)

        warnings.warn(full_message, category=category, stacklevel=stacklevel)
        return func(*args, **kwargs)

    wrapper.__doc__ = f"**DEPRECATED** {full_message}\n\n{func.__doc__ or ''}"
    return cast(F, wrapper)


def _decorate_class(
    cls: C,
    remove_ver: Version,
    error_ver: Version,
    full_message: str,
    category: Type[Warning],
    stacklevel: int,
) -> C:
    """Decorator implementation for classes.

    Applies deprecation behavior to all methods of a class, including the
    constructor. Modifies the class __init__ and all methods to:
    - Raise DeprecatedError if current version >= error_version
    - Emit warning if current version < error_version

    Args:
        cls: The target class to decorate
        remove_ver: Version when functionality will be removed
        error_ver: Version when functionality starts raising errors
        full_message: Complete deprecation message
        category: Warning category to emit
        stacklevel: Warning stack level adjustment

    Returns:
        The decorated class with deprecation behavior
    """
    original_init = cls.__init__

    @wraps(original_init)
    def wrapped_init(self: Any, *args: Any, **kwargs: Any) -> None:
        current_ver = get_current_version()
        if current_ver and current_ver >= error_ver:
            raise DeprecatedError(full_message)

        warnings.warn(full_message, category=category, stacklevel=stacklevel)
        original_init(self, *args, **kwargs)

    cls.__init__ = wrapped_init

    for name, method in inspect.getmembers(cls, inspect.isfunction):
        if name == "__init__":
            continue
        setattr(
            cls,
            name,
            _decorate_callable(
                method, remove_ver, error_ver, full_message, category, stacklevel + 1
            ),
        )

    cls.__doc__ = f"**DEPRECATED CLASS** {full_message}\n\n{cls.__doc__ or ''}"
    return cls


def deprecate(
    remove_version: str,
    message: str,
    since: Optional[str] = None,
    instead: Optional[str] = None,
    category: Type[Warning] = DeprecationWarning,
    stacklevel: int = 2,
    error_version: Optional[str] = None,
) -> Callable[[Union[F, C]], Union[F, C]]:
    """Decorator factory for marking deprecated functionality.

    Primary interface for deprecating functions, methods, and classes. Creates
    a decorator that adds deprecation warnings and eventual error behavior.

    Args:
        remove_version: Version when functionality will be removed (required)
        message: Description of deprecation (required)
        since: Optional version when deprecation was introduced
        instead: Optional recommended alternative
        category: Warning category (default: DeprecationWarning)
        stacklevel: Warning stack level (default: 2)
        error_version: Optional version when functionality starts raising errors
            (defaults to remove_version if not specified)

    Returns:
        A decorator that applies deprecation behavior to the target object

    Example:
        >>> @deprecate("2.0.0", "Use new_function instead")
        >>> def old_function():
        ...     pass
    """
    remove_ver = Version(remove_version)
    error_ver = Version(error_version) if error_version else remove_ver
    full_message = _generate_message(message, remove_version, since, instead)

    def decorator(obj: Union[F, C]) -> Union[F, C]:
        if inspect.isclass(obj):
            return _decorate_class(
                cast(C, obj), remove_ver, error_ver, full_message, category, stacklevel
            )
        return _decorate_callable(
            cast(F, obj), remove_ver, error_ver, full_message, category, stacklevel
        )

    return decorator
