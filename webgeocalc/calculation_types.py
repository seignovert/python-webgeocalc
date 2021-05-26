"""Webgeocalc calculations types."""

from .calculation import Calculation
from .errors import CalculationInvalidAttr
from .vars import VALID_PARAMETERS


class StateVector(Calculation):
    """State vector calculation.

    Calculates the position of one body relative to another,
    calculated in a desired reference frame.

    Parameters
    ----------
    aberration_correction: str, optional
        See: :py:attr:`aberration_correction`
    state_representation: str, optional
        See: :py:attr:`state_representation`

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`kernels`
    kernel_paths: str, [str]
        See: :py:attr:`kernel_paths`
    times: str or [str]
        See: :py:attr:`times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`intervals`
    time_step: int
        See: :py:attr:`time_step`
    time_step_units: str
        See: :py:attr:`time_step_units`
    time_system: str
        See: :py:attr:`time_system`
    time_format: str
        See: :py:attr:`time_format`
    target: str or int
        See: :py:attr:`target`
    observer: str or int
        See: :py:attr:`observer`
    reference_frame: str or int
        See: :py:attr:`reference_frame`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`target`, :py:attr:`observer` and
        :py:attr:`reference_frame` are not provided.

    """

    REQUIRED = ('target', 'observer', 'reference_frame')

    def __init__(self, aberration_correction='CN',
                 state_representation='RECTANGULAR', **kwargs):

        kwargs['calculation_type'] = 'STATE_VECTOR'
        kwargs['aberration_correction'] = aberration_correction
        kwargs['state_representation'] = state_representation

        super().__init__(**kwargs)


class AngularSeparation(Calculation):
    """Angular separation calculation.

    Calculates the angular separation of two bodies as seen by an observer body.

    Parameters
    ----------
    shape_1: str, optional
        See: :py:attr:`shape_1`
    shape_2: str, optional
        See: :py:attr:`shape_2`
    aberration_correction: str, optional
        See: :py:attr:`aberration_correction`

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`kernels`
    kernel_paths: str, [str]
        See: :py:attr:`kernel_paths`
    times: str or [str]
        See: :py:attr:`times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`intervals`
    time_step: int
        See: :py:attr:`time_step`
    time_step_units: str
        See: :py:attr:`time_step_units`
    time_system: str
        See: :py:attr:`time_system`
    time_format: str
        See: :py:attr:`time_format`
    target_1: str or int
        See: :py:attr:`target_1`
    target_2: str or int
        See: :py:attr:`target_2`
    observer: str or int
        See: :py:attr:`observer`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`target_1`, :py:attr:`target_2` and
        :py:attr:`observer` are not provided.

    """

    REQUIRED = ('target_1', 'target_2', 'observer')

    def __init__(self, shape_1='POINT', shape_2='POINT',
                 aberration_correction='CN', **kwargs):

        kwargs['calculation_type'] = 'ANGULAR_SEPARATION'
        kwargs['shape_1'] = shape_1
        kwargs['shape_2'] = shape_2
        kwargs['aberration_correction'] = aberration_correction

        super().__init__(**kwargs)


class AngularSize(Calculation):
    """Angular size calculation.

    Calculates the angular size of a target as seen by an observer.

    Parameters
    ----------
    aberration_correction: str, optional
        See: :py:attr:`aberration_correction`

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`kernels`
    kernel_paths: str, [str]
        See: :py:attr:`kernel_paths`
    times: str or [str]
        See: :py:attr:`times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`intervals`
    time_step: int
        See: :py:attr:`time_step`
    time_step_units: str
        See: :py:attr:`time_step_units`
    time_system: str
        See: :py:attr:`time_system`
    time_format: str
        See: :py:attr:`time_format`
    target: str or int
        See: :py:attr:`target`
    observer: str or int
        See: :py:attr:`observer`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`target` and :py:attr:`observer` are not provided.

    """

    REQUIRED = ('target', 'observer')

    def __init__(self, aberration_correction='CN', **kwargs):

        kwargs['calculation_type'] = 'ANGULAR_SIZE'
        kwargs['aberration_correction'] = aberration_correction

        super().__init__(**kwargs)


