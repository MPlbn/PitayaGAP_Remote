import wave
import numpy as np
from scipy import signal
from constants import *

class WaveCreator:
    def __init__(self):
        self.numberOfBits = WF_NUM_BITS
        self.sampleRate = WF_SAMPLE_RATE
        self.periods = WF_DEFAULT_PERIODS
        self.samplesInPeriod = WF_SAMPLES_IN_PERIOD
        self.maximumValue = 2**(self.numberOfBits-1)-1
        self.minimumValue = -2**(self.numberOfBits-1)

    def getSampleRate(self) -> int:
        return self.sampleRate

    #it will probably need uamp also
    def create(self, uWaveForm):
        t = np.linspace(0, 1, self.periods*self.samplesInPeriod)*2*np.pi
        arbitraryWaveform = []

        match uWaveForm:
            case "Sine":
                arbitraryWaveform = np.sin(self.periods*t)*self.maximumValue
            case "Square":
                arbitraryWaveform = signal.square(self.periods*t)*self.maximumValue
            case "Triangle":
                arbitraryWaveform = signal.sawtooth(self.periods*t, width=0.5)*self.maximumValue
            case "Ramp up":
                arbitraryWaveform = signal.sawtooth(self.periods*t)*self.maximumValue
            case "Ramp down":
                arbitraryWaveform = signal.sawtooth(self.periods*t, width=0)*self.maximumValue
        
        return np.int16(arbitraryWaveform)