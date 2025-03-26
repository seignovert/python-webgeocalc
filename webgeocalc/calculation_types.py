"""Webgeocalc calculations types."""

from .calculation import Calculation
from .errors import CalculationInvalidAttr, CalculationNotImplemented
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
    There are two types of calculation. The default one is the angular separation
    between two targets (``TWO_TARGETS`` mode). The second case is the angular
    separation between two directions (``TWO_DIRECTIONS`` mode).

    Parameters
    ----------
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

    Other Parameters
    ----------------
    spec_type: str, optional
        See: :py:attr:`spec_type` either ``TWO_TARGETS`` (default)
        or ``TWO_DIRECTIONS``.

    Required parameters `TWO_TARGETS`

    target_1: str or int
        See: :py:attr:`target_1`
    shape_1: str, optional
        See: :py:attr:`shape_1` (default: ``POINT``)
    target_2: str or int
        See: :py:attr:`target_2`
    shape_2: str, optional
        See: :py:attr:`shape_2` (default: ``POINT``)
    observer: str or int
        See: :py:attr:`observer`
    aberration_correction: str, optional
        See: :py:attr:`aberration_correction`

    Required parameters `TWO_DIRECTIONS`

    direction_1: dict or Direction
        See: :py:attr:`direction_1`
    direction_2: dict or Direction
        See: :py:attr:`direction_2`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`spec_type` is ``TWO_TARGETS`` or not set:
            If py:attr:`target_1`, :py:attr:`target_2`
                or :py:attr:`observer` are not provided.
        If :py:attr:`spec_type` is ``TWO_DIRECTIONS``:
            If :py:attr:`direction_1` or :py:attr:`direction_2`
                are not provided.

    """

    def __init__(self, spec_type='TWO_TARGETS',
                 aberration_correction='CN', **kwargs):

        kwargs['calculation_type'] = 'ANGULAR_SEPARATION'

        match spec_type:
            case 'TWO_TARGETS':
                self.REQUIRED += ('target_1', 'target_2', 'observer')

                for key in ['shape_1', 'shape_2']:
                    kwargs.setdefault(key, 'POINT')

                kwargs['aberration_correction'] = aberration_correction

            case 'TWO_DIRECTIONS':
                self.REQUIRED += ('direction_1', 'direction_2')

                kwargs['spec_type'] = spec_type

            case _:
                raise CalculationInvalidAttr(
                    'spec_type', spec_type, VALID_PARAMETERS['SPEC_TYPE'],
                )

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
    """Frame transform calculation.

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


class PhaseAngle(Calculation):
    """Phase angle calculation.

    Calculate the phase angle defined by the centers of an illumination source,
    a target and an observer.

    The phase angle is computed using the location of the bodies (if point objects)
    or the center of the bodies (if finite bodies).

    The range of the phase angle is [0, pi].

    Parameters
    ----------
    target: str or int
        See: :py:attr:`target`
    observer: str or int
        See: :py:attr:`observer`
    illuminator: str or int, optional
        See: :py:attr:`illuminator` (default: ``SUN``)
    aberration_correction: str, optional
        See: :py:attr:`aberration_correction` (default: ``CN``)

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

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`target` or :py:attr:`observer` are not provided.

    """

    REQUIRED = ('target', 'observer')

    def __init__(self, illuminator='SUN', aberration_correction='CN', **kwargs):

        kwargs['calculation_type'] = 'PHASE_ANGLE'
        kwargs['illuminator'] = illuminator
        kwargs['aberration_correction'] = aberration_correction

        super().__init__(**kwargs)


class PointingDirection(Calculation):
    """Pointing direction calculation.

    Calculates the pointing direction in a user specified reference frame and
    output it as a unit or full magnitude vector represented in a user
    specified coordinate system.

    The direction can be specified by the position or velocity of an object
    with respect to an observer, or by directly providing a vector,
    which could be specified as coordinates in a given frame, a frame axis,
    an instrument boresight, or as instrument FoV corner vectors.

    The output reference frame may be different than the one used for specification
    of the input vector (if such option is selected). If so, the orientations
    of both frames relative to the inertial space are computed at the same time
    taking into account the aberration corrections given in the direction specification.

    The output direction could be given as unit or non-unit vector in
    Rectangular, Azimuth/Elevation, Right Ascension/Declination/Range,
    Planetocentric, Cylindrical, or Spherical coordinates.

    Parameters
    ----------
    direction: dict or Direction
        See: :py:attr:`direction`
    reference_frame: str or int
        See: :py:attr:`reference_frame`
    vector_magnitude: str, optional
        See: :py:attr:`vector_magnitude` (default: ``UNIT``)
    coordinate_representation: str, optional
        See: :py:attr:`coordinate_representation` (default: ``RECTANGULAR``)

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

    Required parameters `AZ_EL`

    azccw_flag: bool or str
        See: :py:attr:`azccw_flag`
    elplsz_flag: bool or str
        See: :py:attr:`elplsz_flag`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`target` or :py:attr:`reference_frame` are not provided.

    """

    REQUIRED = ('direction', 'reference_frame')

    def __init__(self, vector_magnitude='UNIT',
                 coordinate_representation='RECTANGULAR', **kwargs):

        valid = VALID_PARAMETERS['COORDINATE_REPRESENTATION_POINTING_DIRECTION']
        if coordinate_representation not in valid:
            raise CalculationInvalidAttr(
                'coordinate_representation', coordinate_representation, valid)

        if coordinate_representation == 'AZ_EL':
            self.REQUIRED += ('azccw_flag', 'elplsz_flag')

        kwargs['calculation_type'] = 'POINTING_DIRECTION'
        kwargs['vector_magnitude'] = vector_magnitude
        kwargs['coordinate_representation'] = coordinate_representation

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


