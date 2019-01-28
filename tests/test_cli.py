# -*- coding: utf-8 -*-
import pytest

from webgeocalc.cli import cli_kernel_sets
from webgeocalc.types import KernelSetDetails


def test_cli_kernel_sets(capsys):

    argv = ''.split()
    cli_kernel_sets(argv)
    captured = capsys.readouterr()
    assert 'usage:' in captured.out

    argv = '--all'.split()
    cli_kernel_sets(argv)
    captured = capsys.readouterr()
    assert ' - Solar System Kernels: (id: 1)' in captured.out
    assert ' - Cassini Huygens: (id: 5)' in captured.out

    argv = '--kernel 1 Cassini'.split()
    cli_kernel_sets(argv)
    captured = capsys.readouterr()
    assert ' - Solar System Kernels: (id: 1)\n'  in captured.out
    assert 'Too many kernel sets contains \'Cassini\' in their names:'  in captured.out
