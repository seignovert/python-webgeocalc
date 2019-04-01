# -*- coding: utf-8 -*-
'''Test WGC calculation setup.'''

import pytest

from webgeocalc import Calculation
from webgeocalc.errors import (CalculationConflictAttr, CalculationIncompatibleAttr,
                               CalculationInvalidAttr, CalculationRequiredAttr,
                               CalculationUndefinedAttr)

@pytest.fixture
def kernels():
    '''Input Solar System kernels set.'''
    return 1

@pytest.fixture
def calc():
    '''Input calculation type name.'''
    return 'STATE_VECTOR'

@pytest.fixture
def time():
    '''Input time.'''
    return '2012-10-19T08:24:00.000'

@pytest.fixture
def path():
    '''Input kernel path url.'''
    return 'https://path.to.server/kernel'

@pytest.fixture
def params(calc, path, time):
    '''Input parameters dict.'''
    return {
        'calculation_type': calc,
        'kernel_paths': path,
        'times': time,
    }

@pytest.fixture
def start():
    '''Input start time.'''
    return '2000-01-01'

@pytest.fixture
def end():
    '''Input end time.'''
    return '2000-01-02'

@pytest.fixture
def interval(start, end):
    '''Input interval dict.'''
    return {"startTime": start, "endTime": end}


def test_calculation_required_err(calc, kernels):
    '''Test error if calculation has missing required attributes.'''
    with pytest.raises(CalculationRequiredAttr):
        Calculation()  # 'calculation_type' missing

    with pytest.raises(CalculationRequiredAttr):
        Calculation(calculation_type=calc)  # 'kernels/kernel_paths' missing

    with pytest.raises(CalculationRequiredAttr):
        Calculation(calculation_type=calc, kernels=kernels)  # 'times' missing

def test_calculation_calc_err(params):
    '''Test error if calculation type is invalid.'''
    params['calculation_type'] = 'WRONG'
    with pytest.raises(CalculationInvalidAttr):
        Calculation(**params)

def test_calculation_time_system_err(params):
    '''Test error if time system is invalid.'''
    params['time_system'] = 'WRONG'
    with pytest.raises(CalculationInvalidAttr):
        Calculation(**params)

def test_calculation_missing_sclk_id(params):
    '''Test error if sclk_id is missing.'''
    params['time_system'] = 'SPACECRAFT_CLOCK'
    with pytest.raises(CalculationUndefinedAttr):
        Calculation(**params)

def test_calculation_time_format_error(params):
    '''Test error if time format is invalid.'''
    params['time_format'] = 'WRONG'
    with pytest.raises(CalculationInvalidAttr):
        Calculation(**params)

def test_calculation_time_system_conflict(params):
    '''Test error when time system and time format are incompatible.'''
    params['time_system'] = 'SPACECRAFT_CLOCK'
    params['sclk_id'] = 1
    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(**params)

def test_calculation_time_format_conflict(params):
    '''Test error when time format and time system are incompatible.'''
    params['time_format'] = 'SPACECRAFT_CLOCK_STRING'
    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(**params)

def test_calculation_sclk_id_conflict(params):
    '''Test error when sclk id system and time system are incompatible.'''
    params['sclk_id'] = 1
    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(**params)

def test_calculation_intervals(params, start, end, interval):
    '''Test calculation interval inputs.'''
    del params['times']
    params['time_step'] = 1
    params['time_step_units'] = 'DAYS'

    params['intervals'] = [start, end]
    assert Calculation(**params).payload['intervals'] == [interval]

    params['intervals'] = {"startTime": start, "endTime": end}
    assert Calculation(**params).payload['intervals'] == [interval]

    params['intervals'] = [interval]
    assert Calculation(**params).payload['intervals'] == [interval]

    params['intervals'] = [interval, interval]
    assert Calculation(**params).payload['intervals'] == [interval, interval]

    params['intervals'] = [interval, interval, interval]
    assert Calculation(**params).payload['intervals'] == [interval, interval, interval]

