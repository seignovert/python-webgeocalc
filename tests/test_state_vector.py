"""Test WGC state vector calculation."""

from webgeocalc import StateVector


def test_state_vector_payload():
    """Test state vector payload."""
    assert StateVector(
        kernels=5,
        target='CASSINI',
        observer='SATURN',
        reference_frame='IAU_SATURN',
        times='2012-10-19T08:24:00.000',
        aberration_correction='NONE',
        state_representation='PLANETOGRAPHIC',
    ) == {
        "kernels": [{"type": "KERNEL_SET", "id": 5}],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": ['2012-10-19T08:24:00.000'],
        "calculationType": "STATE_VECTOR",
        "target": 'CASSINI',
        "observer": 'SATURN',
        "referenceFrame": 'IAU_SATURN',
        "aberrationCorrection": 'NONE',
        "stateRepresentation": 'PLANETOGRAPHIC',
    }
