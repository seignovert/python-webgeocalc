# -*- coding: utf-8 -*-

class TooManyKernelSets(ValueError):
    '''This exception is raised when more than one kernel is found'''
    def __init__(self, kernel_set_name, kernel_sets):
        msg = '\n - '.join(
                [f"Too many kernel sets contains '{kernel_set_name}' in their names:"] + \
                [str(kernel) for kernel in kernel_sets]
            )
        super().__init__(msg)

class KernelSetNotFound(ValueError):
    '''This exception is raised when not a kernel set is not found'''
    def __init__(self, kernel_set_name):
        msg = f"Kernel set '{kernel_set_name}' not found"
        super().__init__(msg)


