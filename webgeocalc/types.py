# -*- coding: utf-8 -*-

from .errors import ResultTypeError, ResultAttributeError

def get_type(classname):
    '''Get type based on classname'''
    if not classname in TYPES.keys():
        raise ResultTypeError(classname)
    return TYPES[classname]

class ColumnResult(object):
    '''Column result generic object'''

    def __init__(self, json):
        self._json = json

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__}> {str(self)}"

    def __getattr__(self, attr):
        if not attr in self._json.keys():
            raise ResultAttributeError(self, attr)
        return self._json[attr]

    def keys(self):
        return self._json.keys()

    def values(self):
        return self._json.values()

    def items(self):
        return self._json.items()

class ResultType(ColumnResult):
    '''Result Type object for item generic interface'''

    def __init__(self, json):
        super().__init__(json)

    def __int__(self):
        return int(self.id)

    def __repr__(self):
        return f"<{self.__class__.__name__}> {str(self)} (id: {int(self)})"

    def __contains__(self, item):
        '''Check int or str'''
        if isinstance(item, int):
            return item == int(self)
        return item.lower() in str(self).lower()

class KernelSetDetails(ResultType):
    '''Kernel set details'''

    def __init__(self, json):
        super().__init__(json)

    def __int__(self):
        return int(self.kernelSetId)

    def __str__(self):
        return self.caption

class BodyData(ResultType):
    '''Body data'''

    def __init__(self, json):
        super().__init__(json)

class FrameData(ResultType):
    '''Frame data'''

    def __init__(self, json):
        super().__init__(json)

class InstrumentData(ResultType):
    '''Instrument data'''

    def __init__(self, json):
        super().__init__(json)


class ColumnResult(object):
    '''Column result object'''

    def __init__(self, json):
        self._json = json

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"<{self.__class__.__name__}> {str(self)}"

    def __getattr__(self, attr):
        if not attr in self._json.keys():
            raise ResultAttributeError(self, attr)
        return self._json[attr]

    def keys(self):
        return self._json.keys()

    def values(self):
        return self._json.values()

    def items(self):
        return self._json.items()

    
TYPES = globals()
