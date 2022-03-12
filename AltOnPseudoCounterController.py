from sardana.pool.controller import PseudoCounterController, Type, Description, DefaultValue
from PyTango import AttributeProxy

class AltOnPseudoCounterController(PseudoCounterController):
    """ A  pseudo counter which remembers the input for negative magnetic
    fields and returns it at positive fields"""

    counter_roles = ('I',)
    pseudo_counter_roles = ('O',)
    value = 0

    ctrl_properties = {
        "altOnState": {
            Type: str,
            Description: "tango attribute to determine altOn state from",
            DefaultValue: "domain/family/member/attribute",
            },
        }

    def __init__(self, inst, props):  
        PseudoCounterController.__init__(self, inst, props)
        self.altonproxy = DeviceProxy(self.altOnState)

    def Calc(self, axis, counters):
        counter = counters[0]
        try:
            if self.altonproxy.read().value < 0:
                self.value = counter
        except Exception:
            pass

        return self.value
