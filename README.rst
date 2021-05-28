Python package for NAIF WebGeoCalc API
======================================

|Docs| |Build| |Coverage| |CodeFactor|

|PyPI|  |Python| |Version| |Status|

|DOI| |License|

|Examples|

.. |Docs| image:: https://img.shields.io/readthedocs/webgeocalc.svg?label=Docs&logo=read-the-docs&logoColor=white
        :target: https://webgeocalc.readthedocs.io/
.. |Build| image:: https://github.com/seignovert/python-webgeocalc/workflows/Continuous%20Integration/badge.svg
        :target: https://github.com/seignovert/python-webgeocalc/actions/workflows/actions.yml
.. |Coverage| image:: https://img.shields.io/codecov/c/github/seignovert/python-webgeocalc.svg?label=Codecov&logo=codecov&logoColor=white
              :target: https://codecov.io/gh/seignovert/python-webgeocalc
.. |CodeFactor| image:: https://www.codefactor.io/repository/github/seignovert/python-webgeocalc/badge/main
                :target: https://www.codefactor.io/repository/github/seignovert/python-webgeocalc/overview/main
.. |PyPI| image:: https://img.shields.io/badge/PyPI-webgeocalc-blue.svg?logo=python&logoColor=white
        :target: https://pypi.org/project/webgeocalc
.. |Python| image:: https://img.shields.io/pypi/pyversions/webgeocalc.svg?label=Python
        :target: https://pypi.org/project/webgeocalc
.. |Version| image:: https://img.shields.io/pypi/v/webgeocalc.svg?label=Version
        :target: https://pypi.org/project/webgeocalc
.. |Status| image:: https://img.shields.io/pypi/status/webgeocalc.svg?label=Status
        :target: https://pypi.org/project/webgeocalc
.. |DOI| image:: https://zenodo.org/badge/165558532.svg
        :target: https://zenodo.org/badge/latestdoi/165558532
.. |License| image:: https://img.shields.io/github/license/seignovert/python-webgeocalc.svg?label=License
             :target: https://github.com/seignovert/python-webgeocalc/
.. |Examples| image:: https://img.shields.io/badge/Jupyter%20Notebook-examples-blue.svg?logo=jupyter&logoColor=orange
        :target: https://nbviewer.jupyter.org/github/seignovert/python-webgeocalc/blob/main/examples/api.ipynb


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

Note the user
-------------

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


Usage
-----

.. code:: python

    >>> from webgeocalc import API

    >>> API.url
    'https://wgc2.jpl.nasa.gov:8443/webgeocalc/api'

    >>> API.kernel_sets() # /kernel-sets
    [<KernelSetDetails> Solar System Kernels (id: 1),
     ...
     <KernelSetDetails> Cassini Huygens (id: 5),
     ...
     <KernelSetDetails> SPICE Class -- Binary PCK Lesson Kernels (Earth) (id: 39)]

    >>> API.bodies(5) # /kernel-sets/{kernelSetId}/bodies
    [<BodyData> CASSINI (id: -82),
     ...
     <BodyData> SOLAR SYSTEM BARYCENTER (id: 0)]

    >>> API.frames('Cassini Huygens') # /kernel-sets/{kernelSetId}/frames
    [<FrameData> CASSINI_SATURN_SKR4N_LOCK (id: -82982),
     ...
     <FrameData> ITRF93 (id: 13000)]

    >>> API.instruments('Cassini Huygens') # /kernel-set/{kernelSetId}/instruments
    [<InstrumentData> CASSINI_CIRS_RAD (id: -82898),
     ...
     <InstrumentData> CASSINI_SRU-A (id: -82001)]


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
    {'kernels': [{'type': 'KERNEL_SET', 'id': 5}],
     'times': ['2012-10-19T08:24:00.000'],
     'calculationType': 'STATE_VECTOR',
     'target': 'CASSINI',
     'observer': 'SATURN',
     'referenceFrame': 'IAU_SATURN',
     'aberrationCorrection': 'NONE',
     'stateRepresentation': 'PLANETOGRAPHIC',
     'timeSystem': 'UTC',
     'timeFormat': 'CALENDAR'}

