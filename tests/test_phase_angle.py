"""Test WGC phase angle calculation."""

from webgeocalc import PhaseAngle


def test_phase_angle_payload():
    """Test phase angle payload."""
    assert PhaseAngle(
        kernels=5,
        times='2012-10-19T08:24:00.000',
        target='CASSINI',
        observer='SATURN',
        aberration_correction='CN+S',
    ) == {
        "kernels": [{"type": "KERNEL_SET", "id": 5}],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": ['2012-10-19T08:24:00.000'],
        "calculationType": "PHASE_ANGLE",
        "target": 'CASSINI',
        "observer": 'SATURN',
        "illuminator": 'SUN',
        "aberrationCorrection": 'CN+S',
    }
