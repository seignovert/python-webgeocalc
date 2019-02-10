# -*- coding: utf-8 -*-
'''Webgeocalc Calculations.'''

import time

from .api import API
from .errors import CalculationAlreadySubmitted, CalculationConflictAttr, \
    CalculationIncompatibleAttr, CalculationInvalidAttr, CalculationInvalidValue, \
    CalculationNotCompleted, CalculationRequiredAttr, CalculationTimeOut, \
    CalculationUndefinedAttr
from .types import KernelSetDetails
from .vars import ABERRATION_CORRECTION, ANGULAR_UNITS, ANGULAR_VELOCITY_REPRESENTATION, \
    ANGULAR_VELOCITY_UNITS, AXIS, CALCULATION_TYPE, COORDINATE_REPRESENTATION, \
    INTERCEPT_VECTOR_TYPE, INTERVALS, ORIENTATION_REPRESENTATION, OUTPUT_TIME_FORMAT, \
    SHAPE, STATE_REPRESENTATION, SUB_POINT_TYPE, TIME_FORMAT, TIME_LOCATION, \
    TIME_STEP_UNITS, TIME_SYSTEM


class SetterProperty(object):
    '''Setter property decorator.'''

    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__

    def __set__(self, obj, value):
        return self.func(obj, value)


