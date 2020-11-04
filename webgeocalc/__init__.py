'''WebGeoCalc module.'''

import pbr.version

__version__ = pbr.version.VersionInfo('webgeocalc').version_string()

from .api import API, Api, ESA_API, JPL_API
from .calculation import Calculation
from .calculation_types import (AngularSeparation, AngularSize,
                                FrameTransformation, IlluminationAngles,
                                OsculatingElements, StateVector,
                                SubObserverPoint, SubSolarPoint,
                                SurfaceInterceptPoint, TimeConversion)

__all__ = [
    'Api',
    'API',
    'JPL_API',
    'ESA_API',
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
    '__version__',
]
