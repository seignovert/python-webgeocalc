# -*- coding: utf-8 -*-
'''Test WGC (geometry finder) coordinate search calculation.'''

import pytest

from webgeocalc import GFCoordinateSearch
from webgeocalc.errors import CalculationInvalidAttr


@pytest.fixture
def kernels():
    '''Generic kernel set.'''
    return 5

@pytest.fixture
def intervals():
    '''Input time interval'''
    return ['2012-10-19T07:00:00', '2012-10-19T09:00:00']

@pytest.fixture
def reference_frame():
    '''Input reference frame.'''
    return 'CASSINI_ISS_NAC'

@pytest.fixture
def observer():
    '''Input observer.'''
    return 'CASSINI'

@pytest.fixture
def target():
    '''Input observer.'''
    return 'ENCELADUS'

@pytest.fixture
def time_step():
    '''Input time step.'''
    return 1

@pytest.fixture
def time_step_units():
    '''Input time step units.'''
    return 'MINUTES'

@pytest.fixture
def corr():
    '''Input aberration correction.'''
    return 'NONE'

@pytest.fixture
def coordinate_system():
    '''Input coordinate system search condition'''
    return "SPHERICAL"

@pytest.fixture
def coordinate():
    '''Input coordinate search condition'''
    return "COLATITUDE"

@pytest.fixture
def relational_condition():
    '''Input relational condition search condition'''
    return "<"

@pytest.fixture
def reference_value():
    '''Input reference value search condition'''
    return 0.25

@pytest.fixture
def upper_limit():
    '''Input upper limit search condition'''
    return 0.3

@pytest.fixture
def adjustment_value():
    '''Input adjustment value search condition'''
    return 0.1

@pytest.fixture
def params_1(kernels, intervals, target, reference_frame, observer, time_step,
             time_step_units, corr, coordinate_system, coordinate, relational_condition,
             reference_value, upper_limit, adjustment_value):
    '''Input parameters from WGC API example 1.'''
    return {
        "kernels": kernels,
        "intervals": intervals,
        "time_step": time_step,
        "time_step_units": time_step_units,
        "target": target,
        "observer": observer,
        "reference_frame": reference_frame,
        "aberration_correction": corr,
        'coordinate_system': coordinate_system,
        'coordinate': coordinate,
        'relational_condition': relational_condition,
        'reference_value': reference_value,
        'upper_limit': upper_limit,
        'adjustment_value': adjustment_value,
    }

@pytest.fixture
def payload_1(kernels, intervals, target, reference_frame, observer, time_step,
              time_step_units, corr, coordinate_system, coordinate,
              relational_condition, reference_value, upper_limit, adjustment_value):
    '''Payload from WGC API example 1.'''
    return {
        "kernels": [{
            "type": "KERNEL_SET",
            "id": kernels,
        }],
        "intervals": [{
            "startTime": intervals[0],
            "endTime": intervals[1]
        }],
        "observer": observer,
        "target": target,
        'timeStep': time_step,
        'timeStepUnits': time_step_units,
        'referenceFrame': reference_frame,
        'condition': {
            "coordinateSystem": coordinate_system,
            "coordinate": coordinate,
            'relationalCondition': relational_condition,
            'referenceValue': reference_value,
            'upperLimit': upper_limit,
            'adjustmentValue': adjustment_value,
        },
        'calculationType': 'GF_COORDINATE_SEARCH',
        'aberrationCorrection': corr,
        'timeSystem': 'UTC',
        'timeFormat': 'CALENDAR',
        "intervalAdjustment": "NO_ADJUSTMENT",
        "intervalFiltering": "NO_FILTERING",
        "outputDurationUnits": "SECONDS",
        "shouldComplementWindow": False,
    }

@pytest.fixture
def params_2(kernels, intervals, target, reference_frame, observer, time_step,
             time_step_units, corr, coordinate_system, coordinate,
              relational_condition, reference_value, upper_limit, adjustment_value):
    '''Input parameters from WGC API example 1.'''
    return {
        "kernels": kernels,
        "intervals": intervals,
        "time_step": time_step,
        "time_step_units": time_step_units,
        "target": target,
        "observer": observer,
        "reference_frame": reference_frame,
        "aberration_correction": corr,
        'coordinate_system': coordinate_system,
        'coordinate': coordinate,
        'relational_condition': relational_condition,
        'reference_value': reference_value,
        'upper_limit': upper_limit,
        'adjustment_value': adjustment_value,
        "interval_adjustment": "EXPAND_INTERVALS",
        "interval_adjustment_amount": 30,
        "interval_adjustment_units": "MINUTES",
    }

