.. _advanced_usage:

################
Advanced Usage
################

Property Deprecation
====================

.. code-block:: python

   class UserProfile:
       @property
       @deprecate("3.0.0", "Use full_name instead")
       def name(self) -> str:
           return self._name

Custom Warning Types
====================

.. code-block:: python

   @deprecate("4.0.0", "Experimental feature", category=FutureWarning)
   def experimental_feature():
       pass

Early Error Enforcement
=======================

.. code-block:: python

   @deprecate(
       remove_version="2.0.0",
       message="Migrate to new_system()",
       error_version="1.5.0"  # Errors start in 1.5.0
   )
   def legacy_system():
       pass

Context-Specific Version Overrides
==================================

.. code-block:: python

   from pyminideprecator import scoped_version

   set_current_version("1.0.0", set_global=True)

   with scoped_version("2.0.0"):
       legacy_function()  # Raises DeprecatedError
