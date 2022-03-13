from sardana.pool.controller import PseudoCounterController, Type, MaxDimSize
import numpy as np


class AltOnPseudoCounterController(PseudoCounterController):
    """ A  pseudo counter which remembers the input for negative magnetic
    fields and returns it at positive fields"""

    counter_roles = 'in', 'control'
    pseudo_counter_roles = 'out',
    _value = 0

    def __init__(self, inst, props, *args, **kwargs):
        PseudoCounterController.__init__(self, inst, props, *args, **kwargs)

    def Calc(self, axis, counters):
        counter, control = counters
        if control:
            self._value = counter

        return self._value


class AltOn2DPseudoCounterController(PseudoCounterController):
    """ A  pseudo counter which remembers the input for negative magnetic
    fields and returns it at positive fields"""

    counter_roles = 'in', 'control'
    pseudo_counter_roles = 'out'
    _value = np.zeros((2048, 2048))

    def __init__(self, inst, props, *args, **kwargs):
        PseudoCounterController.__init__(self, inst, props, *args, **kwargs)

    def GetAxisAttributes(self, axis):
        axis_attrs = PseudoCounterController.GetAxisAttributes(self, axis)
        axis_attrs = dict(axis_attrs)
        axis_attrs['Value'][Type] = ((float, ), )
        axis_attrs['Value'][MaxDimSize] = (4096, 4096)
        return axis_attrs

    def Calc(self, axis, counters):
        counter, control = counters
        if control:
            self._value = counter

        return self._value

    def GetAxisPar(self, axis, par):
        if par == "shape":
            return self._value.shape