class Calculation(object):
    '''Webgeocalc calculation object.

    Parameters
    ----------
    time_system: str, optional
        See: :py:attr:`time_system`
    time_format: str, optional
        See: :py:attr:`time_format`
    verbose: bool, optional
        Verbose calculation status during :py:func:`submit`, :py:func:`update`
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
    intercept_vector_type: str
        See: :py:attr:`intercept_vector_type`
    intercept_instrument: str or int
        See: :py:attr:`intercept_instrument`
    intercept_frame: str
        See: :py:attr:`intercept_frame`
    intercept_frame_axis: str
        See: :py:attr:`intercept_frame_axis`
    intercept_vector_x: float
        See: :py:attr:`intercept_vector_x`
    intercept_vector_y: float
        See: :py:attr:`intercept_vector_y`
    intercept_vector_z: float
        See: :py:attr:`intercept_vector_z`
    intercept_vector_ra: float
        See: :py:attr:`intercept_vector_ra`
    intercept_vector_dec: float
        See: :py:attr:`intercept_vector_dec`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`calculation_type`, :py:attr:`time_system` and
        :py:attr:`time_format` are not provided.
    CalculationRequiredAttr
        If neither :py:attr:`kernels` nor :py:attr:`kernel_paths` is not provided.
    CalculationRequiredAttr
        If neither :py:attr:`times` nor :py:attr:`intervals` is not provided.

    '''

    def __init__(self, time_system='UTC', time_format='CALENDAR', verbose=True, **kwargs):
        # Add default parameters to kwargs
        kwargs['time_system'] = time_system
        kwargs['time_format'] = time_format

        # Init parameters
        self.params = kwargs
        self.__kernels = []
        self.id = None
        self.status = 'NOT SUBMITED'
        self.columns = None
        self.values = None
        self.verbose = verbose

        # Required parameters
        self._required(['calculation_type', 'time_system', 'time_format'], kwargs)

        if 'kernels' not in kwargs.keys() and 'kernel_paths' not in kwargs.keys():
            raise CalculationRequiredAttr('kernels\' or \'kernel_paths')

        if 'times' not in kwargs.keys() and 'intervals' not in kwargs.keys():
            raise CalculationRequiredAttr('times\' or \'intervals')

        # Check and set parameters
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return '\n'.join([
            f"<{self.__class__.__name__}> Status: {self.status} (id: {self.id})"
        ] + [
            f' - {k}: {v}' for k, v in self.payload.items()
        ])

    @staticmethod
    def _required(attrs, kwargs):
        # Check required arguments
        for required in attrs:
            if required not in kwargs.keys():
                raise CalculationRequiredAttr(required)

    @property
    def payload(self):
        '''Calculation payload parameters *dict* for JSON input in WebGeoCalc format.

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

        '''
        return {k.split('__')[-1]: v for k, v in vars(self).items() if k.startswith('_')}

    def submit(self):
        '''Submit calculation parameters and get calculation ``id``, ``phase`` and ``progress``.

        Raises
        ------
        CalculationAlreadySubmitted
            If the calculation was already submitted (to avoid duplicated submissions).

        Example
        -------
        >>> calc.submit()  # noqa: E501  # doctest: +SKIP
        [Calculation submit] Status: LOADING_KERNELS (id: 8750344d-645d-4e43-b159-c8d88d28aac6)
        >>> calc.id        # doctest: +SKIP
        '8750344d-645d-4e43-b159-c8d88d28aac6'
        >>> calc.status    # doctest: +SKIP
        'LOADING_KERNELS'

        '''
        if self.id is not None:
            raise CalculationAlreadySubmitted(self.id)

        self.id, self.status, self.progress = API.new_calculation(self.payload)

        if self.verbose:
            print(f'[Calculation submit] Status: {self.status} (id: {self.id})')

    def resubmit(self):
        '''Reset calculation ``id`` and re-submit the calculation.

        See: :py:func:`submit`.
        '''
        self.id = None
        self.submit()

    def update(self):
        '''Update calculation status ``phase`` and ``progress``.

        Example
        -------
        >>> calc.update()  # noqa: E501  # doctest: +SKIP
        [Calculation update] Status: LOADING_KERNELS (id: 8750344d-645d-4e43-b159-c8d88d28aac6)
        >>> calc.update()  # doctest: +SKIP
        [Calculation update] Status: COMPLETE (id: 8750344d-645d-4e43-b159-c8d88d28aac6)
        '''
        if self.id is None:
            self.submit()
        else:
            _, self.status, self.progress = API.status_calculation(self.id)

            if self.verbose:
                print(f'[Calculation update] Status: {self.status} (id: {self.id})')

    @property
    def results(self):
        '''Gets the results of a calculation, if its status is `COMPLETE`.

        Return
        ------
        dict
            Calculation results as *dict* based on output columns. If multiple ``times``
            or ``intervals`` are used, the value of the *dict* will be an array.
            See examples.

        Raises
        ------
        CalculationNotCompleted
            If calculation status is not `COMPLETE`.

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

        '''
        if self.status != 'COMPLETE':
            raise CalculationNotCompleted(self.status)

        if self.columns is None or self.values is None:
            self.columns, self.values = API.results_calculation(self.id)

        if len(self.values) == 1:
            data = self.values[0]
        else:
            # Transpose values array
            data = [[row[i] for row in self.values] for i in range(len(self.columns))]

        return {column.outputID: value for column, value in zip(self.columns, data)}

    def run(self, timeout=30, sleep=1):
        '''Submit, update and retrive calculation results at once.

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

        '''
        if self.columns is not None and self.values is not None:
            return self.results

        for i in range(int(timeout / sleep)):
            self.update()

            if self.status == 'COMPLETE':
                return self.results
            else:
                time.sleep(sleep)
        else:
            raise CalculationTimeOut(timeout, sleep)

    @SetterProperty
    def calculation_type(self, val):
        '''The type of calculation to perform.

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

        '''
        if val in CALCULATION_TYPE:
            self.__calculationType = val
        else:
            raise CalculationInvalidAttr('calculation_type', val, CALCULATION_TYPE)

    @SetterProperty
    def kernels(self, kernel_sets):
        '''Add kernel sets.

        Parameters
        ----------
        kernels: str, int, [str or/and int]
            Kernel set(s) to be used for the calculation::

               [{'type': 'KERNEL_SET', 'id': 5}, ...]

        '''
        self.__kernels += [
            self._kernel_id_obj(kernel_sets)
        ] if isinstance(
            kernel_sets,
            (int, str, KernelSetDetails)
        ) else list(map(self._kernel_id_obj, kernel_sets))

    @staticmethod
    def _kernel_id_obj(kernel_set):
        # Payload kernel set object
        return {"type": "KERNEL_SET", "id": API.kernel_set_id(kernel_set)}

    @SetterProperty
    def kernel_paths(self, paths):
        '''Add path for individual kernel paths.

        Parameters
        ----------
        kernel_paths: str, [str]
            Kernel path(s) to be used for the calculation::

               [{'type': 'KERNEL', 'path': 'pds/wgc/kernels/lsk/naif0012.tls'}, ...]

        '''
        self.__kernels += [
            self._kernel_path_obj(paths)
        ] if isinstance(paths, str) else list(map(self._kernel_path_obj, paths))

    @staticmethod
    def _kernel_path_obj(server_path):
        # Payloaf individual kernel path object
        return {"type": "KERNEL", "path": server_path}

    @SetterProperty
    def times(self, times):
        '''Calculation input times.

        Parameters
        ----------
        times: str or [str]
            String or array of strings representing the time points
            that should be used in the calculation.

        Raises
        ------
        CalculationConflictAttr
            Either this parameter or the py:attr:`intervals` parameter must be supplied.

        '''
        self.__times = [times] if isinstance(times, str) else times

        if 'intervals' in self.params.keys():
            raise CalculationConflictAttr('times', 'intervals')

    @SetterProperty
    def intervals(self, intervals):
        '''Calculation input intervals.

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

        '''
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
                raise CalculationInvalidAttr('intervals', intervals, INTERVALS)
        elif isinstance(intervals, list) and len(intervals) == 1:
            if isinstance(intervals[0], (dict, list)):
                self.__intervals = [self._interval(intervals[0])]
            else:
                raise CalculationInvalidAttr('intervals', intervals, INTERVALS)
        else:
            raise CalculationInvalidAttr('intervals', intervals, INTERVALS)

        if 'time_step' not in self.params.keys():
            raise CalculationUndefinedAttr('intervals', intervals, 'time_step')

    @staticmethod
    def _interval(interval):
        # Parse interval object
        if not len(interval) == 2:
            raise CalculationInvalidAttr('interval', interval, INTERVALS[:2])

        if isinstance(interval, dict):
            if 'startTime' in interval.keys() and 'endTime' in interval.keys():
                return interval
            else:
                raise CalculationInvalidAttr('interval', interval, INTERVALS[:2])
        else:
            return {'startTime': str(interval[0]), 'endTime': str(interval[1])}

    @SetterProperty
    def time_step(self, val):
        '''Time step for intervals.

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

        '''
        self.__timeStep = int(val)

        if 'times' in self.params.keys():
            raise CalculationConflictAttr('time_step', 'times')

        if 'time_step_units' not in self.params.keys():
            raise CalculationUndefinedAttr('time_step', val, 'time_step_units')

    @SetterProperty
    def time_step_units(self, val):
        '''Time step units.

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

        '''
        if val in TIME_STEP_UNITS:
            self.__timeStepUnit = val
        else:
            raise CalculationInvalidAttr('time_step_units', val, TIME_STEP_UNITS)

        if 'times' in self.params.keys():
            raise CalculationConflictAttr('time_step', 'times')
        if 'time_step' not in self.params.keys():
            raise CalculationUndefinedAttr('time_step_units', val, 'time_step')

    @SetterProperty
    def time_system(self, val):
        '''Time System.

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

        '''
        if val in TIME_SYSTEM:
            self.__timeSystem = val
        else:
            raise CalculationInvalidAttr('time_system', val, TIME_SYSTEM)

        if val == 'SPACECRAFT_CLOCK' and 'sclk_id' not in self.params.keys():
            raise CalculationUndefinedAttr('time_system', 'SPACECRAFT_CLOCK', 'sclk_id')

    @SetterProperty
    def time_format(self, val):
        '''Time format input.

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

        '''
        if val in TIME_FORMAT:
            self.__timeFormat = val
        else:
            raise CalculationInvalidAttr('time_format', val, TIME_FORMAT)

        self._required(['time_system'], self.params)

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

    @SetterProperty
    def sclk_id(self, val):
        '''Spacecraft clock kernel id.

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

        '''
        self.__sclkId = int(val)

        self._required(['time_system'], self.params)

        if self.params['time_system'] != 'SPACECRAFT_CLOCK':
            raise CalculationIncompatibleAttr(
                'sclk_id', val, 'time_system',
                self.params['time_system'], ['SPACECRAFT_CLOCK'])

    @SetterProperty
    def output_time_system(self, val):
        '''The time system for results output times.

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

        '''
        if val in TIME_SYSTEM:
            self.__outputTimeSystem = val
        else:
            raise CalculationInvalidAttr('output_time_system', val, TIME_SYSTEM)

        if val == 'SPACECRAFT_CLOCK' and 'output_sclk_id' not in self.params.keys():
            raise CalculationUndefinedAttr(
                'output_time_system', 'SPACECRAFT_CLOCK', 'output_sclk_id')

    @SetterProperty
    def output_time_format(self, val):
        '''The time format for the result output times.

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

        '''
        if val in OUTPUT_TIME_FORMAT:
            self.__outputTimeFormat = val
        else:
            raise CalculationInvalidAttr('output_time_format', val, OUTPUT_TIME_FORMAT)

        self._required(['output_time_system'], self.params)

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

    @SetterProperty
    def output_time_custom_format(self, val):
        '''A SPICE ``timout()`` format string.

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

        '''
        self.__outputTimeCustomFormat = val

        self._required(['output_time_format'], self.params)

        if self.params['output_time_format'] != 'CUSTOM':
            raise CalculationIncompatibleAttr(
                'output_time_custom_format', val, 'output_time_format',
                self.params['output_time_format'], ['CUSTOM'])

    @SetterProperty
    def output_sclk_id(self, val):
        '''The output spacecraft clock kernel id.

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

        '''
        self.__outputSclkId = int(val)

        self._required(['output_time_system'], self.params)

        if self.params['output_time_system'] != 'SPACECRAFT_CLOCK':
            raise CalculationIncompatibleAttr(
                'output_sclk_id', val, 'output_time_system',
                self.params['output_time_system'], ['SPACECRAFT_CLOCK'])

    @SetterProperty
    def target(self, val):
        '''Target body.

        Parameters
        ----------
        target: str or int
            The target body ``name`` or ``id`` from :py:func:`API.bodies`.

        '''
        self.__target = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def target_frame(self, val):
        '''The target body-fixed reference frame name.

        Parameters
        ----------
        target_frame: str
            Reference frame ``name``.

        '''
        self.__targetFrame = val

    @SetterProperty
    def target_1(self, val):
        '''The target body the first body.

        Parameters
        ----------
        target_1: str
            Target body ``name`` or ``id``.

        '''
        self.__target1 = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def target_2(self, val):
        '''The target body the second body.

        Parameters
        ----------
        target_2: str
            Target body ``name`` or ``id``.

        '''
        self.__target2 = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def shape_1(self, val):
        '''The shape to use for the first body.

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

        '''
        if val in SHAPE:
            self.__shape1 = val
        else:
            raise CalculationInvalidAttr('shape_1', val, SHAPE)

    @SetterProperty
    def shape_2(self, val):
        '''The shape to use for the second body.

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

        '''
        if val in SHAPE:
            self.__shape2 = val
        else:
            raise CalculationInvalidAttr('shape_2', val, SHAPE)

    @SetterProperty
    def observer(self, val):
        '''The observing body.

        Parameters
        ----------
        observer: str or int
            The oberving body ``name`` or ``id`` from :py:func:`API.bodies`.

        '''
        self.__observer = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def reference_frame(self, val):
        '''The reference frame.

        Parameters
        ----------
        reference_frame: str or int
            The reference frame ``name`` or ``id`` from :py:func:`API.frames`.

        '''
        self.__referenceFrame = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def frame_1(self, val):
        '''The first reference frame.

        Parameters
        ----------
        frame_1: str or int
            The reference frame ``name`` or ``id`` from :py:func:`API.frames`.

        '''
        self.__frame1 = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def frame_2(self, val):
        '''The second reference frame.

        Parameters
        ----------
        frame_2: str or int
            The reference frame ``name`` or ``id`` from :py:func:`API.frames`.

        '''
        self.__frame2 = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def orbiting_body(self, val):
        '''The SPICE orbiting body.

        Parameters
        ----------
        orbiting_body: str or int
            SPICE body ``name`` or ``id`` for the orbiting body.

        '''
        self.__orbitingBody = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def center_body(self, val):
        '''
        The SPICE body center of motion.

        Parameters
        ----------
        center_body: str or int
            SPICE body ``name`` or ``id`` for the body that is the center of motion.

        '''
        self.__centerBody = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def aberration_correction(self, val):
        '''SPICE aberration correction.

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

        '''
        if val in ABERRATION_CORRECTION:
            self.__aberrationCorrection = val
        else:
            raise CalculationInvalidAttr(
                'aberration_correction', val, ABERRATION_CORRECTION)

    @SetterProperty
    def state_representation(self, val):
        '''State representation.

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

        '''
        if val in STATE_REPRESENTATION:
            self.__stateRepresentation = val
        else:
            raise CalculationInvalidAttr(
                'state_representation', val, STATE_REPRESENTATION)

    @SetterProperty
    def time_location(self, val):
        '''The frame for the input times.

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

        Error
        -----
        NAIF API docs::

            `Only needed if aberrationCorrection is not NONE.`

        Required even when :py:attr:`aberration_correction` is ``NONE``.

        '''
        if val in TIME_LOCATION:
            self.__timeLocation = val
        else:
            raise CalculationInvalidAttr('time_location', val, TIME_LOCATION)

    @SetterProperty
    def orientation_representation(self, val):
        '''The representation of the result transformation.

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

        '''
        if val in ORIENTATION_REPRESENTATION:
            self.__orientationRepresentation = val
        else:
            raise CalculationInvalidAttr(
                'orientation_representation', val, ORIENTATION_REPRESENTATION)

    @SetterProperty
    def axis_1(self, val):
        '''The first axis for Euler angle rotation.

        Parameters
        ----------
        axis_1: str
            Axis name. See: :py:func:`axis`.

        '''
        self.__axis1 = self.axis('axis_1', val)

    @SetterProperty
    def axis_2(self, val):
        '''The second axis for Euler angle rotation.

        Parameters
        ----------
        axis_3: str
            Axis name. See: :py:func:`axis`.

        '''
        self.__axis2 = self.axis('axis_2', val)

    @SetterProperty
    def axis_3(self, val):
        '''The third axis for Euler angle rotation.

        Parameters
        ----------
        axis_3: str
            Axis name. See: :py:func:`axis`.

        '''
        self.__axis3 = self.axis('axis_3', val)

    def axis(self, name, val):
        '''Axis for Euler angle rotation.

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

        '''
        if 'orientation_representation' not in self.params.keys():
            raise CalculationUndefinedAttr(name, val, 'orientation_representation')

        if self.params['orientation_representation'] != 'EULER_ANGLES':
            raise CalculationIncompatibleAttr(
                name, val, 'orientation_representation',
                self.params['orientation_representation'], ['EULER_ANGLES'])

        if val in AXIS:
            return val
        else:
            raise CalculationInvalidAttr(name, val, AXIS)

    @SetterProperty
    def angular_units(self, val):
        '''The angular units.

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

        '''
        if val in ANGULAR_UNITS:
            self.__angularUnits = val
        else:
            raise CalculationInvalidAttr('angular_units', val, ANGULAR_UNITS)

        if 'orientation_representation' not in self.params.keys():
            raise CalculationUndefinedAttr(
                'angular_units', val, 'orientation_representation')

        if not self.params['orientation_representation'] in ['EULER_ANGLES',
                                                             'ANGLE_AND_AXIS']:
            raise CalculationIncompatibleAttr(
                'angular_units', val, 'orientation_representation',
                self.params['orientation_representation'],
                ['EULER_ANGLES', 'ANGLE_AND_AXIS'])

    @SetterProperty
    def angular_velocity_representation(self, val):
        '''Angular velocity representation.

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

        '''
        if val in ANGULAR_VELOCITY_REPRESENTATION:
            self.__angularVelocityRepresentation = val
        else:
            raise CalculationInvalidAttr(
                'angular_velocity_representation', val, ANGULAR_VELOCITY_REPRESENTATION)

    @SetterProperty
    def angular_velocity_units(self, val):
        '''The units for the angular velocity.

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

        '''
        if val in ANGULAR_VELOCITY_UNITS:
            self.__angularVelocityUnits = val
        else:
            raise CalculationInvalidAttr(
                'angular_velocity_units', val, ANGULAR_VELOCITY_UNITS)

        if 'angular_velocity_representation' not in self.params.keys():
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

    @SetterProperty
    def coordinate_representation(self, val):
        '''Coordinate Representation.

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

        '''
        if val in COORDINATE_REPRESENTATION:
            self.__coordinateRepresentation = val
        else:
            raise CalculationInvalidAttr(
                'coordinate_representation', val, COORDINATE_REPRESENTATION)

    @SetterProperty
    def latitude(self, val):
        '''Latitude of the surface point.

        Parameters
        ----------
        latitude: float
            Latitude angle (in degrees).

        Raises
        ------
        CalculationInvalidValue
            If ``latitude`` not in [-90, +90] range.

        '''
        if val >= -90 and val <= 90:
            self.__latitude = val
        else:
            raise CalculationInvalidValue('latitude', val, -90, 90)

    @SetterProperty
    def longitude(self, val):
        '''Longitude of the surface point.

        Parameters
        ----------
        longitude: float
            Longitude angle (in degrees).

        Raises
        ------
        CalculationInvalidValue
            If ``longitude`` not in [-180, +180] range.

        '''
        if val >= -180 and val <= 180:
            self.__longitude = val
        else:
            raise CalculationInvalidValue('longitude', val, -180, 180)

    @SetterProperty
    def sub_point_type(self, val):
        '''Sub-observer point.

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

        '''
        if val in SUB_POINT_TYPE:
            self.__subPointType = val
        else:
            raise CalculationInvalidAttr('sub_point_type', val, SUB_POINT_TYPE)

    @SetterProperty
    def intercept_vector_type(self, val):
        '''Type of intercept vector.

        Parameters
        ----------
        intercept_vector_type: str
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
            but :py:attr:`intercept_instrument` is not provided.
        CalculationRequiredAttr
            If this parameter is ``REFERENCE_FRAME_AXIS`` or ``VECTOR_IN_REFERENCE_FRAME``
            but :py:attr:`intercept_frame` is not provided.
        CalculationRequiredAttr
            If this parameter is ``REFERENCE_FRAME_AXIS`` but
            :py:attr:`intercept_frame_axis` is not provided.
        CalculationUndefinedAttr
            If this parameter is ``VECTOR_IN_INSTRUMENT_FOV``
            or ``VECTOR_IN_REFERENCE_FRAME`` but neither :py:attr:`intercept_vector_x`,
            :py:attr:`intercept_vector_y` and :py:attr:`intercept_vector_z`
            nor :py:attr:`intercept_vector_ra` and :py:attr:`intercept_vector_dec`
            are provided.

        '''
        if val in INTERCEPT_VECTOR_TYPE:
            self.__interceptVectorType = val
        else:
            raise CalculationInvalidAttr(
                'intercept_vector_type', val, INTERCEPT_VECTOR_TYPE)

        if val in ['INSTRUMENT_BORESIGHT', 'INSTRUMENT_FOV_BOUNDARY_VECTORS',
                   'VECTOR_IN_INSTRUMENT_FOV']:
            self._required(['intercept_instrument'], self.params)

        elif val in ['REFERENCE_FRAME_AXIS', 'VECTOR_IN_REFERENCE_FRAME']:
            self._required(['intercept_frame'], self.params)
            if val == 'REFERENCE_FRAME_AXIS':
                self._required(['intercept_frame_axis'], self.params)

        keys = self.params.keys()
        if val in ['VECTOR_IN_INSTRUMENT_FOV', 'VECTOR_IN_REFERENCE_FRAME']:
            if not(
                'intercept_vector_x' in keys and  # noqa: W504
                'intercept_vector_y' in keys and  # noqa: W504
                'intercept_vector_z' in keys
            ) and not(
                'intercept_vector_ra' in keys and  # noqa: W504
                'intercept_vector_dec' in keys
            ):
                raise CalculationUndefinedAttr(
                    'intercept_vector_type', val,
                    "intercept_vector_x/y/z' or 'intercept_vector_ra/dec")

    @SetterProperty
    def intercept_instrument(self, val):
        '''Intercept imnstrument.

        Parameters
        ----------
        intercept_instrument: str or int
            The instrument ``name`` or ``id``.

        Raises
        ------
        CalculationUndefinedAttr
            If :py:attr:`intercept_vector_type` is not provided.
        CalculationIncompatibleAttr
            If :py:attr:`intercept_vector_type` not in ``INSTRUMENT_BORESIGHT``,
            ``INSTRUMENT_FOV_BOUNDARY_VECTORS`` or ``VECTOR_IN_INSTRUMENT_FOV``.

        '''
        if 'intercept_vector_type' not in self.params.keys():
            raise CalculationUndefinedAttr(
                'intercept_instrument', val, 'intercept_vector_type')

        choices = ['INSTRUMENT_BORESIGHT', 'INSTRUMENT_FOV_BOUNDARY_VECTORS',
                   'VECTOR_IN_INSTRUMENT_FOV']
        if not self.params['intercept_vector_type'] in choices:
            raise CalculationIncompatibleAttr(
                'intercept_instrument', val, 'intercept_vector_type',
                self.params['intercept_vector_type'], choices)

        self.__interceptInstrument = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def intercept_frame(self, val):
        '''Intercept vector reference frame.

        Parameters
        ----------
        intercept_frame: str
            The vector's reference frame ``name``.

        Raises
        ------
        CalculationUndefinedAttr
            If :py:attr:`intercept_vector_type` is not provided.
        CalculationIncompatibleAttr
            If :py:attr:`intercept_vector_type` is not in ``REFERENCE_FRAME_AXIS``
            or ``VECTOR_IN_REFERENCE_FRAME``.

        '''
        if 'intercept_vector_type' not in self.params.keys():
            raise CalculationUndefinedAttr(
                'intercept_frame', val, 'intercept_vector_type')

        choices = ['REFERENCE_FRAME_AXIS', 'VECTOR_IN_REFERENCE_FRAME']
        if not self.params['intercept_vector_type'] in choices:
            raise CalculationIncompatibleAttr(
                'intercept_frame', val, 'intercept_vector_type',
                self.params['intercept_vector_type'], choices)

        self.__interceptFrame = val

    @SetterProperty
    def intercept_frame_axis(self, val):
        '''The vector's reference frame axis name.

        Parameters
        ----------
        intercept_frame: str
            The vector's reference frame  axis. One of:

            - X
            - Y
            - Z

        Raises
        ------
        CalculationUndefinedAttr
            If :py:attr:`intercept_vector_type` is not provided.
        CalculationIncompatibleAttr
            If :py:attr:`intercept_vector_type` is not ``REFERENCE_FRAME_AXIS``.
        CalculationInvalidAttr
            If the value provided is invalid.

        '''
        if 'intercept_vector_type' not in self.params.keys():
            raise CalculationUndefinedAttr(
                'intercept_frame_axis', val, 'intercept_vector_type')

        if self.params['intercept_vector_type'] != 'REFERENCE_FRAME_AXIS':
            raise CalculationIncompatibleAttr(
                'intercept_frame_axis', val, 'intercept_vector_type',
                self.params['intercept_vector_type'], ['REFERENCE_FRAME_AXIS'])

        if val in AXIS:
            self.__interceptFrameAxis = val
        else:
            raise CalculationInvalidAttr('intercept_frame_axis', val, AXIS)

    def intercept_vector(self, axis, val):
        '''Intercept vector coordinate.

        Parameters
        ----------
        axis: str
            Axis name.
        val: float
            Value on the axis.

        Raises
        ------
        CalculationUndefinedAttr
            If :py:attr:`intercept_vector_type` is not provided.
        CalculationIncompatibleAttr
            If :py:attr:`intercept_vector_type` is not in ``VECTOR_IN_INSTRUMENT_FOV``
            or ``VECTOR_IN_REFERENCE_FRAME``.

        '''
        if 'intercept_vector_type' not in self.params.keys():
            raise CalculationUndefinedAttr(
                'intercept_vector_' + axis, val, 'intercept_vector_type')

        choices = ['VECTOR_IN_INSTRUMENT_FOV', 'VECTOR_IN_REFERENCE_FRAME']
        if not self.params['intercept_vector_type'] in choices:
            raise CalculationIncompatibleAttr(
                'intercept_vector_' + axis, val, 'intercept_vector_type',
                self.params['intercept_vector_type'], choices)
        return val

    @SetterProperty
    def intercept_vector_x(self, val):
        '''The X intercept vector coordinate.

        Parameters
        ----------
        intercept_vector_x: float
            Intercept x-coordinate. See :py:func:`intercept_vector`.

        '''
        self.__interceptVectorX = self.intercept_vector('x', val)

    @SetterProperty
    def intercept_vector_y(self, val):
        '''The Y intercept vector coordinate.

        Parameters
        ----------
        intercept_vector_y: float
            Intercept y-coordinate. See :py:func:`intercept_vector`.

        '''
        self.__interceptVectorY = self.intercept_vector('y', val)

    @SetterProperty
    def intercept_vector_z(self, val):
        '''The Z intercept vector coordinate.

        Parameters
        ----------
        intercept_vector_z: float
            Intercept z-coordinate. See :py:func:`intercept_vector`.

        '''
        self.__interceptVectorZ = self.intercept_vector('z', val)

    @SetterProperty
    def intercept_vector_ra(self, val):
        '''The right-ascenssion intercept vector coordinate.

        Parameters
        ----------
        intercept_vector_ra: float
            Intercept RA-coordinate. See :py:func:`intercept_vector`.

        '''
        self.__interceptVectorRA = self.intercept_vector('ra', val)

    @SetterProperty
    def intercept_vector_dec(self, val):
        '''The declination intercept vector coordinate.

        Parameters
        ----------
        intercept_vector_dec: float
            Intercept DEC-coordinate. See :py:func:`intercept_vector`.

        '''
        self.__interceptVectorDec = self.intercept_vector('dec', val)


