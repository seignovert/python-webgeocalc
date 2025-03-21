"""WebGeoCalc Payload submodule."""

from abc import ABC

from .errors import CalculationRequiredAttr


class Payload(ABC):
    """Abstract WebGeoCalc payload abstract class.

    Check if any required parameters is missing.

    Raises
    ------
    CalculationRequiredAttr
        If any parameter in :py:attr:`REQUIRED` is not provided.

    """

    REQUIRED = ()

    def __init__(self, **kwargs):
        # Init parameters
        self.params = kwargs

        # Check required parameters
        self._required(*self.REQUIRED)

        # Set parameters
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return '\n'.join([
            f"<{self.__class__.__name__}>"
        ] + [
            f' - {k}: {v}' for k, v in self
        ])

    def __iter__(self):
        return (
            (k.split('__')[-1], v)
            for k, v in vars(self).items()
            if k.startswith('_')
        )

    def __eq__(self, other):
        return self.payload == other

    def _required(self, *attrs):
        """Check if the required arguments are in the params."""
        for attr in attrs:
            if attr not in self.params:
                raise CalculationRequiredAttr(attr)

    @property
    def payload(self) -> dict:
        """Payload parameters *dict* for JSON input in WebGeoCalc format.

        Collect all the properties prefixed with ``__*``.

        Return
        ------
        dict:
            Payload keys and values.

        """
        return dict(self)
