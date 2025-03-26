"""Webgeocalc setup."""

from setuptools import find_packages, setup


with open('README.rst', encoding='utf-8') as f:
    readme = f.read()


setup(
    name='webgeocalc',
    version='1.5.0',
    description='Python package for NAIF WebGeoCalc API',
    author='Benoit Seignovert',
    author_email='benoit.seignovert@univ-nantes.fr',
    url='https://github.com/seignovert/python-webgeocalc',
    project_urls={
        'Bug Tracker': 'https://github.com/seignovert/python-webgeocalc/issues',
        'Code coverage': 'https://codecov.io/gh/seignovert/python-webgeocalc',
        'Travis CI': 'https://travis-ci.org/seignovert/python-webgeocalc',
        'Source Code': 'https://github.com/seignovert/python-webgeocalc',
        'Documentation': 'https://webgeocalc.readthedocs.io/',
    },
    license='MIT',
    python_requires='>=3.11',
    install_requires=[
        'requests>=2.31',
    ],
    packages=find_packages(),
    include_package_data=False,
    keywords=['naif', 'webgeocalc', 'api'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.11',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Astronomy',
    ],
    long_description=readme,
    long_description_content_type='text/x-rst; charset=UTF-8',
    entry_points={
        'console_scripts': [
            'wgc-kernels = webgeocalc.cli:cli_kernel_sets',
            'wgc-bodies = webgeocalc.cli:cli_bodies',
            'wgc-frames = webgeocalc.cli:cli_frames',
            'wgc-instruments = webgeocalc.cli:cli_instruments',
            'wgc-calculation = webgeocalc.cli:cli_calculation',
            'wgc-state-vector = webgeocalc.cli:cli_state_vector',
            'wgc-angular-separation = webgeocalc.cli:cli_angular_separation',
            'wgc-angular-size = webgeocalc.cli:cli_angular_size',
            'wgc-frame-transformation = webgeocalc.cli:cli_frame_transformation',
            'wgc-illumination-angles = webgeocalc.cli:cli_illumination_angles',
            'wgc-phase-angle = webgeocalc.cli:cli_phase_angle',
            'wgc-pointing-direction = webgeocalc.cli:cli_pointing_direction',
            'wgc-subsolar-point = webgeocalc.cli:cli_subsolar_point',
            'wgc-subobserver-point = webgeocalc.cli:cli_subobserver_point',
            'wgc-surface-intercept-point = webgeocalc.cli:cli_surface_intercept_point',
            'wgc-tangent-point = webgeocalc.cli:cli_tangent_point',
            'wgc-osculating-elements = webgeocalc.cli:cli_osculating_elements',
            'wgc-time-conversion = webgeocalc.cli:cli_time_conversion',
            'wgc-gf-coordinate-search = webgeocalc.cli:cli_gf_coordinate_search',
            'wgc-gf-angular-separation-search = '
            'webgeocalc.cli:cli_gf_angular_separation_search',
            'wgc-gf-distance-search = webgeocalc.cli:cli_gf_distance_search',
            'wgc-gf-sub-point-search = webgeocalc.cli:cli_gf_sub_point_search',
            'wgc-gf-occultation-search = webgeocalc.cli:cli_gf_occultation_search',
            'wgc-gf-surface-intercept-point-search = '
            'webgeocalc.cli:cli_gf_surface_intercept_point_search',
            'wgc-gf-target-in-instrument-fov-search = '
            'webgeocalc.cli:cli_gf_target_in_instrument_fov_search',
            'wgc-gf-ray-in-fov-search = webgeocalc.cli:cli_gf_ray_in_fov_search',
            'wgc-gf-range-rate-search = webgeocalc.cli:cli_gf_range_rate_search',
            'wgc-gf-phase-angle-search = webgeocalc.cli:cli_gf_phase_angle_search',
            'wgc-gf-illumination-angles-search = '
            'webgeocalc.cli:cli_gf_illumination_angles_search',
        ],
    },
)
