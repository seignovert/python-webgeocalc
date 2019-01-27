# -*- coding: utf-8 -*-
import time

from .api import API
from .errors import CalculationRequiredAttr, CalculationInvalidAttr, CalculationUndefinedAttr, \
                    CalculationIncompatibleAttr, CalculationConflictAttr, CalculationAlreadySubmitted, \
                    CalculationNotCompleted, CalculationInvalidValue, CalculationTimeOut
from .types import KernelSetDetails
from .vars import CALCULATION_TYPE, TIME_SYSTEM, TIME_FORMAT, TIME_STEP_UNITS, \
                  INTERVALS, ABERRATION_CORRECTION, STATE_REPRESENTATION, SHAPE, TIME_LOCATION, \
                  ORIENTATION_REPRESENTATION, ANGULAR_VELOCITY_REPRESENTATION, AXIS, ANGULAR_UNITS, ANGULAR_VELOCITY_UNITS, \
                  COORDINATE_REPRESENTATION, SUB_POINT_TYPE, INTERCEPT_VECTOR_TYPE, OUTPUT_TIME_FORMAT


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
        self.required(['calculation_type', 'time_system', 'time_format'], kwargs)

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
            [f' - {k}: {v}' for k, v in self.payload.items()]
        )

    @staticmethod
    def required(attrs, kwargs):
        for required in attrs:
            if required not in kwargs.keys():
                raise CalculationRequiredAttr(required)

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
            print(f'[Calculation submit] Status: {self.status} (id: {self.id})')

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

    def run(self, timeout=30, sleep=1):
        '''
        Run calculation: submit and update calculation status to get the results.
        Sleep time is 1 second between each update.
        Timeout is send after 30 secondes.
        '''
        if not self.columns is None and not self.values is None:
            return self.results

        for i in range(int(timeout/sleep)):
            self.update()
            
            if self.status == 'COMPLETE':
                return self.results
            else:
                time.sleep(sleep)
        else:
            raise CalculationTimeOut(timeout, sleep)

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
    def output_time_system(self, val):
        '''
        The time system for the result times.
            - TDB
            - TDT
            - UTC
            - SPACECRAFT_CLOCK

        If SPACECRAFT_CLOCK is selected, then sclkId must also be provided.
        '''
        if val in TIME_SYSTEM:
            self.__outputTimeSystem = val
        else:
            raise CalculationInvalidAttr('output_time_system', val, TIME_SYSTEM)
        
        if val == 'SPACECRAFT_CLOCK' and 'output_sclk_id' not in self.params.keys():
            raise CalculationUndefinedAttr('output_time_system', 'SPACECRAFT_CLOCK', 'output_sclk_id')

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
        
        self.required(['time_system'], self.params)

        if val in ['CALENDAR', 'JULIAN', 'SECONDS_PAST_J2000'] and self.params['time_system'] not in ['UTC', 'TDB', 'TDT']:
            raise CalculationIncompatibleAttr('time_format', val, 'time_system', self.params['time_system'], ['UTC', 'TDB', 'TDT'])
        if val in ['SPACECRAFT_CLOCK_STRING', 'SPACECRAFT_CLOCK_TICKS'] and self.params['time_system'] != 'SPACECRAFT_CLOCK':
            raise CalculationIncompatibleAttr('time_format', val, 'time_system', self.params['time_system'], ['SPACECRAFT_CLOCK'])
    
    @SetterProperty
    def output_time_format(self, val):
        '''
        The time format for the result times:
            - CALENDAR
            - CALENDAR_YMD
            - CALENDAR_DOY
            - JULIAN
            - SECONDS_PAST_J2000
            - SPACECRAFT_CLOCK_STRING
            - SPACECRAFT_CLOCK_TICKS
            - CUSTOM

        CALENDAR_YMD, CALENDAR_DOY, JULIAN, SECONDS_PAST_J2000, and CUSTOM are applicable only when outputTimeSystem is TDB, TDT, or UTC.

        SPACECRAFT_CLOCK_STRING and SPACECRAFT_CLOCK_TICKS are applicable only when outputTimeSystem is SPACECRAFT_CLOCK.

        If CUSTOM is selected, then outputTimeCustomFormat must also be provided. 
        '''
        if val in OUTPUT_TIME_FORMAT:
            self.__outputTimeFormat = val
        else:
            raise CalculationInvalidAttr('output_time_format', val, OUTPUT_TIME_FORMAT)
        
        self.required(['output_time_system'], self.params)

        if val in ['CALENDAR', 'CALENDAR_YMD', 'CALENDAR_DOY', 'JULIAN', 'SECONDS_PAST_J2000', 'CUSTOM'] and \
            self.params['output_time_system'] not in ['UTC', 'TDB', 'TDT']:
            raise CalculationIncompatibleAttr('output_time_format', val, 'output_time_system', self.params['output_time_system'], ['UTC', 'TDB', 'TDT'])
        if val in ['SPACECRAFT_CLOCK_STRING', 'SPACECRAFT_CLOCK_TICKS'] and self.params['output_time_system'] != 'SPACECRAFT_CLOCK':
            raise CalculationIncompatibleAttr('output_time_format', val, 'output_time_system', self.params['output_time_system'], ['SPACECRAFT_CLOCK'])

    @SetterProperty
    def sclk_id(self, val):
        '''
        Spacecraft clock kernel id

        Only used if `time_system` is `SPACECRAFT_CLOCK`.
        '''
        self.__sclkId = int(val)

        self.required(['time_system'], self.params)

        if self.params['time_system'] != 'SPACECRAFT_CLOCK':
            raise CalculationIncompatibleAttr('sclk_id', val, 'time_system', self.params['time_system'], ['SPACECRAFT_CLOCK'])

    @SetterProperty
    def output_sclk_id(self, val):
        '''
        The output SCLK ID.

        Only used if `output_time_system` is `SPACECRAFT_CLOCK`.
        '''
        self.__outputSclkId = int(val)

        self.required(['output_time_system'], self.params)

        if self.params['output_time_system'] != 'SPACECRAFT_CLOCK':
            raise CalculationIncompatibleAttr('output_sclk_id', val, 'output_time_system', self.params['output_time_system'], ['SPACECRAFT_CLOCK'])

    @SetterProperty
    def output_time_custom_format(self, val):
        '''
        A SPICE timout() format string.
        
        Only used if outputTimeFormat is CUSTOM.
        '''
        self.__outputTimeCustomFormat = val

        self.required(['output_time_format'], self.params)

        if self.params['output_time_format'] != 'CUSTOM':
            raise CalculationIncompatibleAttr('output_time_custom_format', val, 'output_time_format', self.params['output_time_format'], ['CUSTOM'])

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
    def target_frame(self, val):
        '''
        The target body-fixed reference frame name.
        '''
        self.__targetFrame = val

    @SetterProperty
    def target_1(self, val):
        '''
        The target body name or ID of the first body.
        '''
        self.__target1 = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def shape_1(self, val):
        '''
        The shape to use for the first body. One of:
            - POINT
            - SPHERE
        '''
        if val in SHAPE:
            self.__shape1 = val
        else:
            raise CalculationInvalidAttr('shape_1', val, SHAPE)

    @SetterProperty
    def target_2(self, val):
        '''
        The target body name or ID of the second body.
        '''
        self.__target2 = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def shape_2(self, val):
        '''
        The shape to use for the second body. One of:
            - POINT
            - SPHERE
        '''
        if val in SHAPE:
            self.__shape2 = val
        else:
            raise CalculationInvalidAttr('shape_2', val, SHAPE)

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
    def frame_1(self, val):
        '''
        The first reference frame name.        
        '''
        self.__frame1 = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def frame_2(self, val):
        '''
        The second reference frame name.        
        '''
        self.__frame2 = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def orbiting_body(self, val):
        '''
        The SPICE body name or ID for the orbiting body.
        '''
        self.__orbitingBody = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def center_body(self, val):
        '''
        The SPICE body name or ID for the body that is the center of motion.
        '''
        self.__centerBody = val if isinstance(val, int) else val.upper()

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

    @SetterProperty
    def time_location(self, val):
        '''
        The frame for the input times. On of:
            - FRAME1
            - FRAME2
        
        (API doc: "Only needed if aberrationCorrection is not NONE"
        => WRONG: required even for aberrationCorrection = NONE.
        '''
        if val in TIME_LOCATION:
            self.__timeLocation = val
        else:
            raise CalculationInvalidAttr('time_location', val, TIME_LOCATION)

    @SetterProperty
    def orientation_representation(self, val):
        '''
        The representation of the result transformation. One of:
            - EULER_ANGLES
            - ANGLE_AND_AXIS
            - SPICE_QUATERNION
            - OTHER_QUATERNION
            - MATRIX_ROW_BY_ROW
            - MATRIX_FLAGGED
            - MATRIX_ALL_ONE_ROW
        '''
        if val in ORIENTATION_REPRESENTATION:
            self.__orientationRepresentation = val
        else:
            raise CalculationInvalidAttr('orientation_representation', val, ORIENTATION_REPRESENTATION)

    @SetterProperty
    def axis_1(self, val):
        '''
        The first axis for Euler angle rotation.
        '''
        self.__axis1 = self.axis('axis_1', val)

    @SetterProperty
    def axis_2(self, val):
        '''
        The second axis for Euler angle rotation.
        '''
        self.__axis2 = self.axis('axis_2', val)

    @SetterProperty
    def axis_3(self, val):
        '''
        The third axis for Euler angle rotation.
        '''
        self.__axis3 = self.axis('axis_3', val)
    
    def axis(self, name, val):
        '''
        Axis for Euler angle rotation. One of:
            - X
            - Y
            - Z

        Note: Only needed if `orientation_representation` is `EULER_ANGLES`.
        '''
        if 'orientation_representation' not in self.params.keys():
            raise CalculationUndefinedAttr(name, val, 'orientation_representation')

        if self.params['orientation_representation'] != 'EULER_ANGLES':
            raise CalculationIncompatibleAttr(name, val, 'orientation_representation', self.params['orientation_representation'], ['EULER_ANGLES'])

        if val in AXIS:
            return val
        else:
            raise CalculationInvalidAttr(name, val, AXIS)

    @SetterProperty
    def angular_units(self, val):
        '''
        The angular units used for the angle of rotation. One of:
            - deg
            - rad 

        Note: Only needed if `orientation_representation` is `EULER_ANGLES` or `ANGLE_AND_AXIS`.
        '''
        if val in ANGULAR_UNITS:
            self.__angularUnits = val
        else:
            raise CalculationInvalidAttr('angular_units', val, ANGULAR_UNITS)

        if 'orientation_representation' not in self.params.keys():
            raise CalculationUndefinedAttr('angular_units', val, 'orientation_representation')

        if not self.params['orientation_representation'] in ['EULER_ANGLES', 'ANGLE_AND_AXIS']:
            raise CalculationIncompatibleAttr('angular_units', val, 'orientation_representation', \
                                              self.params['orientation_representation'], ['EULER_ANGLES', 'ANGLE_AND_AXIS'])

    @SetterProperty
    def angular_velocity_representation(self, val):
        '''
        The representation of angular velocity in the output. One of:
            - NOT_INCLUDED
            - VECTOR_IN_FRAME1
            - VECTOR_IN_FRAME2
            - EULER_ANGLE_DERIVATIVES
            - MATRIX 
        '''
        if val in ANGULAR_VELOCITY_REPRESENTATION:
            self.__angularVelocityRepresentation = val
        else:
            raise CalculationInvalidAttr('angular_velocity_representation', val, ANGULAR_VELOCITY_REPRESENTATION)

    @SetterProperty
    def angular_velocity_units(self, val):
        '''
        The units for the angular velocity. One of:
            - deg/s
            - rad/s
            - RPM
            - Unitary

        Note: Only needed if `angular_velocity_representation` is one of:
            - VECTOR_IN_FRAME1
            - VECTOR_IN_FRAME2
            - EULER_ANGLE_DERIVATIVES

        Note 2: `Unitary` = Unit vector, only applicable for `VECTOR_IN_FRAME1` and `VECTOR_IN_FRAME2`.
        '''
        if val in ANGULAR_VELOCITY_UNITS:
            self.__angularVelocityUnits = val
        else:
            raise CalculationInvalidAttr('angular_velocity_units', val, ANGULAR_VELOCITY_UNITS)

        if 'angular_velocity_representation' not in self.params.keys():
            raise CalculationUndefinedAttr('angular_velocity_units', val, 'angular_velocity_representation')

        CHOICES = ['VECTOR_IN_FRAME1', 'VECTOR_IN_FRAME2', 'EULER_ANGLE_DERIVATIVES']
        if not self.params['angular_velocity_representation'] in CHOICES:
            raise CalculationIncompatibleAttr('angular_velocity_units', val, 'angular_velocity_representation',
                                              self.params['angular_velocity_representation'], CHOICES)
        
        if val == 'Unitary' and not self.params['angular_velocity_representation'] in ['VECTOR_IN_FRAME1', 'VECTOR_IN_FRAME2']:
            raise CalculationIncompatibleAttr('angular_velocity_units', val, 'angular_velocity_representation',
                                              self.params['angular_velocity_representation'], ['VECTOR_IN_FRAME1', 'VECTOR_IN_FRAME2'])

    @SetterProperty
    def coordinate_representation(self, val):
        '''
        Coordinate Representation. One of:
            - LATITUDINAL (planetocentric)
            - PLANETODETIC
            - PLANETOGRAPHIC
        '''
        if val in COORDINATE_REPRESENTATION:
            self.__coordinateRepresentation = val
        else:
            raise CalculationInvalidAttr('coordinate_representation', val, COORDINATE_REPRESENTATION)

    @SetterProperty
    def latitude(self, val):
        '''
        Latitude of the surface point, in degrees, from -90 to +90.
        '''
        if val >= -90 and val <= 90:
            self.__latitude = val
        else:
            raise CalculationInvalidValue('latitude', val, -90, 90)

    @SetterProperty
    def longitude(self, val):
        '''
        Longitude of the surface point, in degrees, from -180 to +180.
        '''
        if val >= -180 and val <= 180:
            self.__longitude = val
        else:
            raise CalculationInvalidValue('longitude', val, -180, 180)

    @SetterProperty
    def sub_point_type(self, val):
        '''
        The method of finding the sub-observer point, as in the SPICE subpnt() API call. One of:
            - Near point: ellipsoid
            - Intercept: ellipsoid
            - NADIR/DSK/UNPRIORITIZED
            - INTERCEPT/DSK/UNPRIORITIZED
        '''
        if val in SUB_POINT_TYPE:
            self.__subPointType = val
        else:
            raise CalculationInvalidAttr('sub_point_type', val, SUB_POINT_TYPE)

    @SetterProperty
    def intercept_vector_type(self, val):
        '''
        Type of vector to be used as the ray direction. One of:
            - INSTRUMENT_BORESIGHT (the instrument boresight vector)
            - INSTRUMENT_FOV_BOUNDARY_VECTORS (the instrument field-of-view boundary vectors)
            - REFERENCE_FRAME_AXIS (an axis of the specified reference frame)
            - VECTOR_IN_INSTRUMENT_FOV (a vector in the reference frame of the specified instrument)
            - VECTOR_IN_REFERENCE_FRAME (a vector in the specified reference frame)
        '''
        if val in INTERCEPT_VECTOR_TYPE:
            self.__interceptVectorType = val
        else:
            raise CalculationInvalidAttr('intercept_vector_type', val, INTERCEPT_VECTOR_TYPE)

        if val in ['INSTRUMENT_BORESIGHT', 'INSTRUMENT_FOV_BOUNDARY_VECTORS', 'VECTOR_IN_INSTRUMENT_FOV']:
            self.required(['intercept_instrument'], self.params)
        elif val in ['REFERENCE_FRAME_AXIS', 'VECTOR_IN_REFERENCE_FRAME']:
            self.required(['intercept_frame'], self.params)
            if val == 'REFERENCE_FRAME_AXIS':
                self.required(['intercept_frame_axis'], self.params)

        keys = self.params.keys()
        if val in ['VECTOR_IN_INSTRUMENT_FOV', 'VECTOR_IN_REFERENCE_FRAME']:
            if not('intercept_vector_x' in keys and 'intercept_vector_y' in keys and 'intercept_vector_z' in keys) and \
               not('intercept_vector_ra' in keys and 'intercept_vector_dec' in keys):
                    raise CalculationUndefinedAttr('intercept_vector_type', val, "intercept_vector_x/y/z' or 'intercept_vector_ra/dec")

    @SetterProperty
    def intercept_instrument(self, val):
        '''
        The instrument name or ID.

        Note: Required only if `intercept_vector_type` is:
            - INSTRUMENT_BORESIGHT
            - INSTRUMENT_FOV_BOUNDARY_VECTORS
            - VECTOR_IN_INSTRUMENT_FOV
        '''
        if 'intercept_vector_type' not in self.params.keys():
            raise CalculationUndefinedAttr('intercept_instrument', val, 'intercept_vector_type')

        CHOICES = ['INSTRUMENT_BORESIGHT', 'INSTRUMENT_FOV_BOUNDARY_VECTORS', 'VECTOR_IN_INSTRUMENT_FOV']
        if not self.params['intercept_vector_type'] in CHOICES:
            raise CalculationIncompatibleAttr('intercept_instrument', val, 'intercept_vector_type',
                                              self.params['intercept_vector_type'], CHOICES)

        self.__interceptInstrument = val if isinstance(val, int) else val.upper()

    @SetterProperty
    def intercept_frame(self, val):
        '''
        The vector's reference frame name.

        Note: Required only if `intercept_vector_type` is:
            - REFERENCE_FRAME_AXIS
            - VECTOR_IN_REFERENCE_FRAME
        '''
        if 'intercept_vector_type' not in self.params.keys():
            raise CalculationUndefinedAttr('intercept_frame', val, 'intercept_vector_type')

        CHOICES = ['REFERENCE_FRAME_AXIS', 'VECTOR_IN_REFERENCE_FRAME']
        if not self.params['intercept_vector_type'] in CHOICES:
            raise CalculationIncompatibleAttr('intercept_frame', val, 'intercept_vector_type',
                                              self.params['intercept_vector_type'], CHOICES)

        self.__interceptFrame = val

    @SetterProperty
    def intercept_frame_axis(self, val):
        '''
        The vector's reference frame name.

        Note: Required only if `intercept_vector_type` is:
            - REFERENCE_FRAME_AXIS
        '''
        if 'intercept_vector_type' not in self.params.keys():
            raise CalculationUndefinedAttr('intercept_frame_axis', val, 'intercept_vector_type')

        if self.params['intercept_vector_type'] != 'REFERENCE_FRAME_AXIS':
            raise CalculationIncompatibleAttr('intercept_frame_axis', val, 'intercept_vector_type',
                                              self.params['intercept_vector_type'], ['REFERENCE_FRAME_AXIS'])

        if val in AXIS:
            self.__interceptFrameAxis = val
        else:
            raise CalculationInvalidAttr('intercept_frame_axis', val, AXIS)

    def intercept_vector(self, axis, val):
        '''
        Intercept vector coordinate.
        '''
        if 'intercept_vector_type' not in self.params.keys():
            raise CalculationUndefinedAttr('intercept_vector_' + axis, val, 'intercept_vector_type')

        CHOICES = ['VECTOR_IN_INSTRUMENT_FOV', 'VECTOR_IN_REFERENCE_FRAME']
        if not self.params['intercept_vector_type'] in CHOICES:
            raise CalculationIncompatibleAttr('intercept_vector_' + axis, val, 'intercept_vector_type',
                                              self.params['intercept_vector_type'], CHOICES)        
        return val

    @SetterProperty
    def intercept_vector_x(self, val):
        '''
        The X intercept vector coordinate.
        '''
        self.__interceptVectorX = self.intercept_vector('x', val)

    @SetterProperty
    def intercept_vector_y(self, val):
        '''
        The Y intercept vector coordinate.
        '''
        self.__interceptVectorY = self.intercept_vector('y', val)

    @SetterProperty
    def intercept_vector_z(self, val):
        '''
        The Z intercept vector coordinate.
        '''
        self.__interceptVectorZ = self.intercept_vector('z', val)

    @SetterProperty
    def intercept_vector_ra(self, val):
        '''
        The RA intercept vector coordinate.
        '''
        self.__interceptVectorRA = self.intercept_vector('ra', val)

    @SetterProperty
    def intercept_vector_dec(self, val):
        '''
        The Dec intercept vector coordinate.
        '''
        self.__interceptVectorDec = self.intercept_vector('dec', val)



