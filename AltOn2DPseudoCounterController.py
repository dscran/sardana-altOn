from sardana.pool.controller import PseudoCounterController, Type, MaxDimSize
from PyTango import DeviceProxy
import numpy as np

class AltOn2DPseudoCounterController(PseudoCounterController):
    """ A  pseudo counter which remembers the input for negative magnetic
    fields and returns it at positive fields"""

    counter_roles = ('I',)
    pseudo_counter_roles = ('O',)
    value = np.zeros((2048, 2048))
    field = 0

    def __init__(self, inst, props, *args, **kwargs):
        PseudoCounterController.__init__(self, inst, props, *args, **kwargs)
        self.magnetState = DeviceProxy("raremag/MagnetState/magnet")

    def GetAxisAttributes(self, axis):
        axis_attrs = PseudoCounterController.GetAxisAttributes(self, axis)
        axis_attrs = dict(axis_attrs)
        axis_attrs['Value'][Type] = ((float, ), )
        axis_attrs['Value'][MaxDimSize] = (2048,2048)
        return axis_attrs

    def Calc(self, axis, counters):
        counter = counters[0]
        try:
            self.field = self.magnetState.magnet

            if self.field < 0:
                self.value = counter
        except:
            pass

        return self.value

    def GetAxisPar(self, axis, par):
        if par == "shape":
            return [self.value.shape[0],self.value.shape[1]]

