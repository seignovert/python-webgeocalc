# -*- coding: utf-8 -*-

class ResultTypeError(TypeError):
    '''This exception is raised when the class is not available'''
    
    def __init__(self, classname):
        msg = f"ResultType '{classname}' is not implemented"
        super().__init__(msg)

class ResultAttributeError(AttributeError):
    '''This exception is raised when the attribute is missing'''
    
    def __init__(self, obj, attr):
        msg = f"'{obj.__class__.__name__}' object has no attribute '{attr}'"
        super().__init__(msg)


def get_type(classname):
    '''Get type based on classname'''
    if not classname in TYPES.keys():
        raise ResultTypeError(classname)
    return TYPES[classname]


class ResultType(object):
    '''Result Type object for item generic interface'''

    def __init__(self, json):
        self._json = json

    def __repr__(self):
        return f"<{self.__class__.__name__}> {str(self)} (id: {int(self)})"

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

class KernelSetDetails(ResultType):
    '''Kernel set details'''

    def __init__(self, json):
        super().__init__(json)

    def __int__(self):
        return int(self.kernelSetId)

    def __str__(self):
        return self.caption


TYPES = globals()
