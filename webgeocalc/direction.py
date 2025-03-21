"""Webgeocalc Directions."""

from .decorator import parameter
from .errors import (CalculationIncompatibleAttr, CalculationInvalidAttr,
                     CalculationUndefinedAttr)
from .payload import Payload
from .vars import VALID_PARAMETERS


class Direction(Payload):
    """Webgeocalc direction object.

    Parameters
    ----------
    direction_type: str
        See: :py:attr:`direction_type`
        Depending on the desired :py:attr:`direction_type`,
        different parameters are required.
    observer: str or int
        See: :py:attr:`observer`
        Not required if :py:attr:`aberration_correction` is ``NONE``
        and :py:attr:`direction vector` is ``VECTOR``.

    Required parameters 'POSITION'

    target: str or int
        See: :py:attr:`target`
    shape: str
        See: :py:attr:`shape`

    Required parameters 'VELOCITY'

    target: str or int
        See: :py:attr:`target`
    reference_frame: str, optional
        See: :py:attr:`reference_frame`

    Required parameters 'VECTOR'

    direction_vector_type: str
        See: :py:attr:`direction_vector_type`
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
    direction_vector_az: float
        See: :py:attr:`direction_vector_az`
    direction_vector_el: float
        See: :py:attr:`direction_vector_el`
    azccw_flag: bool or str
        See: :py:attr:`azccw_flag`
    elplsz_flag: bool or str
        See: :py:attr:`elplsz_flag`

    Other Parameters
    ----------------
    aberration_correction: str, optional
        See: :py:attr:`aberration_correction` (default: ``NONE``)
    anti_vector_flag: str or bool, optional
        See: :py:attr:`anti_vector_flag` (default: ``False``)


    """

    REQUIRED = ('direction_type', )

    def __init__(self, aberration_correction='NONE',
                 anti_vector_flag=False, **kwargs):

        match kwargs.get('direction_type'):
            case 'POSITION':
                self.REQUIRED += ('target', 'observer')
            case 'VELOCITY':
                self.REQUIRED += ('target', 'reference_frame', 'observer')
            case 'VECTOR':
                self.REQUIRED += ('direction_vector_type',)

        kwargs['aberration_correction'] = aberration_correction
        kwargs['anti_vector_flag'] = anti_vector_flag

        super().__init__(**kwargs)

    @parameter(only='DIRECTION_TYPE')
    def direction_type(self, val):
        """Type of direction.

        Method used to specify a direction. Directions could be specified as the
        position of an object as seen from the observer, as the velocity vector of
        an object as seen from the observer in a given reference frame, or by
        providing a vector in a given reference frame.

        Parameters
        ----------
        direction_type: str
            The type of direction string. One of:

            - ``POSITION``
            - ``VELOCITY``
            - ``VECTOR``

            Velocity depends on the reference frame in which it is expressed.

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        self.__directionType = val

    @parameter
    def observer(self, val):
        """Observing body.

        Parameters
        ----------
        observer: str or int
            The observing body ``name`` or ``id`` from :py:func:`API.bodies`.
            Required if :py:attr:`aberration_correction` is not ``'NONE'``
            for direction vector of type ``'VECTOR'``.

        """
        self.__observer = val if isinstance(val, int) else val.upper()

    @parameter
    def target(self, val):
        """Target body.

        Parameters
        ----------
        target: str or int
            The target body ``name`` or ``id`` from :py:func:`API.bodies`.

        """
        self.__target = val if isinstance(val, int) else val.upper()

    @parameter(only='TARGET_SHAPE')
    def shape(self, val):
        """The shape to use for the first body.

        Parameters
        ----------
        shape: str
            One of:

            - ``POINT``
            - ``SPHERE``

        Raises
        -------
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        self.__shape = val

    @parameter
    def reference_frame(self, val):
        """The reference frame name.

        Parameters
        ----------
        reference_frame: str
            The reference frame name.

        """
        self.__referenceFrame = val.upper()

    @parameter(only='DIRECTION_VECTOR_TYPE')
    def direction_vector_type(self, val):
        """Direction vector type.

        Parameters
        ----------
        direction_vector_type: str
            The direction vector type string. One of:

            - ``INSTRUMENT_BORESIGHT``
            - ``REFERENCE_FRAME_AXIS``
            - ``VECTOR_IN_INSTRUMENT_FOV``
            - ``VECTOR_IN_REFERENCE_FRAME``
            - ``INSTRUMENT_FOV_BOUNDARY_VECTORS`` (*)

            (*) only for :py:class:`PointingDirection` calculation.

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.
        CalculationRequiredAttr
            If this parameter is ``INSTRUMENT_BORESIGHT``,
            ``VECTOR_IN_INSTRUMENT_FOV`` or ``INSTRUMENT_FOV_BOUNDARY_VECTORS``
            but :py:attr:`direction_instrument` is not provided.
        CalculationRequiredAttr
            If this parameter is ``REFERENCE_FRAME_AXIS`` or ``VECTOR_IN_REFERENCE_FRAME``
            but :py:attr:`direction_frame` is not provided.
        CalculationRequiredAttr
            If this parameter is ``REFERENCE_FRAME_AXIS`` but
            :py:attr:`direction_frame_axis` is not provided.

        """
        match val:
            case (
                'INSTRUMENT_BORESIGHT' |
                'VECTOR_IN_INSTRUMENT_FOV' |
                'INSTRUMENT_FOV_BOUNDARY_VECTORS'
            ):
                self._required('direction_instrument')
            case 'REFERENCE_FRAME_AXIS':
                self._required('direction_frame', 'direction_frame_axis')
            case 'VECTOR_IN_REFERENCE_FRAME':
                self._required('direction_frame')

        match val:
            case (
                'VECTOR_IN_INSTRUMENT_FOV' |
                'VECTOR_IN_REFERENCE_FRAME'
            ):
                if not self._vector_coordinates():
                    raise CalculationUndefinedAttr(
                        'direction_vector_type', val,
                        "' or '".join([
                            'direction_vector_x/y/z',
                            'direction_vector_ra/dec',
                            'direction_vector_az/el',
                        ])
                    )

        self.__directionVectorType = val

    def _vector_coordinates(self):
        """Check if the vector any coordinates are present."""
        keys = self.params.keys()
        return (
            'direction_vector_x' in keys and
            'direction_vector_y' in keys and
            'direction_vector_z' in keys
        ) or (
            'direction_vector_ra' in keys and
            'direction_vector_dec' in keys
        ) or (
            'direction_vector_az' in keys and
            'direction_vector_el' in keys
        )

    @parameter
    def direction_instrument(self, val):
        """The instrument direction.

        Required only if :py:attr:`direction_vector_type` is ``INSTRUMENT_BORESIGHT``,
        ``VECTOR_IN_INSTRUMENT_FOV`` or ``INSTRUMENT_FOV_BOUNDARY_VECTORS``.

        Parameters
        ----------
        direction_instrument: str or int
            The instrument ``name`` or ``ID``.

        Raises
        ------
        CalculationIncompatibleAttr
            If :py:attr:`direction_vector_type` not in ``INSTRUMENT_BORESIGHT``,
            ``INSTRUMENT_FOV_BOUNDARY_VECTORS`` or ``VECTOR_IN_INSTRUMENT_FOV``.


        """
        only = [
            'INSTRUMENT_BORESIGHT',
            'INSTRUMENT_FOV_BOUNDARY_VECTORS',
            'VECTOR_IN_INSTRUMENT_FOV',
        ]

        if self.params['direction_vector_type'] not in only:
            raise CalculationIncompatibleAttr(
                'direction_instrument', val, 'direction_vector_type',
                self.params['direction_vector_type'], only)

        self.__directionInstrument = val if isinstance(val, int) else val.upper()

    @parameter
    def direction_frame(self, val):
        """The vector's reference frame name.

        Required only if :py:attr:`direction_vector_type` is ``REFERENCE_FRAME_AXIS``
        or ``VECTOR_IN_REFERENCE_FRAME``.

        Parameters
        ----------
        direction_frame: str
            The vector's reference frame name.

        Raises
        ------
        CalculationIncompatibleAttr
            If :py:attr:`direction_vector_type` is not in ``REFERENCE_FRAME_AXIS``
            or ``VECTOR_IN_REFERENCE_FRAME``.

        """
        only = [
            'REFERENCE_FRAME_AXIS',
            'VECTOR_IN_REFERENCE_FRAME',
        ]

        if self.params['direction_vector_type'] not in only:
            raise CalculationIncompatibleAttr(
                'direction_instrument', val, 'direction_vector_type',
                self.params['direction_vector_type'], only)

        self.__directionFrame = val

    @parameter(only='AXIS')
    def direction_frame_axis(self, val):
        """The direction vector frame axis.

        Required only if :py:attr:`direction_vector_type` is ``REFERENCE_FRAME_AXIS``.

        Parameters
        ----------
        direction_frame_axis: str
            The direction frame axis string. One of:

            - ``X``
            - ``Y``
            - ``Z``

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.
        CalculationIncompatibleAttr
            If :py:attr:`direction_vector_type` is not ``REFERENCE_FRAME_AXIS``.
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        if self.params['direction_vector_type'] != 'REFERENCE_FRAME_AXIS':
            raise CalculationIncompatibleAttr(
                'direction_frame_axis', val, 'direction_vector_type',
                self.params['direction_vector_type'], ['REFERENCE_FRAME_AXIS'])

        self.__directionFrameAxis = val

    def _vector(self, axis, val):
        """Direction vector coordinate.

        Parameters
        ----------
        axis: str
            Axis name.
        val: float
            Value on the axis.

        Raises
        ------
        CalculationIncompatibleAttr
            If :py:attr:`direction_vector_type` is not in ``VECTOR_IN_INSTRUMENT_FOV``
            or ``VECTOR_IN_REFERENCE_FRAME``.

        """
        only = [
            'VECTOR_IN_INSTRUMENT_FOV',
            'VECTOR_IN_REFERENCE_FRAME',
        ]

        if self.params['direction_vector_type'] not in only:
            raise CalculationIncompatibleAttr(
                'direction_vector_' + axis, val, 'direction_vector_type',
                self.params['direction_vector_type'], only)

        return val

    @parameter
    def direction_vector_x(self, val):
        """The X direction vector coordinate.

        If :py:attr:`direction_vector_type` is ``VECTOR_IN_INSTRUMENT_FOV`` or
        ``VECTOR_IN_REFERENCE_FRAME``, then either all three of
        :py:attr:`direction_vector_x`,
        :py:attr:`direction_vector_y`, and
        :py:attr:`direction_vector_z` must be provided.

        Parameters
        ----------
        direction_vector_x: float
            The X direction vector coordinate value.

        """
        self.__directionVectorX = self._vector('x', val)

    @parameter
    def direction_vector_y(self, val):
        """The Y direction vector coordinate.

        If :py:attr:`direction_vector_type` is ``VECTOR_IN_INSTRUMENT_FOV`` or
        ``VECTOR_IN_REFERENCE_FRAME``, then either all three of
        :py:attr:`direction_vector_x`,
        :py:attr:`direction_vector_y`, and
        :py:attr:`direction_vector_z` must be provided.

        Parameters
        ----------
        direction_vector_y: float
            The Y direction vector coordinate value.

        """
        self.__directionVectorY = self._vector('y', val)

    @parameter
    def direction_vector_z(self, val):
        """The Z direction vector coordinate.

        If :py:attr:`direction_vector_type` is ``VECTOR_IN_INSTRUMENT_FOV`` or
        ``VECTOR_IN_REFERENCE_FRAME``, then either all three of
        :py:attr:`direction_vector_x`,
        :py:attr:`direction_vector_y`, and
        :py:attr:`direction_vector_z` must be provided.

        Parameters
        ----------
        direction_vector_z: float
            The Z direction vector coordinate value.

        """
        self.__directionVectorZ = self._vector('z', val)

    @parameter
    def direction_vector_ra(self, val):
        """The right ascension direction vector coordinate.

        If :py:attr:`direction_vector_type` is ``VECTOR_IN_INSTRUMENT_FOV`` or
        ``VECTOR_IN_REFERENCE_FRAME``, then either all three of
        :py:attr:`direction_vector_ra` and
        :py:attr:`direction_vector_dec` must be provided.

        Parameters
        ----------
        direction_vector_ra: float
            The right ascension direction vector coordinate value.

        """
        self.__directionVectorRA = self._vector('ra', val)

    @parameter
    def direction_vector_dec(self, val):
        """The declination direction vector coordinate.

        If :py:attr:`direction_vector_type` is ``VECTOR_IN_INSTRUMENT_FOV`` or
        ``VECTOR_IN_REFERENCE_FRAME``, then either all three of
        :py:attr:`direction_vector_ra` and
        :py:attr:`direction_vector_dec` must be provided.

        Parameters
        ----------
        direction_vector_dec: float
            The declination direction vector coordinate value.

        """
        self.__directionVectorDec = self._vector('dec', val)

    @parameter
    def direction_vector_az(self, val):
        """The azimuth direction vector coordinate.

        If :py:attr:`direction_vector_type` is ``VECTOR_IN_INSTRUMENT_FOV`` or
        ``VECTOR_IN_REFERENCE_FRAME``, then either all three of
        :py:attr:`direction_vector_az`,
        :py:attr:`direction_vector_el`,
        :py:attr:`azccw_flag` and
        :py:attr:`elplsz_flag` must be provided.

        Parameters
        ----------
        direction_vector_az: float
            The azimuth direction vector coordinate value.

        """
        self._required('azccw_flag')
        self.__directionVectorAz = self._vector('az', val)

    @parameter
    def direction_vector_el(self, val):
        """The elevation direction vector coordinate.

        If :py:attr:`direction_vector_type` is ``VECTOR_IN_INSTRUMENT_FOV`` or
        ``VECTOR_IN_REFERENCE_FRAME``, then either all three of
        :py:attr:`direction_vector_az`,
        :py:attr:`direction_vector_el`,
        :py:attr:`azccw_flag` and
        :py:attr:`elplsz_flag` must be provided.

        Parameters
        ----------
        direction_vector_el: float
            The elevation vector coordinate value.

        """
        self._required('elplsz_flag')
        self.__directionVectorEl = self._vector('el', val)

    @parameter(only='BOOLEAN')
    def azccw_flag(self, val):
        """Flag indicating how azimuth is measured.

        If :py:attr:`direction_vector_type` is ``VECTOR_IN_INSTRUMENT_FOV`` or
        ``VECTOR_IN_REFERENCE_FRAME``, then either all three of
        :py:attr:`direction_vector_az`,
        :py:attr:`direction_vector_el`,
        :py:attr:`azccw_flag` and
        :py:attr:`elplsz_flag` must be provided.

        Parameters
        ----------
        azccw_flag: bool
            Flag indicating how azimuth is measured.

        Raises
        ------
        CalculationUndefinedAttr
            If :py:attr:`direction_vector_az` is not provided.
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        if 'direction_vector_az' not in self.params:
            raise CalculationUndefinedAttr(
                'azccw_flag', val, 'direction_vector_az')

        if isinstance(val, str):
            val = val.upper() == 'TRUE'

        self.__azccwFlag = val

    @parameter(only='BOOLEAN')
    def elplsz_flag(self, val):
        """Flag indicating how elevation is measured.

        If :py:attr:`direction_vector_type` is ``VECTOR_IN_INSTRUMENT_FOV`` or
        ``VECTOR_IN_REFERENCE_FRAME``, then either all three of
        :py:attr:`direction_vector_az`,
        :py:attr:`direction_vector_el`,
        :py:attr:`azccw_flag` and
        :py:attr:`elplsz_flag` must be provided.

        Parameters
        ----------
        elplsz_flag: bool
            ag indicating how elevation is measured.

        Raises
        ------
        CalculationUndefinedAttr
            If :py:attr:`direction_vector_el` is not provided.
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        if 'direction_vector_el' not in self.params:
            raise CalculationUndefinedAttr(
                'elplsz_flag', val, 'direction_vector_el')

        if isinstance(val, str):
            val = val.upper() == 'TRUE'

        self.__elplszFlag = val

    @parameter
    def aberration_correction(self, val):
        """SPICE aberration correction.

        Parameters
        ----------
        aberration_correction: str
            The SPICE aberration correction string.

            For ``POSITION`` or ``VELOCITY``, one of:

            - ``NONE``
            - ``LT``
            - ``LT+S``
            - ``CN``
            - ``CN+S``
            - ``XLT``
            - ``XLT+S``
            - ``XCN``
            - ``XCN+S``

            For ``VECTOR``, light time correction is applied
            to the rotation from the vector frame to ``J2000``,
            while stellar aberration corrections apply
            to the vector direction. One of:

            - ``NONE``
            - ``LT``
            - ``CN``
            - ``XLT``
            - ``XCN``
            - ``S``
            - ``XS``

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.
        CalculationRequiredAttr
            If this ``DIRECTION_TYPE`` is ``VECTOR`` and
            ``ABERRATION_CORRECTION`` is ``NONE``
            but :py:attr:`observer` is not provided.

        """
        match self.params['direction_type']:
            case 'VECTOR':
                valid = 'ABERRATION_CORRECTION_VECTOR'
                if val != 'NONE':
                    self._required('observer')
            case _:
                valid = 'ABERRATION_CORRECTION'

        if val not in VALID_PARAMETERS[valid]:
            raise CalculationInvalidAttr(
                'aberration_correction',
                val,
                VALID_PARAMETERS[valid],
            )

        self.__aberrationCorrection = val

    @parameter(only='BOOLEAN')
    def anti_vector_flag(self, val):
        """Anti-vector flag.

        Parameters
        ----------
        anti_vector_flag: bool
            `True` if the anti-vector shall be used for the direction, and `False`
            otherwise.

            In type ``POSITION``, required when the target shape is `POINT` (default).
            If provided when the target shape is `SPHERE`, it must be set to false,
            i.e., using anti-vector direction is not supported for target bodies
            modeled as spheres.

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.
        CalculationInvalidAttr
            If this :py:attr:`direction_type` is ``POSITION`` and
            ``SHAPE`` is ``SPHERE`` but :py:attr:`observer` is not provided.

        """
        if isinstance(val, str):
            val = val.upper() == 'TRUE'

        if self.params['direction_type'] == 'POSITION':
            if self.params.get('shape') == 'SPHERE' and val:
                raise CalculationInvalidAttr(
                    'anti_vector_flag', val, ['False']
                )

        self.__antiVectorFlag = val
