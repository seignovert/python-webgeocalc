"""Test WGC angular separation calculation."""

from pytest import fixture

from webgeocalc import AngularSeparation


@fixture
def kernel_paths():
    """Input kernel paths."""
    return [
        'pds/wgc/kernels/lsk/naif0012.tls',
        'pds/wgc/kernels/spk/de430.bsp',
    ]


@fixture
def time():
    """Input time."""
    return '2012-10-19T08:24:00.000'


@fixture
def target_1():
    """Input name for the first target."""
    return 'VENUS'


@fixture
def target_2():
    """Input name for the second target."""
    return 'MERCURY'


@fixture
def observer():
    """Input name of the observer."""
    return 'SUN'


@fixture
def corr():
    """Input aberration correction."""
    return 'NONE'


@fixture
def params(kernel_paths, time, target_1, target_2, observer, corr):
    """Input parameters from WGC API example."""
    return {
        'kernel_paths': kernel_paths,
        'times': time,
        'target_1': target_1,
        'target_2': target_2,
        'observer': observer,
        'aberration_correction': corr,
    }


@fixture
def payload(kernel_paths, time, target_1, target_2, observer, corr):
    """Payload from WGC API example."""
    return {
        "kernels": [{
            "type": "KERNEL",
            "path": kernel_paths[0],
        }, {
            "type": "KERNEL",
            "path": kernel_paths[1],
        }],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": [
            time,
        ],
        "calculationType": "ANGULAR_SEPARATION",
        "target1": target_1,
        "shape1": "POINT",
        "target2": target_2,
        "shape2": "POINT",
        "observer": observer,
        "aberrationCorrection": corr
    }


def test_angular_separation_payload(params, payload):
    """Test angular separation payload."""
    assert AngularSeparation(**params).payload == payload
