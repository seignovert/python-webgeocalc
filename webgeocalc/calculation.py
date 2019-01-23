# -*- coding: utf-8 -*-
from .api import API
from .errors import CalculationRequiredAttr, CalculationInvalidAttr, CalculationUndefinedAttr, \
                    CalculationIncompatibleAttr, CalculationConflictAttr, CalculationAlreadySubmitted, \
                    CalculationNotCompleted
from .types import KernelSetDetails
from .vars import CALCULATION_TYPE, TIME_SYSTEM, TIME_FORMAT, TIME_STEP_UNITS, \
                  INTERVALS, ABERRATION_CORRECTION, STATE_REPRESENTATION


class SetterProperty(object):
    def __init__(self, func, doc=None):
        self.func = func
        self.__doc__ = doc if doc is not None else func.__doc__

    def __set__(self, obj, value):
        return self.func(obj, value)


class Calculation(object):
    '''Calculation class'''

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
        for required in ['calculation_type', 'time_system', 'time_format']:
            if required not in kwargs.keys():
                raise CalculationRequiredAttr(required)

        if 'kernels' not in kwargs.keys() and 'kernel_paths' not in kwargs.keys():
            raise CalculationRequiredAttr('kernels\' or \'kernel_paths')

        if 'times' not in kwargs.keys() and 'intervals' not in kwargs.keys():
            raise CalculationRequiredAttr('times\' or \'intervals')

        # Check and set parameters
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return '\n'.join(
            [f"<{self.__class__.__name__}> Status: {self.status} (id: {self.id})"] +
            [f' - {k.capitalize()}: {v}' for k, v in self.payload.items()]
        )

    @property
    def payload(self):
        '''Calculation payload parameters'''
        return {k.split('__')[-1]: v for k, v in vars(self).items() if k.startswith('_')}

    def submit(self):
        '''Submit calculation parameters and get calculation id, phase and progress'''
        if not self.id is None:
            raise CalculationAlreadySubmitted(self.id)

        self.id, self.status, self.progress = API.new_calculation(self.payload)

        if self.verbose:
            print(f'[Calculation submitted] Status: {self.status} (id: {self.id})')

    def resubmit(self):
        '''Re-submit calculation'''
        self.id = None
        self.submit()

    def update(self):
        '''Update calculation status phase and progress'''
        if self.id is None:
            self.submit()
        else:
            _, self.status, self.progress = API.status_calculation(self.id)
            
            if self.verbose:
                print(f'[Calculation update] Status: {self.status} (id: {self.id})')

    def run(self):
        '''Run calculation'''
        if not self.columns is None and not self.values is None:
            return self.results
        else:
            self.update()

        if self.status == 'COMPLETE':
            return self.results

    @property
    def results(self):
        '''Gets the results of a calculation.'''
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

    @SetterProperty
    def calculation_type(self, val):
        '''
        The type of calculation to perform. One of the following:
            - STATE_VECTOR
            - ANGULAR_SEPARATION
            - ANGULAR_SIZE
            - SUB_OBSERVER_POINT
            - SUB_SOLAR_POINT
            - ILLUMINATION_ANGLES
            - SURFACE_INTERCEPT_POINT
            - OSCULATING_ELEMENTS
            - FRAME_TRANSFORMATION
            - GF_COORDINATE_SEARCH
            - GF_ANGULAR_SEPARATION_SEARCH
            - GF_DISTANCE_SEARCH
            - GF_SUB_POINT_SEARCH
            - GF_OCCULTATION_SEARCH
            - GF_TARGET_IN_INSTRUMENT_FOV_SEARCH
            - GF_SURFACE_INTERCEPT_POINT_SEARCH
            - GF_RAY_IN_FOV_SEARCH
            - TIME_CONVERSION 
        '''
        if val in CALCULATION_TYPE:
            self.__calculationType = val
        else:
            raise CalculationInvalidAttr('calculation_type', val, CALCULATION_TYPE)

    @SetterProperty
    def kernels(self, kernel_sets):
        '''Load one or more kernels at once'''
        self.__kernels += [self.kernel_id_obj(kernel_sets)] if isinstance(kernel_sets, (int, str, KernelSetDetails)) else \
                          list(map(self.kernel_id_obj, kernel_sets))

    @staticmethod
    def kernel_id_obj(kernel_set):
        '''Kernel set object'''
        return {"type": "KERNEL_SET", "id": API.kernel_set_id(kernel_set)}

    @SetterProperty
    def kernel_paths(self, paths):
        '''Add server path for individual kernel'''
        self.__kernels += [self.kernel_path_obj(paths)] if isinstance(paths, str) else list(map(self.kernel_path_obj, paths))

    @staticmethod
    def kernel_path_obj(server_path):
        '''Individual kernel path object'''
        return {"type": "KERNEL", "path": server_path}

    @SetterProperty
    def time_system(self, val):
        '''
        Time System. One of the following:
            - UTC
            - TDB
            - TDT
            - SPACECRAFT_CLOCK 

        If SPACECRAFT_CLOCK is selected, then sclkId must also be provided.
        '''
        if val in TIME_SYSTEM:
            self.__timeSystem = val
        else:
            raise CalculationInvalidAttr('time_system', val, TIME_SYSTEM)
        
        if val == 'SPACECRAFT_CLOCK' and 'sclk_id' not in self.params.keys():
            raise CalculationUndefinedAttr('time_system', 'SPACECRAFT_CLOCK', 'sclk_id')

    @SetterProperty
    def time_format(self, val):
        '''
        Time Format. One of the following:
            - CALENDAR
            - JULIAN
            - SECONDS_PAST_J2000
            - SPACECRAFT_CLOCK_TICKS
            - SPACECRAFT_CLOCK_STRING 

        CALENDAR, JULIAN, and SECONDS_PAST_J2000 are applicable only when timeSystem is UTC, TDB, or TDT.
        SPACECRAFT_CLOCK_STRING and SPACECRAFT_CLOCK_TICKS are applicable only when timeSystem is SPACECRAFT_CLOCK. 
        '''
        if val in TIME_FORMAT:
            self.__timeFormat = val
        else:
            raise CalculationInvalidAttr('time_format', val, TIME_FORMAT)
        
        if val in ['CALENDAR', 'JULIAN', 'SECONDS_PAST_J2000'] and self.params['time_system'] not in ['UTC', 'TDB', 'TDT']:
            raise CalculationIncompatibleAttr('time_format', val, 'time_system', self.params['time_system'], ['UTC', 'TDB', 'TDT'])
        if val in ['SPACECRAFT_CLOCK_STRING', 'SPACECRAFT_CLOCK_TICKS'] and self.params['time_system'] != 'SPACECRAFT_CLOCK':
            raise CalculationIncompatibleAttr('time_format', val, 'time_system', self.params['time_system'], ['SPACECRAFT_CLOCK'])

    @SetterProperty
    def sclk_id(self, val):
        '''
        Spacecraft clock kernel id

        Only used if timeSystem is SPACECRAFT_CLOCK.
        '''
        self.__sclkId = int(val)

        if self.params['time_system'] != 'SPACECRAFT_CLOCK':
            raise CalculationIncompatibleAttr('sclk_id', val, 'time_system', self.params['time_system'], ['SPACECRAFT_CLOCK'])

    @SetterProperty
    def times(self, times):
        '''
        An array of strings representing the time points that should be used in the calculation
        
        Either this parameter or the intervals parameter must be supplied. 
        '''
        self.__times = [times] if isinstance(times, str) else times

        if 'intervals' in self.params.keys():
            raise CalculationConflictAttr('times', 'intervals')

    @SetterProperty
    def intervals(self, intervals):
        '''
        An array of objects with startTime and endTime parameters, representing the time intervals used for the calculation.
        
        Either this parameter or the times parameter must be supplied. If this parameter is used, timeStep must also be supplied.
        '''
        if isinstance(intervals, dict):
            self.__intervals = [self.interval(intervals)]
        elif isinstance(intervals, list) and len(intervals) > 2:
            self.__intervals = list(map(self.interval, intervals))
        elif isinstance(intervals, list) and len(intervals) == 2:
            if isinstance(intervals[0], str) and isinstance(intervals[1], str):
                self.__intervals = [self.interval(intervals)]
            elif isinstance(intervals[0], (dict, list)) and isinstance(intervals[1], (dict, list)):
                self.__intervals = [self.interval(intervals[0]), self.interval(intervals[1])]
            else:
                raise CalculationInvalidAttr('intervals', intervals, INTERVALS)
        elif isinstance(intervals, list) and len(intervals) == 1:
            if isinstance(intervals[0], (dict, list)):
                self.__intervals = [self.interval(intervals[0])]
            else:
                raise CalculationInvalidAttr('intervals', intervals, INTERVALS)
        else:
            raise CalculationInvalidAttr('intervals', intervals, INTERVALS)

        if 'time_step' not in self.params.keys():
            raise CalculationUndefinedAttr('intervals', intervals, 'time_step')

    @staticmethod
    def interval(interval):
        '''Interval object'''
        if not len(interval) == 2:
            raise CalculationInvalidAttr('interval', interval, INTERVALS[:2])
        
        if isinstance(interval, dict):
            if 'startTime' in interval.keys() and 'endTime' in interval.keys():
                return interval
            else:
                raise CalculationInvalidAttr('interval', interval, INTERVALS[:2])
        else:
            return {"startTime": str(interval[0]), "endTime": str(interval[1])}

    @SetterProperty
    def time_step(self, val):
        '''
        The time step/number of steps parameter used for time series or geometry finder calculations.
        This parameter is not used for time series calculations if the times parameter is supplied.
        '''
        self.__timeStep = int(val)

        if 'times' in self.params.keys():
            raise CalculationConflictAttr('time_step', 'times')
        if 'time_step_units' not in self.params.keys():
            raise CalculationUndefinedAttr('time_step', val, 'time_step_units')

    @SetterProperty
    def time_step_units(self, val):
        '''
        Time step units, One of the following:
            - SECONDS
            - MINUTES
            - HOURS
            - DAYS
            - EQUAL_INTERVALS 

        Only used if timeStep is supplied. 
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
    def target(self, val):
        '''
        The target body name or ID from API.bodies(kernel_set).
        '''
        self.__target = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def observer(self, val):
        '''
        The observing body name or ID from API.bodies(kernel_set).
        '''
        self.__observer = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def reference_frame(self, val):
        '''
        The reference frame name or ID from API.frames(kernel_set).
        '''
        self.__referenceFrame = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def aberration_correction(self, val):
        '''
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
        '''
        if val in ABERRATION_CORRECTION:
            self.__aberrationCorrection = val
        else:
            raise CalculationInvalidAttr('aberration_correction', val, ABERRATION_CORRECTION)

    @SetterProperty
    def state_representation(self, val):
        '''
        State representation. One of:
            - RECTANGULAR
            - RA_DEC
            - LATITUDINAL (planetocentric)
            - PLANETODETIC
            - PLANETOGRAPHIC
            - CYLINDRICAL
            - SPHERICAL 
        '''
        if val in STATE_REPRESENTATION:
            self.__stateRepresentation = val
        else:
            raise CalculationInvalidAttr('state_representation', val, STATE_REPRESENTATION)


class StateVector(Calculation):
    '''Calculates the position of one body relative to another, calculated in a desired reference frame.'''

    def __init__(self, aberration_correction='CN', state_representation='RECTANGULAR', **kwargs):

        for required in ['target', 'observer', 'reference_frame']:
            if required not in kwargs.keys():
                raise CalculationRequiredAttr(required)
        
        kwargs['calculation_type'] = 'STATE_VECTOR'
        kwargs['aberration_correction'] = aberration_correction
        kwargs['state_representation'] = state_representation

        super().__init__(**kwargs)
