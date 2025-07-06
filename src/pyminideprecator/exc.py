"""
pyminideprecator exceptions
"""

class DeprecatedError(Exception):
    """
    Exception raised when deprecated functionality is accessed beyond its removal version.

    This error indicates that the code has reached or exceeded the version where
    the deprecated functionality is scheduled for removal, and attempts to use it
    should be treated as errors rather than warnings.

    Attributes:
        message: Explanation of the deprecation error

    """
