"""Test WGC sub observer point calculation."""

from webgeocalc import SubObserverPoint


def test_sub_observer_point_payload():
    """Test sub observer point payload."""
    assert SubObserverPoint(
        kernels=5,
        times='2012-10-19T08:24:00.000',
        target='ENCELADUS',
        target_frame='IAU_ENCELADUS',
        observer='CASSINI',
        aberration_correction='CN+S',
    ) == {
        "kernels": [{"type": "KERNEL_SET", "id": 5}],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": ['2012-10-19T08:24:00.000'],
        "calculationType": "SUB_OBSERVER_POINT",
        "target": 'ENCELADUS',
        "targetFrame": 'IAU_ENCELADUS',
        "observer": 'CASSINI',
        "subPointType": "Near point: ellipsoid",
        "aberrationCorrection": 'CN+S',
        "stateRepresentation": "RECTANGULAR",
    }
