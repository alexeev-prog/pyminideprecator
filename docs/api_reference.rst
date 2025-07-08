.. _api_reference:

#############
API Reference
#############

Decorator
=========

.. autofunction:: pyminideprecator.deprecate

Version Management
==================

.. autofunction:: pyminideprecator.set_current_version
.. autofunction:: pyminideprecator.get_current_version
.. autofunction:: pyminideprecator.scoped_version

Version Class
=============

.. autoclass:: pyminideprecator.Version
   :members:
   :special-members: __eq__, __lt__, __ge__

Exceptions
==========

.. autoexception:: pyminideprecator.DeprecatedError
