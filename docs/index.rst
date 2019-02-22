Python package for NAIF WebGeoCalc API
======================================

|Docs| |Build| |Coverage| |CodeFactor|

|PyPI| |Conda|

|Python| |Version| |Status| |Conda Platform|

|DOI| |License|

|Examples|

.. |Docs| image:: https://img.shields.io/readthedocs/webgeocalc.svg?label=Docs&logo=read-the-docs&logoColor=white
        :target: https://webgeocalc.readthedocs.io/
.. |Build| image:: https://img.shields.io/travis/seignovert/python-webgeocalc.svg?label=Build&logo=travis-ci&logoColor=white
        :target: https://travis-ci.org/seignovert/python-webgeocalc
.. |Coverage| image:: https://img.shields.io/codecov/c/github/seignovert/python-webgeocalc.svg?label=Codecov&logo=codecov&logoColor=white
              :target: https://codecov.io/gh/seignovert/python-webgeocalc
.. |CodeFactor| image:: https://www.codefactor.io/repository/github/seignovert/python-webgeocalc/badge/master
                :target: https://www.codefactor.io/repository/github/seignovert/python-webgeocalc/overview/master
.. |PyPI| image:: https://img.shields.io/badge/PyPI-webgeocalc-blue.svg?logo=python&logoColor=white
        :target: https://pypi.org/project/webgeocalc
.. |Conda| image:: https://img.shields.io/badge/conda|seignovert-webgeocalc-blue.svg?logo=python&logoColor=white
        :target: https://anaconda.org/seignovert/webgeocalc
.. |Python| image:: https://img.shields.io/pypi/pyversions/webgeocalc.svg?label=Python
        :target: https://pypi.org/project/webgeocalc
.. |Conda Platform| image:: https://img.shields.io/conda/pn/seignovert/webgeocalc.svg
          :target: https://anaconda.org/seignovert/webgeocalc
.. |Version| image:: https://img.shields.io/pypi/v/webgeocalc.svg?label=Version
        :target: https://pypi.org/project/webgeocalc
.. |Status| image:: https://img.shields.io/pypi/status/webgeocalc.svg?label=Status
        :target: https://pypi.org/project/webgeocalc
.. |DOI| image:: https://zenodo.org/badge/165558532.svg
        :target: https://zenodo.org/badge/latestdoi/165558532
.. |License| image:: https://img.shields.io/github/license/seignovert/python-webgeocalc.svg?label=License
             :target: https://github.com/seignovert/python-webgeocalc/
.. |Examples| image:: https://img.shields.io/badge/Jupyter%20Notebook-examples-blue.svg?logo=jupyter&logoColor=orange
        :target: https://nbviewer.jupyter.org/github/seignovert/python-webgeocalc/blob/master/examples/api.ipynb


In december 2018, `JPL/NAIF`_ announced an **experimental**
`API RESTful interface`_ for their new `WebGeoCalc server`_
(which make online SPICE calculations).
Documentation_ and `JavaScript examples`_ are already available.

This package provides a Python interface to make SPICE
calculations through this API.

.. _`JPL/NAIF`: https://naif.jpl.nasa.gov/naif/webgeocalc.html
.. _`API RESTful interface`: https://naif.jpl.nasa.gov/naif/WebGeocalc_announcement.pdf
.. _`WebGeoCalc server`: https://wgc2.jpl.nasa.gov:8443/webgeocalc
.. _Documentation: https://wgc2.jpl.nasa.gov:8443/webgeocalc/documents/api-info.html
.. _`JavaScript examples`: https://wgc2.jpl.nasa.gov:8443/webgeocalc/example/perform-calculation.html


.. caution::

    `WebGeoCalc`_ is not design to handle heavy calculation.
    If you need to make intensive queries, use `Spiceypy`_ or `SpiceMiner`_
    package with locally hosted kernels.

.. _`WebGeoCalc`: https://wgc.jpl.nasa.gov:8443/webgeocalc
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