def test_calculation_intervals_errors(params, start, end, interval):
    '''Test errors if intervals input are incorrect.'''
    params['intervals'] = interval

    with pytest.raises(CalculationConflictAttr):
        Calculation(**params)  # 'times' and 'intervals' conflict

    del params['times']

    with pytest.raises(CalculationUndefinedAttr):
        Calculation(**params)  # 'time_step' missing

    params['time_step'] = 1
    with pytest.raises(CalculationUndefinedAttr):
        Calculation(**params)  # 'time_step_units' missing

    params['time_step_units'] = 'DAYS'

    params['intervals'] = {"startTime": start, "wrongEndTime": end}
    with pytest.raises(CalculationInvalidAttr):
        Calculation(**params)

    params['intervals'] = []
    with pytest.raises(CalculationInvalidAttr):
        Calculation(**params)

    params['intervals'] = [start]
    with pytest.raises(CalculationInvalidAttr):
        Calculation(**params)

    params['intervals'] = [start, interval]
    with pytest.raises(CalculationInvalidAttr):
        Calculation(**params)

    params['intervals'] = [start, end, end]
    with pytest.raises(CalculationInvalidAttr):
        Calculation(**params)

def test_calculation_time_step_conflict(params):
    '''Test error when time step and times are incompatible.'''
    params['time_step'] = 1
    with pytest.raises(CalculationConflictAttr):
        Calculation(**params)

def test_calculation_time_step_units_errors(params, interval):
    '''Test errors if time step units are invalid.'''
    params['time_step_units'] = 'DAYS'
    with pytest.raises(CalculationConflictAttr):
        Calculation(**params)  # Conflict with 'times'

    del params['times']
    params['intervals'] = interval

    with pytest.raises(CalculationUndefinedAttr):
        Calculation(**params)  # 'time_step' missing

    params['time_step'] = 1
    params['time_step_units'] = 'WRONG_UNITS'
    with pytest.raises(CalculationInvalidAttr):
        Calculation(**params)

def test_calculation_aberration_correction_error(params):
    '''Test error if aberration correction is invalid.'''
    with pytest.raises(CalculationInvalidAttr):
        Calculation(aberration_correction='WRONG', **params)

def test_calculation_state_representation_error(params):
    '''Test error if state representation is invalid.'''
    with pytest.raises(CalculationInvalidAttr):
        Calculation(state_representation='WRONG', **params)

def test_calculation_shape_error(params):
    '''Test error if shape 1-2 is invalid.'''
    with pytest.raises(CalculationInvalidAttr):
        Calculation(shape_1='WRONG', **params)

    with pytest.raises(CalculationInvalidAttr):
        Calculation(shape_2='WRONG', **params)

def test_calculation_axis_error(params):
    '''Test error if axis inputs are invalid.'''
    with pytest.raises(CalculationUndefinedAttr):
        Calculation(axis_1='X', **params)  # Missing `orientation_representation`

    with pytest.raises(CalculationIncompatibleAttr):
        # Wrong `orientation_representation` with `axis`
        Calculation(orientation_representation='SPICE_QUATERNION', axis_1='X', **params)

def test_calculation_angular_units_error(params):
    '''Test errors if angular units are invalid.'''
    with pytest.raises(CalculationUndefinedAttr):
        Calculation(angular_units='deg', **params)  # Missing `orientation_representation`

    with pytest.raises(CalculationIncompatibleAttr):
        # Wrong `orientation_representation` with `angular_units`
        Calculation(orientation_representation='SPICE_QUATERNION',
                    angular_units='deg', **params)

def test_calculation_angular_velocity_units_error(params):
    '''Test errors with angular velocity units.'''
    with pytest.raises(CalculationUndefinedAttr):
        # Missing `angular_velocity_representation`
        Calculation(angular_velocity_units='deg/s', **params)

    with pytest.raises(CalculationIncompatibleAttr):
        # Wrong `angular_velocity_representation` with `angular_velocity_units`
        Calculation(angular_velocity_representation='NOT_INCLUDED',
                    angular_velocity_units='deg/s', **params)

