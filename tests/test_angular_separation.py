"""Test WGC angular separation calculation."""

from pytest import raises

from webgeocalc import AngularSeparation
from webgeocalc.direction import Direction
from webgeocalc.errors import CalculationInvalidAttr, CalculationRequiredAttr


def test_angular_separation_two_targets_payload():
    """Test angular separation payload for TWO_TARGETS."""
    assert AngularSeparation(
        kernel_paths=[
            'pds/wgc/kernels/lsk/naif0012.tls',
            'pds/wgc/kernels/spk/de430.bsp',
        ],
        times='2012-10-19T08:24:00.000',
        # spec_type='TWO_TARGETS',  # Implicit / default
        target_1='VENUS',
        target_2='MERCURY',
        observer='SUN',
        aberration_correction='NONE',
    ) == {
        "kernels": [{
            "type": "KERNEL",
            "path": 'pds/wgc/kernels/lsk/naif0012.tls',
        }, {
            "type": "KERNEL",
            "path": 'pds/wgc/kernels/spk/de430.bsp',
        }],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": ['2012-10-19T08:24:00.000'],
        "calculationType": "ANGULAR_SEPARATION",
        "target1": 'VENUS',
        "shape1": "POINT",
        "target2": 'MERCURY',
        "shape2": "POINT",
        "observer": 'SUN',
        "aberrationCorrection": 'NONE',
    }


def test_angular_separation_two_directions_payload():
    """Test angular separation payload for TWO_DIRECTIONS."""
    assert AngularSeparation(
        kernels=5,
        times='2012-10-19T08:24:00.000',
        spec_type='TWO_DIRECTIONS',
        direction_1={
            "direction_type": "POSITION",
            "target": "SUN",
            "shape": "POINT",
            "observer": "CASSINI"
        },
        direction_2=Direction(
            direction_type='VECTOR',
            direction_vector_type='REFERENCE_FRAME_AXIS',
            direction_frame='CASSINI_RPWS_EDIPOLE',
            direction_frame_axis='Z',
        ),
    ) == {
        "kernels": [{
            "type": "KERNEL_SET",
            "id": 5,
        }],
        "specType": "TWO_DIRECTIONS",
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": ['2012-10-19T08:24:00.000'],
        "calculationType": "ANGULAR_SEPARATION",
        "direction1": {
            'aberrationCorrection': 'NONE',
            'antiVectorFlag': False,
            "directionType": "POSITION",
            "target": "SUN",
            "shape": "POINT",
            "observer": "CASSINI",
        },
        "direction2": {
            'aberrationCorrection': 'NONE',
            'antiVectorFlag': False,
            "directionType": "VECTOR",
            "directionVectorType": "REFERENCE_FRAME_AXIS",
            "directionFrame": "CASSINI_RPWS_EDIPOLE",
            "directionFrameAxis": "Z",
        },
    }


def test_angular_separation_errors():
    """Test angular separation payload errors."""
    # Missing `observer` or `target_1/2` for TWO_TARGETS
    with raises(CalculationRequiredAttr):
        AngularSeparation(
            kernels=5,
            times='2012-10-19T08:24:00.000',
            target_1='VENUS',
            target_2='MERCURY',
        )

    # Missing `direction_1/2` for TWO_DIRECTIONS
    with raises(CalculationRequiredAttr):
        AngularSeparation(
            kernels=5,
            times='2012-10-19T08:24:00.000',
            spec_type='TWO_DIRECTIONS',
            direction_1={
                "direction_type": "POSITION",
                "target": "SUN",
                "shape": "POINT",
                "observer": "CASSINI"
            },
        )

    # Invalid spec_type value
    with raises(CalculationInvalidAttr):
        AngularSeparation(
            kernels=5,
            times='2012-10-19T08:24:00.000',
            spec_type='WRONG'
        )