class FrameTransformation(Calculation):
    """Frame transforme calculation.

    Calculate the transformation from one reference frame (Frame 1)
    to another reference frame (Frame 2).

    Parameters
    ----------
    aberration_correction: str, optional
        See: :py:attr:`aberration_correction`
    time_location: str, optional
        See: :py:attr:`time_location`
    orientation_representation: str, optional
        See: :py:attr:`orientation_representation`
    axis_1: str, optional
        See: :py:attr:`axis_1`
    axis_2: str, optional
        See: :py:attr:`axis_2`
    axis_3: str, optional
        See: :py:attr:`axis_3`
    angular_units: str, optional
        See: :py:attr:`angular_units`
    angular_velocity_representation: str, optional
        See: :py:attr:`angular_velocity_representation`
    angular_velocity_units: str, optional
        See: :py:attr:`angular_velocity_units`

        Warning
        -------
        Attribute :py:attr:`aberration_correction` must be ``NONE``, `LT``, ``CN``,
        ``XLT`` or ``XCN``.

        Attributes :py:attr:`axis_1`, :py:attr:`axis_2` and :py:attr:`axis_3`
        are imported only if :py:attr:`orientation_representation` is ``EULER_ANGLES``.

        Attribute :py:attr:`angular_units` is imported only
        if :py:attr:`orientation_representation` is ``EULER_ANGLES``
        or ``ANGLE_AND_AXIS``.

        Attribute :py:attr:`angular_velocity_units` is imported only if
        :py:attr:`angular_velocity_representation` is ``VECTOR_IN_FRAME1``,
        ``VECTOR_IN_FRAME2`` or ``EULER_ANGLE_DERIVATIVES``.

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`kernels`
    kernel_paths: str, [str]
        See: :py:attr:`kernel_paths`
    times: str or [str]
        See: :py:attr:`times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`intervals`
    time_step: int
        See: :py:attr:`time_step`
    time_step_units: str
        See: :py:attr:`time_step_units`
    time_system: str
        See: :py:attr:`time_system`
    time_format: str
        See: :py:attr:`time_format`
    frame_1: str or int
        See: :py:attr:`frame_1`
    frame_2: str or int
        See: :py:attr:`frame_2`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`frame_1` and :py:attr:`frame_2` are not provided.
    CalculationInvalidAttr
        If :py:attr:`aberration_correction` is in ``LT+S``, ``CN+S``,
        ``XLT+S`` or ``XCN+S``.

    """

    REQUIRED = ('frame_1', 'frame_2')

    def __init__(self, aberration_correction='CN', time_location='FRAME1',
                 orientation_representation='EULER_ANGLES',
                 axis_1='X', axis_2='Y', axis_3='Z',
                 angular_units='deg',
                 angular_velocity_representation='VECTOR_IN_FRAME1',
                 angular_velocity_units='deg/s',
                 **kwargs):

        if aberration_correction not in VALID_PARAMETERS['ABERRATION_CORRECTION_NO_S']:
            raise CalculationInvalidAttr(
                'aberration_correction', aberration_correction,
                VALID_PARAMETERS['ABERRATION_CORRECTION_NO_S'])

        kwargs['calculation_type'] = 'FRAME_TRANSFORMATION'
        kwargs['aberration_correction'] = aberration_correction
        kwargs['time_location'] = time_location
        kwargs['orientation_representation'] = orientation_representation
        kwargs['angular_velocity_representation'] = angular_velocity_representation

        if orientation_representation == 'EULER_ANGLES':
            kwargs['axis_1'] = axis_1
            kwargs['axis_2'] = axis_2
            kwargs['axis_3'] = axis_3

        if orientation_representation in ['EULER_ANGLES', 'ANGLE_AND_AXIS']:
            kwargs['angular_units'] = angular_units

        if angular_velocity_representation in ['VECTOR_IN_FRAME1', 'VECTOR_IN_FRAME2',
                                               'EULER_ANGLE_DERIVATIVES']:
            kwargs['angular_velocity_units'] = angular_velocity_units

        super().__init__(**kwargs)