class StateVector(Calculation):
    '''
    Calculates the position of one body relative to another, calculated in a desired reference frame.
    
    Required parameters:
    --------------------
        - `kernels` | `kernel_paths`
        - `times` | `intervals` + `time_step` + `time_step_units`
        - `target`: The target body name or ID.
        - `observer`: The observing body name or ID.
        - `reference_frame`: The reference frame name.

    Optional parameters (with default):
    ------------------------------------
        - `time_system`: (UTC)
        - `time_format`: (CALENDAR)
        - `aberration_correction`: (CN) [NONE|LT|LT+S|CN|CN+S|XLT|XLT+S|XCN|XCN+S]
        - `state_representation`: (RECTANGULAR) [RECTANGULAR|RA_DEC|LATITUDINAL|PLANETODETIC|PLANETOGRAPHIC|CYLINDRICAL|SPHERICAL]
    '''

    def __init__(self, aberration_correction='CN', state_representation='RECTANGULAR', **kwargs):

        self.required(['target', 'observer', 'reference_frame'], kwargs)
        
        kwargs['calculation_type'] = 'STATE_VECTOR'
        kwargs['aberration_correction'] = aberration_correction
        kwargs['state_representation'] = state_representation

        super().__init__(**kwargs)

class AngularSeparation(Calculation):
    '''
    Calculates the angular separation of two bodies as seen by an observer body.
    
    Required parameters:
    --------------------
        - `kernels` | `kernel_paths`
        - `times` | `intervals` + `time_step` + `time_step_units`
        - `target_1`: The target body name or ID of the first body.
        - `target_2`: The target body name or ID of the second body.
        - `observer`: The observing body name or ID.

    Optional parameters (with default):
    ------------------------------------
        - `time_system`: (UTC)
        - `time_format`: (CALENDAR)
        - `shape_1`: The shape to use for the first body. (POINT) [POINT|SPHERE]
        - `shape_2`: The shape to use for the second body. (POINT) [POINT|SPHERE]
        - `aberration_correction` (CN) [NONE|LT|LT+S|CN|CN+S|XLT|XLT+S|XCN|XCN+S]
    '''

    def __init__(self, shape_1='POINT', shape_2='POINT', aberration_correction='CN', **kwargs):

        self.required(['target_1', 'target_2', 'observer'], kwargs)
        
        kwargs['calculation_type'] = 'ANGULAR_SEPARATION'
        kwargs['shape_1'] = shape_1
        kwargs['shape_2'] = shape_2
        kwargs['aberration_correction'] = aberration_correction

        super().__init__(**kwargs)

