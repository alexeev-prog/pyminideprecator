.. _best_practices:

################
Best Practices
################

1. Always Provide Alternatives
==============================

.. code-block:: python

   @deprecate("3.0.0", "Old data format", instead="json.loads()")
   def parse_legacy(data):
       pass

2. Use Gradual Enforcement
==========================

.. code-block:: python

   @deprecate(
       remove_version="4.0.0",
       message="Phase out old protocol",
       error_version="3.5.0"  # Gives migration time
   )
   def old_protocol():
       pass

3. Maintain Documentation Context
=================================

.. code-block:: python

   @deprecate("2.0.0", "Replaced by quantum_algorithm()")
   def classical_algorithm():
       """Original algorithm documentation"""

4. Test Deprecation Lifecycle
=============================

.. code-block:: python

   def test_deprecation_phases():
       with scoped_version("1.0.0"):
           with pytest.warns(DeprecationWarning):
               deprecated_function()

       with scoped_version("2.0.0"):
           with pytest.raises(DeprecatedError):
               deprecated_function()

5. Consistent Versioning Schemes
================================

.. code-block:: python

   # Recommended:
   set_current_version("1.2.3", set_global=True)
   set_current_version("2025.12.31", set_global=True)

   # Not supported:
   set_current_version("1.2025.01")
