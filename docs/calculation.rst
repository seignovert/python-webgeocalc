WebGeoCalc calculations
=======================

.. currentmodule:: webgeocalc.calculation

For now only the geometry calculations are implemented:

- :py:class:`StateVector`
- :py:class:`AngularSeparation`
- :py:class:`AngularSize`
- :py:class:`FrameTransformation`
- :py:class:`IlluminationAngles`
- :py:class:`SubSolarPoint`
- :py:class:`SubObserverPoint`
- :py:class:`SurfaceInterceptPoint`
- :py:class:`OsculatingElements`
- :py:class:`TimeConversion`

Import generic WebGeoCalc calculation object:

>>> from webgeocalc import Calculation

or import specific WebGeoCalc calculation object:

>>> from webgeocalc import StateVector, AngularSeparation

Inputs examples and payloads
----------------------------

All WebGeoCalc calculation objects take their input attributes in
``underscore_case`` format.

>>> calc = StateVector(
...    kernels = 5,
...    times = '2012-10-19T08:24:00.000',
...    calculation_type = 'STATE_VECTOR',
...    target = 'CASSINI',
...    observer = 'SATURN',
...    reference_frame = 'IAU_SATURN',
...    aberration_correction = 'NONE',
...    state_representation = 'PLANETOGRAPHIC',
... )

The payload that will be submitted to
the WebGeoCalc API can be retrieve with the
property :py:attr:`Calculation.payload`:

>>> calc.payload   # doctest: +SKIP
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

Example of :py:class:`StateVector` calculation with multi :py:attr:`kernels`
inputs (requested by ``name`` in this case), with multiple :py:attr:`times`
inputs for :py:attr:`target`, :py:attr:`observer` and :py:attr:`frame`
requested by ``id``:

>>> StateVector(
...    kernels = ['Solar System Kernels', 'Cassini Huygens'],
...    times = ['2012-10-19T07:00:00', '2012-10-19T09:00:00'],
...    target = -82,             # CASSINI
...    observer = 699,           # SATURN
...    reference_frame = 10016,  # IAU_SATURN
... ).payload   # doctest: +SKIP
{
    'kernels': [
        {'type': 'KERNEL_SET', 'id': 1},
        {'type': 'KERNEL_SET', 'id': 5}
    ],
    'times': ['2012-10-19T07:00:00', '2012-10-19T09:00:00'],
    'target': -82,
    'observer': 699,
    'referenceFrame': 10016,
    'calculationType': 'STATE_VECTOR',
    'aberrationCorrection': 'CN',
    'stateRepresentation': 'RECTANGULAR',
    'timeSystem': 'UTC',
    'timeFormat': 'CALENDAR'
}


Example of :py:class:`AngularSeparation` calculation
with specific :py:attr:`kernel_paths` and multiple :py:attr:`intervals`:

>>> AngularSeparation(
...    kernel_paths = [
...         'pds/wgc/kernels/lsk/naif0012.tls',
...         'pds/wgc/kernels/spk/de430.bsp'
...    ],
...    intervals = [
...        ['2000-01-01', '2000-01-03'],
...        ['2000-02-01', '2000-02-03']
...    ],
...    time_step = 1,
...    time_step_units = 'DAYS',
...    target_1 = 'VENUS',
...    target_2 = 'MERCURY',
...    observer = 'SUN',
... ).payload   # doctest: +SKIP
{
    'kernels': [
        {'type': 'KERNEL', 'path': 'pds/wgc/kernels/lsk/naif0012.tls'}
        {'type': 'KERNEL', 'path': 'pds/wgc/kernels/spk/de430.bsp'}
    ],
    'intervals': [
        {'startTime': '2000-01-01', 'endTime': '2000-01-03'},
        {'startTime': '2000-02-01', 'endTime': '2000-02-03'}
    ],
    'timeStep': 1,
    'timeStepUnit': 'DAYS',
    'target1': 'VENUS',
    'target2': 'MERCURY',
    'observer': 'SUN',
    'calculationType': 'ANGULAR_SEPARATION',
    'shape1': 'POINT',
    'shape2': 'POINT',
    'aberrationCorrection': 'CN',
    'timeSystem': 'UTC',
    'timeFormat': 'CALENDAR'
}