class AngularSize(Calculation):
    '''
    Calculates the angular size of a target as seen by an observer.
    
    Required parameters:
    --------------------
        - `kernels` | `kernel_paths`
        - `times` | `intervals` + `time_step` + `time_step_units`
        - `target`: The target body name or ID.
        - `observer`: The observing body name or ID.

    Optional parameters (with default):
    ------------------------------------
        - `time_system`: (UTC)
        - `time_format`: (CALENDAR)
        - `aberration_correction` (CN) [NONE|LT|LT+S|CN|CN+S|XLT|XLT+S|XCN|XCN+S]
    '''

    def __init__(self, aberration_correction='CN', **kwargs):

        self.required(['target', 'observer'], kwargs)
        
        kwargs['calculation_type'] = 'ANGULAR_SIZE'
        kwargs['aberration_correction'] = aberration_correction

        super().__init__(**kwargs)


class FrameTransformation(Calculation):
    '''
    Calculate the transformation from one reference frame (Frame 1) to another reference frame (Frame 2).
    
    Required parameters:
    --------------------
        - `kernels` | `kernel_paths`
        - `times` | `intervals` + `time_step` + `time_step_units`
        - `frame_1`: The first reference frame name.
        - `frame_2`: The second reference frame name.

    Optional parameters (with default):
    ------------------------------------
        - `time_system`: (UTC)
        - `time_format`: (CALENDAR)
        - `aberration_correction` (CN) [NONE|LT|CN|XLT|XCN]
        - `time_location`: The frame for the input times. (FRAME1) [FRAME1|FRAME2]
        - `orientation_representation`: The representation of the result transformation. (EULER_ANGLES) [EULER_ANGLES|ANGLE_AND_AXIS|SPICE_QUATERNION|OTHER_QUATERNION|MATRIX_ROW_BY_ROW|MATRIX_FLAGGED|MATRIX_ALL_ONE_ROW]
        - `angular_velocity_representation`: The representation of angular velocity in the output. (VECTOR_IN_FRAME1) [NOT_INCLUDED|VECTOR_IN_FRAME1|VECTOR_IN_FRAME2|EULER_ANGLE_DERIVATIVES|MATRIX]
    
    Only needed if `orientation_representation` is `EULER_ANGLES`:
        - `axis_1`: The first axis for Euler angle rotation. (X) [X|Y|Z]
        - `axis_2`: The second axis for Euler angle rotation (X) [X|Y|Z]
        - `axis_3`: The third axis for Euler angle rotation (X) [X|Y|Z]

    Only needed if `orientation_representation` is `EULER_ANGLES` or `ANGLE_AND_AXIS`:
        - `angular_units`: The angular units used for the angle of rotation. (deg) [deg|rad]
    
    Only needed if `angular_velocity_representation` is one of: `VECTOR_IN_FRAME1`, `VECTOR_IN_FRAME2`, or `EULER_ANGLE_DERIVATIVES`:
        - `angular_velocity_units`: The units for the angular velocity. (deg/s) [deg/s|rad/s|RPM|Unitary]
    
    Note: `Unitary` = Unit vector, only applicable for `VECTOR_IN_FRAME1` and `VECTOR_IN_FRAME2`.
    '''

    def __init__(self, aberration_correction='CN', time_location='FRAME1',
                 orientation_representation='EULER_ANGLES',
                 axis_1='X', axis_2='Y', axis_3='Z',
                 angular_units='deg',
                 angular_velocity_representation='VECTOR_IN_FRAME1',
                 angular_velocity_units='deg/s',
                 **kwargs):

        self.required(['frame_1', 'frame_2'], kwargs)

        ABERRATION_CORRECTION_ALLOWED = list(filter(lambda x: '+S' not in x, ABERRATION_CORRECTION))
        if aberration_correction not in ABERRATION_CORRECTION_ALLOWED:
            raise CalculationInvalidAttr('aberration_correction', aberration_correction, ABERRATION_CORRECTION_ALLOWED)

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

        if angular_velocity_representation in ['VECTOR_IN_FRAME1', 'VECTOR_IN_FRAME2', 'EULER_ANGLE_DERIVATIVES']:
            kwargs['angular_velocity_units'] = angular_velocity_units

        super().__init__(**kwargs)


