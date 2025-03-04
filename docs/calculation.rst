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
- :py:class:`GFCoordinateSearch`

Import generic WebGeoCalc calculation object:

>>> from webgeocalc import Calculation

or import specific WebGeoCalc calculation object:

>>> from webgeocalc import StateVector, AngularSeparation

Inputs examples and payloads
----------------------------

All WebGeoCalc calculation objects take their input attributes in
``snakecase`` format.

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


.. note::

    By default, if no :py:attr:`api` option is provided,
    the query is sent to the :obj:`WGC_URL` API
    (if set in the global environment variables) or JPL API (if not).
    See API_ docs for details.

    .. _API: api.html

    To query on the ESA WGC API, you need to add the ``ESA`` key
    to the any Calculation parameters:

    >>> Calculation(
    ...    api = 'ESA',
    ...    kernels = 6,
    ...    times = '2014-01-01T01:23:45.000',
    ...    calculation_type = 'STATE_VECTOR',
    ...    target = '67P/CHURYUMOV-GERASIMENKO (1969 R1)',
    ...    observer = 'ROSETTA ORBITER',
    ...    reference_frame = '67P/C-G_CK',
    ...    aberration_correction = 'NONE',
    ...    state_representation = 'LATITUDINAL',
    ... ).api
    <Api> http://spice.esac.esa.int/webgeocalc/api

    3-rd party WGC are also supported, either set :obj:`WGC_URL`
    on your system (as mention before), or you can provide directly
    its ``URL`` to the :py:attr:`api` parameter:

    >>> Calculation(
    ...    api = 'https://wgc.obspm.fr/webgeocalc/api',
    ...    kernels = 6,
    ...    times = '2014-01-01T01:23:45.000',
    ...    calculation_type = 'STATE_VECTOR',
    ...    target = '67P/CHURYUMOV-GERASIMENKO (1969 R1)',
    ...    observer = 'ROSETTA ORBITER',
    ...    reference_frame = '67P/C-G_CK',
    ...    aberration_correction = 'NONE',
    ...    state_representation = 'LATITUDINAL',
    ... ).api
    <Api> https://wgc.obspm.fr/webgeocalc/api

    In each cases, every new API is cached to improve
    the kernels loading performances.


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

Calculation names
-----------------

The ``Webgeocalc API`` calculation names slightly differ from the
calculation feature names accessible from the ``Webgeocalc GUI``
web portals.

.. list-table:: Webgeocalc API vs GUI calculation names
   :widths: 33 33 33
   :header-rows: 1

   * - | python-webgeocalc
       | API classes
     - | Webgeocalc API
       | calculation types
     - | Webgeocalc GUI
       | features
   * - :py:class:`StateVector`
     - ``STATE_VECTOR``
     - State Vector
   * - :py:class:`AngularSeparation`
     - ``ANGULAR_SEPARATION``
     - Angular Separation
   * - :py:class:`AngularSize`
     - ``ANGULAR_SIZE``
     - Angular Size
   * - :py:class:`FrameTransformation`
     - ``FRAME_TRANSFORMATION``
     - Frame Transformation
   * - :py:class:`IlluminationAngles`
     - ``ILLUMINATION_ANGLES``
     - Illumination Angles
   * - :py:class:`SubSolarPoint`
     - ``SUB_SOLAR_POINT``
     - Sub-solar Point
   * - :py:class:`SubObserverPoint`
     - ``SUB_OBSERVER_POINT``
     - Sub-observer Point
   * - :py:class:`SurfaceInterceptPoint`
     - ``SURFACE_INTERCEPT_POINT``
     - Surface Intercept Point
   * - :py:class:`OsculatingElements`
     - ``OSCULATING_ELEMENTS``
     - Orbital Elements
   * - :py:class:`TimeConversion`
     - ``TIME_CONVERSION``
     - Time Conversion
   * - :py:class:`GFCoordinateSearch`
     - ``GF_COORDINATE_SEARCH``
     - Position Event Finder


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
 'DISTANCE': 764142.65053372,
 'SPEED': 111.54765158,
 'X': 298293.06093747,
 'Y': -651606.39373107,
 'Z': 265225.08895284,
 'D_X_DT': -98.80322113,
 'D_Y_DT': -51.73215012,
 'D_Z_DT': -2.14166057,
 'TIME_AT_TARGET': '2012-10-19 08:59:57.451094 UTC',
 'LIGHT_TIME': 2.54890552}

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
observer body. There are two types of calculation. The default
one is the angular separation between two targets (`TWO_TARGETS`
mode), which is the default mode.

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

