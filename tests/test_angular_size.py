"""Test WGC angular size calculation."""

from pytest import fixture

from webgeocalc import AngularSize


@fixture
def kernels():
    """Input kernel."""
    return 5  # Cassini-Huygens


@fixture
def time():
    """Input time."""
    return '2012-10-19T08:24:00.000'


@fixture
def target():
    """Input target name."""
    return 'ENCELADUS'


@fixture
def observer():
    """Input observer name."""
    return 'CASSINI'


@fixture
def corr():
    """Input aberration correction."""
    return 'CN+S'


@fixture
def params(kernels, time, target, observer, corr):
    """Input parameters from WGC API example."""
    return {
        'kernels': kernels,
        'times': time,
        'target': target,
        'observer': observer,
        'aberration_correction': corr,
    }


@fixture
def payload(kernels, time, target, observer, corr):
    """Payload from WGC API example."""
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
    """Test angular size payload."""
    assert AngularSize(**params).payload == payload
