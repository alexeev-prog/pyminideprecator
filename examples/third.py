from pyminideprecator import deprecate, set_current_version

# Set current application version
set_current_version('1.2.0')


@deprecate(
    remove_version='2.0.0',
    message='Legacy API function',
    instead='new_api()',
    since='1.0.0',
)
def old_api() -> str:
    """Original documentation"""
    return 'legacy data'


# Generates warning when called
print(old_api())
