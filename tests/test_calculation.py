# -*- coding: utf-8 -*-
import pytest

from webgeocalc import Calculation
from webgeocalc.errors import CalculationRequiredAttr, CalculationInvalidAttr, CalculationUndefinedAttr, CalculationIncompatibleAttr, CalculationConflictAttr

@pytest.fixture
def kernels():
    return 1 # Solar System Kernels set

@pytest.fixture
def calc():
    return 'STATE_VECTOR'

@pytest.fixture
def time():
    return '2012-10-19T08:24:00.000'

@pytest.fixture
def path():
    return 'https://path.to.server/kernel'

@pytest.fixture
def params(calc, path, time):
    return {
        'calculation_type': calc,
        'kernel_paths': path,
        'times': time,
    }

@pytest.fixture
def payload(path, calc, time):
    return {
        "kernels": [{
            "type": "KERNEL",
            "path": path,
        }],
        "calculationType": calc,
        "times": [time],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        }

@pytest.fixture
def start():
    return '2000-01-01'

@pytest.fixture
def end():
    return '2000-01-02'

@pytest.fixture
def interval(start, end):
    return {"startTime": start, "endTime": end}


def test_calculation_required_err(calc, kernels):
    with pytest.raises(CalculationRequiredAttr):
        Calculation()  # 'calculation_type' missing

    with pytest.raises(CalculationRequiredAttr):
        Calculation(calculation_type=calc)  # 'kernels/kernel_paths' missing

    with pytest.raises(CalculationRequiredAttr):
        Calculation(calculation_type=calc, kernels=kernels) # 'times' missing

def test_calculation_payload(params, payload):
    assert Calculation(**params).payload == payload

def test_calculation_calc_err(params):
    params['calculation_type'] = 'WRONG'
    with pytest.raises(CalculationInvalidAttr):
        Calculation(**params)

def test_calculation_time_system_err(params):
    params['time_system'] = 'WRONG'
    with pytest.raises(CalculationInvalidAttr):
        Calculation(**params)

def test_calculation_missing_sclk_id(params):
    params['time_system'] = 'SPACECRAFT_CLOCK'
    with pytest.raises(CalculationUndefinedAttr):
        Calculation(**params)

def test_calculation_time_format_error(params):
    params['time_format'] = 'WRONG'
    with pytest.raises(CalculationInvalidAttr):
        Calculation(**params)

def test_calculation_time_system_conflict(params):
    params['time_system'] = 'SPACECRAFT_CLOCK'
    params['sclk_id'] = 1
    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(**params)

def test_calculation_time_format_conflict(params):
    params['time_format'] = 'SPACECRAFT_CLOCK_STRING'
    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(**params)

def test_calculation_sclk_id_conflict(params):
    params['sclk_id'] = 1
    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(**params)

def test_calculation_intervals(params, start, end, interval):
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
    params['intervals'] = interval

    with pytest.raises(CalculationConflictAttr):
        Calculation(**params) # 'times' and 'intervals' conflict

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
    params['time_step'] = 1
    with pytest.raises(CalculationConflictAttr):
        Calculation(**params) # Conflict with 'times'

def test_calculation_time_step_units_errors(params, interval):
    params['time_step_units'] = 'DAYS'
    with pytest.raises(CalculationConflictAttr):
        Calculation(**params) # Conflict with 'times'

    del params['times']
    params['intervals'] = interval

    with pytest.raises(CalculationUndefinedAttr):
        Calculation(**params)  # 'time_step' missing

    params['time_step'] = 1
    params['time_step_units'] = 'WRONG_UNITS'
    with pytest.raises(CalculationInvalidAttr):
        Calculation(**params)

def test_calculation_aberration_correction_error(params):
    with pytest.raises(CalculationInvalidAttr):
        Calculation(aberration_correction='WRONG', **params)

def test_calculation_state_representation_error(params):
    with pytest.raises(CalculationInvalidAttr):
        Calculation(state_representation='WRONG', **params)

def test_calculation_shape_error(params):
    with pytest.raises(CalculationInvalidAttr):
        Calculation(shape_1='WRONG', **params)

    with pytest.raises(CalculationInvalidAttr):
        Calculation(shape_2='WRONG', **params)

