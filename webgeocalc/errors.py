"""WebGeoCalc errors."""


class APIError(IOError):
    """This exception is raised when the status of the API response is not OK."""


class APIResponseError(NotImplementedError):
    """This exception is raised when the format of the API response is not implemented."""

    def __init__(self, json):
        msg = f'This API JSON response is not implemented yet:\n{json}'
        super().__init__(msg)


class ResultTypeError(TypeError):
    """This exception is raised when the class is not available."""

    def __init__(self, classname):
        msg = f"ResultType '{classname}' is not implemented"
        super().__init__(msg)


class ResultAttributeError(AttributeError):
    """This exception is raised when the attribute is missing."""

    def __init__(self, obj, attr):
        msg = f"'{obj.__class__.__name__}' object has no attribute '{attr}'"
        super().__init__(msg)


class TooManyKernelSets(ValueError):
    """This exception is raised when more than one kernel is found."""

    def __init__(self, kernel_set_name, kernel_sets):
        msg = '\n - '.join([
            f"Too many kernel sets contains '{kernel_set_name}' in their names:"
        ] + [str(kernel) for kernel in kernel_sets])
        super().__init__(msg)


class KernelSetNotFound(ValueError):
    """This exception is raised when not a kernel set is not found."""

    def __init__(self, kernel_set_name):
        msg = f"Kernel set '{kernel_set_name}' not found"
        super().__init__(msg)


class CalculationRequiredAttr(AttributeError):
    """This exception is raised when a calculation attribute is required."""

    def __init__(self, name):
        msg = f"Attribute '{name}' required."
        super().__init__(msg)


class CalculationInvalidAttr(AttributeError):
    """This exception is raised when a calculation attribute is invalid."""

    def __init__(self, name, attr, valids):
        msg = '\n - '.join(
            [f"Attribute '{name}'='{attr}' is only applicable with:"] + valids)
        super().__init__(msg)


class CalculationUndefinedAttr(AttributeError):
    """This exception is raised when a calculation attribute is undefined."""

    def __init__(self, attr, value, missing):
        msg = f"Attribute '{attr}' is set to '{value}' " + \
              f"but '{missing}' attribute is undefined."
        super().__init__(msg)


class CalculationIncompatibleAttr(AttributeError):
    """Calculation incompatible attributes.

    This exception is raised when a calculation attribute is
    not applicable with an other attribute.
    """

    def __init__(self, attr1, value1, attr2, value2, choices):
        msg = '\n - '.join(
            [f"Attribute '{attr1}' is set to '{value1}' "
             f"but '{attr2}'='{value2}' is only applicable with:"] + choices)
        super().__init__(msg)


class CalculationConflictAttr(AttributeError):
    """This exception is raised when two calculation attributes are in conflict."""

    def __init__(self, attr1, attr2):
        msg = f"Attribute '{attr1}' is in conflict with attribute '{attr2}'"
        super().__init__(msg)


class CalculationInvalidValue(ValueError):
    """This exception is raised when calculation attribute is outside a valid range."""

    def __init__(self, attr, value, vmin, vmax):
        msg = f"Attribute '{attr}'={value} is not included in [ {vmin} ; {vmax} ]."
        super().__init__(msg)


class CalculationAlreadySubmitted(IOError):
    """This exception is raised when calculation was already submitted."""

    def __init__(self, calculation_id):
        msg = f"Calculation already submitted with the id: '{calculation_id}'"
        super().__init__(msg)


class CalculationNotCompleted(IOError):
    """This exception is raised when calculation phase is not complete."""

    def __init__(self, phase):
        msg = f"Calculation phase: '{phase}'"
        super().__init__(msg)


class CalculationFailed(IOError):
    """This exception is raised when calculation failed."""

    def __init__(self, phase):
        msg = f"Calculation failed phase: '{phase}'"
        super().__init__(msg)


class CalculationTimeOut(IOError):
    """This exception is raised when calculation time-out."""

    def __init__(self, timeout, sleep):
        msg = f'Calculation time-out after {timeout} seconds' + \
              f' ({int(timeout/sleep)} attempts)'
        super().__init__(msg)
