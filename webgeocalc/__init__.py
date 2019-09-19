'''WebGeoCalc module.'''

import pbr.version

__version__ = pbr.version.VersionInfo('webgeocalc').version_string()

from .api import API, WGC_ESA, WGC_JPL
from .calculation import Calculation
from .calculation_types import (AngularSeparation, AngularSize,
                                FrameTransformation, IlluminationAngles,
                                OsculatingElements, StateVector,
                                SubObserverPoint, SubSolarPoint,
                                SurfaceInterceptPoint, TimeConversion)

__all__ = [
    'API',
    'AngularSeparation',
    'AngularSize',
    'Calculation',
    'FrameTransformation',
    'IlluminationAngles',
    'OsculatingElements',
    'StateVector',
    'SubObserverPoint',
    'SubSolarPoint',
    'SurfaceInterceptPoint',
    'TimeConversion',
    'WGC_JPL',
    'WGC_ESA',
    '__version__',
]