class IlluminationAngles(Calculation):
    """Illumination angles calculation.

    Calculate the emission, phase and solar incidence angles
    at a point on a target as seen from an observer.

    Parameters
    ----------
    shape_1: str, optional
        See: :py:attr:`shape_1`
    coordinate_representation: str, optional
        See: :py:attr:`coordinate_representation`
    aberration_correction: str, optional
        See: :py:attr:`aberration_correction`

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`kernels`
    kernel_paths: str, [str]
        See: :py:attr:`kernel_paths`
    times: str or [str]
        See: :py:attr:`times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`intervals`
    time_step: int
        See: :py:attr:`time_step`
    time_step_units: str
        See: :py:attr:`time_step_units`
    time_system: str
        See: :py:attr:`time_system`
    time_format: str
        See: :py:attr:`time_format`
    target: str or int
        See: :py:attr:`target`
    target_frame: str or int
        See: :py:attr:`target_frame`
    observer: str or int
        See: :py:attr:`observer`
    latitude: str or int
        See: :py:attr:`latitude`
    longitude: str or int
        See: :py:attr:`longitude`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`target`, :py:attr:`target_frame`, :py:attr:`observer`,
        :py:attr:`latitude` and :py:attr:`longitude` are not provided.
    CalculationInvalidAttr
        If :py:attr:`shape_1` is not ``ELLIPSOID`` or ``DSK``.

    """

    REQUIRED = ('target', 'target_frame', 'observer', 'latitude', 'longitude')

    def __init__(self, shape_1='ELLIPSOID', coordinate_representation='LATITUDINAL',
                 aberration_correction='CN', **kwargs):

        kwargs['calculation_type'] = 'ILLUMINATION_ANGLES'
        kwargs['coordinate_representation'] = coordinate_representation
        kwargs['aberration_correction'] = aberration_correction

        if shape_1 in ['ELLIPSOID', 'DSK']:
            kwargs['shape_1'] = shape_1
        else:
            raise CalculationInvalidAttr('shape_1', shape_1, ['ELLIPSOID', 'DSK'])

        super().__init__(**kwargs)


class SubSolarPoint(Calculation):
    """Sub-solar point calculation.

    Calculates the sub-solar point on a target as seen from an observer.

    Parameters
    ----------
    sub_point_type: str, optional
        See: :py:attr:`sub_point_type`
    aberration_correction: str, optional
        See: :py:attr:`aberration_correction`
    state_representation: str, optional
        See: :py:attr:`state_representation`

        Warning
        -------
        Attribute :py:attr:`aberration_correction` must be ``NONE``, `LT``, ``LT+S``,
        ``CN`` or ``CN+S``.

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`kernels`
    kernel_paths: str, [str]
        See: :py:attr:`kernel_paths`
    times: str or [str]
        See: :py:attr:`times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`intervals`
    time_step: int
        See: :py:attr:`time_step`
    time_step_units: str
        See: :py:attr:`time_step_units`
    time_system: str
        See: :py:attr:`time_system`
    time_format: str
        See: :py:attr:`time_format`
    target: str or int
        See: :py:attr:`target`
    target_frame: str or int
        See: :py:attr:`target_frame`
    observer: str or int
        See: :py:attr:`observer`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`target`, :py:attr:`target_frame` and :py:attr:`observer`
        are not provided.
    CalculationInvalidAttr
        If :py:attr:`aberration_correction` is in ``XLT``, ``XLT+S``,
        ``XCN+S`` or ``XCN+S``.

    """

    REQUIRED = ('target', 'target_frame', 'observer')

    def __init__(self, sub_point_type='Near point: ellipsoid', aberration_correction='CN',
                 state_representation='RECTANGULAR', **kwargs):

        if aberration_correction not in VALID_PARAMETERS['ABERRATION_CORRECTION_NO_X']:
            raise CalculationInvalidAttr(
                'aberration_correction', aberration_correction,
                VALID_PARAMETERS['ABERRATION_CORRECTION_NO_X'])

        kwargs['calculation_type'] = 'SUB_SOLAR_POINT'
        kwargs['sub_point_type'] = sub_point_type
        kwargs['aberration_correction'] = aberration_correction
        kwargs['state_representation'] = state_representation

        super().__init__(**kwargs)


