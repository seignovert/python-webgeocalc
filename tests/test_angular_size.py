"""Test WGC angular size calculation."""

from webgeocalc import AngularSize


def test_angular_size_payload():
    """Test angular size payload."""
    assert AngularSize(
        kernels=5,  # Cassini-Huygens
        times='2012-10-19T08:24:00.000',
        target='ENCELADUS',
        observer='CASSINI',
        aberration_correction='CN+S',
    ) == {
        "kernels": [{"type": "KERNEL_SET", "id": 5}],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": ['2012-10-19T08:24:00.000'],
        "calculationType": "ANGULAR_SIZE",
        "target": 'ENCELADUS',
        "observer": 'CASSINI',
        "aberrationCorrection": 'CN+S',
    }
