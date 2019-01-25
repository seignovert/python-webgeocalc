# -*- coding: utf-8 -*-
import pytest
import requests_mock

from webgeocalc import AngularSeparation

@pytest.fixture
def kernel_paths():
    return [
        'pds/wgc/kernels/lsk/naif0012.tls',
        'pds/wgc/kernels/spk/de430.bsp',
    ]

@pytest.fixture
def time():
    return '2012-10-19T08:24:00.000'

@pytest.fixture
def target_1():
    return 'VENUS'

@pytest.fixture
def target_2():
    return 'MERCURY'

@pytest.fixture
def observer():
    return 'SUN'

@pytest.fixture
def corr():
    return 'NONE'

@pytest.fixture
def params(kernel_paths, time, target_1, target_2, observer, corr):
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
    assert AngularSeparation(**params).payload == payload