@pytest.fixture
def payload_2(kernels, intervals, target, reference_frame, observer, time_step,
              time_step_units, corr, coordinate_system, coordinate,
              relational_condition, reference_value, upper_limit, adjustment_value):
    '''Payload from WGC API example 1.'''
    return {
        "kernels": [{
            "type": "KERNEL_SET",
            "id": kernels,
        }],
        "intervals": [{
            "startTime": intervals[0],
            "endTime": intervals[1]
        }],
        "observer": observer,
        "target": target,
        'timeStep': time_step,
        'timeStepUnits': time_step_units,
        'referenceFrame': reference_frame,
        'condition': {
            'coordinateSystem': coordinate_system,
            'coordinate': coordinate,
            'relationalCondition': relational_condition,
            'referenceValue': reference_value,
            'upperLimit': upper_limit,
            'adjustmentValue': adjustment_value,
        },
        'calculationType': 'GF_COORDINATE_SEARCH',
        'aberrationCorrection': corr,
        'outputDurationUnits': 'SECONDS',
        'shouldComplementWindow': False,
        'intervalAdjustment': "EXPAND_INTERVALS",
        "intervalAdjustmentAmount": 30,
        "intervalAdjustmentUnits": "MINUTES",
        'intervalFiltering': 'NO_FILTERING',
        'timeSystem': 'UTC',
        'timeFormat': 'CALENDAR'
    }

@pytest.fixture
def params_3(kernels, intervals, target, reference_frame, observer, time_step,
             time_step_units, corr, coordinate_system, coordinate,
              relational_condition, reference_value, upper_limit, adjustment_value):
    '''Input parameters from WGC API example 1.'''
    return {
        "kernels": kernels,
        "intervals": intervals,
        "time_step": time_step,
        "time_step_units": time_step_units,
        "target": target,
        "observer": observer,
        "reference_frame": reference_frame,
        "aberration_correction": corr,
        'coordinate_system': coordinate_system,
        'coordinate': coordinate,
        'relational_condition': relational_condition,
        'reference_value': reference_value,
        'upper_limit': upper_limit,
        'adjustment_value': adjustment_value,
        "interval_filtering": "OMIT_INTERVALS_SMALLER_THAN_A_THRESHOLD",
        "interval_filtering_threshold": 30,
        "interval_filtering_threshold_units": "MINUTES",
    }

@pytest.fixture
def payload_3(kernels, intervals, target, reference_frame, observer, time_step,
              time_step_units, corr, coordinate_system, coordinate,
              relational_condition, reference_value, upper_limit, adjustment_value):
    '''Payload from WGC API example 1.'''
    return {
        "kernels": [{
            "type": "KERNEL_SET",
            "id": kernels,
        }],
        "intervals": [{
            "startTime": intervals[0],
            "endTime": intervals[1]
        }],
        "observer": observer,
        "target": target,
        'timeStep': time_step,
        'timeStepUnits': time_step_units,
        'referenceFrame': reference_frame,
        'condition': {
            'coordinateSystem': coordinate_system,
            'coordinate': coordinate,
            'relationalCondition': relational_condition,
            'referenceValue': reference_value,
            'upperLimit': upper_limit,
            'adjustmentValue': adjustment_value,
        },
        'calculationType': 'GF_COORDINATE_SEARCH',
        'aberrationCorrection': corr,
        'outputDurationUnits': 'SECONDS',
        'shouldComplementWindow': False,
        'intervalAdjustment': "NO_ADJUSTMENT",
        "intervalFiltering": "OMIT_INTERVALS_SMALLER_THAN_A_THRESHOLD",
        "intervalFilteringThreshold": 30,
        "intervalFilteringThresholdUnits": "MINUTES",
        'timeSystem': 'UTC',
        'timeFormat': 'CALENDAR'
    }

def test_coordinate_search_default(params_1, payload_1):
    '''Test Coordinate Search with single interval and default parameters.'''
    assert GFCoordinateSearch(**params_1).payload == payload_1

def test_coordinate_search_adjust_interval(params_2, payload_2):
    '''Test Coordinate Search with single interval with adjusted interval option.'''
    assert GFCoordinateSearch(**params_2).payload == payload_2

def test_coordinate_search_filter_interval(params_3, payload_3):
    '''Test Coordinate Search with single interval with filtered interval option.'''
    assert GFCoordinateSearch(**params_3).payload == payload_3

def test_coordinate_search_attr_err(params_1, params_2, params_3):
    '''Test errors Coordinate Search with single interval and default parameters.'''
    with pytest.raises(TypeError):
        GFCoordinateSearch(should_complement_window='WRONG', **params_1)

    with pytest.raises(CalculationInvalidAttr):
        GFCoordinateSearch(interval_adjustment='WRONG', **params_1)

    with pytest.raises(CalculationInvalidAttr):
        GFCoordinateSearch(interval_filtering='WRONG', **params_1)

    with pytest.raises(CalculationInvalidAttr):
        GFCoordinateSearch(output_duration_units='WRONG', **params_1)

    with pytest.raises(CalculationInvalidAttr):
        p = params_2.copy()
        del p['interval_adjustment_units']
        GFCoordinateSearch(interval_adjustment_units='WRONG', **p)

    with pytest.raises(CalculationInvalidAttr):
        p = params_3.copy()
        del p['interval_filtering_threshold_units']
        GFCoordinateSearch(interval_filtering_threshold_units='WRONG', **p)
