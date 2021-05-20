# -*- coding: utf-8 -*-
'''Test WGC (geometry finder) coordinate search calculation.'''

import pytest

from webgeocalc import GFCoordinateSearch
from webgeocalc.errors import CalculationInvalidAttr, CalculationInvalidValue

from webgeocalc.vars import ESA_URL, JPL_URL


@pytest.fixture
def kernels():
    '''Generic kernel set.'''
    return 1

@pytest.fixture
def intervals():
    '''Input time interval'''
    return ["1986-08-22", "1986-08-23"]

@pytest.fixture
def reference_frame():
    '''Input reference frame.'''
    return 'EARTH_FIXED'

@pytest.fixture
def observer():
    '''Input observer.'''
    return 'EARTH'

@pytest.fixture
def target():
    '''Input observer.'''
    return 'JUPITER'

@pytest.fixture
def time_step():
    '''Input time step.'''
    return 1

@pytest.fixture
def time_step_units():
    '''Input time step units.'''
    return 'HOURS'

@pytest.fixture
def corr():
    '''Input aberration correction.'''
    return 'LT'

@pytest.fixture
def condition():
    '''Input coordinate search condition'''
    return {
            "coordinateSystem": "PLANETOGRAPHIC",
            "coordinate": "LONGITUDE",
            "relationalCondition": "=",
            "referenceValue": 2.19503
        }

@pytest.fixture
def params_1(kernels, intervals, target, reference_frame, observer, time_step,
             time_step_units, corr, condition):
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
        "condition": condition
    }

@pytest.fixture
def payload_1(kernels, intervals, target, reference_frame, observer, time_step,
              time_step_units, corr, condition):
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
        'condition': condition,
        'calculationType': 'GF_COORDINATE_SEARCH',
        'aberrationCorrection': corr,
        'outputDurationUnits': 'SECONDS',
        'shouldComplementWindow': False,
        'intervalAdjustment': 'NO_ADJUSTMENT',
        'intervalFiltering': 'NO_FILTERING',
        'timeSystem': 'UTC',
        'timeFormat': 'CALENDAR'
    }

@pytest.fixture
def params_2(kernels, intervals, target, reference_frame, observer, time_step,
             time_step_units, corr, condition):
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
        "condition": condition,
        "interval_adjustment": "EXPAND_INTERVALS",
        "interval_adjustment_amount": 30,
        "interval_adjustment_units": "MINUTES",
    }

@pytest.fixture
def payload_2(kernels, intervals, target, reference_frame, observer, time_step,
              time_step_units, corr, condition):
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
        'condition': condition,
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
             time_step_units, corr, condition):
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
        "condition": condition,
        "interval_filtering": "OMIT_INTERVALS_SMALLER_THAN_A_THRESHOLD",
        "interval_filtering_threshold": 30,
        "interval_filtering_threshold_units": "MINUTES",
    }

@pytest.fixture
def payload_3(kernels, intervals, target, reference_frame, observer, time_step,
              time_step_units, corr, condition):
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
        'condition': condition,
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