.. important::

    Calculation required parameters:
        - :py:attr:`calculation_type`
        - :py:attr:`kernels` or/and :py:attr:`kernel_paths`
        - :py:attr:`times` or :py:attr:`intervals` with :py:attr:`time_step` and :py:attr:`time_step_units`

    Calculation default parameters:
        - :py:attr:`time_system`: ``UTC``
        - :py:attr:`time_format`: ``CALENDAR``


Submit payload and retrieve results
------------------------------------

Calculation requests to the WebGeoCalc API are made
in three steps:

1. The ``payload`` is submitted to the API with
:py:func:`Calculation.submit` method,
and a :py:attr:`Calculation.id` is retrieved:

>>> calc.submit() # doctest: +SKIP
[Calculation submit] Status: LOADING_KERNELS (id: 8750344d-645d-4e43-b159-c8d88d28aac6)

2. If the calculation status is `COMPLETE`, the results can
be directly retrieved. Otherwise, you need to update the
calculation status with :py:func:`Calculation.update` method:

>>> calc.update() # doctest: +SKIP
[Calculation update] Status: COMPLETE (id: 8750344d-645d-4e43-b159-c8d88d28aac6)

3. When the calculation status is `COMPLETE`, the
results are retrieved with :py:attr:`Calculation.results`
attribute:

>>> calc.results  # doctest: +SKIP
{
    'DATE': '2012-10-19 09:00:00.000000 UTC',
    'DISTANCE': 764142.63776247,
    'SPEED': 111.54765899,
    'X': 298292.85744169,
    'Y': -651606.58468976,
    'Z': 265224.81187627,
    'D_X_DT': -98.8032491,
    'D_Y_DT': -51.73211296,
    'D_Z_DT': -2.1416539,
    'TIME_AT_TARGET': '2012-10-19 08:59:57.451094 UTC',
    'LIGHT_TIME': 2.54890548
}

.. tip::

    It is possible to submit, update and retrieved the results at once
    with :py:func:`Calculation.run` method:

    >>> calc.run()  # doctest: +SKIP
    [Calculation submit] Status: LOADING_KERNELS (id: 8750344d-645d-4e43-b159-c8d88d28aac6)
    [Calculation update] Status: COMPLETE (id: 8750344d-645d-4e43-b159-c8d88d28aac6)
    {
        'DATE': '2012-10-19 09:00:00.000000 UTC',
        'DISTANCE': 764142.63776247,
        'SPEED': 111.54765899,
        'X': 298292.85744169,
        'Y': -651606.58468976,
        'Z': 265224.81187627,
        'D_X_DT': -98.8032491,
        'D_Y_DT': -51.73211296,
        'D_Z_DT': -2.1416539,
        'TIME_AT_TARGET': '2012-10-19 08:59:57.451094 UTC',
        'LIGHT_TIME': 2.54890548
    }

Generic calculation
-------------------

.. autoclass:: Calculation

State Vector
------------

Calculates the position of one body relative to another,
calculated in a desired reference frame:

>>> StateVector(
...    kernels = 5,
...    times = '2012-10-19T09:00:00',
...    target = 'CASSINI',
...    observer = 'SATURN',
...    reference_frame = 'IAU_SATURN',
... )  # doctest: +SKIP

.. important::

    Calculation required parameters:
        - :py:attr:`kernels` or/and :py:attr:`kernel_paths`
        - :py:attr:`times` or :py:attr:`intervals` with :py:attr:`time_step` and :py:attr:`time_step_units`
        - :py:attr:`target`
        - :py:attr:`observer`
        - :py:attr:`reference_frame`

    Default parameters:
        -  :py:attr:`time_system`: ``UTC``
        -  :py:attr:`time_format`: ``CALENDAR``
        -  :py:attr:`aberration_correction`: ``CN``
        -  :py:attr:`state_representation`: ``RECTANGULAR``

.. autoclass:: StateVector


Angular Separation
------------------

Calculates the angular separation of two bodies as seen by an observer
body.

Required parameters:
~~~~~~~~~~~~~~~~~~~~

-  ``kernels`` or ``kernel_paths``
-  ``times`` or ``intervals`` + ``time_step`` + ``time_step_units``
-  ``target_1``, the target body name or ID of the first body.
-  ``target_2``, the target body name or ID of the second body.
-  ``observer``, the observing body name or ID.

