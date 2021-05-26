"""WebGeoCalc columns and results types."""

from .errors import ResultAttributeError, ResultTypeError


def get_type(classname):
    """Get type based on classname."""
    if classname not in TYPES:
        raise ResultTypeError(classname)
    return TYPES[classname]


class ColumnResult:
    """Column result generic object."""

    def __init__(self, json):
        self._json = json

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__}> {str(self)}"

    def __getattr__(self, attr):
        if attr not in self._json.keys():
            raise ResultAttributeError(self, attr)
        return self._json[attr]

    def keys(self):
        """JSON keys."""
        return self._json.keys()

    def values(self):
        """JSON values."""
        return self._json.values()

    def items(self):
        """JSON items."""
        return self._json.items()


class ResultType(ColumnResult):
    """Result Type object for item generic interface."""

    def __int__(self):
        return int(self.id)

    def __repr__(self):
        return f"<{self.__class__.__name__}> {str(self)} (id: {int(self)})"

    def __contains__(self, item):
        """Check if items is equal to int or str."""
        if isinstance(item, int):
            return item == int(self)
        return item.lower() in str(self).lower()


class KernelSetDetails(ResultType):
    """Kernel set details."""

    def __int__(self):
        return int(self.kernelSetId)

    def __str__(self):
        return self.caption


class BodyData(ResultType):
    """Body data."""


class FrameData(ResultType):
    """Frame data."""


class InstrumentData(ResultType):
    """Instrument data."""


TYPES = globals()