class TangentPoint(Calculation):
    """Tangent point calculation.

    Calculate the tangent point for a given observer, ray emanating
    from the observer, and target.

    The tangent point is defined as the point on the ray nearest to the target's surface.
    This panel also computes the point on the target's surface nearest to
    the tangent point. The locations of both points are optionally corrected for
    light time and stellar aberration, and may be represented using either
    Rectangular, Ra/Dec, Planetocentric, Planetodetic, Planetographic, Spherical or
    Cylindrical coordinates.

    The target's surface shape is modeled as a triaxial ellipsoid.

    For remote sensing observations, for maximum accuracy, reception light time and
    stellar aberration corrections should be used. These corrections model
    observer-target-ray geometry as it is observed.

    For signal transmission applications, for maximum accuracy, transmission light
    time and stellar aberration corrections should be used. These corrections model
    the observer-target-ray geometry that applies to the transmitted signal.
    For example, these corrections are needed to calculate the minimum altitude
    of the signal's path over the target body.

    This calculation ignores differential aberration effects over the target
    body's surface: it computes corrections only at a user-specified point,
    which is called the "aberration correction locus."
    The user may select either the **Tangent point** or corresponding **Surface point**
    as the locus. In many cases, the differences between corrections for
    these points are very small.

    Additionally, the illumination angles (incidence, emission and phase),
    time and local true solar time at the target point (where the aberration
    correction locus is set -- or at the tangent point if no corrections are used),
    and the light time to that point, are computed.

    Parameters
    ----------
    target: str or int
        See: :py:attr:`target`
    target_frame: str or int
        See: :py:attr:`target_frame`
    observer: str or int
        See: :py:attr:`observer`
    direction_vector_type: str
        See: :py:attr:`direction_vector_type`

    direction_object: str or int
        See: :py:attr:`direction_object`.
        Only when :py:attr:`direction_vector_type` is ``DIRECTION_TO_OBJECT``

    direction_instrument: str or int
        See: :py:attr:`direction_instrument`.
        Only when :py:attr:`direction_vector_type` is
        ``INSTRUMENT_BORESIGHT, ``INSTRUMENT_FOV_BOUNDARY_VECTORS``
        or ``VECTOR_IN_INSTRUMENT_FOV``

    direction_frame: str
        See: :py:attr:`direction_frame`.
        Only when :py:attr:`direction_vector_type` is
        ``REFERENCE_FRAME_AXIS`` or ``VECTOR_IN_REFERENCE_FRAME``

    direction_frame_axis: str
        See: :py:attr:`direction_frame_axis`.
        Only when :py:attr:`direction_vector_type` is
        ``REFERENCE_FRAME_AXIS``.

    direction_vector_x: float
        See: :py:attr:`direction_vector_x`.
        Only when :py:attr:`direction_vector_type` is
        ``VECTOR_IN_INSTRUMENT_FOV`` or ``VECTOR_IN_REFERENCE_FRAME``

    direction_vector_y: float
        See: :py:attr:`direction_vector_y`.
        Only when :py:attr:`direction_vector_type` is
        ``VECTOR_IN_INSTRUMENT_FOV`` or ``VECTOR_IN_REFERENCE_FRAME``

    direction_vector_z: float
        See: :py:attr:`direction_vector_z`.
        Only when :py:attr:`direction_vector_type` is
        ``VECTOR_IN_INSTRUMENT_FOV`` or ``VECTOR_IN_REFERENCE_FRAME``

    direction_vector_ra: float
        See: :py:attr:`direction_vector_ra`
        Only when :py:attr:`direction_vector_type` is
        ``VECTOR_IN_INSTRUMENT_FOV`` or ``VECTOR_IN_REFERENCE_FRAME``

    direction_vector_dec: float
        See: :py:attr:`direction_vector_dec`
        Only when :py:attr:`direction_vector_type` is
        ``VECTOR_IN_INSTRUMENT_FOV`` or ``VECTOR_IN_REFERENCE_FRAME``

    direction_vector_az: float
        See: :py:attr:`direction_vector_az`
        Only when :py:attr:`direction_vector_type` is
        ``VECTOR_IN_INSTRUMENT_FOV`` or ``VECTOR_IN_REFERENCE_FRAME``

    direction_vector_el: float
        See: :py:attr:`direction_vector_el`
        Only when :py:attr:`direction_vector_type` is
        ``VECTOR_IN_INSTRUMENT_FOV`` or ``VECTOR_IN_REFERENCE_FRAME``

    azccw_flag: bool or str
        See: :py:attr:`azccw_flag`.
        Only when :py:attr:`direction_vector_az` is provided.

    elplsz_flag: bool or str
        See: :py:attr:`elplsz_flag`.
        Only when :py:attr:`direction_vector_el` is provided.

    computation_method: str, optional
        See: :py:attr:`computation_method` (default: ``ELLIPSOID``)
    vector_ab_corr: str, optional
        See: :py:attr:`vector_ab_corr` (default: ``NONE``)
    aberration_correction: str, optional
        See: :py:attr:`aberration_correction` (default: ``CN``)
    correction_locus: str, optional
        See: :py:attr:`correction_locus`
        (required if :py:attr:`aberration_correction` is not ``NONE``)
    coordinate_representation: str, optional
        See: :py:attr:`coordinate_representation` (default: ``RECTANGULAR``)

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

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`target`, :py:attr:`reference_frame`, :py:attr:`observer`
        or :py:attr:`direction_vector_type` are not provided.
    CalculationRequiredAttr
        If :py:attr:`aberration_correction` is not ``NONE`` and
        :py:attr:`correction_locus` is not provided.

    """

    REQUIRED = ('target', 'target_frame', 'observer', 'direction_vector_type')

    def __init__(self, computation_method='ELLIPSOID',
                 vector_ab_corr='NONE', aberration_correction='CN',
                 coordinate_representation='RECTANGULAR', **kwargs):

        if aberration_correction != 'NONE':
            self.REQUIRED += ('correction_locus',)

        valid = VALID_PARAMETERS['COORDINATE_REPRESENTATION_TANGENT_POINT']
        if coordinate_representation not in valid:
            raise CalculationInvalidAttr(
                'coordinate_representation', coordinate_representation, valid)

        kwargs['calculation_type'] = 'TANGENT_POINT'
        kwargs['computation_method'] = computation_method

        if kwargs.get('direction_vector_type') == 'VECTOR_IN_REFERENCE_FRAME':
            kwargs['vector_ab_corr'] = vector_ab_corr

        kwargs['aberration_correction'] = aberration_correction
        kwargs['coordinate_representation'] = coordinate_representation

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