def test_calculation_direction_vector_type_error(params):
    '''Test error if intercept vector type is invalid.'''
    with pytest.raises(CalculationInvalidAttr):
        Calculation(direction_vector_type='WRONG', **params)

def test_calculation_direction_instrument_error(params):
    '''Test erros when intercept instrument is invalid.'''
    with pytest.raises(CalculationUndefinedAttr):
        # Missing `direction_vector_type`
        Calculation(direction_instrument='CASSINI_ISS_NAC', **params)

    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(direction_instrument='CASSINI_ISS_NAC',
                    direction_vector_type='VECTOR_IN_REFERENCE_FRAME',
                    direction_frame='CASSINI_ISS_NAC', **params)

def test_calculation_direction_frame_error(params):
    '''Test errors when intercept frame is invalid.'''
    with pytest.raises(CalculationUndefinedAttr):
        # Missing 'direction_vector_type'
        Calculation(direction_frame='CASSINI_ISS_NAC', **params)

    with pytest.raises(CalculationIncompatibleAttr):
        # Wrong 'direction_vector_type'
        Calculation(direction_frame='CASSINI_ISS_NAC',
                    direction_vector_type='INSTRUMENT_BORESIGHT', **params)

def test_calculation_direction_frame_axis_error(params):
    '''Test errors when intercept frame axis is invalid.'''
    with pytest.raises(CalculationUndefinedAttr):
        # Missing 'direction_frame'
        Calculation(direction_frame_axis='Z', **params)

    with pytest.raises(CalculationIncompatibleAttr):
        # Wrong 'direction_vector_type'
        Calculation(direction_frame_axis='Z',
                    direction_vector_type='INSTRUMENT_BORESIGHT', **params)

    with pytest.raises(CalculationInvalidAttr):
        # Wrong 'direction_frame_axis'
        Calculation(direction_frame_axis='WRONG',
                    direction_vector_type='REFERENCE_FRAME_AXIS', **params)

def test_calculation_direction_vector_error(params):
    '''Test errors when intercept vector is invalid.'''
    with pytest.raises(CalculationUndefinedAttr):
        # Missing 'direction_vector_type'
        Calculation(direction_vector_x=0, **params)

    with pytest.raises(CalculationIncompatibleAttr):
        # Wrong 'direction_vector_type'
        Calculation(direction_vector_x=0,
                    direction_vector_type='INSTRUMENT_BORESIGHT', **params)

def test_calculation_output_time_system_error(params):
    '''Test errors when output time system is invalid.'''
    with pytest.raises(CalculationInvalidAttr):
        Calculation(output_time_system='WRONG', **params)

    with pytest.raises(CalculationUndefinedAttr):
        # Missing 'output_sclk_id'
        Calculation(output_time_system='SPACECRAFT_CLOCK', **params)

def test_calculation_output_time_format_error(params):
    '''Test errors when output time format is invalid.'''
    with pytest.raises(CalculationInvalidAttr):
        Calculation(output_time_format='WRONG', **params)

    with pytest.raises(CalculationIncompatibleAttr):
        # Wrong 'output_time_system'
        Calculation(output_time_format='CALENDAR',
                    output_time_system='SPACECRAFT_CLOCK', **params)

    with pytest.raises(CalculationIncompatibleAttr):
        # Wrong 'output_time_system'
        Calculation(output_time_format='SPACECRAFT_CLOCK_STRING',
                    output_time_system='UTC', **params)

def test_calculation_output_sclk_id_error(params):
    '''Test errors when output sckl id is invalid.'''
    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(output_sclk_id=-82, output_time_system='WRONG', **params)

def test_calculation_output_time_custom_format_error(params):
    '''Test errors when output time custom is invalid.'''
    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(output_time_custom_format='YYYY Month DD HR:MN',
                    output_time_format='WRONG', **params)
