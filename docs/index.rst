Python package for NAIF WebGeoCalc API
======================================

|Build| |Docs| |Coverage| |PyPI| |Status| |Version| |Python|
|License| |Examples|

.. |Build| image:: https://travis-ci.org/seignovert/python-webgeocalc.svg?branch=master
        :target: https://travis-ci.org/seignovert/python-webgeocalc
.. |Docs| image:: https://readthedocs.org/projects/webgeocalc/badge/?version=latest
        :target: http://webgeocalc.readthedocs.io/en/latest/?badge=latest
.. |Coverage| image:: https://coveralls.io/repos/github/seignovert/python-webgeocalc/badge.svg?branch=master
        :target: https://coveralls.io/github/seignovert/python-webgeocalc?branch=master
.. |PyPI| image:: https://img.shields.io/badge/PyPI-webgeocalc-blue.svg
        :target: https://pypi.org/project/webgeocalc
.. |Status| image:: https://img.shields.io/pypi/status/webgeocalc.svg?label=Status
        :target: https://pypi.org/project/webgeocalc
.. |Version| image:: https://img.shields.io/pypi/v/webgeocalc.svg?label=Version
        :target: https://pypi.org/project/webgeocalc
.. |Python| image:: https://img.shields.io/pypi/pyversions/webgeocalc.svg?label=Python
        :target: https://pypi.org/project/webgeocalc
.. |License| image:: https://img.shields.io/pypi/l/webgeocalc.svg?label=License
        :target: https://pypi.org/project/webgeocalc
.. |Examples| image:: https://img.shields.io/badge/Jupyter%20Notebook-examples-blue.svg
        :target: https://nbviewer.jupyter.org/github/seignovert/python-webgeocalc/blob/master/examples/api.ipynb


In december 2018, `JPL/NAIF`_ announced an **experimental**
`API RESTful interface`_ for their new `WebGeocalc server`_
(which make online SPICE calculations).
Documentation_ and `JavaScript examples`_ are already available.

This package is an **early attempt** to provide a Python interface to
make SPICE calculation through this API.

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


Documentation
-------------

.. toctree::
   :maxdepth: 2

   api
   calculation
   cli

.. note::

    This project is not supported or endorsed by either JPL, NAIF or NASA.
    The code is provided *"as is"*, use at your own risk.
