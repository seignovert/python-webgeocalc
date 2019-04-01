WebGeoCalc calculations
=======================

.. currentmodule:: webgeocalc

For now only the geometry/time calculations are implemented:

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

>>> calc = Calculation(
...    kernels = 5,
...    times = '2012-10-19T08:24:00.000',
...    calculation_type = 'STATE_VECTOR',
...    target = 'CASSINI',
...    observer = 'SATURN',
...    reference_frame = 'IAU_SATURN',
...    aberration_correction = 'NONE',
...    state_representation = 'PLANETOGRAPHIC',
... )

.. important::

    Calculation required parameters:
        - :py:attr:`.calculation_type`
        - :py:attr:`.kernels` or/and :py:attr:`.kernel_paths`
        - :py:attr:`.times` or :py:attr:`.intervals` with :py:attr:`.time_step` and :py:attr:`.time_step_units`

    Calculation default parameters:
        - :py:attr:`.time_system`: ``UTC``
        - :py:attr:`.time_format`: ``CALENDAR``


The payload that will be submitted to
the WebGeoCalc API can be retrieve with the
:py:attr:`.payload` attribute:

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

Example of :py:class:`StateVector` calculation with multi :py:attr:`.kernels`
inputs (requested by ``name`` in this case), with multiple :py:attr:`.times`
inputs for :py:attr:`.target`, :py:attr:`.observer` and
:py:attr:`.reference_frame` requested by ``id``:

>>> StateVector(
...    kernels = ['Solar System Kernels', 'Cassini Huygens'],
...    times = ['2012-10-19T07:00:00', '2012-10-19T09:00:00'],
...    target = -82,             # CASSINI
...    observer = 699,           # SATURN
...    reference_frame = 10016,  # IAU_SATURN
... ).payload
{'kernels': [{'type': 'KERNEL_SET', 'id': 1},
             {'type': 'KERNEL_SET', 'id': 5}],
 'times': ['2012-10-19T07:00:00', '2012-10-19T09:00:00'],
 'target': -82,
 'observer': 699,
 'referenceFrame': 10016,
 'calculationType': 'STATE_VECTOR',
 'aberrationCorrection': 'CN',
 'stateRepresentation': 'RECTANGULAR',
 'timeSystem': 'UTC',
 'timeFormat': 'CALENDAR'}


Example of :py:class:`AngularSeparation` calculation
with specific :py:attr:`.kernel_paths` and multiple :py:attr:`.intervals`:

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
... ).payload
{'kernels': [{'type': 'KERNEL', 'path': 'pds/wgc/kernels/lsk/naif0012.tls'},
             {'type': 'KERNEL', 'path': 'pds/wgc/kernels/spk/de430.bsp'}],
 'intervals': [{'startTime': '2000-01-01', 'endTime': '2000-01-03'},
               {'startTime': '2000-02-01', 'endTime': '2000-02-03'}],
 'timeStep': 1,
 'timeStepUnits': 'DAYS',
 'target1': 'VENUS',
 'target2': 'MERCURY',
 'observer': 'SUN',
 'calculationType': 'ANGULAR_SEPARATION',
 'shape1': 'POINT',
 'shape2': 'POINT',
 'aberrationCorrection': 'CN',
 'timeSystem': 'UTC',
 'timeFormat': 'CALENDAR'}


Submit payload and retrieve results
------------------------------------

Calculation requests to the WebGeoCalc API are made
in three steps:

1. The ``payload`` is submitted to the API with
:py:func:`Calculation.submit` method, and a
``calculation-id`` is retrieved:

>>> calc.submit() # doctest: +SKIP
[Calculation submit] Status: LOADING_KERNELS (id: 8750344d-645d-4e43-b159-c8d88d28aac6)

2. If the calculation status is `COMPLETE`, the results can
be directly retrieved. Otherwise, you need to update the
calculation status with :py:func:`Calculation.update` method:

