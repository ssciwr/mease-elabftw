Command Line Interface
======================

The ``elabftw-list`` command prints a list of experiments:

.. code-block:: bash

   $ elabftw-list --help
   Usage: elabftw-list [OPTIONS] [OWNER]

     Prints a list of eLabFTW experiments belonging to OWNER

     If OWNER is not specified, all experiments are printed.

   Options:
     --help  Show this message and exit.


Example of use:

.. code-block:: bash

   $ elabftw-list Liam
   163: test fake experiment without json metadata (Liam Keegan, 2021-10-07)
   156: test fake experiment with json metadata (Liam Keegan, 2021-10-01)