class StateVector(Calculation):
    '''State vector calculation.

    Calculates the position of one body relative to another,
    calculated in a desired reference frame.

    Parameters
    ----------
    aberration_correction: str, optional
        See: :py:attr:`.aberration_correction`
    state_representation: str, optional
        See: :py:attr:`.state_representation`

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`.kernels`
    kernel_paths: str, [str]
        See: :py:attr:`.kernel_paths`
    times: str or [str]
        See: :py:attr:`.times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`.intervals`
    time_step: int
        See: :py:attr:`.time_step`
    time_step_units: str
        See: :py:attr:`.time_step_units`
    time_system: str
        See: :py:attr:`.time_system`
    time_format: str
        See: :py:attr:`.time_format`
    target: str or int
        See: :py:attr:`.target`
    observer: str or int
        See: :py:attr:`.observer`
    reference_frame: str or int
        See: :py:attr:`.reference_frame`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`.target`, :py:attr:`.observer` and
        :py:attr:`.reference_frame` are not provided.

    '''

    def __init__(self, aberration_correction='CN',
                 state_representation='RECTANGULAR', **kwargs):

        self._required(['target', 'observer', 'reference_frame'], kwargs)

        kwargs['calculation_type'] = 'STATE_VECTOR'
        kwargs['aberration_correction'] = aberration_correction
        kwargs['state_representation'] = state_representation

        super().__init__(**kwargs)