>>> calc.update() # doctest: +SKIP
[Calculation update] Status: COMPLETE (id: 8750344d-645d-4e43-b159-c8d88d28aac6)

3. When the calculation status is `COMPLETE`, the
results are retrieved by the :py:attr:`.results` attribute:

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

    It is possible to submit, update and retrieve the results at once
    with :py:func:`Calculation.run` method:

    >>> calc.run()  # doctest: +SKIP
    [Calculation submit] Status: LOADING_KERNELS (id: 8750344d-645d-4e43-b159-c8d88d28aac6)
    [Calculation update] Status: COMPLETE (id: 8750344d-645d-4e43-b159-c8d88d28aac6)
    {'DATE': '2012-10-19 09:00:00.000000 UTC',
     'DISTANCE': 764142.63776247,
     'SPEED': 111.54765899,
     'X': 298292.85744169,
     'Y': -651606.58468976,
     'Z': 265224.81187627,
     'D_X_DT': -98.8032491,
     'D_Y_DT': -51.73211296,
     'D_Z_DT': -2.1416539,
     'TIME_AT_TARGET': '2012-10-19 08:59:57.451094 UTC',
     'LIGHT_TIME': 2.54890548}

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
...    verbose = False,
... ).run()
{'DATE': '2012-10-19 09:00:00.000000 UTC',
 'DISTANCE': 764142.63776247,
 'SPEED': 111.54765899,
 'X': 298292.85744169,
 'Y': -651606.58468976,
 'Z': 265224.81187627,
 'D_X_DT': -98.8032491,
 'D_Y_DT': -51.73211296,
 'D_Z_DT': -2.1416539,
 'TIME_AT_TARGET': '2012-10-19 08:59:57.451094 UTC',
 'LIGHT_TIME': 2.54890548}

.. important::

    Calculation required parameters:
        - :py:attr:`.kernels` or/and :py:attr:`.kernel_paths`
        - :py:attr:`.times` or :py:attr:`.intervals` with :py:attr:`.time_step` and :py:attr:`.time_step_units`
        - :py:attr:`.target`
        - :py:attr:`.observer`
        - :py:attr:`.reference_frame`

    Default parameters:
        - :py:attr:`.time_system`: ``UTC``
        - :py:attr:`.time_format`: ``CALENDAR``
        - :py:attr:`.aberration_correction`: ``CN``
        - :py:attr:`.state_representation`: ``RECTANGULAR``

.. autoclass:: StateVector


Angular Separation
------------------

Calculates the angular separation of two bodies as seen by an
observer body.

>>> AngularSeparation(
...     kernel_paths = ['pds/wgc/kernels/lsk/naif0012.tls',
...                     'pds/wgc/kernels/spk/de430.bsp'],
...     times = '2012-10-19T08:24:00.000',
...     target_1 = 'VENUS',
...     target_2 = 'MERCURY',
...     observer = 'SUN',
...     verbose = False,
... ).run()
{'DATE': '2012-10-19 08:24:00.000000 UTC', 'ANGULAR_SEPARATION': 175.17072258}

.. important::

    Calculation required parameters:
        - :py:attr:`.kernels` or/and :py:attr:`.kernel_paths`
        - :py:attr:`.times` or :py:attr:`.intervals` with :py:attr:`.time_step` and :py:attr:`.time_step_units`
        - :py:attr:`.target_1`
        - :py:attr:`.target_2`
        - :py:attr:`.observer`

    Default parameters:
        - :py:attr:`.time_system`: ``UTC``
        - :py:attr:`.time_format`: ``CALENDAR``
        - :py:attr:`.shape_1`: ``POINT``
        - :py:attr:`.shape_2`: ``POINT``
        - :py:attr:`.aberration_correction`: ``CN``

.. autoclass:: AngularSeparation


Angular Size
------------

Calculates the angular size of a target as seen by an observer.

.. testsetup::

    from webgeocalc import AngularSize