Optional parameters (with **default**):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``time_system``: **UTC** \| TDB \| TDT \| SPACECRAFT_CLOCK
-  ``time_format``: **CALENDAR** \| JULIAN \| SECONDS_PAST_J2000 \|
   SPACECRAFT_CLOCK_TICKS \| SPACECRAFT_CLOCK_STRING
-  ``shape_1``, the shape to use for the first body: **POINT** \| SPHERE
-  ``shape_2``, the shape to use for the second body: **POINT** \|
   SPHERE
-  ``aberration_correction``: NONE \| LT \| LT+S \| **CN** \| CN+S \|
   XLT \| XLT+S \| XCN \| XCN+S

.. code:: ipython3

    from webgeocalc import AngularSeparation

    AngularSeparation(
        kernel_paths = ['pds/wgc/kernels/lsk/naif0012.tls', 'pds/wgc/kernels/spk/de430.bsp'],
        times = '2012-10-19T08:24:00.000',
        target_1 = 'VENUS',
        target_2 = 'MERCURY',
        observer = 'SUN',
    ).run()


.. parsed-literal::

    [Calculation submit] Status: COMPLETE (id: 0273e817-3af6-4dd7-91ef-7c2d8ef459f9)




.. parsed-literal::

    {'DATE': '2012-10-19 08:24:00.000000 UTC', 'ANGULAR_SEPARATION': 175.17072258}



Angular Size
------------

Calculates the angular size of a target as seen by an observer.

Required parameters:
~~~~~~~~~~~~~~~~~~~~

-  ``kernels`` or ``kernel_paths``
-  ``times`` or ``intervals`` + ``time_step`` + ``time_step_units``
-  ``target``, the target body name or ID.
-  ``observer``, the observing body name or ID.

Optional parameters (with **default**):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``time_system``: **UTC** \| TDB \| TDT \| SPACECRAFT_CLOCK
-  ``time_format``: **CALENDAR** \| JULIAN \| SECONDS_PAST_J2000 \|
   SPACECRAFT_CLOCK_TICKS \| SPACECRAFT_CLOCK_STRING
-  ``aberration_correction``: NONE \| LT \| LT+S \| **CN** \| CN+S \|
   XLT \| XLT+S \| XCN \| XCN+S

.. code:: ipython3

    from webgeocalc import AngularSize

    AngularSize(
        kernels = 5,
        times = '2012-10-19T08:24:00.000',
        target = 'ENCELADUS',
        observer = 'CASSINI',
        aberration_correction = 'CN+S',
    ).run()


.. parsed-literal::

    [Calculation submit] Status: COMPLETE (id: 702a4781-3340-4856-a771-fac9011a7c6b)




.. parsed-literal::

    {'DATE': '2012-10-19 08:24:00.000000 UTC', 'ANGULAR_SIZE': 0.03037939}



Frame Transformation
--------------------

Calculate the transformation from one reference frame (Frame 1) to
another reference frame (Frame 2).

Required parameters:
~~~~~~~~~~~~~~~~~~~~

-  ``kernels`` or ``kernel_paths``
-  ``times`` or ``intervals`` + ``time_step`` + ``time_step_units``
-  ``frame_1``, the first reference frame name.
-  ``frame_2``, the second reference frame name.

Optional parameters (with **default**):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``time_system``: **UTC** \| TDB \| TDT \| SPACECRAFT_CLOCK
-  ``time_format``: **CALENDAR** \| JULIAN \| SECONDS_PAST_J2000 \|
   SPACECRAFT_CLOCK_TICKS \| SPACECRAFT_CLOCK_STRING
-  ``aberration_correction``: NONE \| LT \| **CN** \| XLT \| XCN
-  ``time_location``, the frame for the input times: **FRAME1** \|
   FRAME2
-  ``orientation_representation``: the representation of the result
   transformation: **EULER_ANGLES** \| ANGLE_AND_AXIS \|
   SPICE_QUATERNION \| OTHER_QUATERNION \| MATRIX_ROW_BY_ROW \|
   MATRIX_FLAGGED \| MATRIX_ALL_ONE_ROW
-  ``angular_velocity_representation``, the representation of angular
   velocity in the output: NOT_INCLUDED \| **VECTOR_IN_FRAME1** \|
   VECTOR_IN_FRAME2 \| EULER_ANGLE_DERIVATIVES \| MATRIX

