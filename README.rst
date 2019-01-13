Python package for NAIF WebGeoCalc API
======================================

|Build| |Coverage| |PyPI| |Status| |Version| |Python| |License| |Examples|

.. |Build| image:: https://travis-ci.org/seignovert/python-webgeocalc.svg?branch=master
        :target: https://travis-ci.org/seignovert/python-webgeocalc
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

Install
-------
With ``pip``:

.. code:: bash

    $ pip install webgeocalc

With the ``source files``:

.. code:: bash

    $ git clone https://github.com/seignovert/python-webgeocalc.git webgeocalc
    $ cd webgeocalc ; python setup.py install

Usage
-----

.. code:: python

    >>> from webgeocalc import API

    >>> API.url
    'https://wgc2.jpl.nasa.gov:8443/webgeocalc/api'

    >>> kernels = API.kernel_sets() # /kernel-sets
    [
        <KernelSetDetails> Solar System Kernels (id: 1),
        <KernelSetDetails> Latest Leapseconds Kernel (id: 2),
        ...
        <KernelSetDetails> SPICE Class -- Binary PCK Lesson Kernels (Earth) (id: 39)
    ]

    >>> kernel = kernels[0]
    >>> int(kernel) # kernelSetId
    1

    >>> str(kernel) # Caption
    'Solar System Kernels'

    >>> kernel.description
    'Generic kernels for planets, satellites, and some asteroids covering from 1950-01-01 to 2050-01-01.'

    >>> kernel.keys()
    dict_keys(['caption', 'sclkId', 'description', 'kernelSetId', 'missionId'])

    >>> kernel.values()
    dict_values(['Solar System Kernels', '0', 'Generic kernels for planets, satellites, and some asteroids covering from 1950-01-01 to 2050-01-01.', '1', 'gen'])


Disclaimer
----------
This project is not supported or endorsed by either JPL, NAIF or NASA.
The code is provided *"as is"*, use at your own risk.