The second case is the angular separation between two directions
(`TWO_DIRECTIONS` mode).

>>> AngularSeparation(
...     spec_type = 'TWO_DIRECTIONS',
...     kernels = 5,
...     times = '2012-10-19T08:24:00.000',
...     direction_1 = {
...         "directionType": "VECTOR",
...         "directionVectorType": "REFERENCE_FRAME_AXIS",
...         "directionFrame": "CASSINI_RPWS_EDIPOLE",
...         "directionFrameAxis": "Z"
...     },
...     direction_2 = {
...         "directionType": "POSITION",
...         "target": "SUN",
...         "shape": "POINT",
...         "observer": "CASSINI"
...     },
...     verbose = False,
... ).run()
{'DATE': '2012-10-19 08:24:00.000000 UTC', 'ANGULAR_SEPARATION': 90.10114616}

.. important::

    Calculation required parameters:
        - :py:attr:`.kernels` or/and :py:attr:`.kernel_paths`
        - :py:attr:`.times` or :py:attr:`.intervals` with :py:attr:`.time_step` and :py:attr:`.time_step_units`
        - :py:attr:`.target_1` if :py:attr:`.spec_type` is `TWO_TARGETS` or not set
        - :py:attr:`.target_2` if :py:attr:`.spec_type` is `TWO_TARGETS` or not set
        - :py:attr:`.observer` if :py:attr:`.spec_type` is `TWO_TARGETS` or not set
        - :py:attr:`.direction_1` if :py:attr:`.spec_type` is `TWO_DIRECTIONS`
        - :py:attr:`.direction_2` if :py:attr:`.spec_type` is `TWO_DIRECTIONS`

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
{'DATE': '2012-10-19 08:24:00.000000 UTC', 'ANGULAR_SIZE': 0.03032491}

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
 'ANGLE3': -19.59511576,
 'ANGLE2': -0.00533619,
 'ANGLE1': -0.00345332,
 'AV_X': -2.8406831e-07,
 'AV_Y': 1.83751477e-07,
 'AV_Z': -0.00633942,
 'AV_MAG': 0.00633942}

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
 'INCIDENCE_ANGLE': 25.51886414,
 'EMISSION_ANGLE': 26.31058362,
 'PHASE_ANGLE': 1.00106425,
 'OBSERVER_ALTITUDE': 967670.28784259,
 'TIME_AT_POINT': '2012-10-19 08:23:56.772199 UTC',
 'LIGHT_TIME': 3.22780064,
 'LTST': '13:19:56'}

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
 'X': 232.15437562,
 'Y': -81.18742303,
 'Z': 67.66010394,
 'SUB_POINT_RADIUS': 255.07830453,
 'OBSERVER_ALTITUDE': 967644.95641522,
 'INCIDENCE_ANGLE': 1.10177646e-14,
 'EMISSION_ANGLE': 0.99615507,
 'PHASE_ANGLE': 0.99615507,
 'TIME_AT_POINT': '2012-10-19 08:23:56.772284 UTC',
 'LIGHT_TIME': 3.22771614}

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
 'X': 230.66149425,
 'Y': -85.24005493,
 'Z': 67.58656174,
 'SUB_POINT_RADIUS': 255.02653827,
 'OBSERVER_ALTITUDE': 967644.91882136,
 'INCIDENCE_ANGLE': 0.99589948,
 'EMISSION_ANGLE': 3.94425842e-12,
 'PHASE_ANGLE': 0.99589948,
 'TIME_AT_POINT': '2012-10-19 08:23:56.772284 UTC',
 'LIGHT_TIME': 3.22771602,
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
 'LONGITUDE': 98.76797447,
 'LATITUDE': -38.69300277,
 'INTERCEPT_RADIUS': 57739.67660691,
 'OBSERVER_ALTITUDE': 1831047.98047459,
 'INCIDENCE_ANGLE': 123.05303919,
 'EMISSION_ANGLE': 5.8595724,
 'PHASE_ANGLE': 123.7753032,
 'TIME_AT_POINT': '2012-10-14 00:00:00.000000 UTC',
 'LIGHT_TIME': 6.10771863,
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
 'PERIFOCAL_DISTANCE': 474789.01814487,
 'ECCENTRICITY': 0.70348464,
 'INCLINATION': 38.18736036,
 'ASCENDING_NODE_LONGITUDE': 223.98121958,
 'ARGUMENT_OF_PERIAPSE': 71.59475294,
 'MEAN_ANOMALY_AT_EPOCH': 14.65461277,
 'ORBITING_BODY_RANGE': 753794.66333655,
 'ORBITING_BODY_SPEED': 8.77222221,
 'PERIOD': 2067101.1993984,
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


