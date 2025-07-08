.. _quickstart:

###########
Quick Start
###########

Basic Function Deprecation
==========================

.. code-block:: python

   from pyminideprecator import deprecate, set_current_version

   # Set current application version
   set_current_version("1.2.0", set_global=True)

   @deprecate(
       remove_version="2.0.0",
       message="Legacy API function",
       instead="new_api()",
       since="1.0.0"
   )
   def old_api() -> str:
       return "legacy data"

   # Generates DeprecationWarning
   result = old_api()

Async Function Deprecation
==========================

.. code-block:: python

   from pyminideprecator import deprecate, set_current_version

   set_current_version("1.5.0", set_global=True)

   @deprecate("2.0.0", "Async processor will be removed")
   async def async_data_processor(input: str) -> str:
       await asyncio.sleep(0.1)
       return processed_data

   async def main():
       result = await async_data_processor("sample")  # Warning

Class Deprecation
=================

.. code-block:: python

   from pyminideprecator import deprecate

   @deprecate("2024.01.01", "Old database client", instead="NewDBClient")
   class OldDBClient:
       def __init__(self, url: str):
           self.url = url

       def query(self, sql: str) -> list:
           return ["result1", "result2"]

   # Shows warning on instantiation
   client = OldDBClient("db://localhost")