class AngularSeparation(Calculation):
    '''Angular separation calculation.

    Calculates the angular separation of two bodies as seen by an observer body.

    Parameters
    ----------
    shape_1: str, optional
        See: :py:attr:`.shape_1`
    shape_2: str, optional
        See: :py:attr:`.shape_2`
    aberration_correction: str, optional
        See: :py:attr:`.aberration_correction`

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`.kernels`
    kernel_paths: str, [str]
        See: :py:attr:`.kernel_paths`
    times: str or [str]
        See: :py:attr:`.times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`.intervals`
    time_step: int
        See: :py:attr:`.time_step`
    time_step_units: str
        See: :py:attr:`.time_step_units`
    time_system: str
        See: :py:attr:`.time_system`
    time_format: str
        See: :py:attr:`.time_format`
    target_1: str or int
        See: :py:attr:`.target_1`
    target_2: str or int
        See: :py:attr:`.target_2`
    observer: str or int
        See: :py:attr:`.observer`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`.target_1`, :py:attr:`.target_2` and
        :py:attr:`.observer` are not provided.

    '''

    def __init__(self, shape_1='POINT', shape_2='POINT',
                 aberration_correction='CN', **kwargs):

        self._required(['target_1', 'target_2', 'observer'], kwargs)

        kwargs['calculation_type'] = 'ANGULAR_SEPARATION'
        kwargs['shape_1'] = shape_1
        kwargs['shape_2'] = shape_2
        kwargs['aberration_correction'] = aberration_correction

        super().__init__(**kwargs)

