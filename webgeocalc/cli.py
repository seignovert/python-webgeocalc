# -*- coding: utf-8 -*-
import argparse

from .api import API
from .errors import KernelSetNotFound, TooManyKernelSets

def cli_kernel_sets(argv=None):
    '''
        Get list of kernel sets available on the server.
        GET: /kernel-sets
    '''
    parser = argparse.ArgumentParser(description='List and search kernel sets available in WebGeocalc API.')
    parser.add_argument('--all', '-a', action='store_true', help='List all kernel sets available')
    parser.add_argument('--kernel', '-k', metavar='NAME|ID', nargs='+', help='Search a specific kernel by name or id')

    args, others = parser.parse_known_args(argv)

    if args.all:
        kernels = API.kernel_sets()
        print('\n'.join([f" - {str(kernel)}: (id: {int(kernel)})" for kernel in kernels]))

    elif args.kernel:
        for kernel in args.kernel:
            try:
                kernel = int(kernel)
            except ValueError:
                pass

            try:
                kernel = API.kernel_set(kernel)
                print(f" - {str(kernel)}: (id: {int(kernel)})")

            except (KernelSetNotFound, TooManyKernelSets) as err:
                print(err)
    else:
        parser.print_help()


def cli_bodies(argv=None):
    '''
        Get list of bodies available in a kernel set.
        GET: /kernel-set/{kernelSetId}/bodies
    '''
    parser = argparse.ArgumentParser(description='List bodies available in WebGeocalc API for a specific kernel set.')
    parser.add_argument('kernel', nargs='?', help='Kernel set name or id')
    parser.add_argument('--name', '-n', metavar='BODY', nargs='+', help='Search a specific body by name')

    args, others = parser.parse_known_args(argv)

    if args.kernel:
        try:
            kernel = int(args.kernel)
        except ValueError:
            kernel = args.kernel

        bodies = API.bodies(kernel)

        if args.name:
            for body in bodies:
                for name in args.name:
                    if name in body:
                        print(f" - {str(body)}: (id: {int(body)})")
        else:
            print('\n'.join([f" - {str(body)}: (id: {int(body)})" for body in bodies]))
    else:
        parser.print_help()