Only needed if ``orientation_representation`` is EULER_ANGLES: -
``axis_1``, the first axis for Euler angle rotation: **X** \| Y \| Z -
``axis_2``, the second axis for Euler angle rotation: X \| **Y** \| Z -
``axis_3``, the third axis for Euler angle rotation: X \| Y \| **Z**

Only needed if ``orientation_representation`` is EULER_ANGLES or
ANGLE_AND_AXIS: - ``angular_units``, the angular units used for the
angle of rotation. **deg** \| rad

Only needed if ``angular_velocity_representation`` is one of:
VECTOR_IN_FRAME1, VECTOR_IN_FRAME2, or EULER_ANGLE_DERIVATIVES: -
``angular_velocity_units``, the units for the angular velocity:
**deg/s** \| rad/s \| RPM \| Unitary

**Note:** ``Unitary`` = Unit vector, only applicable for
VECTOR_IN_FRAME1 and VECTOR_IN_FRAME2.

.. code:: ipython3

    from webgeocalc import FrameTransformation

    FrameTransformation(
        kernels = 5,
        times = '2012-10-19T08:24:00.000',
        frame_1 = 'IAU_SATURN',
        frame_2 = 'IAU_ENCELADUS',
        aberration_correction = 'NONE',
    ).run()


.. parsed-literal::

    [Calculation submit] Status: COMPLETE (id: 48875b2c-747a-4039-bda4-156ca8de1955)




.. parsed-literal::

    {'DATE': '2012-10-19 08:24:00.000000 UTC',
     'ANGLE3': -20.58940104,
     'ANGLE2': 0.01874004,
     'ANGLE1': 0.00136319,
     'AV_X': 9.94596495e-07,
     'AV_Y': -7.23492228e-08,
     'AV_Z': -0.00634331,
     'AV_MAG': 0.00634331}



Illumination Angles
-------------------

Calculate the emission, phase and solar incidence angles at a point on a
target as seen from an observer.

Required parameters:
~~~~~~~~~~~~~~~~~~~~

-  ``kernels`` or ``kernel_paths``
-  ``times`` or ``intervals`` + ``time_step`` + ``time_step_units``
-  ``target``, the target body name or ID.
-  ``target_frame``: The target body-fixed reference frame name.
-  ``observer``, the observing body name or ID.
-  ``latitude``, latitude of the surface point, in degrees, from -90 to
   +90.
-  ``longitude``, longitude of the surface point, in degrees, from -180
   to +180.

Optional parameters (with **default**):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``time_system``: **UTC** \| TDB \| TDT \| SPACECRAFT_CLOCK
-  ``time_format``: **CALENDAR** \| JULIAN \| SECONDS_PAST_J2000 \|
   SPACECRAFT_CLOCK_TICKS \| SPACECRAFT_CLOCK_STRING
-  ``shape_1``, the shape to use for the target body: **ELLIPSOID** \|
   DSK
-  ``coordinate_representation``: **LATITUDINAL** (planetocentric) \|
   PLANETODETIC \| PLANETOGRAPHIC
-  ``aberration_correction``: NONE \| LT \| LT+S \| **CN** \| CN+S \|
   XLT \| XLT+S \| XCN \| XCN+S

.. code:: ipython3

    from webgeocalc import IlluminationAngles

    IlluminationAngles(
        kernels = 5,
        times = '2012-10-19T08:24:00.000',
        target = 'ENCELADUS',
        target_frame = 'IAU_ENCELADUS',
        observer = 'CASSINI',
        aberration_correction = 'CN+S',
        latitude = 0.0,
        longitude = 0.0,
    ).run()


.. parsed-literal::

    [Calculation submit] Status: COMPLETE (id: 198e15f2-8fa3-4a14-aacb-dfca7f0d7e10)




.. parsed-literal::

    {'DATE': '2012-10-19 08:24:00.000000 UTC',
     'INCIDENCE_ANGLE': 24.78527742,
     'EMISSION_ANGLE': 25.56007298,
     'PHASE_ANGLE': 1.00079007,
     'OBSERVER_ALTITUDE': 967668.02765637,
     'TIME_AT_POINT': '2012-10-19 08:23:56.772207 UTC',
     'LIGHT_TIME': 3.2277931}



Sub Solar Point
---------------

