Advanced parameters
===================

Payload
--------

.. currentmodule:: webgeocalc.payload

WebGeoCalc API requires JSON encoded payloads. An abstract class :py:class:`Payload` is
available to convert any python keywords values pattern into a structure dictionary that
can be encoded into JSON. It also provided a mechanism to enforce some required keywords
and restrict some parameter to a subset of ``VALID_PARAMETERS``
(see :py:mod:`webgeocalc.vars`).

>>> from webgeocalc.payload import Payload
>>> from webgeocalc.decorator import parameter

>>> class DerivedPayload(Payload):
...     REQUIRED = ('foo',)
...
...     @parameter
...     def foo(self, val):  # required
...         self.__foo = val
...
...     @parameter(only='AXIS')  # optional
...     def baz(self, val):
...         self.__baz = val


>>> DerivedPayload(foo='bar', baz='X').payload
{'foo': 'bar', 'baz': 'X'}

.. autoclass:: webgeocalc.payload.Payload

Direction
---------

.. currentmodule:: webgeocalc.direction

Direction vectors for ``ANGULAR_SEPARATION`` and ``POINTING_DIRECTION`` can be specified as
an explicit :py:type:`dict` but it is recommended to use an explicit with :py:class:`Direction`
object:

>>> from webgeocalc.direction import Direction

>>> Direction(
...     direction_type='POSITION',
...     target='MARS',
...     shape='POINT',
...     observer='EARTH',
...     aberration_correction='LT+S',
... ).payload
{'directionType': 'POSITION',
 'target': 'MARS',
 'shape': 'POINT',
 'observer': 'EARTH',
 'aberrationCorrection': 'LT+S',
 'antiVectorFlag': False}

>>> Direction(
...     direction_type='VELOCITY',
...     target='MARS',
...     reference_frame='ITRF93',
...     observer='EARTH',
...     aberration_correction='XCN+S',
...     anti_vector_flag=True,
... ).payload
{'directionType': 'VELOCITY',
 'target': 'MARS',
 'referenceFrame': 'ITRF93',
 'observer': 'EARTH',
 'aberrationCorrection': 'XCN+S',
 'antiVectorFlag': True}

>>> Direction(
...     direction_type='VECTOR',
...     observer='EARTH',
...     direction_vector_type='REFERENCE_FRAME_AXIS',
...     direction_frame='IAU_EARTH',
...     direction_frame_axis='X',
...     aberration_correction='S',
...     anti_vector_flag=True,
... ).payload
{'directionType': 'VECTOR',
 'observer': 'EARTH',
 'directionVectorType': 'REFERENCE_FRAME_AXIS',
 'directionFrame': 'IAU_EARTH',
 'directionFrameAxis': 'X',
 'aberrationCorrection': 'S',
 'antiVectorFlag': True}

.. important::

    Direction required parameters:
        - :py:attr:`~Direction.direction_type` either ``POSITION``, ``VELOCITY`` or ``VECTOR``
        - :py:attr:`~Direction.observer` (not required if :py:attr:`aberration_correction` is ``NONE``
          and :py:attr:`~Direction.direction vector` is ``VECTOR``)

    Direction ``POSITION`` required parameters:
        - :py:attr:`~Direction.target`
        - :py:attr:`~Direction.shape`

    Direction ``VELOCITY`` required parameters:
        - :py:attr:`~Direction.target`
        - :py:attr:`~Direction.reference_frame`

    Direction ``VECTOR`` required parameters:
        - :py:attr:`~Direction.direction_vector_type` either
          ``INSTRUMENT_BORESIGHT``, ``REFERENCE_FRAME_AXIS``, ``VECTOR_IN_INSTRUMENT_FOV``,
          ``VECTOR_IN_REFERENCE_FRAME`` or ``INSTRUMENT_FOV_BOUNDARY_VECTORS``

    Direction vector ``INSTRUMENT_BORESIGHT`` or ``INSTRUMENT_FOV_BOUNDARY_VECTORS`` required parameters:
        - :py:attr:`~Direction.direction_instrument`

    Direction vector ``REFERENCE_FRAME_AXIS`` required parameters:
        - :py:attr:`~Direction.direction_frame`
        - :py:attr:`~Direction.direction_frame_axis`

    Direction vector ``VECTOR_IN_INSTRUMENT_FOV`` required parameters:
        - :py:attr:`~Direction.direction_instrument`
        - either :py:attr:`~Direction.direction_vector_x`, :py:attr:`~Direction.direction_vector_y` and :py:attr:`~Direction.direction_vector_z`
        - or :py:attr:`~Direction.direction_vector_ra` and :py:attr:`~Direction.direction_vector_dec`
        - or :py:attr:`~Direction.direction_vector_az`, :py:attr:`~Direction.direction_vector_el`, :py:attr:`~Direction.azccw_flag` and :py:attr:`~Direction.elplsz_flag`,

    Direction vector ``VECTOR_IN_REFERENCE_FRAME`` required parameters:
        - :py:attr:`~Direction.direction_frame`
        - either :py:attr:`~Direction.direction_vector_x`, :py:attr:`~Direction.direction_vector_y` and :py:attr:`~Direction.direction_vector_z`
        - or :py:attr:`~Direction.direction_vector_ra` and :py:attr:`~Direction.direction_vector_dec`
        - or :py:attr:`~Direction.direction_vector_az`, :py:attr:`~Direction.direction_vector_el`, :py:attr:`~Direction.azccw_flag` and :py:attr:`~Direction.elplsz_flag`,

    Default parameters:
        - :py:attr:`~Direction.aberration_correction`: ``NONE``
        - :py:attr:`~Direction.anti_vector_flag`: ``False``


.. autoclass:: Direction
