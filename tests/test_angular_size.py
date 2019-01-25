# -*- coding: utf-8 -*-
import pytest
import requests_mock

from webgeocalc import AngularSize
from webgeocalc.errors import CalculationRequiredAttr

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
def observer():
    return 'CASSINI'

@pytest.fixture
def corr():
    return 'CN+S'

@pytest.fixture
def params(kernels, time, target, observer, corr):
    return {
        'kernels': kernels,
        'times': time,
        'target': target,
        'observer': observer,
        'aberration_correction': corr,
    }

@pytest.fixture
def payload(kernels, time, target, observer, corr):
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
        "calculationType": "ANGULAR_SIZE",
        "target": target,
        "observer": observer,
        "aberrationCorrection": corr
    }

def test_angular_size_payload(params, payload):
    assert AngularSize(**params).payload == payload


def test_angular_size_required_err(params, payload):
    with pytest.raises(CalculationRequiredAttr):
        AngularSize()
