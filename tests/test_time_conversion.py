# -*- coding: utf-8 -*-
import pytest
import requests_mock

from webgeocalc import TimeConversion

@pytest.fixture
def kernels():
    return 5

@pytest.fixture
def time():
    return '1/1729329441.042'

@pytest.fixture
def time_2():
    return '2012-10-19T08:24:00.000'

@pytest.fixture
def time_system():
    return 'SPACECRAFT_CLOCK'

@pytest.fixture
def time_format():
    return 'SPACECRAFT_CLOCK_STRING'

@pytest.fixture
def sclk_id():
    return -82 # Cassini Spacecraft

@pytest.fixture
def output_time_format():
    return 'CUSTOM'

@pytest.fixture
def output_time_custom_format():
    return 'YYYY Month DD HR:MN'

@pytest.fixture
def params(kernels, time, time_system, time_format, sclk_id):
    return {
        'kernels': kernels,
        'times': time,
        'time_system': time_system,
        'time_format': time_format,
        'sclk_id': sclk_id,
    }

@pytest.fixture
def payload(kernels, time, time_system, time_format, sclk_id):
    return {
        "kernels": [{
            "type": "KERNEL_SET",
            "id": kernels,
        }],
        "times": [
            time,
        ],
        "calculationType": "TIME_CONVERSION",
        "timeSystem": time_system,
        "timeFormat": time_format,
        "sclkId": sclk_id,
        "outputTimeSystem": "UTC",
        "outputTimeFormat": "CALENDAR",
    }

@pytest.fixture
def params_2(kernels, time_2, output_time_format, output_time_custom_format):
    return {
        'kernels': kernels,
        'times': time_2,
        'output_time_format': output_time_format,
        'output_time_custom_format': output_time_custom_format,
    }

@pytest.fixture
def payload_2(kernels, time_2, output_time_format, output_time_custom_format):
    return {
        "kernels": [{
            "type": "KERNEL_SET",
            "id": kernels,
        }],
        "times": [
            time_2,
        ],
        "calculationType": "TIME_CONVERSION",
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "outputTimeSystem": "UTC",
        "outputTimeFormat": output_time_format,
        "outputTimeCustomFormat": output_time_custom_format,
    }

def test_time_conversion_payload(params, payload):
    assert TimeConversion(**params).payload == payload

def test_time_conversion_custom_format_payload(params_2, payload_2):
    assert TimeConversion(**params_2).payload == payload_2
