# -*- coding: utf-8 -*-
import pytest
import requests_mock

from webgeocalc import SubObserverPoint

@pytest.fixture
def kernels():
    return 5 # Cassini-Huygens

@pytest.fixture
def time():
    return '2012-10-19T08:24:00.000'

@pytest.fixture
def target():
    return 'ENCELADUS'

@pytest.fixture
def target_frame():
    return 'IAU_ENCELADUS'

@pytest.fixture
def observer():
    return 'CASSINI'

@pytest.fixture
def corr():
    return 'CN+S'

@pytest.fixture
def params(kernels, time, target, target_frame, observer, corr):
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
    assert SubObserverPoint(**params).payload == payload
