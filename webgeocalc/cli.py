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

    elif args.kernel is not None:
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