class AngularSize(Calculation):
    '''Angular size calculation.

    Calculates the angular size of a target as seen by an observer.

    Parameters
    ----------
    aberration_correction: str, optional
        See: :py:attr:`.aberration_correction`

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`.kernels`
    kernel_paths: str, [str]
        See: :py:attr:`.kernel_paths`
    times: str or [str]
        See: :py:attr:`.times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`.intervals`
    time_step: int
        See: :py:attr:`.time_step`
    time_step_units: str
        See: :py:attr:`.time_step_units`
    time_system: str
        See: :py:attr:`.time_system`
    time_format: str
        See: :py:attr:`.time_format`
    target: str or int
        See: :py:attr:`.target`
    observer: str or int
        See: :py:attr:`.observer`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`.target` and :py:attr:`.observer` are not provided.

    '''

    def __init__(self, aberration_correction='CN', **kwargs):

        self._required(['target', 'observer'], kwargs)

        kwargs['calculation_type'] = 'ANGULAR_SIZE'
        kwargs['aberration_correction'] = aberration_correction

        super().__init__(**kwargs)


class FrameTransformation(Calculation):
    '''Frame transforme calculation.

    Calculate the transformation from one reference frame (Frame 1)
    to another reference frame (Frame 2).

    Parameters
    ----------
    aberration_correction: str, optional
        See: :py:attr:`.aberration_correction`
    time_location: str, optional
        See: :py:attr:`.time_location`
    orientation_representation: str, optional
        See: :py:attr:`.orientation_representation`
    axis_1: str, optional
        See: :py:attr:`.axis_1`
    axis_2: str, optional
        See: :py:attr:`.axis_2`
    axis_3: str, optional
        See: :py:attr:`.axis_3`
    angular_units: str, optional
        See: :py:attr:`.angular_units`
    angular_velocity_representation: str, optional
        See: :py:attr:`.angular_velocity_representation`
    angular_velocity_units: str, optional
        See: :py:attr:`.angular_velocity_units`

        Warning
        -------
        Attribute :py:attr:`.aberration_correction` must be ``NONE``, `LT``, ``CN``,
        ``XLT`` or ``XCN``.

        Attributes :py:attr:`.axis_1`, :py:attr:`.axis_2` and :py:attr:`.axis_3`
        are imported only if :py:attr:`.orientation_representation` is ``EULER_ANGLES``.

        Attribute :py:attr:`.angular_units` is imported only
        if :py:attr:`.orientation_representation` is ``EULER_ANGLES``
        or ``ANGLE_AND_AXIS``.

        Attribute :py:attr:`.angular_velocity_units` is imported only if
        :py:attr:`.angular_velocity_representation` is ``VECTOR_IN_FRAME1``,
        ``VECTOR_IN_FRAME2`` or ``EULER_ANGLE_DERIVATIVES``.

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`.kernels`
    kernel_paths: str, [str]
        See: :py:attr:`.kernel_paths`
    times: str or [str]
        See: :py:attr:`.times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`.intervals`
    time_step: int
        See: :py:attr:`.time_step`
    time_step_units: str
        See: :py:attr:`.time_step_units`
    time_system: str
        See: :py:attr:`.time_system`
    time_format: str
        See: :py:attr:`.time_format`
    frame_1: str or int
        See: :py:attr:`.frame_1`
    frame_2: str or int
        See: :py:attr:`.frame_2`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`.frame_1` and :py:attr:`.frame_2` are not provided.
    CalculationInvalidAttr
        If :py:attr:`.aberration_correction` is in ``LT+S``, ``CN+S``,
        ``XLT+S`` or ``XCN+S``.

    '''

    def __init__(self, aberration_correction='CN', time_location='FRAME1',
                 orientation_representation='EULER_ANGLES',
                 axis_1='X', axis_2='Y', axis_3='Z',
                 angular_units='deg',
                 angular_velocity_representation='VECTOR_IN_FRAME1',
                 angular_velocity_units='deg/s',
                 **kwargs):

        self._required(['frame_1', 'frame_2'], kwargs)

        aberration_correction_allowed = list(filter(
            lambda x: '+S' not in x, ABERRATION_CORRECTION))

        if aberration_correction not in aberration_correction_allowed:
            raise CalculationInvalidAttr(
                'aberration_correction', aberration_correction,
                aberration_correction_allowed)

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
    '''Illumination angles calculation.

    Calculate the emission, phase and solar incidence angles
    at a point on a target as seen from an observer.

    Parameters
    ----------
    shape_1: str, optional
        See: :py:attr:`shape_1`
    coordinate_representation: str, optional
        See: :py:attr:`coordinate_representation`
    aberration_correction: str, optional
        See: :py:attr:`.aberration_correction`

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`.kernels`
    kernel_paths: str, [str]
        See: :py:attr:`.kernel_paths`
    times: str or [str]
        See: :py:attr:`.times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`.intervals`
    time_step: int
        See: :py:attr:`.time_step`
    time_step_units: str
        See: :py:attr:`.time_step_units`
    time_system: str
        See: :py:attr:`.time_system`
    time_format: str
        See: :py:attr:`.time_format`
    target: str or int
        See: :py:attr:`.target`
    target_frame: str or int
        See: :py:attr:`.target_frame`
    observer: str or int
        See: :py:attr:`.observer`
    latitude: str or int
        See: :py:attr:`.latitude`
    longitude: str or int
        See: :py:attr:`.longitude`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`.target`, :py:attr:`.target_frame`, :py:attr:`.observer`,
        :py:attr:`.latitude` and :py:attr:`.longitude` are not provided.
    CalculationInvalidAttr
        If :py:attr:`.shape_1` is not ``ELLIPSOID`` or ``DSK``.

    '''

    def __init__(self, shape_1='ELLIPSOID', coordinate_representation='LATITUDINAL',
                 aberration_correction='CN', **kwargs):

        self._required(['target', 'target_frame', 'observer',
                       'latitude', 'longitude'], kwargs)

        kwargs['calculation_type'] = 'ILLUMINATION_ANGLES'
        kwargs['coordinate_representation'] = coordinate_representation
        kwargs['aberration_correction'] = aberration_correction

        if shape_1 in ['ELLIPSOID', 'DSK']:
            kwargs['shape_1'] = shape_1
        else:
            raise CalculationInvalidAttr('shape_1', shape_1, ['ELLIPSOID', 'DSK'])

        super().__init__(**kwargs)


