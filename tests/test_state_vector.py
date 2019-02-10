# -*- coding: utf-8 -*-
'''Test WGC state vector calculation.'''

import pytest

from webgeocalc import StateVector

@pytest.fixture
def kernels():
    '''Cassini kernel set.'''
    return 5

@pytest.fixture
def target():
    '''Input target.'''
    return 'CASSINI'

@pytest.fixture
def observer():
    '''Input observer.'''
    return 'SATURN'

@pytest.fixture
def frame():
    '''Input frame.'''
    return 'IAU_SATURN'

@pytest.fixture
def time():
    '''Input time.'''
    return '2012-10-19T08:24:00.000'

@pytest.fixture
def corr():
    '''Input aberration correction.'''
    return 'NONE'

@pytest.fixture
def state():
    '''Input state.'''
    return 'PLANETOGRAPHIC'

@pytest.fixture
def params(kernels, target, observer, frame, time, corr, state):
    '''Input parameters from WGC API example.'''
    return {
        'kernels': kernels,
        'target': target,
        'observer': observer,
        'reference_frame': frame,
        'times': time,
        'aberration_correction': corr,
        'state_representation': state,
    }

@pytest.fixture
def payload(kernels, target, observer, frame, time, corr, state):
    '''Payload from WGC API example.'''
    return {
        "kernels": [
            {
                "type": "KERNEL_SET",
                "id": kernels
            }
        ],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": [
            time
        ],
        "calculationType": "STATE_VECTOR",
        "target": target,
        "observer": observer,
        "referenceFrame": frame,
        "aberrationCorrection": corr,
        "stateRepresentation": state
    }

def test_state_vector_payload(params, payload):
    '''Test state vector payload.'''
    assert StateVector(**params).payload == payload
