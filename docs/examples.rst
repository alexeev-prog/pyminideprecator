.. _examples:

########
Examples
########

Multi-threaded Application
==========================

.. code-block:: python

   from pyminideprecator import set_current_version, deprecate
   import threading

   @deprecate("2.0.0", "Legacy worker function")
   def legacy_worker():
       pass

   def worker(worker_id: int):
       set_current_version(f"1.0.{worker_id}", set_global=True)
       legacy_worker()  # Behavior depends on worker's version

   set_current_version("main_app", set_global=True)

   threads = []
   for i in range(3):
       t = threading.Thread(target=worker, args=(i,))
       threads.append(t)
       t.start()

   for t in threads:
       t.join()

Large-Scale Refactoring
=======================

.. code-block:: python

   # legacy.py
   class LegacySystem:
       @deprecate("3.0.0", "Old authentication", error_version="2.3.0")
       async def authenticate(self, user) -> bool:
           return True

   # migration.py
   from pyminideprecator import set_current_version

   set_current_version("2.0.0", set_global=True)
   legacy = LegacySystem()

   # During migration
   await legacy.authenticate(user)  # Warning

   # After upgrade
   set_current_version("2.3.0", set_global=True)
   await legacy.authenticate(user)  # Raises DeprecatedError
