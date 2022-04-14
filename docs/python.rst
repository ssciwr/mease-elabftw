Python Interface
================

To import the library:

.. code-block:: python

   >>> import mease_elabftw


Listing experiments
-------------------

To get a list of the experiments belong to user "Liam":

.. code-block:: python

   >>> import mease_elabftw
   >>> from pprint import pprint
   >>> pprint(mease_elabftw.list_experiments("Liam"))
   ['163: test fake experiment without json metadata (Liam Keegan, 2021-10-07)',
    '156: test fake experiment with json metadata (Liam Keegan, 2021-10-01)']


NWB metadata
------------

To get a dict of the NWB metadata of the experiment with id ``156``:

.. code-block:: python

   >>> import mease_elabftw
   >>> metadata = mease_elabftw.get_nwb_metadata(156)
   >>> metadata["NWBFile"]["session_description"]
   test fake experiment with json metadata
   >>> metadata["NWBFile"]["identifier"]
   20211001-8b6f100d66f4312d539c52620f79d6a503c1e2d1

Upload a file
-------------

To upload the file "results.csv" to the experiment with id ``156``:

.. code-block:: python

   >>> import mease_elabftw
   mease_elabftw.upload_file(156, "results.csv")
