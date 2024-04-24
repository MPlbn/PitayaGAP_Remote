#!/usr/bin/env python3
import redpitaya_scpi as scpi
import time
rp_s = scpi.scpi('rp-f0ba38.local')

channel = 1

wave_form = 'dc'
freq = 17
ampl = 0
step = 0.1

rp_s.tx_txt('GEN:RST')

rp_s.tx_txt(f'SOUR{channel}:FUNC {str(wave_form).upper()}')
rp_s.tx_txt(f'SOUR{channel}:FREQ:FIX {freq}')
rp_s.tx_txt(f'SOUR{channel}:VOLT {ampl}')

# Enable output
rp_s.tx_txt(f'OUTPUT{channel}:STATE ON')
rp_s.tx_txt(f'SOUR{channel}:TRig:INT')

counter = 0

while(counter < 4):
    ampl += 0.1
    time.sleep(0.2)
    rp_s.tx_txt(f'SOUR{channel}:VOLT ' + str(ampl))
    counter += 1

#try akwizycja
rp_s.tx_txt('ACQ:RST')

rp_s.tx_txt('ACQ:DEC 4')
rp_s.tx_txt('ACQ:START')
#time.sleep(0.0001) #Moze byc potrzebne
rp_s.tx_txt('ACQ:TRig NOW')

while 1:
    rp_s.tx_txt('ACQ:TRig:FILL?')
    if rp_s.rx_txt() == '1':
        break

buff = rp_s.acq_data(channel, convert=True)

print(buff[5000:5050]) 

#Jednak git

rp_s.tx_txt(f'SOUR{channel}:FUNC DC_NEG')
while True:
    temp = input("Zakonczyc?: ")
    if(temp == "y"):
        break

rp_s.tx_txt('OUTPUT1:STATE OFF')
rp_s.close()