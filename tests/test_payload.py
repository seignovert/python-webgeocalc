"""Test WebGeoCalc payload abstract class."""

from pytest import raises

from webgeocalc.decorator import parameter
from webgeocalc.errors import CalculationRequiredAttr
from webgeocalc.payload import Payload


def test_payload_abstract():
    """Test payload abstract class."""
    p = Payload(foo='bar')

    # Input parameters
    assert p.params == {'foo': 'bar'}

    # No parameter explicitly defined (with @parameter)
    assert not p.payload

    # Keywords are set as regular properties
    getattr(p, 'foo', 'bar')

    assert repr(p) == '<Payload>'


def test_payload_derived():
    """Test payload derived class."""
    class DerivedPayload(Payload):
        """Derived payload class."""

        REQUIRED = ('foo',)

        @parameter  # required
        def foo(self, val):
            """Foo parameter."""
            self.__foo = val

        @parameter(only='AXIS')  # optional
        def baz(self, val):
            """Baz parameter."""
            self.__baz = val

    # With all parameters (and more)
    d = DerivedPayload(foo='bar', baz='X', qux='quux')

    assert d.params == {'foo': 'bar', 'baz': 'X', 'qux': 'quux'}
    assert d.payload == {'foo': 'bar', 'baz': 'X'}  # parameters only

    assert repr(d) == '<DerivedPayload>\n - foo: bar\n - baz: X'

    # __iter__
    for key, value in d:
        assert key == 'foo'
        assert value == 'bar'
        break

    # Only with required parameter(s)
    assert DerivedPayload(foo='bar').payload == {'foo': 'bar'}

    # Without required parameter(s)
    with raises(CalculationRequiredAttr):
        _ = DerivedPayload()
