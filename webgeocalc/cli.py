"""Command line interface."""

import argparse
import re

from .api import Api, ESA_API, JPL_API
from .calculation_types import (AngularSeparation, AngularSize,
                                Calculation, FrameTransformation, GFCoordinateSearch,
                                IlluminationAngles, OsculatingElements,
                                StateVector, SubObserverPoint, SubSolarPoint,
                                SurfaceInterceptPoint, TimeConversion)
from .errors import KernelSetNotFound, TooManyKernelSets


class GetApi(argparse.Action):
    """Custom API from key action."""

    def __call__(self, parser, args, values, option_string=None):
        """Select API based on the provided key."""
        key = values.upper()
        api = JPL_API if key == 'JPL' else ESA_API if key == 'ESA' else Api(key)
        setattr(args, self.dest, api)


API_ARGS = {
    'metavar': 'JPL|ESA|URL',
    'default': Api(),
    'action': GetApi,
    'help': 'Webgeocalc endpoint choice '
            '(default on `WGC_URL` if set '
            'in global environment variables '
            'or `JPL_URL` if not)',
}


def cli_kernel_sets(argv=None):
    """Get list of kernel sets available on the server.

    GET: /kernel-sets
    """
    parser = argparse.ArgumentParser(
        description='List and search kernel sets available in WebGeoCalc API.')
    parser.add_argument('--all', '-a', action='store_true',
                        help='List all kernel sets available')
    parser.add_argument('--kernel', '-k', metavar='NAME|ID', nargs='+',
                        help='Search a specific kernel by name or id')
    parser.add_argument('--api', **API_ARGS)

    args, _ = parser.parse_known_args(argv)

    if args.all:
        kernels = args.api.kernel_sets()
        print('\n'.join([f" - {str(kernel)}: (id: {int(kernel)})" for kernel in kernels]))

    elif args.kernel:
        for kernel in args.kernel:
            try:
                kernel = int(kernel)
            except ValueError:
                pass

            try:
                kernel = args.api.kernel_set(kernel)
                print(f" - {str(kernel)}: (id: {int(kernel)})")

            except (KernelSetNotFound, TooManyKernelSets) as err:
                print(err)
    else:
        parser.print_help()


def cli_bodies(argv=None):
    """Get list of bodies available in a kernel set.

    GET: /kernel-set/{kernelSetId}/bodies
    """
    parser = argparse.ArgumentParser(
        description='List bodies available in WebGeoCalc API for a specific kernel set.')
    parser.add_argument('kernel', nargs='?', help='Kernel set name or id')
    parser.add_argument('--name', '-n', metavar='BODY', nargs='+',
                        help='Search a specific body by name or id')
    parser.add_argument('--api', **API_ARGS)

    args, _ = parser.parse_known_args(argv)

    if args.kernel:
        try:
            kernel = int(args.kernel)
        except ValueError:
            kernel = args.kernel

        bodies = args.api.bodies(kernel)

        if args.name:
            for body in bodies:
                for name in args.name:
                    if name in body:
                        print(f" - {str(body)}: (id: {int(body)})")
        else:
            print('\n'.join([f" - {str(body)}: (id: {int(body)})" for body in bodies]))
    else:
        parser.print_help()


def cli_frames(argv=None):
    """Get list of frames available in a kernel set.

    GET: /kernel-set/{kernelSetId}/frames
    """
    parser = argparse.ArgumentParser(
        description='List frames available in WebGeoCalc API for a specific kernel set.')
    parser.add_argument('kernel', nargs='?', help='Kernel set name or id')
    parser.add_argument('--name', '-n', metavar='FRAME',
                        nargs='+', help='Search a specific frame by name or id')
    parser.add_argument('--api', **API_ARGS)

    args, _ = parser.parse_known_args(argv)

    if args.kernel:
        try:
            kernel = int(args.kernel)
        except ValueError:
            kernel = args.kernel

        frames = args.api.frames(kernel)

        if args.name:
            for frame in frames:
                for name in args.name:
                    if name in frame:
                        print(f" - {str(frame)}: (id: {int(frame)})")
        else:
            print('\n'.join([f" - {str(frame)}: (id: {int(frame)})" for frame in frames]))
    else:
        parser.print_help()


def cli_instruments(argv=None):
    """Get list of instruments available in a kernel set.

    GET: /kernel-set/{kernelSetId}/instruments
    """
    parser = argparse.ArgumentParser(description='List instruments available'
                                     'in WebGeoCalc API for a specific kernel set.')
    parser.add_argument('kernel', nargs='?', help='Kernel set name or id')
    parser.add_argument('--name', '-n', metavar='INSTRUMENT', nargs='+',
                        help='Search a specific instrument by name or id')
    parser.add_argument('--api', **API_ARGS)

    args, _ = parser.parse_known_args(argv)

    if args.kernel:
        try:
            kernel = int(args.kernel)
        except ValueError:
            kernel = args.kernel

        instruments = args.api.instruments(kernel)

        if args.name:
            for instrument in instruments:
                for name in args.name:
                    if name in instrument:
                        print(f" - {str(instrument)}: (id: {int(instrument)})")
        else:
            print('\n'.join(
                [f" - {str(instrument)}: (id: {int(instrument)})"
                 for instrument in instruments]))
    else:
        parser.print_help()