class SubObserverPoint(Calculation):
    """Sub-observer point calculation.

    Calculate the sub-observer point on a target as seen from an observer.

    Parameters
    ----------
    sub_point_type: str, optional
        See: :py:attr:`sub_point_type`
    aberration_correction: str, optional
        See: :py:attr:`aberration_correction`
    state_representation: str, optional
        See: :py:attr:`state_representation`

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`kernels`
    kernel_paths: str, [str]
        See: :py:attr:`kernel_paths`
    times: str or [str]
        See: :py:attr:`times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`intervals`
    time_step: int
        See: :py:attr:`time_step`
    time_step_units: str
        See: :py:attr:`time_step_units`
    time_system: str
        See: :py:attr:`time_system`
    time_format: str
        See: :py:attr:`time_format`
    target: str or int
        See: :py:attr:`target`
    target_frame: str or int
        See: :py:attr:`target_frame`
    observer: str or int
        See: :py:attr:`observer`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`target`, :py:attr:`target_frame`
        and :py:attr:`observer` are not provided.

    """

    REQUIRED = ('target', 'target_frame', 'observer')

    def __init__(self, sub_point_type='Near point: ellipsoid', aberration_correction='CN',
                 state_representation='RECTANGULAR', **kwargs):

        kwargs['calculation_type'] = 'SUB_OBSERVER_POINT'
        kwargs['sub_point_type'] = sub_point_type
        kwargs['aberration_correction'] = aberration_correction
        kwargs['state_representation'] = state_representation

        super().__init__(**kwargs)


