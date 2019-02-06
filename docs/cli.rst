Command line interface
======================

Some entry points are available through the command line
interface to get the list of available kernels, the body
objects, the frames and instruments available on the
WebGeoCalc API.

.. note::

    For now, calculation can not be submitted directly
    through the command line.


Kernel sets
-----------

List all the available kernel sets:

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

    $ wgc-kernels --kernel 5 'Solar'

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