class SubSolarPoint(Calculation):
    '''Sub-solar point calculation.

    Calculates the sub-solar point on a target as seen from an observer.

    Parameters
    ----------
    sub_point_type: str, optional
        See: :py:attr:`sub_point_type`
    aberration_correction: str, optional
        See: :py:attr:`.aberration_correction`
    state_representation: str, optional
        See: :py:attr:`state_representation`

        Warning
        -------
        Attribute :py:attr:`.aberration_correction` must be ``NONE``, `LT``, ``LT+S``,
        ``CN`` or ``CN+S``.

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`.kernels`
    kernel_paths: str, [str]
        See: :py:attr:`.kernel_paths`
    times: str or [str]
        See: :py:attr:`.times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`.intervals`
    time_step: int
        See: :py:attr:`.time_step`
    time_step_units: str
        See: :py:attr:`.time_step_units`
    time_system: str
        See: :py:attr:`.time_system`
    time_format: str
        See: :py:attr:`.time_format`
    target: str or int
        See: :py:attr:`.target`
    target_frame: str or int
        See: :py:attr:`.target_frame`
    observer: str or int
        See: :py:attr:`.observer`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`.target`, :py:attr:`.target_frame` and :py:attr:`.observer`
        are not provided.
    CalculationInvalidAttr
        If :py:attr:`.aberration_correction` is in ``XLT``, ``XLT+S``,
        ``XCN+S`` or ``XCN+S``.

    '''

    def __init__(self, sub_point_type='Near point: ellipsoid', aberration_correction='CN',
                 state_representation='RECTANGULAR', **kwargs):

        self._required(['target', 'target_frame', 'observer'], kwargs)

        aberration_correction_allowed = list(filter(
            lambda x: 'X' not in x, ABERRATION_CORRECTION))

        if aberration_correction not in aberration_correction_allowed:
            raise CalculationInvalidAttr(
                'aberration_correction', aberration_correction,
                aberration_correction_allowed)

        kwargs['calculation_type'] = 'SUB_SOLAR_POINT'
        kwargs['sub_point_type'] = sub_point_type
        kwargs['aberration_correction'] = aberration_correction
        kwargs['state_representation'] = state_representation

        super().__init__(**kwargs)