>>> AngularSize(
...     kernels = 5,
...     times = '2012-10-19T08:24:00.000',
...     target = 'ENCELADUS',
...     observer = 'CASSINI',
...     aberration_correction = 'CN+S',
...     verbose = False,
... ).run()
{'DATE': '2012-10-19 08:24:00.000000 UTC', 'ANGULAR_SIZE': 0.03037939}

.. important::

    Calculation required parameters:
        - :py:attr:`.kernels` or/and :py:attr:`.kernel_paths`
        - :py:attr:`.times` or :py:attr:`.intervals` with :py:attr:`.time_step` and :py:attr:`.time_step_units`
        - :py:attr:`.target`
        - :py:attr:`.observer`

    Default parameters:
        - :py:attr:`.time_system`: ``UTC``
        - :py:attr:`.time_format`: ``CALENDAR``
        - :py:attr:`.aberration_correction`: ``CN``

.. autoclass:: AngularSize


Frame Transformation
--------------------

Calculate the transformation from one reference frame (Frame 1) to
another reference frame (Frame 2).

.. testsetup::

    from webgeocalc import FrameTransformation

>>> FrameTransformation(
...     kernels = 5,
...     times = '2012-10-19T08:24:00.000',
...     frame_1 = 'IAU_SATURN',
...     frame_2 = 'IAU_ENCELADUS',
...     aberration_correction = 'NONE',
...     verbose = False,
... ).run()
{'DATE': '2012-10-19 08:24:00.000000 UTC',
 'ANGLE3': -20.58940104,
 'ANGLE2': 0.01874004,
 'ANGLE1': 0.00136319,
 'AV_X': 9.94596495e-07,
 'AV_Y': -7.23492228e-08,
 'AV_Z': -0.00634331,
 'AV_MAG': 0.00634331}

.. important::

    Calculation required parameters:
        - :py:attr:`.kernels` or/and :py:attr:`.kernel_paths`
        - :py:attr:`.times` or :py:attr:`.intervals` with :py:attr:`.time_step` and :py:attr:`.time_step_units`
        - :py:attr:`.frame_1`
        - :py:attr:`.frame_2`

    Default parameters:
        - :py:attr:`.time_system`: ``UTC``
        - :py:attr:`.time_format`: ``CALENDAR``
        - :py:attr:`.aberration_correction`: ``CN``
        - :py:attr:`.time_location`: ``FRAME1``,
        - :py:attr:`.orientation_representation`: ``EULER_ANGLES``,
        - :py:attr:`.axis_1`: ``X``,
        - :py:attr:`.axis_2`: ``Y``,
        - :py:attr:`.axis_3`: ``Z``,
        - :py:attr:`.angular_units`: ``deg``,
        - :py:attr:`.angular_velocity_representation`: ``VECTOR_IN_FRAME1``,
        - :py:attr:`.angular_velocity_units`: ``deg/s``'

.. autoclass:: FrameTransformation


Illumination Angles
-------------------

Calculate the emission, phase and solar incidence angles at a point on a
target as seen from an observer.

.. testsetup::

    from webgeocalc import IlluminationAngles

>>> IlluminationAngles(
...    kernels = 5,
...    times = '2012-10-19T08:24:00.000',
...    target = 'ENCELADUS',
...    target_frame = 'IAU_ENCELADUS',
...    observer = 'CASSINI',
...    aberration_correction = 'CN+S',
...    latitude = 0.0,
...    longitude = 0.0,
...    verbose = False,
... ).run()
{'DATE': '2012-10-19 08:24:00.000000 UTC',
 'INCIDENCE_ANGLE': 24.78527742,
 'EMISSION_ANGLE': 25.56007298,
 'PHASE_ANGLE': 1.00079007,
 'OBSERVER_ALTITUDE': 967668.02765637,
 'TIME_AT_POINT': '2012-10-19 08:23:56.772207 UTC',
 'LIGHT_TIME': 3.2277931,
 'LTST': '13:15:59'}