class SurfaceInterceptPoint(Calculation):
    """Surface intercept point calculation.

    Calculate the intercept point of a vector or vectors
    on a target as seen from an observer.

    Parameters
    ----------
    shape_1: str, optional
        See: :py:attr:`shape_1`
    direction_vector_type: str, optional
        See: :py:attr:`direction_vector_type`
    aberration_correction: str, optional
        See: :py:attr:`aberration_correction`
    state_representation: str, optional
        See: :py:attr:`state_representation`

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`kernels`
    kernel_paths: str, [str]
        See: :py:attr:`kernel_paths`
    times: str or [str]
        See: :py:attr:`times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`intervals`
    time_step: int
        See: :py:attr:`time_step`
    time_step_units: str
        See: :py:attr:`time_step_units`
    time_system: str
        See: :py:attr:`time_system`
    time_format: str
        See: :py:attr:`time_format`
    target: str or int
        See: :py:attr:`target`
    target_frame: str or int
        See: :py:attr:`target_frame`
    observer: str or int
        See: :py:attr:`observer`
    direction_instrument: str or int
        See: :py:attr:`direction_instrument`
    direction_frame: str
        See: :py:attr:`direction_frame`
    direction_frame_axis: str
        See: :py:attr:`direction_frame_axis`
    direction_vector_x: float
        See: :py:attr:`direction_vector_x`
    direction_vector_y: float
        See: :py:attr:`direction_vector_y`
    direction_vector_z: float
        See: :py:attr:`direction_vector_z`
    direction_vector_ra: float
        See: :py:attr:`direction_vector_ra`
    direction_vector_dec: float
        See: :py:attr:`direction_vector_dec`

        Warnings
        --------
        Attributes :py:attr:`direction_instrument` is needed only if
        :py:attr:`direction_vector_type` is ``INSTRUMENT_BORESIGHT``,
        ``INSTRUMENT_FOV_BOUNDARY_VECTORS`` or ``VECTOR_IN_INSTRUMENT_FOV``.

        Attributes :py:attr:`direction_frame` is needed only if
        :py:attr:`direction_vector_type` is ``REFERENCE_FRAME_AXIS`` or
        ``VECTOR_IN_REFERENCE_FRAME``.

        Attributes :py:attr:`direction_vector_x` + :py:attr:`direction_vector_y` +
        :py:attr:`direction_vector_z` or :py:attr:`direction_vector_ra` +
        :py:attr:`direction_vector_dec` is needed only if
        :py:attr:`direction_vector_type` is ``VECTOR_IN_INSTRUMENT_FOV`` or
        ``VECTOR_IN_REFERENCE_FRAME``.

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`target`, :py:attr:`target_frame`
        and :py:attr:`observer` are not provided.
    CalculationInvalidAttr
        If :py:attr:`shape_1` is not ``ELLIPSOID`` or ``DSK``.

    """

    REQUIRED = ('target', 'target_frame', 'observer')

    def __init__(self, shape_1='ELLIPSOID', direction_vector_type='INSTRUMENT_BORESIGHT',
                 aberration_correction='CN', state_representation='RECTANGULAR',
                 **kwargs):

        kwargs['calculation_type'] = 'SURFACE_INTERCEPT_POINT'
        kwargs['direction_vector_type'] = direction_vector_type
        kwargs['aberration_correction'] = aberration_correction
        kwargs['state_representation'] = state_representation

        if shape_1 in ['ELLIPSOID', 'DSK']:
            kwargs['shape_1'] = shape_1
        else:
            raise CalculationInvalidAttr('shape_1', shape_1, ['ELLIPSOID', 'DSK'])

        super().__init__(**kwargs)


class OsculatingElements(Calculation):
    """Osculating elements calculation.

    Calculate the osculating elements of the orbit of a target body around a central body.

    The orbit may be elliptical, parabolic, or hyperbolic.

    Parameters
    ----------
    reference_frame: str, optional
        See: :py:attr:`reference_frame`

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`kernels`
    kernel_paths: str, [str]
        See: :py:attr:`kernel_paths`
    times: str or [str]
        See: :py:attr:`times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`intervals`
    time_step: int
        See: :py:attr:`time_step`
    time_step_units: str
        See: :py:attr:`time_step_units`
    time_system: str
        See: :py:attr:`time_system`
    time_format: str
        See: :py:attr:`time_format`
    orbiting_body: str or int
        See: :py:attr:`orbiting_body`
    center_body: str or int
        See: :py:attr:`center_body`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`orbiting_body` and :py:attr:`center_body` are not provided.

    """

    REQUIRED = ('orbiting_body', 'center_body')

    def __init__(self, reference_frame='J2000', **kwargs):

        kwargs['calculation_type'] = 'OSCULATING_ELEMENTS'
        kwargs['reference_frame'] = reference_frame

        super().__init__(**kwargs)


