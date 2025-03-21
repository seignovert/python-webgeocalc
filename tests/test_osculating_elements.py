"""Test WGC angular size calculation."""

from webgeocalc import OsculatingElements


def test_osculating_elements_payload():
    """Test osculating elements payload."""
    assert OsculatingElements(
        kernels=[1, 5],
        times='2012-10-19T08:24:00.000',
        orbiting_body='CASSINI',
        center_body='SATURN',
    ) == {
        "kernels": [
            {"type": "KERNEL_SET", "id": 1},
            {"type": "KERNEL_SET", "id": 5},
        ],
        "timeSystem": "UTC",
        "timeFormat": "CALENDAR",
        "times": ['2012-10-19T08:24:00.000'],
        "calculationType": "OSCULATING_ELEMENTS",
        "orbitingBody": 'CASSINI',
        "centerBody": 'SATURN',
        "referenceFrame": "J2000",
    }