def _split(string, sep=','):
    # Replace and split string
    for char in ['[', ']', '=', '"', "'"]:
        string = string.replace(char, '')
    return string.split(sep)


def _underscore_case(string):
    # Convert string to underscore case (ie. snake case)
    string = string.replace('-', '_')
    sub = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', sub).lower()


def _int_float_str(value):
    # Parse value type.
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def _params(params):
    # Parse input parameters
    out = {}
    key = None
    for param in params:
        if param.startswith('--'):
            if '=' in param:
                key = param[2:].split('=')
                param = ','.join(key[1:])
                key = _underscore_case(key[0])
            else:
                key = _underscore_case(param[2:])
                continue

        if key is None:
            continue

        for value in _split(param):
            if value == '':
                continue

            value = _int_float_str(value)

            if key not in out:
                out[key] = value
            elif not isinstance(out[key], list):
                out[key] = [out[key], value]
            else:
                out[key] += [value]

    return out


def cli_calculation(argv=None, calculation=Calculation, desc='generic'):
    """Submit and get calculation results.

    - POST: /calculation/new + payload
    - GET: /calculation/{id}
    - GET: /calculation/{id}/results
    """
    parser = argparse.ArgumentParser(
        description=f'Submit {desc} calculation to the WebGeoCalc API')

    parser.add_argument('--quiet', '-q', action='store_true',
                        help='Disable verbose output status.')
    parser.add_argument('--payload', '-p', action='store_true',
                        help='Display payload before the calculation results.')
    parser.add_argument('--dry-run', '-d', action='store_true',
                        help='Dry run. Show only the payload.')
    parser.add_argument('--KEY', metavar='VALUE', nargs='*',
                        help='Key parameter and its value(s).')

    args, others = parser.parse_known_args(argv)
    params = _params(others)

    if params:
        params['verbose'] = not args.quiet
        try:
            calc = calculation(**params)

            if (args.payload or args.dry_run) and not args.quiet:

                print(f'API: {calc.api}')

                payload = calc.payload
                print('Payload:\n{')

                for key, value in payload.items():
                    print(f'  {key}: {value},')
                print('}')

            if not args.dry_run:
                if not args.quiet:
                    print('\nAPI status:')

                res = calc.run()
                if not args.quiet:
                    print('\nResults:')

                for key, value in res.items():
                    print(f'{key}:\n> {value}')

        except (AttributeError, ValueError, IOError) as err:
            print(err)
    else:
        parser.print_help()


def cli_state_vector(argv=None):
    """Submit state vector calculation with the CLI."""
    cli_calculation(argv, StateVector, desc='State Vector')


def cli_angular_separation(argv=None):
    """Submit angular separation calcultion with the CLI."""
    cli_calculation(argv, AngularSeparation, desc='Angular Separation')


def cli_angular_size(argv=None):
    """Submit angular size calcultion with the CLI."""
    cli_calculation(argv, AngularSize, desc='Angular Size')


def cli_frame_transformation(argv=None):
    """Submit frame transformation calcultion with the CLI."""
    cli_calculation(argv, FrameTransformation, desc='Frame Transformation')


def cli_illumination_angles(argv=None):
    """Submit illumination angles calcultion with the CLI."""
    cli_calculation(argv, IlluminationAngles, desc='Illumination Angles')


def cli_subsolar_point(argv=None):
    """Submit sub-solar point calcultion with the CLI."""
    cli_calculation(argv, SubSolarPoint, desc='Sub-Solar Point')


def cli_subobserver_point(argv=None):
    """Submit sub-observer point calcultion with the CLI."""
    cli_calculation(argv, SubObserverPoint, desc='Sub-Observer Point')


def cli_surface_intercept_point(argv=None):
    """Submit surface intercept point calcultion with the CLI."""
    cli_calculation(argv, SurfaceInterceptPoint, desc='Surface Intercept Point')


def cli_osculating_elements(argv=None):
    """Submit osculating elements calcultion with the CLI."""
    cli_calculation(argv, OsculatingElements, desc='Osculating Elements')


def cli_time_conversion(argv=None):
    """Submit time conversion calcultion with the CLI."""
    cli_calculation(argv, TimeConversion, desc='Time Conversion')


def cli_gf_coordinate_search(argv=None):
    """Submit geometry finder coordinate search with the CLI."""
    cli_calculation(argv, GFCoordinateSearch, desc='Position Event Finder')
