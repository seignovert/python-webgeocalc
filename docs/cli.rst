Command line interface
======================

Some entry points are available through the command line
interface.


Kernel sets
-----------

List all the available kernel sets available on the
WebGeoCalc API:

.. code:: bash

    $ wgc-kernels --all

     - Solar System Kernels: (id: 1)
     - Latest Leapseconds Kernel: (id: 2)
     ...
     - Cassini Huygens: (id: 5)
     ...
     - SPICE Class -- Binary PCK Lesson Kernels (Earth): (id: 39)


Search a kernel by ``name`` or ``id``:

.. code:: bash

    $ wgc-kernels --kernel 'Cassini Huygens'

     - Cassini Huygens: (id: 5)

    $ wgc-kernels --kernel Cassini

    Too many kernel sets contains 'Cassini' in their names:
     - Cassini Huygens
     - SPICE Class -- CASSINI Remote Sensing Lesson Kernels


Search multiple kernels at once (``name`` and ``id`` can be mixed):

.. code:: bash

    $ wgc-kernels --kernel 5 Solar

     - Cassini Huygens: (id: 5)
     - Solar System Kernels: (id: 1)

Bodies
------

List all the bodies for a specific kernel set (by ``id`` or by ``name``):

.. code:: bash

    $ wgc-bodies 'Cassini Huygens'

     - CASSINI: (id: -82)
     - CAS: (id: -82)
    ...
     - SOLAR SYSTEM BARYCENTER: (id: 0)


Search for a specific body in a kernel set:

.. code:: bash

    $ wgc-bodies 'Cassini Huygens' --name Titan

     - TITAN: (id: 606)


Frames
------

List and search frames for a specific kernel set:

.. code:: bash

    $ wgc-frames 'Cassini Huygens' --name Titan

     - CASSINI_MIMI_PROF_TITAN: (id: -82960)
     - CASSINI_TITAN_CENTERED: (id: -82953)
     - CASSINI_SZM_TITAN: (id: -82926)
     - IAU_TITAN: (id: 10044)
     - IAU_TITANIA: (id: 10058)


Instruments
-----------

List and search instruments for a specific kernel set:

.. code:: bash

    $ wgc-instruments 'Cassini Huygens' --name ISS

     - CASSINI_ISS_WAC_RAD: (id: -82369)
     - CASSINI_ISS_NAC_RAD: (id: -82368)
     - CASSINI_ISS_WAC: (id: -82361)
     - CASSINI_ISS_NAC: (id: -82360)


Calculations
------------

The command line can submit generic and specific calculation directly
with the command line interface:

.. code:: bash

    $ wgc-calculation --help
    usage: wgc-calculation [-h] [--quiet] [--payload] [--dry-run]
                        [--KEY [VALUE [VALUE ...]]]

    Submit generic calculation to the WebGeoCalc API

    optional arguments:
    -h, --help            show this help message and exit
    --quiet, -q           Disable verbose output status.
    --payload, -p         Display payload before the calculation results.
    --dry-run, -d         Dry run. Show only the payload.
    --KEY [VALUE [VALUE ...]]
                            Key parameter and its value(s).

Example:

.. code:: bash

    $ wgc-calculation --payload \
                      --kernels 1 \
                      --times 2012-10-19T08:24:00.000 \
                      --calculation_type STATE_VECTOR \
                      --target CASSINI \
                      --observer SATURN \
                      --reference_frame IAU_SATURN \
                      --aberration_correction NONE \
                      --state_representation PLANETOGRAPHIC
    Payload:
    {
      kernels: [{'type': 'KERNEL_SET', 'id': 5}],
      times: ['2012-10-19T08:24:00.000'],
      calculationType: STATE_VECTOR,
      target: CASSINI,
      observer: SATURN,
      referenceFrame: IAU_SATURN,
      aberrationCorrection: NONE,
      stateRepresentation: PLANETOGRAPHIC,
      timeSystem: UTC,
      timeFormat: CALENDAR,
    }

    API status:
    [Calculation submit] Status: COMPLETE (id: 37d10124-a65b-44fa-9489-6c0d28cf25d2)

    Results:
    DATE:
    > 2012-10-19 08:24:00.000000 UTC
    LONGITUDE:
    > 46.18900522
    LATITUDE:
    > 21.26337134
    ALTITUDE:
    > 694259.8921163
    D_LONGITUDE_DT:
    > 0.00888655
    D_LATITUDE_DT:
    > -0.00031533
    D_ALTITUDE_DT:
    > 4.77080305
    SPEED:
    > 109.34997994
    TIME_AT_TARGET:
    > 2012-10-19 08:24:00.000000 UTC
    LIGHT_TIME:
    > 2.51438831

The *key* parameter can be in ``underscore_case`` or ``camelCase``.
Multiple *values* can be inserted after the *key* (with ``<space>`` or ``,`` separator),
as well as duplicated *keys*. Use single (``'``) or double (``"``) quotes if the
value contains spaces. Assignation with ``=`` sign can also be used:

.. code:: bash

    $ wgc-state-vector --dry-run \
                       --kernels 1 5 \
                       --times 2012-10-19T09:00:00 \
                       --times '2012-10-19T10:00:00' \
                       --target=CASSINI \
                       --observer = SATURN \
                       --referenceFrame "IAU_SATURN"
    Payload:
    {
      kernels: [{'type': 'KERNEL_SET', 'id': 1}, {'type': 'KERNEL_SET', 'id': 5}],
      times: ['2012-10-19T09:00:00', '2012-10-19T10:00:00'],
      target: CASSINI,
      observer: SATURN,
      referenceFrame: IAU_SATURN,
      calculationType: STATE_VECTOR,
      aberrationCorrection: CN,
      stateRepresentation: RECTANGULAR,
      timeSystem: UTC,
      timeFormat: CALENDAR,
    }

Here is the list of all the calculation entry point available on the CLI:

    - ``wgc-calculation``
    - ``wgc-state-vector``
    - ``wgc-angular-separation``
    - ``wgc-angular-size``
    - ``wgc-frame-transformation``
    - ``wgc-illumination-angles``
    - ``wgc-subsolar-point``
    - ``wgc-subobserver-point``
    - ``wgc-surface-intercept-point``
    - ``wgc-osculating-elements``
    - ``wgc-time-conversion``