class IlluminationAngles(Calculation):
    '''
    Calculate the emission, phase and solar incidence angles at a point on a target as seen from an observer.
    
    Required parameters:
    --------------------
        - `kernels` | `kernel_paths`
        - `times` | `intervals` + `time_step` + `time_step_units`
        - `target`: The target body name or ID.
        - `target_frame`: The target body-fixed reference frame name.
        - `observer`: The observing body name or ID.
        - `latitude`: Latitude of the surface point, in degrees, from -90 to +90.
        - `longitude`: Longitude of the surface point, in degrees, from -180 to +180.

    Optional parameters (with default):
    ------------------------------------
        - `time_system`: (UTC)
        - `time_format`: (CALENDAR)
        - `shape_1`: The shape to use for the target body. (ELLIPSOID) [ELLIPSOID|DSK]
        - `coordinate_representation` (LATITUDINAL) [LATITUDINAL|PLANETODETIC|PLANETOGRAPHIC]
        - `aberration_correction` (CN) [NONE|LT|LT+S|CN|CN+S|XLT|XLT+S|XCN|XCN+S]
    '''

    def __init__(self, shape_1='ELLIPSOID', coordinate_representation='LATITUDINAL', aberration_correction='CN', **kwargs):

        self.required(['target', 'target_frame', 'observer', 'latitude', 'longitude'], kwargs)

        kwargs['calculation_type'] = 'ILLUMINATION_ANGLES'
        kwargs['coordinate_representation'] = coordinate_representation
        kwargs['aberration_correction'] = aberration_correction

        if shape_1 in ['ELLIPSOID', 'DSK']:
            kwargs['shape_1'] = shape_1
        else:
            raise CalculationInvalidAttr('shape_1', shape_1, ['ELLIPSOID', 'DSK'])

        super().__init__(**kwargs)


