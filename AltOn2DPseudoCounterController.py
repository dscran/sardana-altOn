from sardana.pool.controller import PseudoCounterController, Type, MaxDimSize, Description, DefaultValue
from PyTango import AttributeProxy
import numpy as np

class AltOn2DPseudoCounterController(PseudoCounterController):
    """ A  pseudo counter which remembers the input for negative magnetic
    fields and returns it at positive fields"""

    counter_roles = ('I',)
    pseudo_counter_roles = ('O',)
    value = np.zeros((2048, 2048))
    field = 0

    ctrl_properties = {
        "altOnState": {
            Type: str,
            Description: "tango attribute to determine altOn state from",
            DefaultValue: "domain/family/member/attribute",
            },
        }

    def __init__(self, inst, props, *args, **kwargs):
        PseudoCounterController.__init__(self, inst, props, *args, **kwargs)
        self.stateproxy = DeviceProxy(self.altOnState)

    def GetAxisAttributes(self, axis):
        axis_attrs = PseudoCounterController.GetAxisAttributes(self, axis)
        axis_attrs = dict(axis_attrs)
        axis_attrs['Value'][Type] = ((float, ), )
        axis_attrs['Value'][MaxDimSize] = (2048, 2048)
        return axis_attrs

    def Calc(self, axis, counters):
        counter = counters[0]
        try:
            if self.stateproxy.read().value < 0:
                self.value = counter
        except Exception:
            pass

        return self.value

    def GetAxisPar(self, axis, par):
        if par == "shape":
            return [self.value.shape[0],self.value.shape[1]]

