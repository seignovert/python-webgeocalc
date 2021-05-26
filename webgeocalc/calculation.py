"""Webgeocalc Calculations."""

import time

from .api import API, Api, ESA_API, JPL_API
from .decorator import parameter
from .errors import (CalculationAlreadySubmitted, CalculationConflictAttr,
                     CalculationFailed, CalculationIncompatibleAttr,
                     CalculationInvalidAttr, CalculationInvalidValue,
                     CalculationNotCompleted, CalculationRequiredAttr,
                     CalculationTimeOut, CalculationUndefinedAttr)
from .types import KernelSetDetails
from .vars import CALCULATION_FAILED_PHASES, VALID_PARAMETERS


APIs = {
    '': API,
    'JPL': JPL_API,
    'ESA': ESA_API,
}


class Calculation:
    """Webgeocalc calculation object.

    Parameters
    ----------
    api: str or webgeocalc.Api, optional
        WebGeoCalc API endpoint.
        By default, if no :py:attr:`api` option is provided,
        the query is sent to the ``WGC_URL`` API
        (if set in the global environment variables)
        or :py:obj:`JPL_API` (if not).
        Keyword are also accepted (``JPL`` and ``ESA``).
        Custom 3-rd party endpoints can be used
        (with their ``URL`` or as a custom :py:class:`webgeocalc.api.Api`).
    time_system: str, optional
        See: :py:attr:`time_system`
    time_format: str, optional
        See: :py:attr:`time_format`
    verbose: bool, optional
        Verbose calculation phase during :py:func:`submit`, :py:func:`update`
        and :py:func:`run`.

    Other Parameters
    ----------------
    calculation_type: str
        See: :py:attr:`calculation_type`
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
    sclk_id: int
        See: :py:attr:`sclk_id`
    output_time_system: str
        See: :py:attr:`output_time_system`
    output_time_format: str
        See: :py:attr:`output_time_format`
    output_time_custom_format: str
        See: :py:attr:`output_time_custom_format`
    output_sclk_id: int
        See: :py:attr:`output_sclk_id`
    target: str or int
        See: :py:attr:`target`
    target_frame: str
        See: :py:attr:`target_frame`
    target_1: str
        See: :py:attr:`target_1`
    target_2: str
        See: :py:attr:`target_2`
    shape_1: str
        See: :py:attr:`shape_1`
    shape_2: str
        See: :py:attr:`shape_2`
    observer: str or int
        See: :py:attr:`observer`
    reference_frame: str or int
        See: :py:attr:`reference_frame`
    frame_1: str ot int
        See: :py:attr:`frame_1`
    frame_2: str or int
        See: :py:attr:`frame_2`
    orbiting_body: str
        See: :py:attr:`orbiting_body`
    center_body: str
        See: :py:attr:`center_body`
    aberration_correction: str
        See: :py:attr:`aberration_correction`
    state_representation: str
        See: :py:attr:`state_representation`
    time_location: str
        See: :py:attr:`time_location`
    orientation_representation: str
        See: :py:attr:`orientation_representation`
    axis_1: str
        See: :py:attr:`axis_1`
    axis_2: str
        See: :py:attr:`axis_2`
    axis_3: str
        See: :py:attr:`axis_3`
    angular_units: str
        See: :py:attr:`angular_units`
    angular_velocity_representation: str
        See: :py:attr:`angular_velocity_representation`
    angular_velocity_units: str
        See: :py:attr:`angular_velocity_units`
    coordinate_representation: str
        See: :py:attr:`coordinate_representation`
    latitude: float
        See: :py:attr:`latitude`
    longitude: float
        See: :py:attr:`longitude`
    sub_point_type: str
        See: :py:attr:`sub_point_type`
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

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`calculation_type`, :py:attr:`time_system` and
        :py:attr:`time_format` are not provided.
    CalculationRequiredAttr
        If neither :py:attr:`kernels` nor :py:attr:`kernel_paths` is not provided.
    CalculationRequiredAttr
        If neither :py:attr:`times` nor :py:attr:`intervals` is not provided.

    """

    REQUIRED = ()

    def __init__(self, api='', time_system='UTC',
                 time_format='CALENDAR', verbose=True, **kwargs):
        # Add default parameters to kwargs
        kwargs['time_system'] = time_system
        kwargs['time_format'] = time_format

        # Init parameters
        self.params = kwargs
        self.__kernels = []
        self.id = None
        self.phase = 'NOT SUBMITTED'
        self.columns = None
        self.values = None
        self.verbose = verbose

        # Select API (with caching)
        api_key = str(api).upper()
        if api_key not in APIs:
            APIs[api_key] = api if isinstance(api, Api) else Api(api)

        self.api = APIs[api_key]

        # Check required parameters
        if 'kernels' not in kwargs and 'kernel_paths' not in kwargs:
            raise CalculationRequiredAttr("kernels' or 'kernel_paths")

        if 'times' not in kwargs and 'intervals' not in kwargs:
            raise CalculationRequiredAttr("times' or 'intervals")

        self._required('calculation_type', 'time_system', 'time_format',
                       *self.REQUIRED)

        # Set parameters
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return '\n'.join([
            f"<{self.__class__.__name__}> Phase: {self.phase} (id: {self.id})"
        ] + [
            f' - {k}: {v}' for k, v in self.payload.items()
        ])

    def _required(self, *attrs):
        """Check if the required arguments are in the params."""
        for attr in attrs:
            if attr not in self.params:
                raise CalculationRequiredAttr(attr)

    @property
    def payload(self):
        """Calculation payload parameters *dict* for JSON input in WebGeoCalc format.

        Return
        ------
        dict
            Payload keys and values.

        Example
        -------
        >>> Calculation(
        ...    kernels = 'Cassini Huygens',
        ...    times = '2012-10-19T08:24:00.000',
        ...    calculation_type = 'STATE_VECTOR',
        ...    target = 'CASSINI',
        ...    observer = 'SATURN',
        ...    reference_frame = 'IAU_SATURN',
        ...    aberration_correction = 'NONE',
        ...    state_representation = 'PLANETOGRAPHIC',
        ... ).payload  # noqa: E501
        {'kernels': [{'type': 'KERNEL_SET', 'id': 5}], 'times': ['2012-10-19T08:24:00.000'], ...}

        """
        return {k.split('__')[-1]: v for k, v in vars(self).items() if k.startswith('_')}

    def submit(self):
        """Submit calculation parameters and get calculation ``id`` and ``phase``.

        Raises
        ------
        CalculationAlreadySubmitted
            If the calculation was already submitted (to avoid duplicated submissions).

        Example
        -------
        >>> calc.submit()  # noqa: E501  # doctest: +SKIP
        [Calculation submit] Phase: QUEUED | POSITION: 6 (id: 8750344d-645d-4e43-b159-c8d88d28aac6)
        >>> calc.id        # doctest: +SKIP
        '8750344d-645d-4e43-b159-c8d88d28aac6'
        >>> calc.phase     # doctest: +SKIP
        'QUEUED | POSITION: 6'

        """
        if self.id is not None:
            raise CalculationAlreadySubmitted(self.id)

        self.id, self.phase = self.api.new_calculation(self.payload)

        if self.verbose:
            print(f'[Calculation submit] Phase: {self.phase} (id: {self.id})')

    def resubmit(self):
        """Reset calculation ``id`` and re-submit the calculation.

        See: :py:func:`submit`.
        """
        self.id = None
        self.submit()

    def cancel(self):
        """Cancels calculation if already submitted."""
        if self.id is not None:
            _, self.phase = self.api.cancel_calculation(self.id)

            if self.verbose:
                print(f'[Calculation cancellation] Phase: {self.phase} (id: {self.id})')

    def update(self):
        """Update calculation phase ``phase``.

        Example
        -------
        >>> calc.update()  # noqa: E501  # doctest: +SKIP
        [Calculation update] Phase: QUEUED | POSITION: 3 (id: 8750344d-645d-4e43-b159-c8d88d28aac6)
        >>> calc.update()  # noqa: E501  # doctest: +SKIP
        [Calculation update] Phase: STARTING (id: 8750344d-645d-4e43-b159-c8d88d28aac6)
        >>> calc.update()  # noqa: E501  # doctest: +SKIP
        [Calculation update] Phase: LOADING_KERNELS (id: 8750344d-645d-4e43-b159-c8d88d28aac6)
        >>> calc.update()  # noqa: E501  # doctest: +SKIP
        [Calculation update] Phase: CALCULATING (id: 8750344d-645d-4e43-b159-c8d88d28aac6)
        >>> calc.update()  # doctest: +SKIP
        [Calculation update] Phase: COMPLETE (id: 8750344d-645d-4e43-b159-c8d88d28aac6)

        """
        if self.id is None:
            self.submit()
        else:
            _, self.phase = self.api.phase_calculation(self.id)

            if self.verbose:
                print(f'[Calculation update] Phase: {self.phase} (id: {self.id})')

    @property
    def results(self):
        """Gets the results of a calculation, if its phase is `COMPLETE`.

        Return
        ------
        dict
            Calculation results as *dict* based on output columns. If multiple ``times``
            or ``intervals`` are used, the value of the *dict* will be an array.
            See examples.

        Raises
        ------
        CalculationNotCompleted
            If calculation phase is not `COMPLETE`.

        Examples
        --------
        >>> calc.results     # doctest: +SKIP
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

        >>> ang_sep = AngularSeparation(
        ...     kernel_paths = ['pds/wgc/kernels/lsk/naif0012.tls', 'pds/wgc/kernels/spk/de430.bsp'],
        ...     times = ['2012-10-19T08:24:00.000', '2012-10-19T09:00:00.000'],
        ...     target_1 = 'VENUS',
        ...     target_2 = 'MERCURY',
        ...     observer = 'SUN',
        ...     verbose = False,
        ... )  # noqa: E501
        >>> ang_sep.submit()      # doctest: +SKIP
        >>> ang_sep.results       # doctest: +SKIP
        {'DATE': ['2012-10-19 08:24:00.000000 UTC', '2012-10-19 09:00:00.000000 UTC'],
         'ANGULAR_SEPARATION': [175.17072258, 175.18555938]}

        """
        if self.phase != 'COMPLETE':
            raise CalculationNotCompleted(self.phase)

        if self.columns is None or self.values is None:
            self.columns, self.values = self.api.results_calculation(self.id)

        if len(self.values) == 1:
            data = self.values[0]
        else:
            # Transpose values array
            data = [[row[i] for row in self.values] for i in range(len(self.columns))]

        return {column.outputID: value for column, value in zip(self.columns, data)}

    def run(self, timeout=30, sleep=1):
        """Submit, update and retrive calculation results at once.

        See: :py:func:`submit`, :py:func:`update` and :py:attr:`results`.

        Parameters
        ----------
        timeout: int, optional
            Auto-update time out (in seconds).
        sleep: int, optional
            Sleep duration (in seconds) between each update.

        Raises
        ------
        CalculationTimeOut
            If calculation reach the timeout duration.

        """
        if self.columns is not None and self.values is not None:
            return self.results

        for _ in range(int(timeout / sleep)):
            self.update()

            if self.phase == 'COMPLETE':
                return self.results

            if self.phase in CALCULATION_FAILED_PHASES:
                raise CalculationFailed(self.phase)

            time.sleep(sleep)

        raise CalculationTimeOut(timeout, sleep)

    @parameter(only='CALCULATION_TYPE')
    def calculation_type(self, val):
        """The type of calculation to perform.

        Parameters
        ----------
        calculation_type: str
            One of the following:

            - STATE_VECTOR
            - ANGULAR_SEPARATION
            - ANGULAR_SIZE
            - SUB_OBSERVER_POINT
            - SUB_SOLAR_POINT
            - ILLUMINATION_ANGLES
            - SURFACE_INTERCEPT_POINT
            - OSCULATING_ELEMENTS
            - FRAME_TRANSFORMATION
            - TIME_CONVERSION
            - GF_COORDINATE_SEARCH
            - GF_ANGULAR_SEPARATION_SEARCH
            - GF_DISTANCE_SEARCH
            - GF_SUB_POINT_SEARCH
            - GF_OCCULTATION_SEARCH
            - GF_TARGET_IN_INSTRUMENT_FOV_SEARCH
            - GF_SURFACE_INTERCEPT_POINT_SEARCH
            - GF_RAY_IN_FOV_SEARCH

            Note
            ----
            This parameters will be auto-filled for specific calculation sub-classes.

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        self.__calculationType = val

    @parameter
    def kernels(self, kernel_sets):
        """Add kernel sets.

        Parameters
        ----------
        kernels: str, int, [str or/and int]
            Kernel set(s) to be used for the calculation::

               [{'type': 'KERNEL_SET', 'id': 5}, ...]

        """
        self.__kernels += [
            self._kernel_id_obj(kernel_sets)
        ] if isinstance(
            kernel_sets,
            (int, str, KernelSetDetails)
        ) else list(map(self._kernel_id_obj, kernel_sets))

    def _kernel_id_obj(self, kernel_set):
        # Payload kernel set object
        return {"type": "KERNEL_SET", "id": self.api.kernel_set_id(kernel_set)}

    @parameter
    def kernel_paths(self, paths):
        """Add path for individual kernel paths.

        Parameters
        ----------
        kernel_paths: str, [str]
            Kernel path(s) to be used for the calculation::

               [{'type': 'KERNEL', 'path': 'pds/wgc/kernels/lsk/naif0012.tls'}, ...]

        """
        self.__kernels += [
            self._kernel_path_obj(paths)
        ] if isinstance(paths, str) else list(map(self._kernel_path_obj, paths))

    @staticmethod
    def _kernel_path_obj(server_path):
        # Payloaf individual kernel path object
        return {"type": "KERNEL", "path": server_path}

    @parameter
    def times(self, times):
        """Calculation input times.

        Parameters
        ----------
        times: str or [str]
            String or array of strings representing the time points
            that should be used in the calculation.

        Raises
        ------
        CalculationConflictAttr
            Either this parameter or the py:attr:`intervals` parameter must be supplied.

        """
        self.__times = [times] if isinstance(times, str) else times

        if 'intervals' in self.params:
            raise CalculationConflictAttr('times', 'intervals')

    @parameter
    def intervals(self, intervals):
        """Calculation input intervals.

        Parameters
        ----------
        intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
            An array of objects with startTime and endTime parameters,
            representing the time intervals used for the calculation.

            Warning
            -------
            Either this parameter or the :py:attr:`times` parameter must be supplied.

        Raises
        ------
        CalculationInvalidAttr
            If :py:attr:intervals` input format is invalid.
            For example, if :py:attr:intervals` is provided an dict,
            ``startTime`` and ``endTime`` must be present.
        CalculationUndefinedAttr
            If this parameter is used, :py:attr:`time_step` must also be supplied.

        """
        if isinstance(intervals, dict):
            self.__intervals = [self._interval(intervals)]
        elif isinstance(intervals, list) and len(intervals) > 2:
            self.__intervals = list(map(self._interval, intervals))
        elif isinstance(intervals, list) and len(intervals) == 2:
            if isinstance(intervals[0], str) and isinstance(intervals[1], str):
                self.__intervals = [self._interval(intervals)]
            elif isinstance(intervals[0], (dict, list)) and \
                    isinstance(intervals[1], (dict, list)):
                self.__intervals = [
                    self._interval(intervals[0]), self._interval(intervals[1])]
            else:
                raise CalculationInvalidAttr(
                    name='intervals',
                    attr=intervals,
                    valids=VALID_PARAMETERS['INTERVALS']
                )
        elif isinstance(intervals, list) and len(intervals) == 1:
            if isinstance(intervals[0], (dict, list)):
                self.__intervals = [self._interval(intervals[0])]
            else:
                raise CalculationInvalidAttr(
                    name='intervals',
                    attr=intervals,
                    valids=VALID_PARAMETERS['INTERVALS']
                )
        else:
            raise CalculationInvalidAttr(
                name='intervals',
                attr=intervals,
                valids=VALID_PARAMETERS['INTERVALS']
            )

        if 'time_step' not in self.params:
            raise CalculationUndefinedAttr('intervals', intervals, 'time_step')

    @staticmethod
    def _interval(interval):
        # Parse interval object
        if not len(interval) == 2:
            raise CalculationInvalidAttr(
                name='intervals',
                attr=interval,
                valids=VALID_PARAMETERS['INTERVALS'][:2]
            )

        if isinstance(interval, dict):
            if 'startTime' in interval.keys() and 'endTime' in interval.keys():
                return interval

            raise CalculationInvalidAttr(
                name='intervals',
                attr=interval,
                valids=VALID_PARAMETERS['INTERVALS'][:2]
            )

        return {'startTime': str(interval[0]), 'endTime': str(interval[1])}

    @parameter
    def time_step(self, val):
        """Time step for intervals.

        Parameters
        ----------
        time_step: int
            Number of steps parameter used for time series or
            geometry finder calculations.

        Raises
        ------
        CalculationConflictAttr
            If :py:attr:`times` attribute is supplied.
        CalculationUndefinedAttr
            If :py:attr:`time_step_units` is not supplied.

        """
        self.__timeStep = int(val)

        if 'times' in self.params:
            raise CalculationConflictAttr('time_step', 'times')

        if 'time_step_units' not in self.params:
            raise CalculationUndefinedAttr('time_step', val, 'time_step_units')

    @parameter(only='TIME_STEP_UNITS')
    def time_step_units(self, val):
        """Time step units.

        Parameters
        ----------
        time_step_units: str
            One of the following:

            - SECONDS
            - MINUTES
            - HOURS
            - DAYS
            - EQUAL_INTERVALS

        Raises
        -------
        CalculationInvalidAttr
            If the value provided is invalid.
        CalculationConflictAttr
            If :py:attr:`times` attribute is supplied.
        CalculationUndefinedAttr
            If :py:attr:`time_step` is not supplied.

        """
        self.__timeStepUnits = val

        if 'times' in self.params:
            raise CalculationConflictAttr('time_step', 'times')
        if 'time_step' not in self.params:
            raise CalculationUndefinedAttr('time_step_units', val, 'time_step')

    @parameter(only='TIME_SYSTEM')
    def time_system(self, val):
        """Time System.

        Parameters
        ----------
        time_system: str
            One of the following:

            - UTC
            - TDB
            - TDT
            - SPACECRAFT_CLOCK

        Raises
        -------
        CalculationInvalidAttr
            If the value provided is invalid.
        CalculationUndefinedAttr
            If ``SPACECRAFT_CLOCK`` is selected, but
            :py:attr:`sclk_id` attribute is not provided.

        """
        self.__timeSystem = val

        if val == 'SPACECRAFT_CLOCK' and 'sclk_id' not in self.params:
            raise CalculationUndefinedAttr('time_system', 'SPACECRAFT_CLOCK', 'sclk_id')

    @parameter(only='TIME_FORMAT')
    def time_format(self, val):
        """Time format input.

        Parameters
        ----------
        time_format: str
            One of the following:

            - CALENDAR
            - JULIAN
            - SECONDS_PAST_J2000
            - SPACECRAFT_CLOCK_TICKS
            - SPACECRAFT_CLOCK_STRING

        Raises
        -------
        CalculationInvalidAttr
            If the value provided is invalid.
        CalculationRequiredAttr
            If :py:attr:`time_system` is not provided.
        CalculationIncompatibleAttr
            If ``CALENDAR``, ``JULIAN`` or ``SECONDS_PAST_J2000`` is selected but
            :py:attr:`time_system` attribute is not in ``UTC``, ``TDB`` or ``TDT``,
            or ``SPACECRAFT_CLOCK_STRING`` or ``SPACECRAFT_CLOCK_TICKS`` is selected but
            :py:attr:`time_system` attribute is not ``SPACECRAFT_CLOCK``.

        """
        self.__timeFormat = val

        self._required('time_system')

        if val in ['CALENDAR', 'JULIAN', 'SECONDS_PAST_J2000'] and \
                self.params['time_system'] not in ['UTC', 'TDB', 'TDT']:
            raise CalculationIncompatibleAttr(
                'time_format', val, 'time_system', self.params['time_system'],
                ['UTC', 'TDB', 'TDT'])

        if val in ['SPACECRAFT_CLOCK_STRING', 'SPACECRAFT_CLOCK_TICKS'] and \
                self.params['time_system'] != 'SPACECRAFT_CLOCK':
            raise CalculationIncompatibleAttr(
                'time_format', val, 'time_system',
                self.params['time_system'], ['SPACECRAFT_CLOCK'])

    @parameter
    def sclk_id(self, val):
        """Spacecraft clock kernel id.

        Parameters
        ----------
        sclk_id: int
            Spacecraft clock kernel id.

        Raises
        ------
        CalculationRequiredAttr
            If :py:attr:`time_system` is not provided.
        CalculationIncompatibleAttr
            If :py:attr:`time_system` is not ``SPACECRAFT_CLOCK``.

        """
        self.__sclkId = int(val)

        self._required('time_system')

        if self.params['time_system'] != 'SPACECRAFT_CLOCK':
            raise CalculationIncompatibleAttr(
                'sclk_id', val, 'time_system',
                self.params['time_system'], ['SPACECRAFT_CLOCK'])

    @parameter(only='TIME_SYSTEM')
    def output_time_system(self, val):
        """The time system for results output times.

        Parameters
        ----------
        output_time_system: str
            One of the following:

            - UTC
            - TDB
            - TDT
            - SPACECRAFT_CLOCK

        Raises
        -------
        CalculationInvalidAttr
            If the value provided is invalid.
        CalculationUndefinedAttr
            If ``SPACECRAFT_CLOCK`` is selected, but
            :py:attr:`output_sclk_id` attribute is not provided.

        """
        self.__outputTimeSystem = val

        if val == 'SPACECRAFT_CLOCK' and 'output_sclk_id' not in self.params:
            raise CalculationUndefinedAttr(
                'output_time_system', 'SPACECRAFT_CLOCK', 'output_sclk_id')

    @parameter(only='OUTPUT_TIME_FORMAT')
    def output_time_format(self, val):
        """The time format for the result output times.

        Parameters
        ----------
        output_time_format: str
            One of the following:

            - CALENDAR
            - CALENDAR_YMD
            - CALENDAR_DOY
            - JULIAN
            - SECONDS_PAST_J2000
            - SPACECRAFT_CLOCK_STRING
            - SPACECRAFT_CLOCK_TICKS
            - CUSTOM

            Warning
            -------
            If ``CUSTOM`` is selected, then :py:attr:`output_time_custom_format`
            must also be provided.

        Raises
        -------
        CalculationInvalidAttr
            If the value provided is invalid.
        CalculationRequiredAttr
            If :py:attr:`output_time_system` is not provided.
        CalculationIncompatibleAttr
            If ``CALENDAR_YMD``, ``CALENDAR_DOY``, ``JULIAN``, ``SECONDS_PAST_J2000``
            or ``CUSTOM`` is selected but :py:attr:`outputTimeSystem` is not in
            ``TDB``, ``TDT`` or ``UTC``, or ``SPACECRAFT_CLOCK_STRING`` or
            ``SPACECRAFT_CLOCK_TICKS`` is selected but :py:attr:`output_time_system`
            is not ``SPACECRAFT_CLOCK``.

        """
        self.__outputTimeFormat = val

        self._required('output_time_system')

        if val in ['CALENDAR', 'CALENDAR_YMD', 'CALENDAR_DOY',
                   'JULIAN', 'SECONDS_PAST_J2000', 'CUSTOM'] and \
                self.params['output_time_system'] not in ['UTC', 'TDB', 'TDT']:
            raise CalculationIncompatibleAttr(
                'output_time_format', val,
                'output_time_system', self.params['output_time_system'],
                ['UTC', 'TDB', 'TDT'])

        if val in ['SPACECRAFT_CLOCK_STRING', 'SPACECRAFT_CLOCK_TICKS'] and \
                self.params['output_time_system'] != 'SPACECRAFT_CLOCK':
            raise CalculationIncompatibleAttr(
                'output_time_format', val,
                'output_time_system', self.params['output_time_system'],
                ['SPACECRAFT_CLOCK'])

    @parameter
    def output_time_custom_format(self, val):
        """A SPICE ``timout()`` format string.

        Parameters
        ----------
        output_time_custom_format: str
            A SPICE ``timout()`` format string.

        Raises
        ------
        CalculationRequiredAttr
            If :py:attr:`output_time_format` is not provided.
        CalculationIncompatibleAttr
            If :py:attr:`output_time_format` is not ``CUSTOM``.

        """
        self.__outputTimeCustomFormat = val

        self._required('output_time_format')

        if self.params['output_time_format'] != 'CUSTOM':
            raise CalculationIncompatibleAttr(
                'output_time_custom_format', val, 'output_time_format',
                self.params['output_time_format'], ['CUSTOM'])

    @parameter
    def output_sclk_id(self, val):
        """The output spacecraft clock kernel id.

        Parameters
        ----------
        output_sclk_id: int
            Spacecraft clock kernel id.

        Raises
        ------
        CalculationRequiredAttr
            If :py:attr:`output_time_system` is not provided.
        CalculationIncompatibleAttr
            If :py:attr:`output_time_system` is not ``SPACECRAFT_CLOCK``.

        """
        self.__outputSclkId = int(val)

        self._required('output_time_system')

        if self.params['output_time_system'] != 'SPACECRAFT_CLOCK':
            raise CalculationIncompatibleAttr(
                'output_sclk_id', val, 'output_time_system',
                self.params['output_time_system'], ['SPACECRAFT_CLOCK'])

    @parameter
    def target(self, val):
        """Target body.

        Parameters
        ----------
        target: str or int
            The target body ``name`` or ``id`` from :py:func:`API.bodies`.

        """
        self.__target = val if isinstance(val, int) else val.upper()

    @parameter
    def target_frame(self, val):
        """The target body-fixed reference frame name.

        Parameters
        ----------
        target_frame: str
            Reference frame ``name``.

        """
        self.__targetFrame = val

    @parameter
    def target_1(self, val):
        """The target body the first body.

        Parameters
        ----------
        target_1: str
            Target body ``name`` or ``id``.

        """
        self.__target1 = val if isinstance(val, int) else val.upper()

    @parameter
    def target_2(self, val):
        """The target body the second body.

        Parameters
        ----------
        target_2: str
            Target body ``name`` or ``id``.

        """
        self.__target2 = val if isinstance(val, int) else val.upper()

    @parameter(only='SHAPE')
    def shape_1(self, val):
        """The shape to use for the first body.

        Parameters
        ----------
        shape_1: str
            One of:

            - POINT
            - SPHERE

        Raises
        -------
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        self.__shape1 = val

    @parameter(only='SHAPE')
    def shape_2(self, val):
        """The shape to use for the second body.

        Parameters
        ----------
        shape_2: str
            One of:

            - POINT
            - SPHERE

        Raises
        -------
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        self.__shape2 = val

    @parameter
    def observer(self, val):
        """The observing body.

        Parameters
        ----------
        observer: str or int
            The observing body ``name`` or ``id`` from :py:func:`API.bodies`.

        """
        self.__observer = val if isinstance(val, int) else val.upper()

    @parameter
    def reference_frame(self, val):
        """The reference frame.

        Parameters
        ----------
        reference_frame: str or int
            The reference frame ``name`` or ``id`` from :py:func:`API.frames`.

        """
        self.__referenceFrame = val if isinstance(val, int) else val.upper()

    @parameter
    def frame_1(self, val):
        """The first reference frame.

        Parameters
        ----------
        frame_1: str or int
            The reference frame ``name`` or ``id`` from :py:func:`API.frames`.

        """
        self.__frame1 = val if isinstance(val, int) else val.upper()

    @parameter
    def frame_2(self, val):
        """The second reference frame.

        Parameters
        ----------
        frame_2: str or int
            The reference frame ``name`` or ``id`` from :py:func:`API.frames`.

        """
        self.__frame2 = val if isinstance(val, int) else val.upper()

    @parameter
    def orbiting_body(self, val):
        """The SPICE orbiting body.

        Parameters
        ----------
        orbiting_body: str or int
            SPICE body ``name`` or ``id`` for the orbiting body.

        """
        self.__orbitingBody = val if isinstance(val, int) else val.upper()

    @parameter
    def center_body(self, val):
        """
        The SPICE body center of motion.

        Parameters
        ----------
        center_body: str or int
            SPICE body ``name`` or ``id`` for the body that is the center of motion.

        """
        self.__centerBody = val if isinstance(val, int) else val.upper()

    @parameter(only='ABERRATION_CORRECTION')
    def aberration_correction(self, val):
        """SPICE aberration correction.

        Parameters
        ----------
        aberration_correction: str
            The SPICE aberration correction string. One of:

            - NONE
            - LT
            - LT+S
            - CN
            - CN+S
            - XLT
            - XLT+S
            - XCN
            - XCN+S

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        self.__aberrationCorrection = val

    @parameter(only='STATE_REPRESENTATION')
    def state_representation(self, val):
        """State representation.

        Parameters
        ----------
        state_representation: str
            One of:

            - RECTANGULAR
            - RA_DEC
            - LATITUDINAL (planetocentric)
            - PLANETODETIC
            - PLANETOGRAPHIC
            - CYLINDRICAL
            - SPHERICAL

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        self.__stateRepresentation = val

    @parameter(only='TIME_LOCATION')
    def time_location(self, val):
        """The frame for the input times.

        Parameters
        ----------
        time_location: str
            One of:

            - FRAME1
            - FRAME2

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.

        Warning
        -------
        NAIF API docs::

            `Only needed if aberrationCorrection is not NONE.`

        Required even when :py:attr:`aberration_correction` is ``NONE``.

        """
        self.__timeLocation = val

    @parameter(only='ORIENTATION_REPRESENTATION')
    def orientation_representation(self, val):
        """The representation of the result transformation.

        Parameters
        ----------
        orientation_representation: str
            Orientation result transformation. One of:

            - EULER_ANGLES
            - ANGLE_AND_AXIS
            - SPICE_QUATERNION
            - OTHER_QUATERNION
            - MATRIX_ROW_BY_ROW
            - MATRIX_FLAGGED
            - MATRIX_ALL_ONE_ROW

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        self.__orientationRepresentation = val

    @parameter
    def axis_1(self, val):
        """The first axis for Euler angle rotation.

        Parameters
        ----------
        axis_1: str
            Axis name. See: :py:func:`axis`.

        """
        self.__axis1 = self.axis('axis_1', val)

    @parameter
    def axis_2(self, val):
        """The second axis for Euler angle rotation.

        Parameters
        ----------
        axis_3: str
            Axis name. See: :py:func:`axis`.

        """
        self.__axis2 = self.axis('axis_2', val)

    @parameter
    def axis_3(self, val):
        """The third axis for Euler angle rotation.

        Parameters
        ----------
        axis_3: str
            Axis name. See: :py:func:`axis`.

        """
        self.__axis3 = self.axis('axis_3', val)

    def axis(self, name, val):
        """Axis for Euler angle rotation.

        Parameters
        ----------
        name: str
            Axis name. One of:

            - X
            - Y
            - Z

        val: float
            Value on the axis.

        Return
        ------
        float
            Value on the axis.

        Raises
        ------
        CalculationInvalidAttr
            If the ``name`` provided is invalid.
        CalculationUndefinedAttr
            If :py:attr:`orientation_representation` is not supplied.
        CalculationIncompatibleAttr
            If :py:attr:`orientation_representation` is not ``EULER_ANGLES``.

        """
        if 'orientation_representation' not in self.params:
            raise CalculationUndefinedAttr(name, val, 'orientation_representation')

        if self.params['orientation_representation'] != 'EULER_ANGLES':
            raise CalculationIncompatibleAttr(
                name, val, 'orientation_representation',
                self.params['orientation_representation'], ['EULER_ANGLES'])

        if val in VALID_PARAMETERS['AXIS']:
            return val

        raise CalculationInvalidAttr(name, val, VALID_PARAMETERS['AXIS'])

    @parameter(only='ANGULAR_UNITS')
    def angular_units(self, val):
        """The angular units.

        Parameters
        ----------
        angular_units: str
            The angular units used for the angle of rotation. One of:

            - deg
            - rad

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.
        CalculationUndefinedAttr
            If :py:attr:`orientation_representation` is not supplied.
        CalculationIncompatibleAttr
            If :py:attr:`orientation_representation` is
            not `EULER_ANGLES` or `ANGLE_AND_AXIS`.

        """
        self.__angularUnits = val

        if 'orientation_representation' not in self.params:
            raise CalculationUndefinedAttr(
                'angular_units', val, 'orientation_representation')

        if not self.params['orientation_representation'] in ['EULER_ANGLES',
                                                             'ANGLE_AND_AXIS']:
            raise CalculationIncompatibleAttr(
                'angular_units', val, 'orientation_representation',
                self.params['orientation_representation'],
                ['EULER_ANGLES', 'ANGLE_AND_AXIS'])

    @parameter(only='ANGULAR_VELOCITY_REPRESENTATION')
    def angular_velocity_representation(self, val):
        """Angular velocity representation.

        Parameters
        ----------
        angular_velocity_representation: str
            The representation of angular velocity in the output. One of:

            - NOT_INCLUDED
            - VECTOR_IN_FRAME1
            - VECTOR_IN_FRAME2
            - EULER_ANGLE_DERIVATIVES
            - MATRIX

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        self.__angularVelocityRepresentation = val

    @parameter(only='ANGULAR_VELOCITY_UNITS')
    def angular_velocity_units(self, val):
        """The units for the angular velocity.

        Parameters
        ----------
        angular_velocity_units: str
            One of:

            - deg/s
            - rad/s
            - RPM
            - Unitary *(ie, Unit vector)*

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.
        CalculationUndefinedAttr
            If :py:attr:`angular_velocity_representation` is not supplied.
        CalculationIncompatibleAttr
            If :py:attr:`angular_velocity_representation` is not ``VECTOR_IN_FRAME1``,
            ``VECTOR_IN_FRAME2`` or ``EULER_ANGLE_DERIVATIVES``
        CalculationIncompatibleAttr
            If ``Unitary`` selected but :py:attr:`angular_velocity_representation` is not
            ``VECTOR_IN_FRAME1`` or ``VECTOR_IN_FRAME2``.

        """
        self.__angularVelocityUnits = val

        if 'angular_velocity_representation' not in self.params:
            raise CalculationUndefinedAttr(
                'angular_velocity_units', val, 'angular_velocity_representation')

        choices = ['VECTOR_IN_FRAME1', 'VECTOR_IN_FRAME2', 'EULER_ANGLE_DERIVATIVES']
        if not self.params['angular_velocity_representation'] in choices:
            raise CalculationIncompatibleAttr(
                'angular_velocity_units', val, 'angular_velocity_representation',
                self.params['angular_velocity_representation'], choices)

        if val == 'Unitary' and not self.params['angular_velocity_representation'] in \
                ['VECTOR_IN_FRAME1', 'VECTOR_IN_FRAME2']:
            raise CalculationIncompatibleAttr(
                'angular_velocity_units', val, 'angular_velocity_representation',
                self.params['angular_velocity_representation'],
                ['VECTOR_IN_FRAME1', 'VECTOR_IN_FRAME2'])

    @parameter(only='COORDINATE_REPRESENTATION')
    def coordinate_representation(self, val):
        """Coordinate Representation.

        Parameters
        ----------
        coordinate_representation: str
            One of:

            - LATITUDINAL *(planetocentric)*
            - PLANETODETIC
            - PLANETOGRAPHIC

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        self.__coordinateRepresentation = val

    @parameter
    def latitude(self, val):
        """Latitude of the surface point.

        Parameters
        ----------
        latitude: float
            Latitude angle (in degrees).

        Raises
        ------
        CalculationInvalidValue
            If ``latitude`` not in [-90, +90] range.

        """
        if -90 <= val <= 90:
            self.__latitude = val
        else:
            raise CalculationInvalidValue('latitude', val, -90, 90)

    @parameter
    def longitude(self, val):
        """Longitude of the surface point.

        Parameters
        ----------
        longitude: float
            Longitude angle (in degrees).

        Raises
        ------
        CalculationInvalidValue
            If ``longitude`` not in [-180, +180] range.

        """
        if -180 <= val <= 180:
            self.__longitude = val
        else:
            raise CalculationInvalidValue('longitude', val, -180, 180)

    @parameter(only='SUB_POINT_TYPE')
    def sub_point_type(self, val):
        """Sub-observer point.

        Parameters
        ----------
        sub_point_type: str
            The method of finding the sub-observer point, as in
            the SPICE ``subpnt()`` API call. One of:

            - Near point: ellipsoid
            - Intercept: ellipsoid
            - NADIR/DSK/UNPRIORITIZED
            - INTERCEPT/DSK/UNPRIORITIZED

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        self.__subPointType = val

    @parameter(only='DIRECTION_VECTOR_TYPE')
    def direction_vector_type(self, val):
        """Type of ray's direction vector.

        Parameters
        ----------
        direction_vector_type: str
            Type of vector to be used as the ray direction. One of:

            - INSTRUMENT_BORESIGHT *(the instrument boresight vector)*
            - INSTRUMENT_FOV_BOUNDARY_VECTORS *(the instrument field-of-view
              boundary vectors)*
            - REFERENCE_FRAME_AXIS *(an axis of the specified reference frame)*
            - VECTOR_IN_INSTRUMENT_FOV *(a vector in the reference frame of the
              specified instrument)*
            - VECTOR_IN_REFERENCE_FRAME *(a vector in the specified reference frame)*

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.
        CalculationRequiredAttr
            If this parameter is ``INSTRUMENT_BORESIGHT``,
            ``INSTRUMENT_FOV_BOUNDARY_VECTORS`` or ``VECTOR_IN_INSTRUMENT_FOV``
            but :py:attr:`direction_instrument` is not provided.
        CalculationRequiredAttr
            If this parameter is ``REFERENCE_FRAME_AXIS`` or ``VECTOR_IN_REFERENCE_FRAME``
            but :py:attr:`direction_frame` is not provided.
        CalculationRequiredAttr
            If this parameter is ``REFERENCE_FRAME_AXIS`` but
            :py:attr:`direction_frame_axis` is not provided.
        CalculationUndefinedAttr
            If this parameter is ``VECTOR_IN_INSTRUMENT_FOV``
            or ``VECTOR_IN_REFERENCE_FRAME`` but neither :py:attr:`direction_vector_x`,
            :py:attr:`direction_vector_y` and :py:attr:`direction_vector_z`
            nor :py:attr:`direction_vector_ra` and :py:attr:`direction_vector_dec`
            are provided.

        """
        self.__directionVectorType = val

        if val in ['INSTRUMENT_BORESIGHT', 'INSTRUMENT_FOV_BOUNDARY_VECTORS',
                   'VECTOR_IN_INSTRUMENT_FOV']:
            self._required('direction_instrument')

        elif val in ['REFERENCE_FRAME_AXIS', 'VECTOR_IN_REFERENCE_FRAME']:
            self._required('direction_frame')
            if val == 'REFERENCE_FRAME_AXIS':
                self._required('direction_frame_axis')

        keys = self.params.keys()
        if val in ['VECTOR_IN_INSTRUMENT_FOV', 'VECTOR_IN_REFERENCE_FRAME']:
            if not(
                    'direction_vector_x' in keys and  # noqa: W504
                    'direction_vector_y' in keys and  # noqa: W504
                    'direction_vector_z' in keys
            ) and not(
                'direction_vector_ra' in keys and  # noqa: W504
                'direction_vector_dec' in keys
            ):
                raise CalculationUndefinedAttr(
                    'direction_vector_type', val,
                    "direction_vector_x/y/z' or 'direction_vector_ra/dec")

    @parameter
    def direction_instrument(self, val):
        """Direction instrument.

        Parameters
        ----------
        direction_instrument: str or int
            The instrument ``name`` or ``id``.

        Raises
        ------
        CalculationUndefinedAttr
            If :py:attr:`direction_vector_type` is not provided.
        CalculationIncompatibleAttr
            If :py:attr:`direction_vector_type` not in ``INSTRUMENT_BORESIGHT``,
            ``INSTRUMENT_FOV_BOUNDARY_VECTORS`` or ``VECTOR_IN_INSTRUMENT_FOV``.

        """
        if 'direction_vector_type' not in self.params:
            raise CalculationUndefinedAttr(
                'direction_instrument', val, 'direction_vector_type')

        choices = ['INSTRUMENT_BORESIGHT', 'INSTRUMENT_FOV_BOUNDARY_VECTORS',
                   'VECTOR_IN_INSTRUMENT_FOV']
        if not self.params['direction_vector_type'] in choices:
            raise CalculationIncompatibleAttr(
                'direction_instrument', val, 'direction_vector_type',
                self.params['direction_vector_type'], choices)

        self.__directionInstrument = val if isinstance(val, int) else val.upper()

    @parameter
    def direction_frame(self, val):
        """Direction vector reference frame.

        Parameters
        ----------
        direction_frame: str
            The vector's reference frame ``name``.

        Raises
        ------
        CalculationUndefinedAttr
            If :py:attr:`direction_vector_type` is not provided.
        CalculationIncompatibleAttr
            If :py:attr:`direction_vector_type` is not in ``REFERENCE_FRAME_AXIS``
            or ``VECTOR_IN_REFERENCE_FRAME``.

        """
        if 'direction_vector_type' not in self.params:
            raise CalculationUndefinedAttr(
                'direction_frame', val, 'direction_vector_type')

        choices = ['REFERENCE_FRAME_AXIS', 'VECTOR_IN_REFERENCE_FRAME']
        if not self.params['direction_vector_type'] in choices:
            raise CalculationIncompatibleAttr(
                'direction_frame', val, 'direction_vector_type',
                self.params['direction_vector_type'], choices)

        self.__directionFrame = val

    @parameter(only='AXIS')
    def direction_frame_axis(self, val):
        """The vector's reference frame axis name.

        Parameters
        ----------
        direction_frame: str
            The vector's reference frame  axis. One of:

            - X
            - Y
            - Z

        Raises
        ------
        CalculationUndefinedAttr
            If :py:attr:`direction_vector_type` is not provided.
        CalculationIncompatibleAttr
            If :py:attr:`direction_vector_type` is not ``REFERENCE_FRAME_AXIS``.
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        if 'direction_vector_type' not in self.params:
            raise CalculationUndefinedAttr(
                'direction_frame_axis', val, 'direction_vector_type')

        if self.params['direction_vector_type'] != 'REFERENCE_FRAME_AXIS':
            raise CalculationIncompatibleAttr(
                'direction_frame_axis', val, 'direction_vector_type',
                self.params['direction_vector_type'], ['REFERENCE_FRAME_AXIS'])

        self.__directionFrameAxis = val

    def direction_vector(self, axis, val):
        """Direction vector coordinate.

        Parameters
        ----------
        axis: str
            Axis name.
        val: float
            Value on the axis.

        Raises
        ------
        CalculationUndefinedAttr
            If :py:attr:`direction_vector_type` is not provided.
        CalculationIncompatibleAttr
            If :py:attr:`direction_vector_type` is not in ``VECTOR_IN_INSTRUMENT_FOV``
            or ``VECTOR_IN_REFERENCE_FRAME``.

        """
        if 'direction_vector_type' not in self.params:
            raise CalculationUndefinedAttr(
                'direction_vector_' + axis, val, 'direction_vector_type')

        choices = ['VECTOR_IN_INSTRUMENT_FOV', 'VECTOR_IN_REFERENCE_FRAME']
        if not self.params['direction_vector_type'] in choices:
            raise CalculationIncompatibleAttr(
                'direction_vector_' + axis, val, 'direction_vector_type',
                self.params['direction_vector_type'], choices)
        return val

    @parameter
    def direction_vector_x(self, val):
        """The X ray's direction vector coordinate.

        Parameters
        ----------
        direction_vector_x: float
            Direction x-coordinate. See :py:func:`direction_vector`.

        """
        self.__directionVectorX = self.direction_vector('x', val)

    @parameter
    def direction_vector_y(self, val):
        """The Y ray's direction vector coordinate.

        Parameters
        ----------
        direction_vector_y: float
            Direction y-coordinate. See :py:func:`direction_vector`.

        """
        self.__directionVectorY = self.direction_vector('y', val)

    @parameter
    def direction_vector_z(self, val):
        """The Z ray's direction vector coordinate.

        Parameters
        ----------
        direction_vector_z: float
            Direction z-coordinate. See :py:func:`direction_vector`.

        """
        self.__directionVectorZ = self.direction_vector('z', val)

    @parameter
    def direction_vector_ra(self, val):
        """The right-ascension ray's direction vector coordinate.

        Parameters
        ----------
        direction_vector_ra: float
            Direction RA-coordinate. See :py:func:`direction_vector`.

        """
        self.__directionVectorRA = self.direction_vector('ra', val)

    @parameter
    def direction_vector_dec(self, val):
        """The declination ray's direction vector coordinate.

        Parameters
        ----------
        direction_vector_dec: float
            Direction DEC-coordinate. See :py:func:`direction_vector`.

        """
        self.__directionVectorDec = self.direction_vector('dec', val)

    @parameter(only='TIME_UNITS')
    def output_duration_units(self, val):
        """Output duration time units.

        Time units to use for displaying the duration of each interval found by the
        event search.

        Parameters
        ----------
        output_duration_units: str
            One of the following:

            - SECONDS
            - MINUTES
            - HOURS
            - DAYS

        Raises
        -------
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        self.__outputDurationUnits = val

    @parameter
    def should_complement_window(self, val):
        """Specifies whether to complement the intervals in the result window.

        That is, instead of finding the intervals where the condition is satisfied,
        find the intervals where the condition is not satisfied.

        Parameters
        ----------
        should_complement_window: bool
            Complement result window

        Raises
        -------
        TypeError
            If the value provided is not bool type.

        """
        if isinstance(val, bool):
            self.__shouldComplementWindow = val
        else:
            raise TypeError('Attribute should_complement_window should be a boolean.')

    @parameter(only='INTERVAL_ADJUSTMENT')
    def interval_adjustment(self, val):
        """Specifies whether to expand or contract the intervals in the result.

        Expanding the intervals will cause intervals that overlap, after expansion,
        to be combined into one interval.

        Parameters
        ----------
        interval_adjustment: str
            One of the following:

            - NO_ADJUSTMENT
            - EXPAND_INTERVALS
            - CONTRACT_INTERVALS

        Raises
        -------
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        self.__intervalAdjustment = val

    @parameter
    def interval_adjustment_amount(self, val):
        """The amount by which to expand or contract each interval at the endpoints.

        Each endpoint will be moved by this amount.

        Parameters
        ----------
        interval_adjustment_amount: float

        Raises
        ------
        CalculationUndefinedAttr:
            If :py:attr:`interval_adjustment_units` is not supplied

        """
        self.__intervalAdjustmentAmount = val

        if 'interval_adjustment_units' not in self.params:
            raise CalculationUndefinedAttr('interval_adjustment_amount', val,
                                           'interval_adjustment_units')

    @parameter(only='TIME_UNITS')
    def interval_adjustment_units(self, val):
        """The unit of the interval adjustment amount.

        Parameters
        ----------
        interval_adjustment_units: str
            One of the following:

            - SECONDS
            - MINUTES
            - HOURS
            - DAYS

        Raises
        -------
        CalculationInvalidAttr
            If the value provided is invalid.

        Raises
        ------
        CalculationUndefinedAttr:
            If :py:attr:`interval_adjustment_amount` is not supplied

        """
        self.__intervalAdjustmentUnits = val

        if 'interval_adjustment_amount' not in self.params:
            raise CalculationUndefinedAttr('interval_adjustment_units', val,
                                           'interval_adjustment_amount')

    @parameter(only='INTERVAL_FILTERING')
    def interval_filtering(self, val):
        """Specifies whether to omit interval smaller than a minimum threshold size.

        This threshold is applied after expansion or contraction of the intervals.

        Parameters
        ----------
        interval_filtering: str
            One of the following:

            - NO_FILTERING
            - OMIT_INTERVALS_SMALLER_THAN_A_THRESHOLD

        Raises
        -------
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        self.__intervalFiltering = val

    @parameter
    def interval_filtering_threshold(self, val):
        """Interval duration filtering threshold value.

        Parameters
        ----------
        interval_filtering_threshold: float
            Interval duration filtering threshold value.

        Raises
        ------
        CalculationUndefinedAttr:
            If :py:attr:`interval_filtering_threshold_units` is not supplied

        """
        self.__intervalFilteringThreshold = val

        if 'interval_filtering_threshold_units' not in self.params:
            raise CalculationUndefinedAttr('interval_filtering_threshold', val,
                                           'interval_filtering_threshold_units')

    @parameter(only='TIME_UNITS')
    def interval_filtering_threshold_units(self, val):
        """Units of the interval duration filtering threshold value.

        Parameters
        ----------
        interval_filtering_threshold_units: str
            One of the following:

            - SECONDS
            - MINUTES
            - HOURS
            - DAYS

        Raises
        -------
        CalculationInvalidAttr
            If the value provided is invalid.

        Raises
        ------
        CalculationUndefinedAttr:
            If :py:attr:`interval_filtering_threshold` is not supplied

        """
        self.__intervalFilteringThresholdUnits = val

        if 'interval_filtering_threshold' not in self.params:
            raise CalculationUndefinedAttr('interval_filtering_threshold_units', val,
                                           'interval_filtering_threshold')

    @parameter(only='COORDINATE_SYSTEM')
    def coordinate_system(self, val):
        """The name of the coordinate system in which to evaluate the coordinate.

        Only required for GF_COORDINATE_SEARCH, GF_SUB_POINT_SEARCH, and
        GF_SURFACE_INTERCEPT_POINT_SEARCH.

        Parameters
        ----------
        coordinate_system: str
            One of the following:

            - RECTANGULAR
            - RA/DEC
            - LATITUDINAL (planetocentric)
            - CYLINDRICAL
            - SPHERICAL
            - GEODETIC
            - PLANETOGRAPHIC

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        self.gf_condition(coordinateSystem=val)

    @parameter(only='COORDINATE')
    def coordinate(self, val):
        """The name of the SPICE coordinate to search on.

        Only needed for GF_COORDINATE_SEARCH, GF_SUB_POINT_SEARCH, and
        GF_SURFACE_INTERCEPT_POINT_SEARCH.

        Parameters
        ----------
        coordinate: str
             One of the following:

            - X
            - Y
            - Z
            - LONGITUDE
            - LATITUDE
            - COLATITUDE
            - RIGHT ASCENSION
            - DECLINATION
            - RANGE
            - RADIUS
            - ALTITUDE

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.

        """
        self.gf_condition(coordinate=val)

    @parameter(only='RELATIONAL_CONDITION')
    def relational_condition(self, val):
        """The relationship for the geometry finder test.

        Parameters
        ----------
        relational_condition: str
            One of the following:

            - =
            - <
            - >
            - RANGE
            - ABSMAX
            - ABSMIN
            - LOCMAX
            - LOCMIN

        Raises
        ------
        CalculationInvalidAttr
            If the value provided is invalid.
        CalculationUndefinedAttr:
            If the value is ``RANGE`, and :py:attr:`upper_limit` is not supplied.
            If the value is ``ABSMIN`` or ``ABSMAX``, and :py:attr:`adjustment_value`
            is not supplied.
            If the value is ``=``,  ``<``, ``>`` or ``RANGE``, and
            :py:attr:`reference_value` is not supplied.
        """
        self.gf_condition(relationalCondition=val)

        if val == 'RANGE' and 'upper_limit' not in self.params:
            raise CalculationUndefinedAttr(
                attr='relational_condition',
                value=val,
                missing='upper_limit'
            )

        if val in ('ABSMIN', 'ABSMAX') and \
                'adjustment_value' not in self.params:
            raise CalculationUndefinedAttr(
                attr='relational_condition',
                value=val,
                missing='adjustment_value'
            )

        if val in ('=', '<', '>', 'RANGE') and \
                'reference_value' not in self.params:
            raise CalculationUndefinedAttr(
                attr='relational_condition',
                value=val,
                missing='reference_value'
            )

    @parameter
    def reference_value(self, val):
        """The value to compare against, or the lower value of a range.

        Only needed if relationalCondition is not ABSMAX, ABSMIN, LOCMAX, or LOCMIN.

        Parameters
        ----------
        reference_value: float

        """
        self.gf_condition(referenceValue=val)

    @parameter
    def upper_limit(self, val):
        """The upper limit of a range. Only needed if relationalCondition is RANGE.

        Parameters
        ----------
        upper_limit: float

        """
        self.gf_condition(upperLimit=val)

    @parameter
    def adjustment_value(self, val):
        """The adjustment value to apply for ABSMIN and ABSMAX searches.

        Required if relationalCondition is ABSMIN or ABSMAX.

        Parameters
        ----------
        adjustment_value: float

        """
        self.gf_condition(adjustmentValue=val)

    def gf_condition(self, **kwargs):
        """Geometry Finder condition object.

        See the documentation for gfposc() for more details.

        Raises
        ------
        CalculationUndefinedAttr:
            If :py:attr:`calculation_type` is ``GF_COORDINATE_SEARCH``,
            ``GF_SUB_POINT_SEARCH`` or ``GF_SURFACE_INTERCEPT_POINT_SEARCH``, and
            :py:attr:`coordinate_system` or :py:attr:`coordinate` are not present.
        """
        try:
            self.__condition.update(kwargs)

        except AttributeError:
            # This set of checks is run only once.
            if self.params['calculation_type'] in (
                'GF_COORDINATE_SEARCH',
                'GF_SUB_POINT_SEARCH',
                'GF_SURFACE_INTERCEPT_POINT_SEARCH'
            ):
                if 'coordinate_system' not in self.params:
                    raise CalculationUndefinedAttr(
                        attr='calculation_type',
                        value=self.params['calculation_type'],
                        missing='coordinate_system'
                    ) from None

                if 'coordinate' not in self.params:
                    raise CalculationUndefinedAttr(
                        attr='calculation_type',
                        value=self.params['calculation_type'],
                        missing='coordinate'
                    ) from None

            self.__condition = kwargs
