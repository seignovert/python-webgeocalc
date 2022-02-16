"""Webgeocalc setup."""

from setuptools import find_packages, setup


with open('README.rst', encoding='utf-8') as f:
    readme = f.read()


setup(
    name='webgeocalc',
    version='1.4.0',
    description='Python package for NAIF WebGeoCalc API',
    author='Benoit Seignovert',
    author_email='benoit.a.seignovert@univ-nantes.fr',
    url='https://github.com/seignovert/python-webgeocalc',
    project_urls={
        'Bug Tracker': 'https://github.com/seignovert/python-webgeocalc/issues',
        'Code coverage': 'https://codecov.io/gh/seignovert/python-webgeocalc',
        'Travis CI': 'https://travis-ci.org/seignovert/python-webgeocalc',
        'Source Code': 'https://github.com/seignovert/python-webgeocalc',
        'Documentation': 'https://webgeocalc.readthedocs.io/',
    },
    license='MIT',
    python_requires='>=3.8',
    install_requires=[
        'requests==2.25.1',
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
        'Programming Language :: Python :: 3.8',
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
            'wgc-subsolar-point = webgeocalc.cli:cli_subsolar_point',
            'wgc-subobserver-point = webgeocalc.cli:cli_subobserver_point',
            'wgc-surface-intercept-point = webgeocalc.cli:cli_surface_intercept_point',
            'wgc-osculating-elements = webgeocalc.cli:cli_osculating_elements',
            'wgc-time-conversion = webgeocalc.cli:cli_time_conversion',
            'wgc-gf-coordinate-search = webgeocalc.cli:cli_gf_coordinate_search',
        ],
    },
)
