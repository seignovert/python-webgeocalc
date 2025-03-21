"""Test WGC time conversion calculation."""

from webgeocalc import TimeConversion


def test_time_conversion_payload():
    """Test time conversion payload with spacecraft clock input."""
    assert TimeConversion(
        kernels=5,
        times='1/1729329441.042',
        time_system='SPACECRAFT_CLOCK',
        time_format='SPACECRAFT_CLOCK_STRING',
        sclk_id=-82,
    ) == {
        "kernels": [{"type": "KERNEL_SET", "id": 5}],
        "times": ['1/1729329441.042'],
        "calculationType": "TIME_CONVERSION",
        "timeSystem": 'SPACECRAFT_CLOCK',
        "timeFormat": 'SPACECRAFT_CLOCK_STRING',
        "sclkId": -82,
        "outputTimeSystem": "UTC",
        "outputTimeFormat": "CALENDAR",
    }


def test_time_conversion_custom_format_payload():
    """Test time conversion payload with custom format output."""
    assert TimeConversion(
        kernels=5,
        times='2012-10-19T08:24:00.000',
        output_time_format='CUSTOM',
        output_time_custom_format='YYYY Month DD HR:MN',
    ) == {
        "kernels": [{"type": "KERNEL_SET", "id": 5}],
        "times": ['2012-10-19T08:24:00.000'],
        "calculationType": "TIME_CONVERSION",
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "outputTimeSystem": "UTC",
        "outputTimeFormat": 'CUSTOM',
        "outputTimeCustomFormat": 'YYYY Month DD HR:MN',
    }