def test_calculation_axis_error(params):
    with pytest.raises(CalculationUndefinedAttr):
        Calculation(axis_1='X', **params) # Missing `orientation_representation`

    with pytest.raises(CalculationIncompatibleAttr):
        # Wrong `orientation_representation` with `axis`
        Calculation(orientation_representation='SPICE_QUATERNION', axis_1='X', **params)

def test_calculation_angular_units_error(params):
    with pytest.raises(CalculationUndefinedAttr):
        Calculation(angular_units='deg', **params) # Missing `orientation_representation`

    with pytest.raises(CalculationIncompatibleAttr):
        # Wrong `orientation_representation` with `angular_units`
        Calculation(orientation_representation='SPICE_QUATERNION', angular_units='deg', **params)

def test_calculation_angular_velocity_units_error(params):
    with pytest.raises(CalculationUndefinedAttr):
        Calculation(angular_velocity_units='deg/s', **params) # Missing `angular_velocity_representation`

    with pytest.raises(CalculationIncompatibleAttr):
        # Wrong `angular_velocity_representation` with `angular_velocity_units`
        Calculation(angular_velocity_representation='NOT_INCLUDED', angular_velocity_units='deg/s', **params)

def test_calculation_intercept_vector_type_error(params):
    with pytest.raises(CalculationInvalidAttr):
        Calculation(intercept_vector_type='WRONG', **params)

def test_calculation_intercept_instrument_error(params):
    with pytest.raises(CalculationUndefinedAttr):
        Calculation(intercept_instrument='CASSINI_ISS_NAC', **params) # Missing `intercept_vector_type`

    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(intercept_instrument='CASSINI_ISS_NAC', intercept_vector_type='VECTOR_IN_REFERENCE_FRAME',
                    intercept_frame='CASSINI_ISS_NAC', **params)

def test_calculation_intercept_frame_error(params):
    with pytest.raises(CalculationUndefinedAttr):
        Calculation(intercept_frame='CASSINI_ISS_NAC', **params) # Missing 'intercept_vector_type'

    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(intercept_frame='CASSINI_ISS_NAC', intercept_vector_type='INSTRUMENT_BORESIGHT', **params) # Wrong 'intercept_vector_type'

def test_calculation_intercept_frame_axis_error(params):
    with pytest.raises(CalculationUndefinedAttr):
        Calculation(intercept_frame_axis='Z', **params) # Missing 'intercept_frame'

    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(intercept_frame_axis='Z', intercept_vector_type='INSTRUMENT_BORESIGHT', **params) # Wrong 'intercept_vector_type'

    with pytest.raises(CalculationInvalidAttr):
        Calculation(intercept_frame_axis='WRONG', intercept_vector_type='REFERENCE_FRAME_AXIS', **params) # Wrong 'intercept_frame_axis'

def test_calculation_intercept_vector_error(params):
    with pytest.raises(CalculationUndefinedAttr):
        Calculation(intercept_vector_x=0, **params) # Missing 'intercept_vector_type'

    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(intercept_vector_x=0, intercept_vector_type='INSTRUMENT_BORESIGHT', **params) # Wrong 'intercept_vector_type'

def test_calculation_output_time_system_error(params):
    with pytest.raises(CalculationInvalidAttr):
        Calculation(output_time_system='WRONG', **params)

    with pytest.raises(CalculationUndefinedAttr):
        Calculation(output_time_system='SPACECRAFT_CLOCK', **params) # Missing 'output_sclk_id'

def test_calculation_output_time_format_error(params):
    with pytest.raises(CalculationInvalidAttr):
        Calculation(output_time_format='WRONG', **params)

    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(output_time_format='CALENDAR', output_time_system='SPACECRAFT_CLOCK', **params) # Wrong 'output_time_system'

    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(output_time_format='SPACECRAFT_CLOCK_STRING', output_time_system='UTC', **params) # Wrong 'output_time_system'

def test_calculation_output_sclk_id_error(params):
    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(output_sclk_id=-82, output_time_system='WRONG', **params)

def test_calculation_output_time_custom_format_error(params):
    with pytest.raises(CalculationIncompatibleAttr):
        Calculation(output_time_custom_format='YYYY Month DD HR:MN', output_time_format='WRONG', **params)
