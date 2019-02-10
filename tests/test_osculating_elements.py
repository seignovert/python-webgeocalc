# -*- coding: utf-8 -*-
'''Test WGC angular size calculation.'''

import pytest

from webgeocalc import OsculatingElements

@pytest.fixture
def kernels():
    '''Kernels sets Solar and Cassini.'''
    return [1, 5]

@pytest.fixture
def time():
    '''Input time.'''
    return '2012-10-19T08:24:00.000'

@pytest.fixture
def orbiting():
    '''Orbiting body.'''
    return 'CASSINI'

@pytest.fixture
def center():
    '''Center body.'''
    return 'SATURN'


@pytest.fixture
def params(kernels, time, orbiting, center):
    '''Input parameters from WGC API example.'''
    return {
        'kernels': kernels,
        'times': time,
        'orbiting_body': orbiting,
        'center_body': center,
    }

@pytest.fixture
def payload(kernels, time, orbiting, center):
    '''Payload from WGC API example.'''
    return {
        "kernels": [{
            "type": "KERNEL_SET",
            "id": kernels[0],
        }, {
            "type": "KERNEL_SET",
            "id": kernels[1],
        }],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": [
            time,
        ],
        "calculationType": "OSCULATING_ELEMENTS",
        "orbitingBody": orbiting,
        "centerBody": center,
        "referenceFrame": "J2000",
    }

def test_osculating_elements_payload(params, payload):
    '''Test osculating elements payload.'''
    assert OsculatingElements(**params).payload == payload
