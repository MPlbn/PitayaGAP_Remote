#!/usr/bin/env python3

import sys
import matplotlib.pyplot as pplot
import redpitaya_scpi as scpi
import Generate
import Acquire

#constants generation
IP = 'rp-f0ba38.local'
WAVE_FORM = 'sine'
FREQUENCY = 1000
AMPLITUDE = 1
GENERATOR = Generate.Generator(IP)

#constants acquisition
DECIMATION = 32
TRIGGER_LVL = 0.5
TRIGGER_DELAY = 0
ACQUISITOR = Acquire.Acquisitor(IP)

#Reseting generation and acquisition
GENERATOR.reset()
ACQUISITOR.reset()

#settings
GENERATOR.setup(1, WAVE_FORM, AMPLITUDE, FREQUENCY)
ACQUISITOR.setup(DECIMATION, TRIGGER_LVL, TRIGGER_DELAY)

#Starting generation
GENERATOR.startGenerating()

#Starting acquisition
buffer = ACQUISITOR.runAcquisition()

#plotting
pplot.plot(buffer)
pplot.ylabel('testWykres')
pplot.show()

#closing scpi connection
scpi.scpi(IP).close()