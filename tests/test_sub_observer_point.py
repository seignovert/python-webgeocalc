# -*- coding: utf-8 -*-
'''Test WGC sub observer point calculation.'''

import pytest

from webgeocalc import SubObserverPoint

@pytest.fixture
def kernels():
    '''Cassini kernel set.'''
    return 5

@pytest.fixture
def time():
    '''Input time.'''
    return '2012-10-19T08:24:00.000'

@pytest.fixture
def target():
    '''Input target.'''
    return 'ENCELADUS'

@pytest.fixture
def target_frame():
    '''Input target frame.'''
    return 'IAU_ENCELADUS'

@pytest.fixture
def observer():
    '''Input observer.'''
    return 'CASSINI'

@pytest.fixture
def corr():
    '''Input aberration correction.'''
    return 'CN+S'

@pytest.fixture
def params(kernels, time, target, target_frame, observer, corr):
    '''Input parameters from WGC API example.'''
    return {
        'kernels': kernels,
        'times': time,
        'target': target,
        'target_frame': target_frame,
        'observer': observer,
        'aberration_correction': corr,
    }

@pytest.fixture
def payload(kernels, time, target, target_frame, observer, corr):
    '''Payload from WGC API example.'''
    return {
        "kernels": [{
            "type": "KERNEL_SET",
            "id": kernels,
        }],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": [
            time,
        ],
        "calculationType": "SUB_OBSERVER_POINT",
        "target": target,
        "targetFrame": target_frame,
        "observer": observer,
        "subPointType": "Near point: ellipsoid",
        "aberrationCorrection": corr,
        "stateRepresentation": "RECTANGULAR",
    }

def test_sub_observer_point_payload(params, payload):
    '''Test sub observer point payload.'''
    assert SubObserverPoint(**params).payload == payload
