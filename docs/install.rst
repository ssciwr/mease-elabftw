Installation
============

To install using pip:

.. code-block:: bash

    python -m pip install git+https://github.com/ssciwr/mease-elabftw

You also need to generate an API key in eLabFTW (User Panel -> API Keys -> GENERATE AN API KEY),
and then set the environment variable `ELABFTW_TOKEN` to this key, e.g.

.. code-block:: bash

    export ELABFTW_TOKEN=abc123abc123abc123

This key is needed to authenticate requests to the eLabFTW server.
