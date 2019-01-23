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

Note the user
-------------

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

    >>> API.kernel_sets() # /kernel-sets
    [
        <KernelSetDetails> Solar System Kernels (id: 1),
        ...
        <KernelSetDetails> Cassini Huygens (id: 5),
        ...
        <KernelSetDetails> SPICE Class -- Binary PCK Lesson Kernels (Earth) (id: 39)
    ]

    >>> API.bodies(5) # /kernel-sets/{kernelSetId}/bodies
    [
        <BodyData> CASSINI (id: -82),
        <BodyData> CAS (id: -82),
        ...
        <BodyData> SOLAR SYSTEM BARYCENTER (id: 0)
    ]

    >>> API.frames('Cassini Huygens') # /kernel-sets/{kernelSetId}/frames
    [
        <FrameData> CASSINI_SATURN_SKR4N_LOCK (id: -82982),
        ...
        <FrameData> ITRF93 (id: 13000)
    ]

    >>> API.instruments('Cassini Huygens') # /kernel-set/{kernelSetId}/intruments
    [
        <InstrumentData> CASSINI_CIRS_RAD (id: -82898),
        ...
        <InstrumentData> CASSINI_SRU-A (id: -82001)
    ]


Prepare calculation payload:

.. code:: python

    >>> from webgeocalc import Calculation

    >>> calc = Calculation(
        kernels = 'Cassini Huygens',
        times = '2012-10-19T08:24:00.000',
        calculation_type = 'STATE_VECTOR',
        target = 'CASSINI',
        observer = 'SATURN',
        reference_frame = 'IAU_SATURN',
        aberration_correction = 'NONE',
        state_representation = 'PLANETOGRAPHIC',
    )

    >>> calc.payload
    {
        'kernels': [{'type': 'KERNEL_SET', 'id': 5}],
        'times': ['2012-10-19T08:24:00.000'],
        'calculationType': 'STATE_VECTOR',
        'target': 'CASSINI',
        'observer': 'SATURN',
        'referenceFrame': 'IAU_SATURN',
        'aberrationCorrection': 'NONE',
        'stateRepresentation': 'PLANETOGRAPHIC',
        'timeSystem': 'UTC',
        'timeFormat': 'CALENDAR'
    }

Run calculation:

.. code:: python

    >>> calc.submit()
    [Calculation submitted] Status: LOADING_KERNELS (id: 19fd1c05-3bfe-47c7-bd16-28612249ae89)

    >>> calc.update()
    [Calculation update] Status: COMPLETE (id: 19fd1c05-3bfe-47c7-bd16-28612249ae89)

    >>> calc.results
    {
        'DATE': '2012-10-19 08:24:00.000000 UTC',
        'LONGITUDE': 46.18900522,
        'LATITUDE': 21.26337134,
        'ALTITUDE': 694259.8921163,
        'D_LONGITUDE_DT': 0.00888655,
        'D_LATITUDE_DT': -0.00031533,
        'D_ALTITUDE_DT': 4.77080305,
        'SPEED': 109.34997994,
        'TIME_AT_TARGET': '2012-10-19 08:24:00.000000 UTC',
        'LIGHT_TIME': 2.51438831
    }

More details can be found in the `Jupyter Notebooks`_.

.. _`Jupyter Notebooks`: https://nbviewer.jupyter.org/github/seignovert/python-webgeocalc/blob/master/examples/api.ipynb

Disclaimer
----------
This project is not supported or endorsed by either JPL, NAIF or NASA.
The code is provided *"as is"*, use at your own risk.