class SubObserverPoint(Calculation):
    '''Sub-observer point calculation.

    Calculate the sub-observer point on a target as seen from an observer.

    Parameters
    ----------
    sub_point_type: str, optional
        See: :py:attr:`sub_point_type`
    aberration_correction: str, optional
        See: :py:attr:`.aberration_correction`
    state_representation: str, optional
        See: :py:attr:`state_representation`

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`.kernels`
    kernel_paths: str, [str]
        See: :py:attr:`.kernel_paths`
    times: str or [str]
        See: :py:attr:`.times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`.intervals`
    time_step: int
        See: :py:attr:`.time_step`
    time_step_units: str
        See: :py:attr:`.time_step_units`
    time_system: str
        See: :py:attr:`.time_system`
    time_format: str
        See: :py:attr:`.time_format`
    target: str or int
        See: :py:attr:`.target`
    target_frame: str or int
        See: :py:attr:`.target_frame`
    observer: str or int
        See: :py:attr:`.observer`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`.target`, :py:attr:`.target_frame`
        and :py:attr:`.observer` are not provided.

    '''

    def __init__(self, sub_point_type='Near point: ellipsoid', aberration_correction='CN',
                 state_representation='RECTANGULAR', **kwargs):

        self._required(['target', 'target_frame', 'observer'], kwargs)

        kwargs['calculation_type'] = 'SUB_OBSERVER_POINT'
        kwargs['sub_point_type'] = sub_point_type
        kwargs['aberration_correction'] = aberration_correction
        kwargs['state_representation'] = state_representation

        super().__init__(**kwargs)