class TimeConversion(Calculation):
    """Time conversion calculation.

    Convert times from one time system or format to another.

    Parameters
    ----------
    output_time_system: str, optional
        See: :py:attr:`output_time_system`
    output_time_format: str, optional
        See: :py:attr:`output_time_format`

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`kernels`
    kernel_paths: str, [str]
        See: :py:attr:`kernel_paths`
    times: str or [str]
        See: :py:attr:`times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`intervals`
    time_step: int
        See: :py:attr:`time_step`
    time_step_units: str
        See: :py:attr:`time_step_units`
    time_system: str
        See: :py:attr:`time_system`
    time_format: str
        See: :py:attr:`time_format`
    output_sclk_id: str
        See: :py:attr:`output_sclk_id`
    output_time_custom_format: str
        See: :py:attr:`output_time_custom_format`

        Warnings
        --------
        Attributes :py:attr:`output_sclk_id` is needed only if
        :py:attr:`output_time_system` is ``SPACECRAFT_CLOCK``.

        Attributes :py:attr:`output_time_custom_format` is needed only if
        :py:attr:`output_time_format` is ``CUSTOM``.

    """

    def __init__(self, output_time_system='UTC', output_time_format='CALENDAR', **kwargs):

        kwargs['calculation_type'] = 'TIME_CONVERSION'
        kwargs['output_time_system'] = output_time_system
        kwargs['output_time_format'] = output_time_format

        super().__init__(**kwargs)


class GFCoordinateSearch(Calculation):
    """Coordinate Search (Geometry Finder) calculation.

    Find time intervals when a coordinate of an observer-target position vector
    satisfies a condition.

    Parameters
    ----------
    output_duration_units: str, optional
        See: :py:attr:`output_duration_units`
    should_complement_window: bool, optional
        See: :py:attr:`should_complement_window`
    interval_adjustment: str, optional
        See: :py:attr:`interval_adjustment`
    interval_filtering: str, optional
        See: :py:attr:`interval_filtering`
    aberration_correction: str, optional
        See: :py:attr:`aberration_correction`
    coordinate_system: str
        See: :py:attr:`coordinate_system`
    coordinate: str
        See: :py:attr:`coordinate`
    relational_condition: str
        See: :py:attr:`relational_condition`
    reference_value: float, optional
        See: :py:attr:`reference_value`
    upper_limit: float, optional
        See: :py:attr:`upper_limit`
    adjustment_value, float, optional
        See: :py:attr:`adjustment_value`

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`kernels`
    kernel_paths: str, [str]
        See: :py:attr:`kernel_paths`
    times: str or [str]
        See: :py:attr:`times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`intervals`
    time_step: int
        See: :py:attr:`time_step`
    time_step_units: str
        See: :py:attr:`time_step_units`
    time_system: str
        See: :py:attr:`time_system`
    time_format: str
        See: :py:attr:`time_format`
    target: str or int
        See: :py:attr:`target`
    observer: str or int
        See: :py:attr:`observer`
    reference_frame: str or int
        See: :py:attr:`reference_frame`

        Warnings
        --------
        Attributes :py:attr:`upper_limit` is needed only if
        :py:attr:`relational_condition` is ``RANGE``.

        Attributes :py:attr:`adjustment_value` is needed only if
        :py:attr:`relational_condition` is ``ABSMIN`` or ``ABSMAX``.

        Attribute :py:attr:`reference_value` is needed only if
        :py:attr:`relational_condition` is ``=``, ``<``, ``>`` or
        ``RANGE``.

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`target`, :py:attr:`observer`,
        :py:attr:`reference_frame`, :py:attr:`coordinate_system`,
        :py:attr:`coordinate`, or :py:attr:`relational_condition` are not
        provided.

    """

    REQUIRED = ('target', 'observer', 'reference_frame', 'relational_condition')

    def __init__(self, output_duration_units='SECONDS',
                 should_complement_window=False,
                 interval_adjustment='NO_ADJUSTMENT',
                 interval_filtering='NO_FILTERING',
                 aberration_correction='CN', **kwargs):

        kwargs['calculation_type'] = 'GF_COORDINATE_SEARCH'
        kwargs['aberration_correction'] = aberration_correction
        kwargs['output_duration_units'] = output_duration_units
        kwargs['should_complement_window'] = should_complement_window
        kwargs['interval_adjustment'] = interval_adjustment
        kwargs['interval_filtering'] = interval_filtering

        super().__init__(**kwargs)
