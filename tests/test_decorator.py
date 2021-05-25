"""Test Webgeocalc decorators."""

from pytest import raises

from webgeocalc.decorator import parameter
from webgeocalc.errors import CalculationInvalidAttr


def test_decorator_parameter():
    """Test decorator parameter."""
    class A:
        """Dummy class."""

        @parameter
        def foo(self, value):
            """Dummy parameter."""
            self.foo_ = value

        @parameter()
        def bar(self, value):
            """Dummy parameter with ()."""
            self.bar_ = value

        @parameter(only='CALCULATION_TYPE')
        def baz(self, value):
            """Dummy parameter with a valid ``only``."""
            self.baz_ = value

        @parameter(only='WRONG')
        def qux(self, value):
            """Dummy parameter with an invalid ``only``."""
            self.qux_ = value

    a = A()

    # Generic setter without @parameter decorator
    setattr(a, 'b', 10)
    assert a.b == 10     # pylint: disable=no-member

    # Decorator without parenthesis: @parameter
    setattr(a, 'foo', 20)
    assert a.foo_ == 20

    # The attribute ``foo`` should not be defined (setter only).
    with raises(AttributeError):
        _ = a.foo

    # Decorator with parenthesis: @parameter()
    setattr(a, 'bar', 30)
    assert a.bar_ == 30

    # Decorator with a valid `only` key and a valid value
    setattr(a, 'baz', 'STATE_VECTOR')
    assert a.baz_ == 'STATE_VECTOR'

    # Decorator with a valid `only` key and an invalid value
    err = "Attribute 'CALCULATION_TYPE'='WRONG' is only applicable with:\n - STATE_VECTOR"
    with raises(CalculationInvalidAttr, match=err):
        setattr(a, 'baz', 'WRONG')

    # Decorator with an invalid `only` key (not in VALID_PARAMETERS)
    with raises(KeyError):
        setattr(a, 'qux', 'STATE_VECTOR')