class SubSolarPoint(Calculation):
    '''
    Calculates the sub-solar point on a target as seen from an observer.
    
    Required parameters:
    --------------------
        - `kernels` | `kernel_paths`
        - `times` | `intervals` + `time_step` + `time_step_units`
        - `target`: The target body name or ID.
        - `target_frame`: The target body-fixed reference frame name.
        - `observer`: The observing body name or ID.

    Optional parameters (with default):
    ------------------------------------
        - `time_system`: (UTC)
        - `time_format`: (CALENDAR)
        - `sub_point_type`: The method of finding the sub-solar point. (Near point: ellipsoid) [Near point: ellipsoid|Intercept: ellipsoid|NADIR/DSK/UNPRIORITIZED|INTERCEPT/DSK/UNPRIORITIZED]
        - `aberration_correction` (CN) [NONE|LT|LT+S|CN|CN+S|XLT|XLT+S|XCN|XCN+S]
        - `state_representation` (RECTANGULAR) [RECTANGULAR|RA_DEC|LATITUDINAL|PLANETODETIC|PLANETOGRAPHIC|CYLINDRICAL|SPHERICAL]
    '''

    def __init__(self, sub_point_type='Near point: ellipsoid', aberration_correction='CN', state_representation='RECTANGULAR', **kwargs):

        self.required(['target', 'target_frame', 'observer'], kwargs)

        ABERRATION_CORRECTION_ALLOWED = list(filter(lambda x: 'X' not in x, ABERRATION_CORRECTION))
        if aberration_correction not in ABERRATION_CORRECTION_ALLOWED:
            raise CalculationInvalidAttr('aberration_correction', aberration_correction, ABERRATION_CORRECTION_ALLOWED)

        kwargs['calculation_type'] = 'SUB_SOLAR_POINT'
        kwargs['sub_point_type'] = sub_point_type
        kwargs['aberration_correction'] = aberration_correction
        kwargs['state_representation'] = state_representation

        super().__init__(**kwargs)

