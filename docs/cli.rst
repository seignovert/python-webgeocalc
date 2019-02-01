Call the API from the command line
==================================

Kernel sets
-----------

List and search kernel sets available in WebGeocalc API (``/kernel_sets``):

.. code:: bash

    wgc-kernels


.. parsed-literal::

    usage: wgc-kernels [-h] [--all] [--kernel NAME|ID [NAME|ID ...]]

    List and search kernel sets available in WebGeocalc API.

    optional arguments:
      -h, --help            show this help message and exit
      --all, -a             List all kernel sets available
      --kernel NAME|ID [NAME|ID ...], -k NAME|ID [NAME|ID ...]
                            Search a specific kernel by name or id


List all the available kernels:

.. code:: bash

    wgc-kernels --all


.. parsed-literal::

     - Solar System Kernels: (id: 1)
     - Latest Leapseconds Kernel: (id: 2)
     ...
     - Cassini Huygens: (id: 5)
     ...
     - SPICE Class -- Binary PCK Lesson Kernels (Earth): (id: 39)


Search a kernel by ``name`` or ``id``:

.. code:: bash

    wgc-kernels --kernel Cassini


.. parsed-literal::

    Too many kernel sets contains 'Cassini' in their names:
     - Cassini Huygens
     - SPICE Class -- CASSINI Remote Sensing Lesson Kernels


.. code:: bash

    wgc-kernels --kernel 'Cassini Huygens'


.. parsed-literal::

     - Cassini Huygens: (id: 5)


Search multiple kernels at once (``name`` and ``id`` can be mixed):

.. code:: bash

    wgc-kernels --kernel 5 'Solar'


.. parsed-literal::

     - Cassini Huygens: (id: 5)
     - Solar System Kernels: (id: 1)


Bodies
------

List all the bodies (``/kernel-set/{kernelSetId}/bodies``)
for a specific kernel set (by ``id`` or by ``name``):

.. code:: bash

    wgc-bodies 'Cassini Huygens'


.. parsed-literal::

     - CASSINI: (id: -82)
     - CAS: (id: -82)
    ...
     - SOLAR SYSTEM BARYCENTER: (id: 0)


Search for a specific body in a kernel set:

.. code:: bash

    wgc-bodies 'Cassini Huygens' --name Titan


.. parsed-literal::

     - TITAN: (id: 606)


Frames
------

List and search frames (``/kernel-set/{kernelSetId}/frames``)
for a specific kernel set:

.. code:: bash

    wgc-frames 'Cassini Huygens' --name Titan


.. parsed-literal::

     - CASSINI_MIMI_PROF_TITAN: (id: -82960)
     - CASSINI_TITAN_CENTERED: (id: -82953)
     - CASSINI_SZM_TITAN: (id: -82926)
     - IAU_TITAN: (id: 10044)
     - IAU_TITANIA: (id: 10058)


Instruments
-----------

List and search instruments (``/kernel-set/{kernelSetId}/instruments``)
for a specific kernel set:

.. code:: bash

    wgc-instruments 'Cassini Huygens' --name ISS


.. parsed-literal::

     - CASSINI_ISS_WAC_RAD: (id: -82369)
     - CASSINI_ISS_NAC_RAD: (id: -82368)
     - CASSINI_ISS_WAC: (id: -82361)
     - CASSINI_ISS_NAC: (id: -82360)
