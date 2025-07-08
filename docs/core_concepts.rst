.. _core_concepts:

##############
Core Concepts
##############

Version Management System
=========================

pyminideprecator supports two versioning schemes:

1. **Semantic Versioning (SemVer)**
   - Format: ``MAJOR.MINOR.PATCH`` (e.g., ``1.2.3``)
   - Numeric ordering (``1.2.3 < 1.2.4 < 2.0.0``)

2. **Date-based Versioning**
   - Format: ``YYYY.MM.DD`` (e.g., ``2025.12.31``)
   - Chronological ordering

Thread-Safe Context-aware Execution
===================================

pyminideprecator uses a hybrid approach for version management:

.. code-block:: python

   import threading
   from pyminideprecator import set_current_version, get_current_version

   # Set global version in main thread
   set_current_version("1.0.0", set_global=True)

   def worker():
       # Set thread-specific global version
       set_current_version("2.0.0", set_global=True)
       print(f"Worker version: {get_current_version()}")  # 2.0.0

   t = threading.Thread(target=worker)
   t.start()
   t.join()

   print(f"Main version: {get_current_version()}")  # 1.0.0

Lifecycle Management
====================

Deprecations follow a three-phase lifecycle:

.. mermaid::

   graph LR
       A[Current Version < Error Version] --> B[Warning Phase]
       B --> C[Usable with warnings]
       D[Current Version >= Error Version] --> E[Error Phase]
       E --> F[Usage raises DeprecatedError]
       G[Current Version >= Removal Version] --> H[Removed]
