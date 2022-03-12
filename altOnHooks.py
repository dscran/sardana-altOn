# -*- coding: utf-8 -*-
"""
Created on Tue May 22 12:57:08 2018

@author: MBI Berlin
"""
from sardana.macroserver.macro import macro, Type
import time
import os
from PyTango import DeviceProxy

@macro()
def userPreAcq(self):
    acqConf  = self.getEnv('acqConf')
    altOn    = acqConf['altOn']
    waittime = acqConf['waitTime']

    if waittime:
        time.sleep(waittime)
        self.debug('waiting for %.2f s', waittime)

    if altOn:
        # move magnet to minus amplitude
        magnConf = self.getEnv('magnConf')
        ampl = magnConf['ampl']
        magwaittime = magnConf['waitTime']
        magnet = self.getMotion(["magnet"])
        magnetState = DeviceProxy('raremag/MagnetState/magnet')

        magnet.move(-1*ampl)
        magnetState.magnet = -1*ampl

        self.debug('mag. waiting for %.2f s', magwaittime)
        time.sleep(magwaittime)

        parent = self.getParentMacro()
        if parent:
            integ_time = parent.integ_time
            mnt_grp = self.getObj(self.getEnv('ActiveMntGrp'), type_class=Type.MeasurementGroup)
            state, data = mnt_grp.count(integ_time)

        magnet.move(+1 * ampl)
        magnetState.magnet = +1 * ampl

        self.debug('mag. waiting for %.2f s', magwaittime)
        time.sleep(magwaittime)

