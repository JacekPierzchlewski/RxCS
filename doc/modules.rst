RxCS modules documentation
==========================


The modules in the RxCS toolbox can be diveded into two categories:

    1. **API modules**. These modules contain API functions which can be called directly by a user. |br|
       The API function name do not begin with *'_'* (an underscore character).  |br|
       Please not that these modules may also contain non-API functions, which begin with *'_'* (an underscore character). |br| |br|

    2. **Internal RxCS modules**. These modules contain only non-API functions which are internal for  RxCS. |br|
       The non-API function name always begin with *'_'* (an underscore character).

This section contains list of API functions from the API modules modules which are present in the RxCS toolbox. |br|
For description of other functions please refer directly to a module source file.


.. warning::
   Do not use non-API functions unless you realy know what you are doing!


PLEASE NOTE: To preserve code simplicity RxCS toolbox do not use objects (classes).


1. API modules - signal generators:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

6.1 rxcs.sig.sigRandMult:
-------------------------

.. automodule:: sigRandMult
   :members: main


2. API modules - signal acquisition:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


3. API modules - CS signal processing:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


4. API modules - system analysis:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


5. API modules - main frames:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


6. API modules - auxiliary modules:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

6.1 rxcs.console:
------------------------

.. automodule:: console
   :members: pack, progress, module_progress, module_progress_done, warning, info, bullet_info, note, param, bullet_param

7. Test scripts (rxcs/test):
~~~~~~~~~~~~~~~~

7.1 :sigRandMult_test:
------------------------

.. automodule:: sigRandMult_test


.. |br| raw:: html

   <br />