.. important::

    Calculation required parameters:
        - :py:attr:`.kernels` or/and :py:attr:`.kernel_paths`
        - :py:attr:`.times` or :py:attr:`.intervals` with :py:attr:`.time_step` and :py:attr:`.time_step_units`
        - :py:attr:`.target`
        - :py:attr:`.target_frame`
        - :py:attr:`.observer`
        - :py:attr:`.latitude`
        - :py:attr:`.longitude`

    Default parameters:
        - :py:attr:`.time_system`: ``UTC``
        - :py:attr:`.time_format`: ``CALENDAR``
        - :py:attr:`.shape_1`: ``ELLIPSOID``
        - :py:attr:`.coordinate_representation`: ``LATITUDINAL``
        - :py:attr:`.aberration_correction`: ``CN``

.. autoclass:: IlluminationAngles


Sub Solar Point
---------------

Calculates the sub-solar point on a target as seen from an observer.

.. testsetup::

    from webgeocalc import SubSolarPoint

>>> SubSolarPoint(
...     kernels = 5,
...     times = '2012-10-19T08:24:00.000',
...     target = 'ENCELADUS',
...     target_frame = 'IAU_ENCELADUS',
...     observer = 'CASSINI',
...     aberration_correction = 'CN+S',
...     verbose = False,
... ).run()
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

.. important::

    Calculation required parameters:
        - :py:attr:`.kernels` or/and :py:attr:`.kernel_paths`
        - :py:attr:`.times` or :py:attr:`.intervals` with :py:attr:`.time_step` and :py:attr:`.time_step_units`
        - :py:attr:`.target`
        - :py:attr:`.target_frame`
        - :py:attr:`.observer`

    Default parameters:
        - :py:attr:`.time_system`: ``UTC``
        - :py:attr:`.time_format`: ``CALENDAR``
        - :py:attr:`.sub_point_type`: ``Near point: ellipsoid``
        - :py:attr:`.aberration_correction`: ``CN``
        - :py:attr:`.state_representation`: ``RECTANGULAR``

.. autoclass:: SubSolarPoint


Sub Observer Point
------------------

Calculate the sub-observer point on a target as seen from an observer.

.. testsetup::

    from webgeocalc import SubObserverPoint

>>> SubObserverPoint(
...     kernels = 5,
...     times = '2012-10-19T08:24:00.000',
...     target = 'ENCELADUS',
...     target_frame = 'IAU_ENCELADUS',
...     observer = 'CASSINI',
...     aberration_correction = 'CN+S',
...     verbose = False,
... ).run()
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
 'LIGHT_TIME': 3.22771334,
 'LTST': '11:58:49'}

.. important::

    Calculation required parameters:
        - :py:attr:`.kernels` or/and :py:attr:`.kernel_paths`
        - :py:attr:`.times` or :py:attr:`.intervals` with :py:attr:`.time_step` and :py:attr:`.time_step_units`
        - :py:attr:`.target`
        - :py:attr:`.target_frame`
        - :py:attr:`.observer`

    Default parameters:
        - :py:attr:`.time_system`: ``UTC``
        - :py:attr:`.time_format`: ``CALENDAR``
        - :py:attr:`.sub_point_type`: ``Near point: ellipsoid``
        - :py:attr:`.aberration_correction`: ``CN``
        - :py:attr:`.state_representation`: ``RECTANGULAR``

.. autoclass:: SubObserverPoint


Surface Intercept Point
-----------------------

Calculate the intercept point of a vector or vectors on a target as seen
from an observer.

.. testsetup::

    from webgeocalc import SurfaceInterceptPoint

