from sardana.pool.controller import PseudoCounterController

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
            ### TODO: the negative sign is just here for debugging!
            self._value = -counter

        return self._value
