# -*- coding: utf-8 -*-
import pytest
import requests_mock

from webgeocalc import OsculatingElements

@pytest.fixture
def kernels():
    return [1, 5]

@pytest.fixture
def time():
    return '2012-10-19T08:24:00.000'

@pytest.fixture
def orbiting():
    return 'CASSINI'

@pytest.fixture
def center():
    return 'SATURN'


@pytest.fixture
def params(kernels, time, orbiting, center):
    return {
        'kernels': kernels,
        'times': time,
        'orbiting_body': orbiting,
        'center_body': center,
    }

@pytest.fixture
def payload(kernels, time, orbiting, center):
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
    assert OsculatingElements(**params).payload == payload
