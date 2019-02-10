# -*- coding: utf-8 -*-
'''Test WGC time conversion calculation.'''

import pytest

from webgeocalc import TimeConversion

@pytest.fixture
def kernels():
    '''Cassini kernel set.'''
    return 5

@pytest.fixture
def time_1():
    '''Input time in spacecraft clock format.'''
    return '1/1729329441.042'

@pytest.fixture
def time_2():
    '''Input time 2.'''
    return '2012-10-19T08:24:00.000'

@pytest.fixture
def time_system():
    '''Input time system.'''
    return 'SPACECRAFT_CLOCK'

@pytest.fixture
def time_format():
    '''Input time format.'''
    return 'SPACECRAFT_CLOCK_STRING'

@pytest.fixture
def sclk_id():
    '''Cassini spacecraft id.'''
    return -82

@pytest.fixture
def output_time_format():
    '''Input output time format.'''
    return 'CUSTOM'

@pytest.fixture
def output_time_custom_format():
    '''Input output time custom format.'''
    return 'YYYY Month DD HR:MN'

@pytest.fixture
def params_1(kernels, time_1, time_system, time_format, sclk_id):
    '''Input parameters from WGC API example 1.'''
    return {
        'kernels': kernels,
        'times': time_1,
        'time_system': time_system,
        'time_format': time_format,
        'sclk_id': sclk_id,
    }

@pytest.fixture
def payload_1(kernels, time_1, time_system, time_format, sclk_id):
    '''Payload from WGC API example 1.'''
    return {
        "kernels": [{
            "type": "KERNEL_SET",
            "id": kernels,
        }],
        "times": [
            time_1,
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
    '''Input parameters from WGC API example 2.'''
    return {
        'kernels': kernels,
        'times': time_2,
        'output_time_format': output_time_format,
        'output_time_custom_format': output_time_custom_format,
    }

@pytest.fixture
def payload_2(kernels, time_2, output_time_format, output_time_custom_format):
    '''Payload from WGC API example 2.'''
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

def test_time_conversion_payload(params_1, payload_1):
    '''Test time conversion payload with spacecraft clock input.'''
    assert TimeConversion(**params_1).payload == payload_1

def test_time_conversion_custom_format_payload(params_2, payload_2):
    '''Test time conversion payload with custom format output.'''
    assert TimeConversion(**params_2).payload == payload_2