Geometry Finder: Coordinate Search
----------------------------------


Find time intervals when a coordinate of an observer-target position vector satisfies a condition.

.. testsetup::

    from webgeocalc import GFCoordinateSearch

>>> GFCoordinateSearch(
...     kernels = 5,
...     intervals = ['2012-10-19T07:00:00', '2012-10-19T09:00:00'],
...     observer = 'CASSINI',
...     target = 'ENCELADUS',
...     reference_frame = 'CASSINI_ISS_NAC',
...     time_step = 1,
...     time_step_units = 'MINUTES',
...     aberration_correction = 'NONE',
...     interval_adjustment = 'EXPAND_INTERVALS',
...     interval_adjustment_amount = 1,
...     interval_adjustment_units = 'SECONDS',
...     interval_filtering = 'FILTER_INTERVALS',
...     interval_filtering_threshold = 1,
...     interval_filtering_threshold_units = 'MINUTES',
...     coordinate_system = 'SPHERICAL',
...     coordinate = 'COLATITUDE',
...     relational_condition = '<',
...     reference_value = 0.25,
...     verbose = False,
... ).run()
{'DATE': '2012-10-19 08:39:33.814938 UTC', 'DURATION': 3394.11539114}

.. important::

    Calculation required parameters:
        - :py:attr:`.kernels` or/and :py:attr:`.kernel_paths`
        - :py:attr:`.times` or :py:attr:`.intervals` with :py:attr:`.time_step` and :py:attr:`.time_step_units`
        - :py:attr:`.observer`
        - :py:attr:`.target`
        - :py:attr:`.reference_frame`
        - :py:attr:`.coordinate_system`
        - :py:attr:`.coordinate`
        - :py:attr:`.relational_condition`
        - :py:attr:`.reference_value` only if :py:attr:`.relational_condition` is not ``ABSMAX``, ``ABSMIN``, ``LOCMAX``, or ``LOCMIN``
        - :py:attr:`.upper_limit` only if :py:attr:`.relational_condition` is ``RANGE``
        - :py:attr:`.adjustment_value` only if :py:attr:`.relational_condition` is ``ABSMAX`` or ``ABSMIN``

    Default parameters:
        - :py:attr:`.time_system`: ``UTC``
        - :py:attr:`.time_format`: ``CALENDAR``
        - :py:attr:`.output_duration_units`: ``SECONDS``
        - :py:attr:`.should_complement_window`: ``False``
        - :py:attr:`.interval_adjustment`: ``NO_ADJUSTMENT``
        - :py:attr:`.interval_filtering`: ``NO_FILTERING``

.. autoclass:: GFCoordinateSearch
