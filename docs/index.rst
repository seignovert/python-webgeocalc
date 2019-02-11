Python package for NAIF WebGeoCalc API
======================================

|Docs| |Build| |Coverage|

|PyPI| |Python| |Version| |Status| |License|

|Examples|

.. |Docs| image:: https://img.shields.io/readthedocs/webgeocalc.svg?label=Docs&logo=read-the-docs&logoColor=white
        :target: https://webgeocalc.readthedocs.io/
.. |Build| image:: https://img.shields.io/travis/seignovert/python-webgeocalc.svg?label=CI&logo=travis-ci&logoColor=white
        :target: https://travis-ci.org/seignovert/python-webgeocalc
.. |Coverage| image:: https://img.shields.io/coveralls/github/seignovert/python-webgeocalc.svg?label=Coverage
        :target: https://coveralls.io/github/seignovert/python-webgeocalc?branch=master
.. |PyPI| image:: https://img.shields.io/badge/PyPI-webgeocalc-blue.svg?logo=python&logoColor=white
        :target: https://pypi.org/project/webgeocalc
.. |Python| image:: https://img.shields.io/pypi/pyversions/webgeocalc.svg?label=Python
        :target: https://pypi.org/project/webgeocalc
.. |Version| image:: https://img.shields.io/pypi/v/webgeocalc.svg?label=Version
        :target: https://pypi.org/project/webgeocalc
.. |Status| image:: https://img.shields.io/pypi/status/webgeocalc.svg?label=Status
        :target: https://pypi.org/project/webgeocalc
.. |License| image:: https://img.shields.io/pypi/l/webgeocalc.svg?label=License
        :target: https://pypi.org/project/webgeocalc
.. |Examples| image:: https://img.shields.io/badge/Jupyter%20Notebook-examples-blue.svg?logo=jupyter&logoColor=orange
        :target: https://nbviewer.jupyter.org/github/seignovert/python-webgeocalc/blob/master/examples/api.ipynb


In december 2018, `JPL/NAIF`_ announced an **experimental**
`API RESTful interface`_ for their new `WebGeocalc server`_
(which make online SPICE calculations).
Documentation_ and `JavaScript examples`_ are already available.

This package provides a Python interface to make SPICE
calculations through this API.

.. _`JPL/NAIF`: https://naif.jpl.nasa.gov/naif/webgeocalc.html
.. _`API RESTful interface`: https://naif.jpl.nasa.gov/naif/WebGeocalc_announcement.pdf
.. _`WebGeocalc server`: https://wgc2.jpl.nasa.gov:8443/webgeocalc
.. _Documentation: https://wgc2.jpl.nasa.gov:8443/webgeocalc/documents/api-info.html
.. _`JavaScript examples`: https://wgc2.jpl.nasa.gov:8443/webgeocalc/example/perform-calculation.html


.. caution::

    `WebGeoCalc`_ is not design to handle heavy calculation.
    If you need to make intensive queries, use `Spiceypy`_ or `SpiceMiner`_
    package with locally hosted kernels.

.. _`WebGeocalc`: https://wgc.jpl.nasa.gov:8443/webgeocalc
.. _`Spiceypy`: https://github.com/AndrewAnnex/Spiceypy
.. _`SpiceMiner`: https://github.com/DaRasch/spiceminer

Install
-------
With ``pip``:

.. code:: bash

    $ pip install webgeocalc

With ``conda``:

.. code:: bash

    $ conda install -c seignovert webgeocalc

From the sources:

.. code:: bash

    $ git clone https://github.com/seignovert/python-webgeocalc.git webgeocalc
    $ cd webgeocalc
    $ python setup.py install


Documentation
-------------

.. toctree::
   :maxdepth: 2

   api
   calculation
   cli

.. important::

    This project is not supported or endorsed by either JPL, NAIF or NASA.
    The code is provided *"as is"*, use at your own risk.
