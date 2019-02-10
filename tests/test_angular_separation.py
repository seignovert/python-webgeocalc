# -*- coding: utf-8 -*-
'''Test WGC angular separation calculation.'''

import pytest

from webgeocalc import AngularSeparation

@pytest.fixture
def kernel_paths():
    '''Input kernel paths.'''
    return [
        'pds/wgc/kernels/lsk/naif0012.tls',
        'pds/wgc/kernels/spk/de430.bsp',
    ]

@pytest.fixture
def time():
    '''Input time.'''
    return '2012-10-19T08:24:00.000'

@pytest.fixture
def target_1():
    '''Input name for the first target.'''
    return 'VENUS'

@pytest.fixture
def target_2():
    '''Input name for the second target.'''
    return 'MERCURY'

@pytest.fixture
def observer():
    '''Input name of the observer.'''
    return 'SUN'

@pytest.fixture
def corr():
    '''Input aberration correction.'''
    return 'NONE'

@pytest.fixture
def params(kernel_paths, time, target_1, target_2, observer, corr):
    '''Input parameters from WGC API example.'''
    return {
        'kernel_paths': kernel_paths,
        'times': time,
        'target_1': target_1,
        'target_2': target_2,
        'observer': observer,
        'aberration_correction': corr,
    }

@pytest.fixture
def payload(kernel_paths, time, target_1, target_2, observer, corr):
    '''Payload from WGC API example.'''
    return {
        "kernels": [{
            "type": "KERNEL",
            "path": kernel_paths[0],
        }, {
            "type": "KERNEL",
            "path": kernel_paths[1],
        }],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": [
            time,
        ],
        "calculationType": "ANGULAR_SEPARATION",
        "target1": target_1,
        "shape1": "POINT",
        "target2": target_2,
        "shape2": "POINT",
        "observer": observer,
        "aberrationCorrection": corr
    }

def test_angular_separation_payload(params, payload):
    '''Test angular separation payload.'''
    assert AngularSeparation(**params).payload == payload
