#!/usr/bin/python3

from pitConstants import *
import rp

class PitGenerator:
    def __init__(self, uWForm, uFreq, uAmp):
        self.waveform = GEN_WAVEFORMS[uWForm]
        self.frequency = int(uFreq)
        self.amplitude = float(uAmp)

    def setup(self):
        rp.rp_GenWaveForm(DEFAULT_CHANNEL, self.waveform)
        rp.rp_GenFreqDirect(DEFAULT_CHANNEL, self.frequency)
        rp.rp_GenAmp(DEFAULT_CHANNEL, self.amplitude)

    def reset(self):
        rp.rp_GenReset()    

    def runGeneration(self):
        rp.rp_GenOutEnable(DEFAULT_CHANNEL)
        rp.rp_GenTriggerOnly(DEFAULT_CHANNEL)
