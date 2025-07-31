from pyminideprecator import DeprecatedError, deprecate, set_current_version

set_current_version("1.2.0")


@deprecate(
    remove_version="2.0.0",
    message="Legacy API function",
    instead="new_api()",
    since="1.0.0",
)
def old_api() -> str:
    """Original documentation."""
    return "legacy data"


print(
    old_api()
)  # Warning: Deprecated since 1.0.0. Legacy API function. Use new_api() instead. Will be removed in 2.0.0.

set_current_version("2.0.0")
try:
    old_api()  # Raises DeprecatedError
except DeprecatedError as e:
    print(e)