Calculates the sub-solar point on a target as seen from an observer.

Required parameters:
~~~~~~~~~~~~~~~~~~~~

-  ``kernels`` or ``kernel_paths``
-  ``times`` or ``intervals`` + ``time_step`` + ``time_step_units``
-  ``target``, the target body name or ID.
-  ``target_frame``: The target body-fixed reference frame name.
-  ``observer``, the observing body name or ID.

Optional parameters (with **default**):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``time_system``: **UTC** \| TDB \| TDT \| SPACECRAFT_CLOCK
-  ``time_format``: **CALENDAR** \| JULIAN \| SECONDS_PAST_J2000 \|
   SPACECRAFT_CLOCK_TICKS \| SPACECRAFT_CLOCK_STRING
-  ``sub_point_type``, the method of finding the sub-solar point: **Near
   point: ellipsoid** \| Intercept: ellipsoid \| NADIR/DSK/UNPRIORITIZED
   \| INTERCEPT/DSK/UNPRIORITIZED
-  ``aberration_correction``: NONE \| LT \| LT+S \| **CN** \| CN+S
-  ``state_representation``: **RECTANGULAR** \| RA_DEC \| LATITUDINAL \|
   PLANETODETIC \| PLANETOGRAPHIC \| CYLINDRICAL \| SPHERICAL

.. code:: ipython3

    from webgeocalc import SubSolarPoint

    SubSolarPoint(
        kernels = 5,
        times = '2012-10-19T08:24:00.000',
        target = 'ENCELADUS',
        target_frame = 'IAU_ENCELADUS',
        observer = 'CASSINI',
        aberration_correction = 'CN+S',
    ).run()


.. parsed-literal::

    [Calculation submit] Status: COMPLETE (id: dd504b37-36bf-4d2f-9ec9-9eb971e17e48)




.. parsed-literal::

    {'DATE': '2012-10-19 08:24:00.000000 UTC',
     'X': 234.00550655,
     'Y': -77.32612213,
     'Z': 67.42916937,
     'SUB_POINT_RADIUS': 255.50851089,
     'OBSERVER_ALTITUDE': 967644.15493281,
     'INCIDENCE_ANGLE': 4.49798357e-15,
     'EMISSION_ANGLE': 0.99611862,
     'PHASE_ANGLE': 0.99611862,
     'TIME_AT_POINT': '2012-10-19 08:23:56.772287 UTC',
     'LIGHT_TIME': 3.22771347}



Sub Observer Point
------------------

Calculate the sub-observer point on a target as seen from an observer.

Required parameters:
~~~~~~~~~~~~~~~~~~~~

-  ``kernels`` or ``kernel_paths``
-  ``times`` or ``intervals`` + ``time_step`` + ``time_step_units``
-  ``target``, the target body name or ID.
-  ``target_frame``: The target body-fixed reference frame name.
-  ``observer``, the observing body name or ID.

Optional parameters (with **default**):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``time_system``: **UTC** \| TDB \| TDT \| SPACECRAFT_CLOCK
-  ``time_format``: **CALENDAR** \| JULIAN \| SECONDS_PAST_J2000 \|
   SPACECRAFT_CLOCK_TICKS \| SPACECRAFT_CLOCK_STRING
-  ``sub_point_type``, the method of finding the sub-observer point:
   **Near point: ellipsoid** \| Intercept: ellipsoid \|
   NADIR/DSK/UNPRIORITIZED \| INTERCEPT/DSK/UNPRIORITIZED
-  ``aberration_correction``: NONE \| LT \| LT+S \| **CN** \| CN+S \|
   XLT \| XLT+S \| XCN \| XCN+S
-  ``state_representation``: **RECTANGULAR** \| RA_DEC \| LATITUDINAL \|
   PLANETODETIC \| PLANETOGRAPHIC \| CYLINDRICAL \| SPHERICAL

.. code:: ipython3

    from webgeocalc import SubObserverPoint

    SubObserverPoint(
        kernels = 5,
        times = '2012-10-19T08:24:00.000',
        target = 'ENCELADUS',
        target_frame = 'IAU_ENCELADUS',
        observer = 'CASSINI',
        aberration_correction = 'CN+S',
    ).run()


.. parsed-literal::

    [Calculation submit] Status: COMPLETE (id: 5d409208-ed15-4a72-ad7a-e2349ae7eca6)




