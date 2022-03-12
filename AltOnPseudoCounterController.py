from sardana.pool.controller import PseudoCounterController, Type, Description, DefaultValue
from tango import AttributeProxy

class AltOnPseudoCounterController(PseudoCounterController):
    """ A  pseudo counter which remembers the input for negative magnetic
    fields and returns it at positive fields"""

    counter_roles = 'I',
    pseudo_counter_roles = 'O',
    _value = 0

    # ctrl_properties = {
    #     "altOnState": {
    #         Type: str,
    #         Description: "tango attribute to determine altOn state from",
    #         DefaultValue: "domain/family/member/attribute",
    #         },
    #     }

    def __init__(self, inst, props, *args, **kwargs):
        PseudoCounterController.__init__(self, inst, props, *args, **kwargs)
        try:
            self.altonproxy = AttributeProxy("sys/tg_test/1/long_scalar")
        except Exception as ex:
            self._log.error(ex)

    def Calc(self, axis, counters):
        counter = counters[0]
        try:
            altOnValue = self.altonproxy.read().value
            self._log.debug(f"altOnValue={altOnValue}")
            if altOnValue < 80:
                self._value = counter
        except Exception as ex:
            self._log.error("Can't determine AltOn State: {ex}")

        return self._value