class SubObserverPoint(Calculation):
    '''
    Calculate the sub-observer point on a target as seen from an observer.
    
    Required parameters:
    --------------------
        - `kernels` | `kernel_paths`
        - `times` | `intervals` + `time_step` + `time_step_units`
        - `target`: The target body name or ID.
        - `target_frame`: The target body-fixed reference frame name.
        - `observer`: The observing body name or ID.

    Optional parameters (with default):
    ------------------------------------
        - `time_system`: (UTC)
        - `time_format`: (CALENDAR)
        - `sub_point_type`: The method of finding the sub-observer point. (Near point: ellipsoid) [Near point: ellipsoid|Intercept: ellipsoid|NADIR/DSK/UNPRIORITIZED|INTERCEPT/DSK/UNPRIORITIZED]
        - `aberration_correction`: (CN) [NONE|LT|LT+S|CN|CN+S|XLT|XLT+S|XCN|XCN+S]
        - `state_representation`: (RECTANGULAR) [RECTANGULAR|RA_DEC|LATITUDINAL|PLANETODETIC|PLANETOGRAPHIC|CYLINDRICAL|SPHERICAL]
    '''

    def __init__(self, sub_point_type='Near point: ellipsoid', aberration_correction='CN', state_representation='RECTANGULAR', **kwargs):

        self.required(['target', 'target_frame', 'observer'], kwargs)

        kwargs['calculation_type'] = 'SUB_OBSERVER_POINT'
        kwargs['sub_point_type'] = sub_point_type
        kwargs['aberration_correction'] = aberration_correction
        kwargs['state_representation'] = state_representation

        super().__init__(**kwargs)


