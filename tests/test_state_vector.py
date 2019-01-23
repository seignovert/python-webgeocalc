# -*- coding: utf-8 -*-
import pytest
import requests_mock

from webgeocalc import StateVector
from webgeocalc.errors import CalculationRequiredAttr
from webgeocalc.vars import API_URL

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

@pytest.fixture
def new_calculation_response():
    return {
        "status": "OK",
        "message": "The operation was successful.",
        "calculationId": "0788aba2-d4e5-4028-9ef1-4867ad5385e0",
        "result": {
            "phase": "COMPLETE",
            "progress": 0
        }
    }

def test_state_vector_payload(params, payload):
    assert StateVector(**params).payload == payload


def test_state_vector_required_err(params, payload):
    with pytest.raises(CalculationRequiredAttr):
        StateVector()


def test_state_vector_submit(requests_mock, params, new_calculation_response):
    requests_mock.post(API_URL + '/calculation/new', json=new_calculation_response)
    calculation = StateVector(**params)
    
    calculation.submit()
    assert calculation.id == new_calculation_response['calculationId']

