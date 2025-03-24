WebGeoCalc calculations
=======================

.. currentmodule:: webgeocalc

For now only these geometry/time calculations are implemented:

- :py:class:`StateVector`
- :py:class:`AngularSeparation`
- :py:class:`AngularSize`
- :py:class:`FrameTransformation`
- :py:class:`IlluminationAngles`
- :py:class:`PhaseAngle`
- :py:class:`PointingDirection`
- :py:class:`SubSolarPoint`
- :py:class:`SubObserverPoint`
- :py:class:`SurfaceInterceptPoint`
- :py:class:`TangentPoint`
- :py:class:`OsculatingElements`
- :py:class:`GFCoordinateSearch`
- ``GFAngularSeparationSearch`` (not implemented)
- ``GFDistanceSearch`` (not implemented)
- ``GFSubPointSearch`` (not implemented)
- ``GFOccultationSearch`` (not implemented)
- ``GFSurfaceInterceptPointSearch`` (not implemented)
- ``GFTargetInInstrumentFovSearch`` (not implemented)
- ``GFRayInFovSearch`` (not implemented)
- ``GFRangeRateSearch`` (not implemented)
- ``GFPhaseAngleSearch`` (not implemented)
- ``GFIlluminationAnglesSearch`` (not implemented)
- :py:class:`TimeConversion`

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
        - :py:attr:`~Calculation.calculation_type`
        - :py:attr:`~Calculation.kernels` or/and :py:attr:`~Calculation.kernel_paths`
        - :py:attr:`~Calculation.times` or :py:attr:`~Calculation.intervals` with :py:attr:`~Calculation.time_step` and :py:attr:`~Calculation.time_step_units`

    Calculation default parameters:
        - :py:attr:`~Calculation.time_system`: ``UTC``
        - :py:attr:`~Calculation.time_format`: ``CALENDAR``


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
:py:attr:`~Calculation.payload` attribute:

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

Example of :py:class:`StateVector` calculation with multi :py:attr:`~Calculation.kernels`
inputs (requested by ``name`` in this case), with multiple :py:attr:`~Calculation.times`
inputs for :py:attr:`~Calculation.target`, :py:attr:`~Calculation.observer` and
:py:attr:`~Calculation.reference_frame` requested by ``id``:

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
with specific :py:attr:`~Calculation.kernel_paths` and multiple :py:attr:`~Calculation.intervals`:

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
results are retrieved by the :py:attr:`~Calculation.results` attribute:

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
   * - :py:class:`PhaseAngle`
     - ``PHASE_ANGLE``
     - Phase Angle
   * - :py:class:`PointingDirection`
     - ``POINTING_DIRECTION``
     - Pointing Direction
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
        - :py:attr:`~Calculation.kernels` or/and :py:attr:`~Calculation.kernel_paths`
        - :py:attr:`~Calculation.times` or :py:attr:`~Calculation.intervals` with :py:attr:`~Calculation.time_step` and :py:attr:`~Calculation.time_step_units`
        - :py:attr:`~Calculation.target`
        - :py:attr:`~Calculation.observer`
        - :py:attr:`~Calculation.reference_frame`

    Default parameters:
        - :py:attr:`~Calculation.time_system`: ``UTC``
        - :py:attr:`~Calculation.time_format`: ``CALENDAR``
        - :py:attr:`~Calculation.aberration_correction`: ``CN``
        - :py:attr:`~Calculation.state_representation`: ``RECTANGULAR``

.. autoclass:: StateVector


Angular Separation
------------------