# pylint: disable=abstract-method
class GFAngularSeparationSearch(CalculationNotImplemented):
    """Angular separation search geometry finder.

    Find time intervals when the angle between two bodies,
    as seen by an observer, satisfies a condition.

    """


class GFDistanceSearch(CalculationNotImplemented):
    """Distance search geometry finder.

    Find time intervals when the distance between a target
    and observer satisfies a condition.

    """


class GFSubPointSearch(CalculationNotImplemented):
    """Sub-point search geometry finder.

    Find time intervals when a coordinate of the sub-observer point
    on a target satisfies a condition.

    """


class GFOccultationSearch(CalculationNotImplemented):
    """Occultation search geometry finder.

    Find time intervals when an observer sees one target occulted by,
    or in transit across, another.

    """


class GFSurfaceInterceptPointSearch(CalculationNotImplemented):
    """Surface intercept point search geometry finder.

    Find time intervals when a coordinate of a surface intercept vector
    satisfies a condition.

    """


class GFTargetInInstrumentFovSearch(CalculationNotImplemented):
    """Target in instrument fov search geometry finder.

    Find time intervals when a target intersects the space bounded by
    the field-of-view of an instrument.

    """


class GFRayInFovSearch(CalculationNotImplemented):
    """Ray in fov search geometry finder.

    Find time intervals when a specified ray is contained in the space bounded
    by an instrument's field-of-view.

    """


class GFRangeRateSearch(CalculationNotImplemented):
    """Range rate search geometry finder.

    Find time intervals when the range rate between a target and observer
    satisfies a condition.

    """


class GFPhaseAngleSearch(CalculationNotImplemented):
    """Phase angle search geometry finder.

    Find time intervals for which a specified constraint on the phase angle defined
    by an illumination source, a target, and an observer body centers is met.

    """


class GFIlluminationAnglesSearch(CalculationNotImplemented):
    """Illumination angles search geometry finder.

    Find the time intervals, within a specified time window, when one of the illumination
    angles — phase, incidence or emission — at the specified target body surface point
    as seen from an observer satisfies a given constraint.

    """
