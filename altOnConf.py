from sardana.macroserver.macro import imacro, macro, Macro, Type, Optional, UnknownEnv
import PyTango
import numpy as np

@imacro()
def acqconf(self):
    # run all the other configuration
    try:
        acqConf = self.getEnv('acqConf')
    except UnknownEnv:
        self.output("No altOn configuration in environment. Creating new.")
        acqConf = dict(altOn=False, waitTime=0, counters=[])

    label, unit = "Alternate On/Off", ""
    acqConf = dict(altOn=False, waitTime=0, counters=[])

    alt_on = self.input(
            "Alternate Mode On/Off?",
            data_type=Type.Boolean,
            title="Alternate Mode",
            key=label,
            unit=unit,
            default_value=acqConf['altOn'])

    acqConf['altOn'] = alt_on

    self.setEnv('acqConf', acqConf)

    self.execMacro('waittime')
    self.execMacro('magnconf')
    self.execMacro('acqrep')

@macro()
def acqrep(self):
    acqConf = self.getEnv('acqConf')
    magnConf = self.getEnv('magnConf')
    infodict = {
        'enabled': str(acqConf['altOn']),
        'wait time': f"{acqConf['waitTime']:.2f} s",
        'magnet amplitude': f"{magnConf['ampl']:.2f} A",
        'magnet wait time': f"{magnConf['waitTime']:.2f} s",
        'counters used': f"{acqConf['counters']}",
        }
    pad = max([len(k) for k in infodict])
    self.output(f"\nAltOn configuration\n{19*'='}")
    for k, v in infodict.items():
        self.output(f"{k:>{pad}s}: {v}")

@imacro([["time", Type.Float, Optional, "time in seconds"] ])
def waittime(self, time):
    """Macro waittime"""
    acqConf = self.getEnv('acqConf')
    if time is None:
        label, unit = "Waittime", "s"
        time = self.input("Wait time before every acquisition?",
                          data_type=Type.Float,
                          title="Waittime Amplitude", key=label, unit=unit,
                          default_value=acqConf['waitTime'], minimum=0.0,
                          maximum=100)

    acqConf['waitTime'] = time
    self.setEnv('acqConf', acqConf)
    self.output("waittime set to %.2f s", time)


@imacro([
    ["moveable", Type.Moveable, Optional, "magnet motor to switch"],
    ["ampl", Type.Float, Optional, "current amplitude"],
    ["waittime", Type.Float, Optional, "wait time after switch"],
    ])
def magnconf(self, moveable, ampl, waittime):
    """Macro magnampl"""
    try:
        magnConf = self.getEnv('magnConf')
    except UnknownEnv:
        self.output("No altOn magnet configuration found in environment. "
                    "Creating new.")
        magnConf = dict(moveable=None, ampl=.1, waitTime=.1)
    magnConf = dict(moveable=None, ampl=.1, waitTime=.1)

    if moveable is None:
        moveable = self.input(
            msg="Moveable to switch:",
            data_type=Type.String,
            default_value=magnConf['moveable'],
            )
        try:
            mov = 0
    magnConf['moveable'] = moveable

    if ampl is None:
        label, unit = "Amplitude", "A"
        magnConf['ampl'] = self.input(
            msg="Set magnet amplitude:",
            data_type=Type.Float,
            title="Magnet Amplitude",
            key=label,
            unit=unit,
            default_value=magnConf['ampl'],
            minimum=0.0,
            maximum=10)

    if waittime is None:
        label, unit = "Waittime", "s"
        magnConf['waittime'] = self.input(
            msg="Set magnet waittime:",
            data_type=Type.Float,
            title="Magnet Waittime",
            key=label,
            unit=unit,
            default_value=magnConf['waitTime'],
            minimum=0.0,
            maximum=100)

    self.setEnv('magnConf', magnConf)

