#!/usr/bin/env python3
import redpitaya_scpi as scpi
import time
import numpy as np

rp_s = scpi.scpi('rp-f0ba38.local')
channel = 1

wave_form = 'dc'
freq = 1000
step = 0.1
ampl = 0.0

def GenChange(uAampl):
    test = uAampl
    test += step
    time.sleep(0.2)
    rp_s.tx_txt(f'SOUR{channel}:VOLT ' + str(test))
    return test

def AcqRst():
    rp_s.tx_txt('ACQ:RST')
    rp_s.tx_txt('ACQ:DEC 4')

def AcqStart():
    rp_s.tx_txt('ACQ:START')

def AcqRun():
    rp_s.tx_txt('ACQ:TRig NOW')

    while 1:
        rp_s.tx_txt('ACQ:TRig:FILL?')
        if rp_s.rx_txt() == '1':
            break

def AcqGetBuff():
    return rp_s.acq_data(1, convert=True)

def AcqStop():
    rp_s.tx_txt('ACQ:STOP')

def GenRst():
    rp_s.tx_txt('GEN:RST')

def GenSet():
    rp_s.tx_txt(f'SOUR{channel}:FUNC {str(wave_form).upper()}')
    rp_s.tx_txt(f'SOUR{channel}:FREQ:FIX {freq}')
    rp_s.tx_txt(f'SOUR{channel}:VOLT {ampl}')

def GenStart():
    rp_s.tx_txt(f'OUTPUT{channel}:STATE ON')
    rp_s.tx_txt(f'SOUR{channel}:TRig:INT')

def GenStop():
    rp_s.tx_txt('OUTPUT1:STATE OFF')


## main test

GenRst()
GenSet()
GenStart()



counter = 0
fullBuff = []

while(counter < 4):
    ampl = GenChange(ampl)
    AcqRst()
    AcqStart()
    #time.sleep(1)
    AcqRun()
    buff = AcqGetBuff()[16000:16010]
    print(buff)
    fullBuff += buff
    AcqStop()
    counter += 1

#Jednak git

print(f"fullBuff: {fullBuff}")
while True:
    temp = input("Zakonczyc?: ")
    if(temp == "y"):
        break

GenStop()
rp_s.close()