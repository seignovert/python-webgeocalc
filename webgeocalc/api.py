# -*- coding: utf-8 -*-
'''WebGeoCalc API module.'''

import os

import requests

from .errors import APIError, APIReponseError, KernelSetNotFound, TooManyKernelSets
from .types import ColumnResult, KernelSetDetails, get_type
from .vars import ESA_URL, JPL_URL


class Api:
    '''WebGeoCalc API object.

    Parameters
    ----------
    url : str, optional
        API root URL.
        Use ``WGC_URL`` global environment variable if present.
        If not, fallback on :py:obj:`JPL_URL`:
        ``https://wgc2.jpl.nasa.gov:8443/webgeocalc/api``

    '''

    def __init__(self, url=''):
        self.url = str(url) if url != '' else os.environ.get('WGC_URL', JPL_URL)
        self._kernel_sets = None
        self._meta = None

    def __str__(self):
        return self.url

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self}'

    def __getitem__(self, key):
        if key in self.metadata:
            return self.metadata[key]
        raise KeyError(key)

    def get(self, url):
        '''Generic GET request on the API.

        Parameters
        ----------
        url: str
            Request url with GET method.

        Returns
        -------
        list or tuple:
            Parsed json API response. See: :py:func:`read`.

        Raises
        ------
        requests.reponse.HTMLError
            If HTML error is thrown by the API (HTML code not equal 200)

        Example
        -------
        >>> API.get('/kernel-sets')
        [<KernelSetDetails> Solar System Kernels (id: 1), ...]

        '''
        response = requests.get(self.url + url)
        if response.ok:
            return self.read(response.json())

        return response.raise_for_status()

    def post(self, url, payload):
        '''Generic POST request on the API.

        Parameters
        ----------
        url: str
            Request url with POST method.

        payload: dict
            Calculation payload data.

        Returns
        -------
        list or tuple:
            Parsed json API response. See: :py:func:`read`.

        Raises
        ------
        requests.reponse.HTMLError
            If HTML error is thrown by the API (HTML code not equal 200)

        Example
        -------
        >>> API.post('/calculation/new', payload=calculation_payload)  # doctest: +SKIP
        ('0788aba2-d4e5-4028-9ef1-4867ad5385e0', 'COMPLETE')

        '''
        response = requests.post(self.url + url, json=payload)
        if response.ok:
            return self.read(response.json())

        return response.raise_for_status()

    @staticmethod
    def read(json):
        '''Read content from API JSON reponse.

        Parameters
        ----------
        json: dict
            API JSON response

        Returns
        -------
        list or tuple
            Parsed content of the JSON API response.

            If the response contents ``resultType`` and ``items`` keys, then
            return type will be:

            [`Result objects`: :obj:`webgeocalc.types.ResultType`]

            If response contents ``result``, then return type will be:

            (`Calculation id`: str, `Phase`: str)

            If the response contents ``columns`` and ``rows``, then
            return type will be:

            (`Columns`: [:obj:`webgeocalc.types.ColumnResult`],
             `Results rows`: [[int, float or str], ...])

            Else an error is thrown.

        Raises
        ------
        APIError
            If the API status is not ``OK``.
        APIReponseError
            If the format of the API response is unexpected.

        '''
        if 'status' not in json:
            return json

        if json['status'] != 'OK':
            raise APIError(json['error']['shortDescription'])

        keys = json.keys()

        if 'resultType' in keys and 'items' in json:
            dtype = get_type(json['resultType'])
            return [dtype(item) for item in json['items']]

        if 'result' in keys:
            phase = json['result']['phase']
            if phase == 'QUEUED':
                phase += f' | POSITION: {json["result"]["position"]}'

            return json['calculationId'], phase

        if 'columns' in keys and 'rows' in keys:
            cols = [ColumnResult(col) for col in json['columns']]
            return cols, json['rows']

        raise APIReponseError(json)

    def kernel_sets(self):
        '''Get list of all kernel sets available on the webgeocalc server.

        ``GET: /kernel-sets``

        Returns
        -------
        [:obj:`webgeocalc.types.KernelSetDetails`]
            List of kernel sets.

        '''
        if self._kernel_sets is None:
            self._kernel_sets = self.get('/kernel-sets')
        return self._kernel_sets

    def kernel_set(self, kernel_set):
        '''Get kernel set by ``caption`` name or kernel set ``id``.

        Parameters
        ----------
        kernel_set: str or int
            Kernel set ``name`` or ``id``.

        Returns
        --------
        :obj:`webgeocalc.types.KernelSetDetails`
            Kernel set details object.

        '''
        kernel_sets = list(filter(lambda x: kernel_set in x, self.kernel_sets()))
        if len(kernel_sets) == 1:
            return kernel_sets[0]

        if len(kernel_sets) > 1:
            raise TooManyKernelSets(kernel_set, kernel_sets)

        raise KernelSetNotFound(kernel_set)

    def kernel_set_id(self, kernel_set):
        '''Extract kernel set ``id`` based on ``id``, ``name`` or `object`.

        Parameters
        ----------
        kernel_set: str, int or :obj:`webgeocalc.types.KernelSetDetails`
            Kernel sets ``name``, ``id`` or `object`.

        Returns
        -------
        int
            Kernel set ``id``.

        '''
        if isinstance(kernel_set, int):
            return kernel_set

        if isinstance(kernel_set, str):
            return int(self.kernel_set(kernel_set))

        if isinstance(kernel_set, KernelSetDetails):
            return int(kernel_set)

        raise TypeError(f"'kernel_set' must be a 'int', a 'str' of a 'KernelSetDetails' object:\n' + \
                        '>>> Type({kernel_set}) = {type(kernel_set)}")

    def bodies(self, kernel_set):
        '''Get list of bodies available in a kernel set.

        ``GET: /kernel-set/{kernelSetId}/bodies``

        Parameters
        ----------
        kernel_set: str, int or :obj:`webgeocalc.types.KernelSetDetails`
            Kernel sets ``name``, ``id`` or `object`.

        Returns
        -------
        [:obj:`webgeocalc.types.BodyData`]
            List of bodies in the requested kernel set.

        '''
        kernel_set_id = self.kernel_set_id(kernel_set)
        return self.get(f'/kernel-set/{kernel_set_id}/bodies')

    def frames(self, kernel_set):
        '''Get list of frames available in a kernel set.

        ``GET: /kernel-set/{kernelSetId}/frames``

        Parameters
        ----------
        kernel_set: str, int or :obj:`webgeocalc.types.KernelSetDetails`
            Kernel sets ``name``, ``id`` or `object`.

        Returns
        -------
        [:obj:`webgeocalc.types.FrameData`]
            List of frames in the requested kernel set.

        '''
        kernel_set_id = self.kernel_set_id(kernel_set)
        return self.get(f'/kernel-set/{kernel_set_id}/frames')

    def instruments(self, kernel_set):
        '''Get list of instruments available in a kernel set.

        ``GET: /kernel-set/{kernelSetId}/instruments``

        Parameters
        ----------
        kernel_set: str, int or :obj:`webgeocalc.types.KernelSetDetails`
            Kernel sets ``name``, ``id`` or `object`.

        Returns
        -------
        [:obj:`webgeocalc.types.InstrumentData`]
            List of instruments in the requested kernel set.

        '''
        kernel_set_id = self.kernel_set_id(kernel_set)
        return self.get(f'/kernel-set/{kernel_set_id}/instruments')

    def new_calculation(self, payload):
        '''Starts a new calculation.

        ``POST: /calculation/new``

        Parameters
        ----------
        payload: dict
            Calculation payload.

        Returns
        -------
        (str, str)
            Tuple of the calculation phase:
            ``(calculation-id, phase)``
            See: :py:func:`read`.

        Example
        -------
        >>> API.calculation_new(calculation_payload)  # doctest: +SKIP
        ('0788aba2-d4e5-4028-9ef1-4867ad5385e0', 'LOADING_KERNELS')

        '''
        return self.post('/calculation/new', payload)

    def phase_calculation(self, calculation_id):
        '''Gets the phase of a calculation.

        ``GET: /calculation/{id}``

        Parameters
        ----------
        calculation_id: str
            Calculation id.

        Returns
        -------
        (str, str)
            Tuple of the calculation phase:
            ``(calculation-id, phase)``
            See: :py:func:`read`.

        Example
        -------
        >>> API.phase_calculation('0788aba2-d4e5-4028-9ef1-4867ad5385e0')  # noqa: E501  # doctest: +SKIP
        ('0788aba2-d4e5-4028-9ef1-4867ad5385e0', 'COMPLETE')

        '''
        return self.get(f'/calculation/{calculation_id}')

    def cancel_calculation(self, calculation_id):
        '''Cancels a previously requested calculation, should this not be completed, or its results..

        ``GET: /calculation/{id}/cancel``

        Calculations that have been already ``DISPATCHED``, previously ``CANCELLED`` or
        that have ``EXPIRED`` cannot be cancelled, and requesting it will produce an `error`.

        Parameters
        ----------
        calculation_id: str
            Calculation id.

        Returns
        -------
        (str, str)
            Tuple of the calculation phase:
            ``(calculation-id, phase)``
            See: :py:func:`read`.

        Example
        -------
        >>> API.phase_calculation('0788aba2-d4e5-4028-9ef1-4867ad5385e0')  # noqa: E501  # doctest: +SKIP
        ('0788aba2-d4e5-4028-9ef1-4867ad5385e0', 'CANCELLED')

        '''
        return self.get(f'/calculation/{calculation_id}/cancel')

    def results_calculation(self, calculation_id):
        '''Gets the results of a complete calculation.

        ``GET: /calculation/{id}/results``

        Parameters
        ----------
        calculation_id: str
            Calculation id.

        Returns
        -------
        ([:obj:`webgeocalc.types.ColumnResult`], [[int, float or str], ...])
            Tuple of calculation results:
            ``(columns, rows)``
            See: :py:func:`read`.

        Example
        -------
        >>> API.results_calculation('0788aba2-d4e5-4028-9ef1-4867ad5385e0')  # noqa: E501  # doctest: +SKIP
        ([<ColumnResult> UTC calendar date, ...], [['2000-01-01 00:00:00.000000 UTC', ...], [...]])

        '''
        return self.get(f'/calculation/{calculation_id}/results')

    @property
    def metadata(self):
        """API metadata."""
        if self._meta is None:
            self._meta = self.get('/')
        return self._meta


# Export default API object
API = Api()
JPL_API = Api(JPL_URL)
ESA_API = Api(ESA_URL)
