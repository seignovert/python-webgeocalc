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
    params['aberration_correction'] = 'WRONG'
    with pytest.raises(CalculationInvalidAttr):
        Calculation(**params)

def test_calculation_state_representation_error(params):
    params['state_representation'] = 'WRONG'
    with pytest.raises(CalculationInvalidAttr):
        Calculation(**params)
