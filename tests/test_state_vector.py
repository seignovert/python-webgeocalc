# -*- coding: utf-8 -*-
import pytest
import requests_mock

from webgeocalc import StateVector
from webgeocalc.errors import CalculationRequiredAttr

@pytest.fixture
def kernels():
    return 5 # 'Cassini Huygens' kernel set

@pytest.fixture
def target():
    return 'CASSINI'

@pytest.fixture
def observer():
    return 'SATURN'

@pytest.fixture
def frame():
    return 'IAU_SATURN'

@pytest.fixture
def time():
    return '2012-10-19T08:24:00.000'

@pytest.fixture
def corr():
    return 'NONE'

@pytest.fixture
def state():
    return 'PLANETOGRAPHIC'

@pytest.fixture
def params(kernels, target, observer, frame, time, corr, state):
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
    assert StateVector(**params).payload == payload


def test_state_vector_required_err(params, payload):
    with pytest.raises(CalculationRequiredAttr):
        StateVector()