>>> SurfaceInterceptPoint(
...     kernels = 5,
...     times = '2012-10-14T00:00:00',
...     target = 'SATURN',
...     target_frame = 'IAU_SATURN',
...     observer = 'CASSINI',
...     direction_vector_type = 'INSTRUMENT_BORESIGHT',
...     direction_instrument = 'CASSINI_ISS_NAC',
...     aberration_correction = 'NONE',
...     state_representation = 'LATITUDINAL',
...     verbose = False,
... ).run()
{'DATE': '2012-10-14 00:00:00.000000 UTC',
 'LONGITUDE': 98.7675609,
 'LATITUDE': -38.69027976,
 'INTERCEPT_RADIUS': 57739.95803153,
 'OBSERVER_ALTITUDE': 1831047.67987589,
 'INCIDENCE_ANGLE': 123.05323675,
 'EMISSION_ANGLE': 5.8567773,
 'PHASE_ANGLE': 123.77530312,
 'TIME_AT_POINT': '2012-10-14 00:00:00.000000 UTC',
 'LIGHT_TIME': 6.10771763,
 'LTST': '20:03:06'}

.. important::

    Calculation required parameters:
        - :py:attr:`.kernels` or/and :py:attr:`.kernel_paths`
        - :py:attr:`.times` or :py:attr:`.intervals` with :py:attr:`.time_step` and :py:attr:`.time_step_units`
        - :py:attr:`.target`
        - :py:attr:`.target_frame`
        - :py:attr:`.observer`

    Default parameters:
        - :py:attr:`.time_system`: ``UTC``
        - :py:attr:`.time_format`: ``CALENDAR``
        - :py:attr:`shape_1`: ``ELLIPSOID``
        - :py:attr:`.intercept_vector_type`: ``INSTRUMENT_BORESIGHT``
        - :py:attr:`.aberration_correction`: ``CN``
        - :py:attr:`.state_representation`: ``RECTANGULAR``

.. autoclass:: SurfaceInterceptPoint


Osculating Elements
-------------------

Calculate the osculating elements of the orbit of a target body around a
central body. The orbit may be elliptical, parabolic, or hyperbolic.

.. testsetup::

    from webgeocalc import OsculatingElements

>>> OsculatingElements(
...     kernels = [1,5],
...     times = '2012-10-19T08:24:00.000',
...     orbiting_body = 'CASSINI',
...     center_body = 'SATURN',
...     verbose = False,
... ).run()
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

.. important::

    Calculation required parameters:
        - :py:attr:`.kernels` or/and :py:attr:`.kernel_paths`
        - :py:attr:`.times` or :py:attr:`.intervals` with :py:attr:`.time_step` and :py:attr:`.time_step_units`
        - :py:attr:`.orbiting_body`
        - :py:attr:`.center_body`

    Default parameters:
        - :py:attr:`.time_system`: ``UTC``
        - :py:attr:`.time_format`: ``CALENDAR``
        - :py:attr:`.reference_frame`: ``J2000``

.. autoclass:: OsculatingElements


Time Conversion
---------------

Convert times from one time system or format to another.

.. testsetup::

    from webgeocalc import TimeConversion

>>> TimeConversion(
...     kernels = 5,
...     times = '1/1729329441.04',
...     time_system = 'SPACECRAFT_CLOCK',
...     time_format = 'SPACECRAFT_CLOCK_STRING',
...     sclk_id = -82,
...     verbose = False,
... ).run()
{'DATE': '1/1729329441.004', 'DATE2': '2012-10-19 08:24:02.919085 UTC'}

.. important::

    Calculation required parameters:
        - :py:attr:`.kernels` or/and :py:attr:`.kernel_paths`
        - :py:attr:`.times` or :py:attr:`.intervals` with :py:attr:`.time_step` and :py:attr:`.time_step_units`

    Default parameters:
        - :py:attr:`.time_system`: ``UTC``
        - :py:attr:`.time_format`: ``CALENDAR``
        - :py:attr:`.output_time_system`: ``UTC``
        - :py:attr:`.output_time_format`: ``CALENDAR``

.. autoclass:: TimeConversion
