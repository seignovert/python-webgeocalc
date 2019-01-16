# -*- coding: utf-8 -*-
import pytest

from webgeocalc import Calculation

@pytest.fixture
def cassini_payload():
    return '{"kernels":[{"type":"KERNEL_SET","id":5}]}'

@pytest.fixture
def solar_cassini_payload():
    return '{"kernels":[{"type":"KERNEL_SET","id":1},{"type":"KERNEL_SET","id":5}]}'

@pytest.fixture
def individual_kernel_path():
    return 'https://path.to.server/kernel'

@pytest.fixture
def individual_kernel_payload(individual_kernel_path):
    return '{"kernels":[{"type":"KERNEL","path":"%s"}]}' % individual_kernel_path


def test_kernel_single_payload(cassini_payload):
    assert Calculation('Cassini Huygens').payload == cassini_payload


def test_kernel_multiple_payload(solar_cassini_payload):
    assert Calculation([1, 'Cassini Huygens']).payload == solar_cassini_payload


def test_kernel_custom_payload(individual_kernel_path, individual_kernel_payload):
    calc = Calculation(None)
    calc.add_kernel_path(individual_kernel_path)
    assert calc.payload == individual_kernel_payload
