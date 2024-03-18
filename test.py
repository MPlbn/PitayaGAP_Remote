#!/usr/bin/env python3

import sys
import matplotlib.pyplot as pplot
import redpitaya_scpi as scpi

#constants generation
IP = 'rp-f0ba38.local'
RP_S = scpi.scpi(IP)
WAVE_FORM = 'sine'
FREQUENCY = 1000
AMPLITUDE = 1

#constants acquisition
DECIMATION = 32
TRIGGER_LVL = 0.5
TRIGGER_DELAY = 0


#Reseting generation and acquisition
RP_S.tx_txt('GEN:RST')
RP_S.tx_txt('ACQ:RST')

#settings
RP_S.sour_set(1, WAVE_FORM, AMPLITUDE, FREQUENCY)
RP_S.acq_set(DECIMATION, TRIGGER_LVL, TRIGGER_DELAY)

#Starting generation
RP_S.tx_txt('OUTPUT1:STATE ON')
RP_S.tx_txt('SOUR1:TRIG:INT')

#Starting acquisition
RP_S.tx_txt('ACQ:START')
RP_S.tx_txt('ACQ:TRIG CH1_PE')
#Next Acquisition step

while True:
    RP_S.tx_txt('ACQ:TRIG:FILL?')
    if RP_S.rx_txt() == '1':
        break

buffer = RP_S.acq_data(1, convert=True)

#plotting
pplot.plot(buffer)
pplot.ylabel('Guwno')
pplot.show()

#closing scpi connection
RP_S.close()