class SurfaceInterceptPoint(Calculation):
    '''
    Calculate the intercept point of a vector or vectors on a target as seen from an observer.
    
    Required parameters:
    --------------------
        - `kernels` | `kernel_paths`
        - `times` | `intervals` + `time_step` + `time_step_units`
        - `target`: The target body name or ID.
        - `target_frame`: The target body-fixed reference frame name.
        - `observer`: The observing body name or ID.

    Optional parameters (with default):
    ------------------------------------
        - `time_system`: (UTC)
        - `time_format`: (CALENDAR)
        - `shape_1`: The shape to use for the target body. (ELLIPSOID) [ELLIPSOID|DSK]
        - `intercept_vector_type`: Type of vector to be used as the ray direction. (INSTRUMENT_BORESIGHT) [INSTRUMENT_BORESIGHT|INSTRUMENT_FOV_BOUNDARY_VECTORS|REFERENCE_FRAME_AXIS|VECTOR_IN_INSTRUMENT_FOV|VECTOR_IN_REFERENCE_FRAME]
        - `aberration_correction`: (CN) [NONE|LT|LT+S|CN|CN+S|XLT|XLT+S|XCN|XCN+S]
        - `state_representation`: (RECTANGULAR) [RECTANGULAR|RA_DEC|LATITUDINAL|PLANETODETIC|PLANETOGRAPHIC|CYLINDRICAL|SPHERICAL]

    Only needed if `intercept_vector_type` is `INSTRUMENT_BORESIGHT`, `INSTRUMENT_FOV_BOUNDARY_VECTORS` or `VECTOR_IN_INSTRUMENT_FOV`:
        - `intercept_instrument`: The instrument name or ID.
        
    Only needed if `intercept_vector_type` is `REFERENCE_FRAME_AXIS` or `VECTOR_IN_REFERENCE_FRAME`:
        - `intercept_frame`: The vector's reference frame name.

    Only needed if `intercept_vector_type` is `REFERENCE_FRAME_AXIS`:
        - `intercept_frame_axis`: The intercept frame axis.

    Only need if `intercept_vector_type` is `VECTOR_IN_INSTRUMENT_FOV` or `VECTOR_IN_REFERENCE_FRAME`:
        - `intercept_vector_x` + `intercept_vector_y` + `intercept_vector_z` | `intercept_vector_ra` + `intercept_vector_dec`: intercept vector coordinates.
    '''

    def __init__(self, shape_1='ELLIPSOID', intercept_vector_type='INSTRUMENT_BORESIGHT', \
                 aberration_correction='CN', state_representation='RECTANGULAR', **kwargs):

        self.required(['target', 'target_frame', 'observer'], kwargs)

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
    '''
    Calculate the osculating elements of the orbit of a target body around a central body.
    The orbit may be elliptical, parabolic, or hyperbolic.
    
    Required parameters:
    --------------------
        - `kernels` | `kernel_paths`
        - `times` | `intervals` + `time_step` + `time_step_units`
        - `orbiting_body`: The SPICE body name or ID for the orbiting body.
        - `center_body`: The SPICE body name or ID for the body that is the center of motion.

    Optional parameters (with default):
    ------------------------------------
        - `time_system`: (UTC)
        - `time_format`: (CALENDAR)
        - `reference_frame`: The reference frame name. (J2000)
    '''

    def __init__(self, reference_frame='J2000', **kwargs):

        self.required(['orbiting_body', 'center_body'], kwargs)
        
        kwargs['calculation_type'] = 'OSCULATING_ELEMENTS'
        kwargs['reference_frame'] = reference_frame

        super().__init__(**kwargs)