.. parsed-literal::

    {'DATE': '2012-10-19 08:24:00.000000 UTC',
     'X': 232.5831733,
     'Y': -81.40386728,
     'Z': 67.35505213,
     'SUB_POINT_RADIUS': 255.45689491,
     'OBSERVER_ALTITUDE': 967644.11734179,
     'INCIDENCE_ANGLE': 0.99586304,
     'EMISSION_ANGLE': 1.66981544e-12,
     'PHASE_ANGLE': 0.99586304,
     'TIME_AT_POINT': '2012-10-19 08:23:56.772287 UTC',
     'LIGHT_TIME': 3.22771334}



Surface Intercept Point
-----------------------

Calculate the intercept point of a vector or vectors on a target as seen
from an observer.

Required parameters:
~~~~~~~~~~~~~~~~~~~~

-  ``kernels`` or ``kernel_paths``
-  ``times`` or ``intervals`` + ``time_step`` + ``time_step_units``
-  ``target``, the target body name or ID.
-  ``target_frame``, the target body-fixed reference frame name.
-  ``observer``, the observing body name or ID.

Optional parameters (with **default**):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``time_system``: **UTC** \| TDB \| TDT \| SPACECRAFT_CLOCK
-  ``time_format``: **CALENDAR** \| JULIAN \| SECONDS_PAST_J2000 \|
   SPACECRAFT_CLOCK_TICKS \| SPACECRAFT_CLOCK_STRING
-  ``shape_1``, the shape to use for the target body. **ELLIPSOID** \|
   DSK
-  ``intercept_vector_type``, type of vector to be used as the ray
   direction. **INSTRUMENT_BORESIGHT** \| INSTRUMENT_FOV_BOUNDARY_VECTOR
   S \|REFERENCE_FRAME_AXIS \| VECTOR_IN_INSTRUMENT_FOV \|
   VECTOR_IN_REFERENCE_FRAME
-  ``aberration_correction``: NONE \| LT \| LT+S \| **CN** \| CN+S \|
   XLT \| XLT+S \| XCN \| XCN+S
-  ``state_representation``: **RECTANGULAR** \| RA_DEC \| LATITUDINAL \|
   PLANETODETIC \| PLANETOGRAPHIC \| CYLINDRICAL \| SPHERICAL

Only needed if ``intercept_vector_type`` is INSTRUMENT_BORESIGHT,
INSTRUMENT_FOV_BOUNDARY_VECTORS or VECTOR_IN_INSTRUMENT_FOV: -
``intercept_instrument``, the instrument name or ID.

Only needed if ``intercept_vector_type`` is REFERENCE_FRAME_AXIS or
VECTOR_IN_REFERENCE_FRAME: - ``intercept_frame``, the vector’s reference
frame name.

Only needed if ``intercept_vector_type`` is REFERENCE_FRAME_AXIS: -
``intercept_frame_axis``, the intercept frame axis.

Only need if ``intercept_vector_type`` is VECTOR_IN_INSTRUMENT_FOV or
VECTOR_IN_REFERENCE_FRAME: - ``intercept_vector_x`` +
``intercept_vector_y`` + ``intercept_vector_z`` or
``intercept_vector_ra`` + ``intercept_vector_dec``: intercept vector
coordinates.

.. code:: ipython3

    from webgeocalc import SurfaceInterceptPoint

    SurfaceInterceptPoint(
        kernels = 5,
        times = '2012-10-14T00:00:00',
        target = 'SATURN',
        target_frame = 'IAU_SATURN',
        observer = 'CASSINI',
        intercept_vector_type = 'INSTRUMENT_BORESIGHT',
        intercept_instrument = 'CASSINI_ISS_NAC',
        aberration_correction = 'NONE',
        state_representation = 'LATITUDINAL',
    ).run()


.. parsed-literal::

    [Calculation submit] Status: COMPLETE (id: bc3c7b6b-c4e1-4937-a4bd-edd91db8acf3)




.. parsed-literal::

    {'DATE': '2012-10-14 00:00:00.000000 UTC',
     'LONGITUDE': 98.7675609,
     'LATITUDE': -38.69027976,
     'INTERCEPT_RADIUS': 57739.95803153,
     'OBSERVER_ALTITUDE': 1831047.67987589,
     'INCIDENCE_ANGLE': 123.05323675,
     'EMISSION_ANGLE': 5.8567773,
     'PHASE_ANGLE': 123.77530312,
     'TIME_AT_POINT': '2012-10-14 00:00:00.000000 UTC',
     'LIGHT_TIME': 6.10771763}



