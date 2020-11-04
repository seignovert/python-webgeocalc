Basic usage of WebGeoCalc API
==============================

The :obj:`API` variable in :obj:`webgeocalc` provide an access to
the WebGeoCalc API:

>>> from webgeocalc import API
>>> API.url
'https://wgc2.jpl.nasa.gov:8443/webgeocalc/api'

The default API endpoint can be defined with the :obj:`WGC_URL`
global environment variable.
If it is not present, the :obj:`API` will fallback
to the JPL (:obj:`wgc2`) endpoint (as shown above).

You can also use the ESA webgeocalc server:

>>> from webgeocalc import ESA_API
>>> ESA_API.url
'http://spice.esac.esa.int/webgeocalc/api'


Or any 3rd party WGC endpoint:

>>> from webgeocalc import Api
>>> obs_api = Api('https://wgc.obspm.fr/webgeocalc/api')
>>> obs_api.url
'https://wgc.obspm.fr/webgeocalc/api'


Metadata
--------

Some metadata are public provided on the home page of the API
and can be retrieved directly as items:

>>> API['description']
'WGC2 -- a WebGeocalc Server with enabled API at NAIF, JPL'

>>> API['version']
'2.2.2'


Request kernel sets
-------------------

List all the kernel sets available on the API:

>>> API.kernel_sets()
[<KernelSetDetails> Solar System Kernels (id: 1), ...]

or request a single kernel set with it ``name`` of ``id``:

>>> API.kernel_set('Cassini Huygens')
<KernelSetDetails> Cassini Huygens (id: 5)

Convert it as *int* and you will get its ``id``:

>>> int(API.kernel_set('Cassini Huygens'))
5

Convert it as *str* and you will get its ``caption`` name:

>>> str(API.kernel_set(5))
'Cassini Huygens'

Get all the kernel set attributes and values:

>>> dict(API.kernel_set('Cassini Huygens').items())
{'caption': 'Cassini Huygens', 'sclkId': '-82', 'description': ...}

If more than one kernel set is found, an error is thrown:

>>> API.kernel_set('Cassini')
Traceback (most recent call last):
    ...
TooManyKernelSets: Too many kernel sets contains 'Cassini' in their names:
    - Cassini Huygens
    - SPICE Class -- CASSINI Remote Sensing Lesson Kernels


Request bodies
--------------

List all bodies contains in kernel set (by ``name`` or ``id``):

>>> API.bodies('Cassini Huygens')
[<BodyData> CASSINI (id: -82), ...]


Request frames
--------------

List all frames contains in kernel set (by ``name`` or ``id``):

>>> API.frames('Cassini Huygens')
[<FrameData> CASSINI_SATURN_SKR4N_LOCK (id: -82982), ...]


Request instruments
-------------------

List all instruments contains in kernel set (by ``name`` or ``id``):

>>> API.instruments('Cassini Huygens')
[<InstrumentData> CASSINI_CIRS_RAD (id: -82898), ...]


API class
---------

.. currentmodule:: webgeocalc.api

.. autoclass:: Api
