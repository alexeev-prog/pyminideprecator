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

   modules
   pyminideprecator

------------------

.. _pyminideprecator:

#######################
pyminideprecator
#######################

.. image:: https://raw.githubusercontent.com/alexeev-prog/pyminideprecator/main/docs/pallet-0.png
   :alt: pyminideprecator logo
   :align: center

Professional deprecation management for modern Python projects.

.. image:: https://img.shields.io/pypi/v/pyminideprecator.svg
   :target: https://pypi.org/project/pyminideprecator/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/pyminideprecator.svg
   :target: https://pypi.org/project/pyminideprecator/
   :alt: Python Versions

.. image:: https://img.shields.io/badge/coverage-100%25-brightgreen
   :alt: Test Coverage

.. image:: https://img.shields.io/github/license/alexeev-prog/pyminideprecator.svg
   :target: https://github.com/alexeev-prog/pyminideprecator/blob/main/LICENSE
   :alt: License

-----

**pyminideprecator** is a lightweight yet powerful decorator-based solution for managing
code deprecation in Python libraries and applications. It provides a robust mechanism
to mark deprecated code with automatic warnings that escalate to errors at specified
version thresholds, supporting both semantic versioning and date-based versioning.

Key Features:
- Zero-dependency implementation
- Thread-safe and async-compatible
- Automatic docstring integration
- Semantic and date-based version comparison
- Gradual deprecation with warning-to-error transition
- Full async support for coroutines
- 100% test coverage with mutation testing

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   quickstart
   core_concepts
   advanced_usage
   api_reference
   best_practices
   examples

-----

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