Osculating Elements
-------------------

Calculate the osculating elements of the orbit of a target body around a
central body. The orbit may be elliptical, parabolic, or hyperbolic.

Required parameters:
~~~~~~~~~~~~~~~~~~~~

-  ``kernels`` or ``kernel_paths``
-  ``times`` or ``intervals`` + ``time_step`` + ``time_step_units``
-  ``orbiting_body``: The SPICE body name or ID for the orbiting body.
-  ``center_body``: The SPICE body name or ID for the body that is the
   center of motion.

Optional parameters (with **default**):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``time_system``: **UTC** \| TDB \| TDT \| SPACECRAFT_CLOCK
-  ``time_format``: **CALENDAR** \| JULIAN \| SECONDS_PAST_J2000 \|
   SPACECRAFT_CLOCK_TICKS \| SPACECRAFT_CLOCK_STRING
-  ``reference_frame``, the reference frame name. *J2000*

.. code:: ipython3

    from webgeocalc import OsculatingElements

    OsculatingElements(
        kernels = [1,5],
        times = '2012-10-19T08:24:00.000',
        orbiting_body = 'CASSINI',
        center_body = 'SATURN',
    ).run()


.. parsed-literal::

    [Calculation submit] Status: COMPLETE (id: 43919bd8-4c11-4dfc-9ff7-dfe247073169)




.. parsed-literal::

    {'DATE': '2012-10-19 08:24:00.000000 UTC',
     'PERIFOCAL_DISTANCE': 474789.03917271,
     'ECCENTRICITY': 0.70348463,
     'INCLINATION': 38.18727034,
     'ASCENDING_NODE_LONGITUDE': 223.98123058,
     'ARGUMENT_OF_PERIAPSE': 71.59474487,
     'MEAN_ANOMALY_AT_EPOCH': 14.65461204,
     'ORBITING_BODY_RANGE': 753794.65101401,
     'ORBITING_BODY_SPEED': 8.77222231,
     'PERIOD': 2067101.2236748,
     'CENTER_BODY_GM': 37931207.49865224}



Time Conversion
---------------

Convert times from one time system or format to another.

Required parameters:
~~~~~~~~~~~~~~~~~~~~

-  ``kernels`` or ``kernel_paths``
-  ``times`` or ``intervals`` + ``time_step`` + ``time_step_units``

Optional parameters (with **default**):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``time_system``: **UTC** \| TDB \| TDT \| SPACECRAFT_CLOCK
-  ``time_format``: **CALENDAR** \| JULIAN \| SECONDS_PAST_J2000 \|
   SPACECRAFT_CLOCK_TICKS \| SPACECRAFT_CLOCK_STRING
-  ``output_time_system``, the time system for the result times: TDB \|
   TDT \| **UTC** \| SPACECRAFT_CLOCK
-  ``output_time_format``, the time format for the result times:
   **CALENDAR** \| CALENDAR_YMD \| CALENDAR_DOY \| JULIAN
   \|SECONDS_PAST_J2000 \| SPACECRAFT_CLOCK_STRING \|
   SPACECRAFT_CLOCK_TICKS \| CUSTOM

Only used if ``outputTimeSystem`` is SPACECRAFT_CLOCK. -
``output_sclk_id``, the output SCLK ID.

Only used if ``output_time_format`` is CUSTOM. -
``output_time_custom_format``, a SPICE ``timeout()`` format string.

.. code:: ipython3

    from webgeocalc import TimeConversion

    TimeConversion(
        kernels = 5,
        times = '1/1729329441.04',
        time_system = 'SPACECRAFT_CLOCK',
        time_format = 'SPACECRAFT_CLOCK_STRING',
        sclk_id = -82,
    ).run()


.. parsed-literal::

    [Calculation submit] Status: COMPLETE (id: 917f5cda-157f-4dc9-b4d7-bf46eaa8409a)




.. parsed-literal::

    {'DATE': '1/1729329441.004', 'DATE2': '2012-10-19 08:24:02.919085 UTC'}
