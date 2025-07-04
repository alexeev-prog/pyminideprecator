.. pyEchoNext documentation master file, created by
   sphinx-quickstart on Fri Apr 18 00:12:47 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

pyminideprecator documentation
========================

------------------

.. toctree::
   :maxdepth: 2
   :caption: Source code docs:

   pyminideprecator
   pyminideprecator.config
   pyminideprecator.deprecator
   pyminideprecator.exc
   pyminideprecator.version

------------------

.. _pyminideprecator:

========================
pyminideprecator
========================

.. image:: https://img.shields.io/badge/python-3.8%2B-blue
    :target: https://pypi.org/project/pyminideprecator/
    :alt: Python Version

.. image:: https://img.shields.io/badge/license-MIT-green
    :target: LICENSE
    :alt: License

.. image:: https://img.shields.io/badge/coverage-100%25-brightgreen
    :target: https://pypi.org/project/pyminideprecator/
    :alt: Code Coverage

Minimalistic and robust deprecation management decorator for Python applications and libraries.

-----------
Installation
-----------

Install via pip:

.. code-block:: bash

    pip install pyminideprecator

----------
Quick Start
----------

Basic Function Deprecation
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from pyminideprecator import deprecate, set_current_version

    # Set current application version
    set_current_version("1.2.0")

    @deprecate(
        remove_version="2.0.0",
        message="Legacy API function",
        instead="new_api()",
        since="1.0.0"
    )
    def old_api() -> str:
        """Original documentation"""
        return "legacy data"

    # Generates warning when called
    print(old_api())

Class Deprecation
^^^^^^^^^^^^^^^^^

.. code-block:: python

    @deprecate(
        remove_version="2024.01.01",
        message="Old database client",
        instead="NewDBClient"
    )
    class OldDBClient:
        def __init__(self, url: str):
            self.url = url

        def query(self, sql: str) -> list:
            return ["result1", "result2"]

    # Shows warning on instantiation
    client = OldDBClient("db://localhost")

-------------
Core Concepts
-------------

Version Management
^^^^^^^^^^^^^^^^^^

pyminideprecator supports two version formats:

1. **Semantic Versioning** (SemVer):
   - Format: ``MAJOR.MINOR.PATCH``
   - Example: ``1.2.3``, ``2.0.0``
   - Comparison: Numeric ordering

2. **Date-based Versions**:
   - Format: ``YYYY.MM.DD``
   - Example: ``2023.12.31``, ``2024.01.01``
   - Comparison: Chronological ordering

Lifecycle Management
^^^^^^^^^^^^^^^^^^^^

.. mermaid::

    graph LR
        A[Current Version < Error Version] --> B[Warning]
        C[Current Version >= Error Version] --> D[Error]

--------------
API Reference
--------------

Decorator: ``@deprecate``
^^^^^^^^^^^^^^^^^^^^^^^^^

Marks functions, classes, or methods as deprecated.

Parameters:
    remove_version (str):
        Version when functionality will be removed (required)

    message (str):
        Deprecation description (required)

    since (Optional[str]):
        Version when deprecated (default: None)

    instead (Optional[str]):
        Replacement suggestion (default: None)

    category (Type[Warning]):
        Warning class (default: DeprecationWarning)

    stacklevel (int):
        Warning stack level (default: 2)

    error_version (Optional[str]):
        Version when errors start (default: remove_version)

Function: ``set_current_version(version: Union[str, Version, None])``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sets the current application version.

Parameters:
    version: Version string, Version object, or None to clear

Function: ``get_current_version() -> Optional[Version]``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Returns the current application version.

Class: ``Version``
^^^^^^^^^^^^^^^^^^

Represents a version for comparison operations.

.. code-block:: python

    class Version:
        def __init__(self, version_str: str) -> None:
            """
            Initialize a Version object

            :param version_str: Version string (semantic or date-based)
            :raises ValueError: For invalid version formats
            """

        def __lt__(self, other: Version) -> bool:
            """Less than comparison"""

        def __ge__(self, other: Version) -> bool:
            """Greater or equal comparison"""

Exception: ``DeprecatedError``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Raised when deprecated functionality is used beyond its error version.

.. code-block:: python

    class DeprecatedError(Exception):
        """Exception for removed functionality"""

-----------------
Advanced Usage
-----------------

Property Deprecation
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    class DataModel:
        @property
        @deprecate("2.5.0", "Use new_property instead")
        def old_property(self) -> str:
            return self._value

Static Method Deprecation
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    class Utilities:
        @deprecate("3.0.0", "Use new_utility()")
        @staticmethod
        def old_utility() -> int:
            return 42

Custom Warning Type
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    @deprecate(
        "3.0.0",
        "Future removal",
        category=FutureWarning
    )
    def future_function():
        pass

Different Error Version
^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    @deprecate(
        remove_version="2.0.0",
        message="Early removal",
        error_version="1.9.0"
    )
    def early_removal_func():
        pass

-------------------
Integration Guide
-------------------

pytest Testing
^^^^^^^^^^^^^^

.. code-block:: python

    import pytest
    from pyminideprecator import set_current_version

    def test_deprecation_warning():
        set_current_version("1.0.0")

        with pytest.warns(DeprecationWarning):
            deprecated_function()

    def test_deprecation_error():
        set_current_version("2.0.0")

        with pytest.raises(DeprecatedError):
            deprecated_function()

Sphinx Documentation
^^^^^^^^^^^^^^^^^^^^

Deprecation notices automatically appear in docstrings:

.. code-block:: python

    @deprecate("2.0.0", "Deprecated function")
    def sample_function():
        """Original documentation"""

Resulting docstring:

.. code-block:: text

    **DEPRECATED** Deprecated function Will be removed in 2.0.0.

    Original documentation

-----------------
Best Practices
-----------------

1. **Set version early**: Configure at application start
2. **Provide alternatives**: Always use ``instead`` parameter
3. **Gradual enforcement**: Set ``error_version`` before ``remove_version``
4. **Document history**: Include ``since`` for context
5. **Test states**: Verify warning and error behaviors
6. **Semantic versioning**: Follow SemVer for predictable deprecation cycles
7. **Clear messaging**: Explain why functionality is deprecated

-------------
Limitations
-------------

1. Global version state
2. Cannot compare semantic vs date-based versions
3. No async function support (planned for v2)
4. Limited to Python 3.8+

-------------
Contributing
-------------

Contributions are welcome. See `CONTRIBUTING.md <https://github.com/alexeev-prog/pyminideprecator/blob/main/CONTRIBUTING.md>`_
for guidelines.

-------
License
-------

MIT License - See `LICENSE <https://github.com/alexeev-prog/pyminideprecator/blob/main/LICENSE>`_
for details.

------------
Changelog
------------

v0.1.0 (2023-10-15)
^^^^^^^^^^^^^^^^^^^^
- Initial release
- Core deprecation functionality
- Semantic and date-based version support
- Class and function decoration
- 100% test coverage

-----------------
Indices and Tables
-----------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
