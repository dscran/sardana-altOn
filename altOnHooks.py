# -*- coding: utf-8 -*-
"""
Created on 12.03.2022

@author: MBI Berlin
"""
from sardana.macroserver.macro import macro, Type
import time
import os
from tango import DeviceProxy

@macro()
def altOnHook(self):
    acqConf = self.getEnv('acqConf')
    altOn = acqConf['altOn']
    waittime = acqConf['waitTime']

    if waittime:
        time.sleep(waittime)
        self.debug('waiting for %.2f s', waittime)

    if altOn:
        # move magnet to minus amplitude
        magnConf = self.getEnv('magnConf')
        ampl = magnConf['ampl']
        magwaittime = magnConf['waitTime']
        magnet = self.getMotion([magnConf['moveable']])
        # magnetState = DeviceProxy('raremag/MagnetState/magnet')

        magnet.move(-ampl)
        # magnetState.magnet = -ampl

        self.debug('mag. waiting for %.2f s', magwaittime)
        time.sleep(magwaittime)

        parent = self.getParentMacro()
        if parent:
            integ_time = parent.integ_time
            mnt_grp = self.getObj(
                self.getEnv('ActiveMntGrp'),
                type_class=Type.MeasurementGroup)
            state, data = mnt_grp.count(integ_time)

        magnet.move(+ampl)
        # magnetState.magnet = +1 * ampl

        self.debug('mag. waiting for %.2f s', magwaittime)
        time.sleep(magwaittime)

@macro()
def disableDeterministic(self):
    """Deterministic scan needs to be disabled for altOn scans.
    See https://github.com/sardana-org/sardana/pull/1427
    and https://github.com/sardana-org/sardana/issues/1426
    """

    parent = self.getParentMacro()
    if parent: # macro is called from another macro
        # self.execMacro('send2ctrl ge1dctrl set_exposure 0 {:}'.format(parent.integ_time))
        # self.execMacro('send2ctrl ge1dctrl set_exposure 1 {:}'.format(parent.integ_time)) 
        # self.execMacro('send2ctrl ge1dctrl dark 0')
        # self.execMacro('send2ctrl ge1dctrl dark 1')
        # time.sleep(1.2*parent.integ_time)
        # reset pointNb to 0
        # geCtrlPointNB = AttributeProxy('controller/greateyeslabview1dcontroller/ge1dctrl/pointnb')
        # geCtrlPointNB.write(0)

        # disable deterministic scans
        acqConf  = self.getEnv('acqConf')
        altOn    = acqConf['altOn']
        if altOn:
            self.output("disable deterministic scan mode for altOn")
            parent._gScan.deterministic_scan = False