Run calculation:

.. code:: python

    >>> calc.run()
    [Calculation submitted] Status: LOADING_KERNELS (id: 19fd1c05-3bfe-47c7-bd16-28612249ae89)
    [Calculation update] Status: COMPLETE (id: 19fd1c05-3bfe-47c7-bd16-28612249ae89)
    {'DATE': '2012-10-19 08:24:00.000000 UTC',
     'LONGITUDE': 46.18900522,
     'LATITUDE': 21.26337134,
     'ALTITUDE': 694259.8921163,
     'D_LONGITUDE_DT': 0.00888655,
     'D_LATITUDE_DT': -0.00031533,
     'D_ALTITUDE_DT': 4.77080305,
     'SPEED': 109.34997994,
     'TIME_AT_TARGET': '2012-10-19 08:24:00.000000 UTC',
     'LIGHT_TIME': 2.51438831}

    >>> from webgeocalc import AngularSeparation

More details can be found in the `docs`_ and in the `Jupyter Notebooks`_.

.. _`docs`: https://webgeocalc.readthedocs.io/en/stable/calculation.html
.. _`Jupyter Notebooks`: https://nbviewer.jupyter.org/github/seignovert/python-webgeocalc/blob/main/examples/calculation.ipynb

Command Line Interface (cli)
----------------------------

The webgeocalc API can be call directly from the command line interface:

.. code:: bash

    $ wgc-kernels --all
     - Solar System Kernels: (id: 1)
    ...
     - Cassini Huygens: (id: 5)
    ...
     - SPICE Class -- Binary PCK Lesson Kernels (Earth): (id: 39)

    $ wgc-instruments 'Cassini Huygens' --name ISS
     - CASSINI_ISS_WAC_RAD: (id: -82369)
     - CASSINI_ISS_NAC_RAD: (id: -82368)
     - CASSINI_ISS_WAC: (id: -82361)
     - CASSINI_ISS_NAC: (id: -82360)

    $ wgc-state-vector --kernels 5 \
                       --times 2012-10-19T09:00:00 \
                       --target CASSINI \
                       --observer SATURN \
                       --reference_frame IAU_SATURN
    API status:
    [Calculation submit] Status: COMPLETE (id: 041bf912-178f-4450-b787-12a49c8a3101)

    Results:
    DATE:
    > 2012-10-19 09:00:00.000000 UTC
    DISTANCE:
    > 764142.63776247
    SPEED:
    > 111.54765899
    X:
    > 298292.85744169
    Y:
    > -651606.58468976
    Z:
    > 265224.81187627
    D_X_DT:
    > -98.8032491
    D_Y_DT:
    > -51.73211296
    D_Z_DT:
    > -2.1416539
    TIME_AT_TARGET:
    > 2012-10-19 08:59:57.451094 UTC
    LIGHT_TIME:
    > 2.54890548

More examples can be found in here_.

.. _here: https://webgeocalc.readthedocs.io/en/stable/cli.html


Local development and testing
-----------------------------

Setup:
```bash
pip install -e .
pip install -r tests/requirements.txt -r docs/requirements.txt
```

Linter:
```bash
flake8 setup.py docs/conf.py tests/ webgeocalc/
pylint webgeocalc/ tests/*.py
```

Pytest:
```bash
pytest --cov=webgeocalc/ tests/
pytest --nbval-lax examples/
```

Docs:
```bash
sphinx-build docs docs/_build --color -W -bhtml
sphinx-build docs docs/_build --color -W -bdoctest
```


Disclaimer
----------
This project is not supported or endorsed by either JPL, NAIF or NASA.
The code is provided *"as is"*, use at your own risk.
