"""Webgeocalc decorators."""

from .errors import CalculationInvalidAttr
from .vars import VALID_PARAMETERS


def parameter(_func=None, *, only=None):
    """Parameter decorator setter with a validation check.

    Can be used in the following forms:

    - @parameter
    - @parameter()
    - @parameter(only='VALID_PARAMETERS_KEY')

    Parameters
    ----------
    func: callable, optional
        Setter function.
    only: str
        Validator parameter key.

    Raises
    ------
    AttributeError
        If the user try to access the decorated function.
    KeyError
        If the provided key (in `only`) is not in the ``VALID_PARAMETERS``.
    CalculationInvalidAttr
        If the provided value is not valid.

    Note
    ----
    The decorator is defined as a `setter` only.
    The decorated function do not return a value (raises an ``AttributeError``).

    """

    def decorator(func):
        """Decorator setter with valid checker."""

        def fset(_self, value):
            """Parameter setter."""
            if only and value not in VALID_PARAMETERS[only]:
                raise CalculationInvalidAttr(
                    name=only,
                    attr=value,
                    valids=VALID_PARAMETERS[only],
                )
            return func(_self, value)

        return property(fset=fset, doc=func.__doc__)

    return decorator if _func is None else decorator(_func)
