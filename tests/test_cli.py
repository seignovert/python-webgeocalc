# -*- coding: utf-8 -*-
import pytest

from webgeocalc.cli import cli_kernel_sets, cli_bodies


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
    assert ' - Solar System Kernels: (id: 1)' in captured.out
    assert 'Too many kernel sets contains \'Cassini\' in their names:'  in captured.out

def test_cli_bodies(capsys):

    argv = ''.split()
    cli_bodies(argv)
    captured = capsys.readouterr()
    assert 'usage:' in captured.out

    argv = ['Cassini Huygens']
    cli_bodies(argv)
    captured = capsys.readouterr()
    assert ' - CASSINI: (id: -82)' in captured.out
    assert ' - TITAN: (id: 606)' in captured.out

    argv = '5 --name Titan'.split()
    cli_bodies(argv)
    captured = capsys.readouterr()
    assert ' - TITAN: (id: 606)\n' == captured.out