class SurfaceInterceptPoint(Calculation):
    '''Surface intercept point calculation.

    Calculate the intercept point of a vector or vectors
    on a target as seen from an observer.

    Parameters
    ----------
    shape_1: str, optional
        See: :py:attr:`shape_1`
    intercept_vector_type: str, optional
        See: :py:attr:`intercept_vector_type`
    aberration_correction: str, optional
        See: :py:attr:`.aberration_correction`
    state_representation: str, optional
        See: :py:attr:`state_representation`

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`.kernels`
    kernel_paths: str, [str]
        See: :py:attr:`.kernel_paths`
    times: str or [str]
        See: :py:attr:`.times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`.intervals`
    time_step: int
        See: :py:attr:`.time_step`
    time_step_units: str
        See: :py:attr:`.time_step_units`
    time_system: str
        See: :py:attr:`.time_system`
    time_format: str
        See: :py:attr:`.time_format`
    target: str or int
        See: :py:attr:`.target`
    target_frame: str or int
        See: :py:attr:`.target_frame`
    observer: str or int
        See: :py:attr:`.observer`
    intercept_instrument: str or int
        See: :py:attr:`intercept_instrument`
    intercept_frame: str
        See: :py:attr:`intercept_frame`
    intercept_frame_axis: str
        See: :py:attr:`intercept_frame_axis`
    intercept_vector_x: float
        See: :py:attr:`intercept_vector_x`
    intercept_vector_y: float
        See: :py:attr:`intercept_vector_y`
    intercept_vector_z: float
        See: :py:attr:`intercept_vector_z`
    intercept_vector_ra: float
        See: :py:attr:`intercept_vector_ra`
    intercept_vector_dec: float
        See: :py:attr:`intercept_vector_dec`

        Warnings
        --------
        Attributes :py:attr:`.intercept_instrument` is needed only if
        :py:attr:`intercept_vector_type` is ``INSTRUMENT_BORESIGHT``,
        ``INSTRUMENT_FOV_BOUNDARY_VECTORS`` or ``VECTOR_IN_INSTRUMENT_FOV``.

        Attributes :py:attr:`.intercept_frame` is needed only if
        :py:attr:`intercept_vector_type` is ``REFERENCE_FRAME_AXIS`` or
        ``VECTOR_IN_REFERENCE_FRAME``.

        Attributes :py:attr:`.intercept_vector_x` + :py:attr:`.intercept_vector_y` +
        :py:attr:`.intercept_vector_z` or :py:attr:`.intercept_vector_ra` +
        :py:attr:`.intercept_vector_dec` is needed only if
        :py:attr:`intercept_vector_type` is ``VECTOR_IN_INSTRUMENT_FOV`` or
        ``VECTOR_IN_REFERENCE_FRAME``.

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`.target`, :py:attr:`.target_frame`
        and :py:attr:`.observer` are not provided.
    CalculationInvalidAttr
        If :py:attr:`.shape_1` is not ``ELLIPSOID`` or ``DSK``.

    '''

    def __init__(self, shape_1='ELLIPSOID', intercept_vector_type='INSTRUMENT_BORESIGHT',
                 aberration_correction='CN', state_representation='RECTANGULAR',
                 **kwargs):

        self._required(['target', 'target_frame', 'observer'], kwargs)

        kwargs['calculation_type'] = 'SURFACE_INTERCEPT_POINT'
        kwargs['intercept_vector_type'] = intercept_vector_type
        kwargs['aberration_correction'] = aberration_correction
        kwargs['state_representation'] = state_representation

        if shape_1 in ['ELLIPSOID', 'DSK']:
            kwargs['shape_1'] = shape_1
        else:
            raise CalculationInvalidAttr('shape_1', shape_1, ['ELLIPSOID', 'DSK'])

        super().__init__(**kwargs)

class OsculatingElements(Calculation):
    '''Osculating elements calculation.

    Calculate the osculating elements of the orbit of a target body around a central body.

    The orbit may be elliptical, parabolic, or hyperbolic.

    Parameters
    ----------
    reference_frame: str, optional
        See: :py:attr:`reference_frame`

    Other Parameters
    ----------------
    kernels: str, int, [str or/and int]
        See: :py:attr:`.kernels`
    kernel_paths: str, [str]
        See: :py:attr:`.kernel_paths`
    times: str or [str]
        See: :py:attr:`.times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`.intervals`
    time_step: int
        See: :py:attr:`.time_step`
    time_step_units: str
        See: :py:attr:`.time_step_units`
    time_system: str
        See: :py:attr:`.time_system`
    time_format: str
        See: :py:attr:`.time_format`
    orbiting_body: str or int
        See: :py:attr:`.orbiting_body`
    center_body: str or int
        See: :py:attr:`.center_body`

    Raises
    ------
    CalculationRequiredAttr
        If :py:attr:`.orbiting_body` and :py:attr:`.center_body` are not provided.

    '''

    def __init__(self, reference_frame='J2000', **kwargs):

        self._required(['orbiting_body', 'center_body'], kwargs)

        kwargs['calculation_type'] = 'OSCULATING_ELEMENTS'
        kwargs['reference_frame'] = reference_frame

        super().__init__(**kwargs)

class TimeConversion(Calculation):
    '''Time conversion calculation.

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
        See: :py:attr:`.kernels`
    kernel_paths: str, [str]
        See: :py:attr:`.kernel_paths`
    times: str or [str]
        See: :py:attr:`.times`
    intervals: [str, str] or {'startTime': str, 'endTime': str} or [interval, ...]
        See: :py:attr:`.intervals`
    time_step: int
        See: :py:attr:`.time_step`
    time_step_units: str
        See: :py:attr:`.time_step_units`
    time_system: str
        See: :py:attr:`.time_system`
    time_format: str
        See: :py:attr:`.time_format`
    output_sclk_id: str
        See: :py:attr:`output_sclk_id`
    output_time_custom_format: str
        See: :py:attr:`output_time_custom_format`

        Warnings
        --------
        Attributes :py:attr:`.output_sclk_id` is needed only if
        :py:attr:`output_time_system` is ``SPACECRAFT_CLOCK``.

        Attributes :py:attr:`.output_time_custom_format` is needed only if
        :py:attr:`output_time_format` is ``CUSTOM``.

    '''

    def __init__(self, output_time_system='UTC', output_time_format='CALENDAR', **kwargs):

        kwargs['calculation_type'] = 'TIME_CONVERSION'
        kwargs['output_time_system'] = output_time_system
        kwargs['output_time_format'] = output_time_format

        super().__init__(**kwargs)
