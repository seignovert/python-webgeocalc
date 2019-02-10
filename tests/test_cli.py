# -*- coding: utf-8 -*-
'''Test WGC command line inputs.'''

from webgeocalc.cli import cli_bodies, cli_frames, cli_instruments, cli_kernel_sets


def test_cli_kernel_sets(capsys):
    '''Test GET kernels with CLI.'''
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
    assert 'Too many kernel sets contains \'Cassini\' in their names:' in captured.out

def test_cli_bodies(capsys):
    '''Test GET bodies with CLI.'''
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

def test_cli_frames(capsys):
    '''Test GET frames with CLI.'''
    argv = ''.split()
    cli_frames(argv)
    captured = capsys.readouterr()
    assert 'usage:' in captured.out

    argv = ['Cassini Huygens']
    cli_frames(argv)
    captured = capsys.readouterr()
    assert ' - IAU_TITAN: (id: 10044)' in captured.out
    assert ' - J2000: (id: 1)' in captured.out

    argv = '5 --name Titan'.split()
    cli_frames(argv)
    captured = capsys.readouterr()
    assert ' - IAU_TITAN: (id: 10044)' in captured.out
    assert ' - J2000: (id: 1)' not in captured.out

def test_cli_instruments(capsys):
    '''Test GET instruments with CLI.'''
    argv = ''.split()
    cli_instruments(argv)
    captured = capsys.readouterr()
    assert 'usage:' in captured.out

    argv = ['Cassini Huygens']
    cli_instruments(argv)
    captured = capsys.readouterr()
    assert ' - CASSINI_ISS_WAC: (id: -82361)' in captured.out
    assert ' - CASSINI_VIMS_IR: (id: -82370)' in captured.out

    argv = '5 --name ISS'.split()
    cli_instruments(argv)
    captured = capsys.readouterr()
    assert ' - CASSINI_ISS_WAC: (id: -82361)' in captured.out
    assert ' - CASSINI_VIMS_IR: (id: -82370)' not in captured.out
