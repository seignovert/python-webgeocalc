"""Test WGC angular size calculation."""

from pytest import fixture

from webgeocalc import OsculatingElements


@fixture
def kernels():
    """Kernels sets Solar and Cassini."""
    return [1, 5]


@fixture
def time():
    """Input time."""
    return '2012-10-19T08:24:00.000'


@fixture
def orbiting():
    """Orbiting body."""
    return 'CASSINI'


@fixture
def center():
    """Center body."""
    return 'SATURN'


@fixture
def params(kernels, time, orbiting, center):
    """Input parameters from WGC API example."""
    return {
        'kernels': kernels,
        'times': time,
        'orbiting_body': orbiting,
        'center_body': center,
    }


@fixture
def payload(kernels, time, orbiting, center):
    """Payload from WGC API example."""
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
    """Test osculating elements payload."""
    assert OsculatingElements(**params).payload == payload