class TimeConversion(Calculation):
    '''
    Convert times from one time system or format to another.
    
    Required parameters:
    --------------------
        - `kernels` | `kernel_paths`
        - `times` | `intervals` + `time_step` + `time_step_units`

    Optional parameters (with default):
    ------------------------------------
        - `time_system`: (UTC)
        - `time_format`: (CALENDAR)
        - `output_time_system`: The time system for the result times. (UTC) [TDB|TDT|UTC|SPACECRAFT_CLOCK]
        - `output_time_format`: The time format for the result times. (CALENDAR) [CALENDAR|CALENDAR_YMD|CALENDAR_DOY|JULIAN|SECONDS_PAST_J2000|SPACECRAFT_CLOCK_STRING|SPACECRAFT_CLOCK_TICKS|CUSTOM]

    Only used if `outputTimeSystem` is `SPACECRAFT_CLOCK`.
        - `output_sclk_id`: The output SCLK ID.
    
    Only used if `output_time_format` is `CUSTOM`.
        - `output_time_custom_format`: A SPICE timout() format string.
    '''

    def __init__(self, output_time_system='UTC', output_time_format='CALENDAR', **kwargs):
     
        kwargs['calculation_type'] = 'TIME_CONVERSION'
        kwargs['output_time_system'] = output_time_system
        kwargs['output_time_format'] = output_time_format

        super().__init__(**kwargs)