Calculates the angular separation of two bodies/directions as seen
by an observer body. There are two types of calculation. The default
one is the angular separation between two targets (``TWO_TARGETS``
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
(``TWO_DIRECTIONS`` mode).

>>> AngularSeparation(
...     kernels = 5,
...     times = '2012-10-19T08:24:00.000',
...     spec_type = 'TWO_DIRECTIONS',
...     direction_1 = {
...         'direction_type': 'VECTOR',
...         'direction_vector_type': 'REFERENCE_FRAME_AXIS',
...         'direction_frame': 'CASSINI_RPWS_EDIPOLE',
...         'direction_frame_axis': 'Z'
...     },
...     direction_2 = {
...         'direction_type': 'POSITION',
...         'target': 'SUN',
...         'shape': 'POINT',
...         'observer': 'CASSINI'
...     },
...     verbose = False,
... ).run()
{'DATE': '2012-10-19 08:24:00.000000 UTC', 'ANGULAR_SEPARATION': 90.10114616}

.. important::

    Calculation required parameters:
        - :py:attr:`~Calculation.kernels` or/and :py:attr:`~Calculation.kernel_paths`
        - :py:attr:`~Calculation.times` or :py:attr:`~Calculation.intervals` with :py:attr:`~Calculation.time_step` and :py:attr:`~Calculation.time_step_units`

    Default parameters:
        - :py:attr:`~Calculation.spec_type`: ``TWO_TARGETS``
        - :py:attr:`~Calculation.time_system`: ``UTC``
        - :py:attr:`~Calculation.time_format`: ``CALENDAR``

    Additional required parameters for ``TWO_TARGETS``:
        - :py:attr:`~Calculation.target_1`
        - :py:attr:`~Calculation.target_2`
        - :py:attr:`~Calculation.observer`

    Additional default parameters for ``TWO_TARGETS``:
        - :py:attr:`~Calculation.shape_1`: ``POINT``
        - :py:attr:`~Calculation.shape_2`: ``POINT``
        - :py:attr:`~Calculation.aberration_correction`: ``CN``

    Additional required parameters for ``TWO_DIRECTIONS``:
        - :py:attr:`~Calculation.direction_1`
        - :py:attr:`~Calculation.direction_2`

.. hint::

    The directions can be specified either with an explicit :py:type:`dict`
    or with a :py:class:`Direction` object:

    >>> from webgeocalc.direction import Direction

    >>> AngularSeparation(
    ...     kernels = 5,
    ...     times = '2012-10-19T08:24:00.000',
    ...     spec_type = 'TWO_DIRECTIONS',
    ...     direction_1 = Direction(
    ...         direction_type = 'VECTOR',
    ...         direction_vector_type = 'REFERENCE_FRAME_AXIS',
    ...         direction_frame = 'CASSINI_RPWS_EDIPOLE',
    ...         direction_frame_axis = 'Z',
    ...     ),
    ...     direction_2 = Direction(
    ...         direction_type = 'POSITION',
    ...         target = 'SUN',
    ...         shape = 'POINT',
    ...         observer = 'CASSINI',
    ...     ),
    ... )  # doctest: +SKIP


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
        - :py:attr:`~Calculation.kernels` or/and :py:attr:`~Calculation.kernel_paths`
        - :py:attr:`~Calculation.times` or :py:attr:`~Calculation.intervals` with :py:attr:`~Calculation.time_step` and :py:attr:`~Calculation.time_step_units`
        - :py:attr:`~Calculation.target`
        - :py:attr:`~Calculation.observer`

    Default parameters:
        - :py:attr:`~Calculation.time_system`: ``UTC``
        - :py:attr:`~Calculation.time_format`: ``CALENDAR``
        - :py:attr:`~Calculation.aberration_correction`: ``CN``

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
        - :py:attr:`~Calculation.kernels` or/and :py:attr:`~Calculation.kernel_paths`
        - :py:attr:`~Calculation.times` or :py:attr:`~Calculation.intervals` with :py:attr:`~Calculation.time_step` and :py:attr:`~Calculation.time_step_units`
        - :py:attr:`~Calculation.frame_1`
        - :py:attr:`~Calculation.frame_2`

    Default parameters:
        - :py:attr:`~Calculation.time_system`: ``UTC``
        - :py:attr:`~Calculation.time_format`: ``CALENDAR``
        - :py:attr:`~Calculation.aberration_correction`: ``CN``
        - :py:attr:`~Calculation.time_location`: ``FRAME1``,
        - :py:attr:`~Calculation.orientation_representation`: ``EULER_ANGLES``,
        - :py:attr:`~Calculation.axis_1`: ``X``,
        - :py:attr:`~Calculation.axis_2`: ``Y``,
        - :py:attr:`~Calculation.axis_3`: ``Z``,
        - :py:attr:`~Calculation.angular_units`: ``deg``,
        - :py:attr:`~Calculation.angular_velocity_representation`: ``VECTOR_IN_FRAME1``,
        - :py:attr:`~Calculation.angular_velocity_units`: ``deg/s``'

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
        - :py:attr:`~Calculation.kernels` or/and :py:attr:`~Calculation.kernel_paths`
        - :py:attr:`~Calculation.times` or :py:attr:`~Calculation.intervals` with :py:attr:`~Calculation.time_step` and :py:attr:`~Calculation.time_step_units`
        - :py:attr:`~Calculation.target`
        - :py:attr:`~Calculation.target_frame`
        - :py:attr:`~Calculation.observer`
        - :py:attr:`~Calculation.latitude`
        - :py:attr:`~Calculation.longitude`

    Default parameters:
        - :py:attr:`~Calculation.time_system`: ``UTC``
        - :py:attr:`~Calculation.time_format`: ``CALENDAR``
        - :py:attr:`~Calculation.shape_1`: ``ELLIPSOID``
        - :py:attr:`~Calculation.coordinate_representation`: ``LATITUDINAL``
        - :py:attr:`~Calculation.aberration_correction`: ``CN``

.. autoclass:: IlluminationAngles


Phase Angle
-----------

Calculate the phase angle defined by the centers of an illumination source,
a target and an observer.

The phase angle is computed using the location of the bodies (if point objects)
or the center of the bodies (if finite bodies). The range of the phase angle is [0, pi].

.. testsetup::

    from webgeocalc import PhaseAngle

>>> PhaseAngle(
...    kernels = 5,
...    times = '2012-10-19T08:24:00.000',
...    target = 'ENCELADUS',
...    target_frame = 'IAU_ENCELADUS',
...    observer = 'CASSINI',
...    illuminator = 'SUN',
...    aberration_correction = 'CN+S',
...    verbose = False,
... ).run()
{'DATE': '2012-10-19 08:24:00.000000 UTC', 'PHASE_ANGLE': 0.99571442}

.. important::

    Calculation required parameters:
        - :py:attr:`~Calculation.kernels` or/and :py:attr:`~Calculation.kernel_paths`
        - :py:attr:`~Calculation.times` or :py:attr:`~Calculation.intervals` with :py:attr:`~Calculation.time_step` and :py:attr:`~Calculation.time_step_units`
        - :py:attr:`~Calculation.target`
        - :py:attr:`~Calculation.observer`

    Default parameters:
        - :py:attr:`~Calculation.illuminator`: ``SUN``
        - :py:attr:`~Calculation.aberration_correction`: ``CN``

.. autoclass:: PhaseAngle


Pointing Direction
------------------

Calculates the pointing direction in a user specified reference frame and output
it as a unit or full magnitude vector represented in a user specified coordinate system.

The direction can be specified by the position or velocity of an object with respect
to an observer, or by directly providing a vector, which could be specified as coordinate
in a given frame, a frame axis, an instrument boresight, or as instrument FoV corner vectors.

The output reference frame may be different than the one used for specification
of the input vector (if such option is selected). If so, the orientations of both frames
relative to the inertial space are computed at the same time taking into account the
aberration corrections given in the direction specification.

The output direction could be given as unit or non-unit vector in Rectangular,
Azimuth/Elevation, Right Ascension/Declination/Range, Planetocentric, Cylindrical,
or Spherical coordinates.

.. testsetup::

    from webgeocalc import PointingDirection

>>> PointingDirection(
...     kernels = 5,
...     times = '2012-10-19T08:24:00.000',
...     direction = {
...         'direction_type': 'VECTOR',
...         'observer': 'Cassini',
...         'direction_vector_type': 'INSTRUMENT_FOV_BOUNDARY_VECTORS',
...         'direction_instrument': 'CASSINI_ISS_NAC',
...         'aberration_correction': 'CN',
...     },
...     reference_frame = 'J2000',
...     coordinate_representation = 'RA_DEC',
...     verbose = False,
... ).run()
{'DATE': ['2012-10-19 08:24:00.000000 UTC',
  '2012-10-19 08:24:00.000000 UTC',
  '2012-10-19 08:24:00.000000 UTC',
  '2012-10-19 08:24:00.000000 UTC'],
 'BOUNDARY_POINT_NUMBER': [1.0, 2.0, 3.0, 4.0],
 'RIGHT_ASCENSION': [209.67659835, 209.39258312, 209.60578464, 209.88990474],
 'DECLINATION': [-9.57807208, -9.78811104, -10.06810257, -9.85788588],
 'RANGE': [1.0, 1.0, 1.0, 1.0]}


.. important::

    Calculation required parameters:
        - :py:attr:`~Calculation.kernels` or/and :py:attr:`~Calculation.kernel_paths`
        - :py:attr:`~Calculation.times` or :py:attr:`~Calculation.intervals` with :py:attr:`~Calculation.time_step` and :py:attr:`~Calculation.time_step_units`
        - :py:attr:`~Calculation.direction`
        - :py:attr:`~Calculation.reference_frame`

    Default parameters:
        - :py:attr:`~Calculation.vector_magnitude`: ``UNIT``
        - :py:attr:`~Calculation.coordinate_representation`: ``RECTANGULAR``
        - :py:attr:`~Calculation.time_system`: ``UTC``
        - :py:attr:`~Calculation.time_format`: ``CALENDAR``

    Additional required parameters for ``coordinate_representation='AZ_EL'``:
        - :py:attr:`~Calculation.azccw_flag`
        - :py:attr:`~Calculation.elplsz_flag`

.. hint::

    The direction can be specified either with an explicit :py:type:`dict`
    or with a :py:class:`Direction` object (see :py:class:`AngularSeparation`
    with ``TWO_DIRECTIONS``).

.. autoclass:: PointingDirection


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
        - :py:attr:`~Calculation.kernels` or/and :py:attr:`~Calculation.kernel_paths`
        - :py:attr:`~Calculation.times` or :py:attr:`~Calculation.intervals` with :py:attr:`~Calculation.time_step` and :py:attr:`~Calculation.time_step_units`
        - :py:attr:`~Calculation.target`
        - :py:attr:`~Calculation.target_frame`
        - :py:attr:`~Calculation.observer`

    Default parameters:
        - :py:attr:`~Calculation.time_system`: ``UTC``
        - :py:attr:`~Calculation.time_format`: ``CALENDAR``
        - :py:attr:`~Calculation.sub_point_type`: ``Near point: ellipsoid``
        - :py:attr:`~Calculation.aberration_correction`: ``CN``
        - :py:attr:`~Calculation.state_representation`: ``RECTANGULAR``

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
        - :py:attr:`~Calculation.kernels` or/and :py:attr:`~Calculation.kernel_paths`
        - :py:attr:`~Calculation.times` or :py:attr:`~Calculation.intervals` with :py:attr:`~Calculation.time_step` and :py:attr:`~Calculation.time_step_units`
        - :py:attr:`~Calculation.target`
        - :py:attr:`~Calculation.target_frame`
        - :py:attr:`~Calculation.observer`

    Default parameters:
        - :py:attr:`~Calculation.time_system`: ``UTC``
        - :py:attr:`~Calculation.time_format`: ``CALENDAR``
        - :py:attr:`~Calculation.sub_point_type`: ``Near point: ellipsoid``
        - :py:attr:`~Calculation.aberration_correction`: ``CN``
        - :py:attr:`~Calculation.state_representation`: ``RECTANGULAR``

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
        - :py:attr:`~Calculation.kernels` or/and :py:attr:`~Calculation.kernel_paths`
        - :py:attr:`~Calculation.times` or :py:attr:`~Calculation.intervals` with :py:attr:`~Calculation.time_step` and :py:attr:`~Calculation.time_step_units`
        - :py:attr:`~Calculation.target`
        - :py:attr:`~Calculation.target_frame`
        - :py:attr:`~Calculation.observer`

    Default parameters:
        - :py:attr:`~Calculation.time_system`: ``UTC``
        - :py:attr:`~Calculation.time_format`: ``CALENDAR``
        - :py:attr:`shape_1`: ``ELLIPSOID``
        - :py:attr:`~Calculation.intercept_vector_type`: ``INSTRUMENT_BORESIGHT``
        - :py:attr:`~Calculation.aberration_correction`: ``CN``
        - :py:attr:`~Calculation.state_representation`: ``RECTANGULAR``

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
        - :py:attr:`~Calculation.kernels` or/and :py:attr:`~Calculation.kernel_paths`
        - :py:attr:`~Calculation.times` or :py:attr:`~Calculation.intervals` with :py:attr:`~Calculation.time_step` and :py:attr:`~Calculation.time_step_units`
        - :py:attr:`~Calculation.orbiting_body`
        - :py:attr:`~Calculation.center_body`

    Default parameters:
        - :py:attr:`~Calculation.time_system`: ``UTC``
        - :py:attr:`~Calculation.time_format`: ``CALENDAR``
        - :py:attr:`~Calculation.reference_frame`: ``J2000``

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
        - :py:attr:`~Calculation.kernels` or/and :py:attr:`~Calculation.kernel_paths`
        - :py:attr:`~Calculation.times` or :py:attr:`~Calculation.intervals` with :py:attr:`~Calculation.time_step` and :py:attr:`~Calculation.time_step_units`

    Default parameters:
        - :py:attr:`~Calculation.time_system`: ``UTC``
        - :py:attr:`~Calculation.time_format`: ``CALENDAR``
        - :py:attr:`~Calculation.output_time_system`: ``UTC``
        - :py:attr:`~Calculation.output_time_format`: ``CALENDAR``

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
        - :py:attr:`~Calculation.kernels` or/and :py:attr:`~Calculation.kernel_paths`
        - :py:attr:`~Calculation.times` or :py:attr:`~Calculation.intervals` with :py:attr:`~Calculation.time_step` and :py:attr:`~Calculation.time_step_units`
        - :py:attr:`~Calculation.observer`
        - :py:attr:`~Calculation.target`
        - :py:attr:`~Calculation.reference_frame`
        - :py:attr:`~Calculation.coordinate_system`
        - :py:attr:`~Calculation.coordinate`
        - :py:attr:`~Calculation.relational_condition`
        - :py:attr:`~Calculation.reference_value` only if :py:attr:`~Calculation.relational_condition` is not ``ABSMAX``, ``ABSMIN``, ``LOCMAX``, or ``LOCMIN``
        - :py:attr:`~Calculation.upper_limit` only if :py:attr:`~Calculation.relational_condition` is ``RANGE``
        - :py:attr:`~Calculation.adjustment_value` only if :py:attr:`~Calculation.relational_condition` is ``ABSMAX`` or ``ABSMIN``

    Default parameters:
        - :py:attr:`~Calculation.time_system`: ``UTC``
        - :py:attr:`~Calculation.time_format`: ``CALENDAR``
        - :py:attr:`~Calculation.output_duration_units`: ``SECONDS``
        - :py:attr:`~Calculation.should_complement_window`: ``False``
        - :py:attr:`~Calculation.interval_adjustment`: ``NO_ADJUSTMENT``
        - :py:attr:`~Calculation.interval_filtering`: ``NO_FILTERING``

.. autoclass:: GFCoordinateSearch
