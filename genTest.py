#!/usr/bin/env python3
import redpitaya_scpi as scpi
import time
import numpy as np
from Generate import Generator


#WORKS
generator = Generator(uIP='rp-f0ba38.local')
generator.setup(uChannelNumber=1, uWaveform='SINE', uFrequency=1000000, uAmplitude=0.5)
generator.setSCPIsettings()
generator.startGenerating()
time.sleep(10)
generator.stopGenerating()