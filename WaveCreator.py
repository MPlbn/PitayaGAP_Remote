import wave
import numpy as np
from scipy import signal
from constants import *

class WaveCreator:
    def __init__(self):
        self.numberOfBits = WF_NUM_BITS
        self.sampleRate = WF_SAMPLE_RATE
        self.periods = WF_DEFAULT_PERIODS
        self.samplesInPeriod = 0
        self.fullSize = WF_FULL_SIZE
        self.maximumValue = 2**(self.numberOfBits-1)-1
        self.minimumValue = -2**(self.numberOfBits-1)

    def getSampleRate(self) -> int:
        return self.sampleRate

    #it will probably need uamp also
    def create(self, uWaveForm, uHighestVal, uLowestVal, uStartingVal, uFrequency):

        t = np.linspace(0, 1, self.fullSize)*2*np.pi
        arbitraryWaveform = []
        maxVal = self.maximumValue*uHighestVal
        minVal = self.minimumValue*uLowestVal
        minVal *= -1

        if(uFrequency < 10):
            self.periods = uFrequency
        else:
            self.periods = 10
        
        startNorm = 2*(uStartingVal - uLowestVal)/(uHighestVal - uLowestVal) - 1

        match uWaveForm:
            case "Sine":
                shift = np.arcsin(startNorm)
                arbitraryWaveform = np.sin(self.periods*t + shift)
            
            case "Square":
                if(startNorm > 0):
                    shift = 0
                else:
                    shift = np.pi
                arbitraryWaveform = signal.square(self.periods*t + shift)
            
            case "Triangle":
                shift = 0.25 + 0.25*startNorm
                arbitraryWaveform = signal.sawtooth(self.periods*t + shift*2*np.pi, width=0.5)
            
            case "Ramp up":
                shift = (startNorm + 1)/2
                arbitraryWaveform = signal.sawtooth(self.periods*t + shift*2*np.pi)
            
            case "Ramp down":
                shift = (1 - (startNorm + 1)/2)
                arbitraryWaveform = signal.sawtooth(self.periods*t + shift*2*np.pi, width=0)
        
        arbitraryWaveform = (arbitraryWaveform + 1)/2
        arbitraryWaveform = arbitraryWaveform * (maxVal - minVal) + minVal

        #return arbitraryWaveform
        return np.int16(arbitraryWaveform)
    
    def createZero(self):
        t = np.linspace(0, 1, self.fullSize)*2*np.pi
        waveform = np.array(self.samplesInPeriod*t)
        return np.int16(waveform)
    
    def createStepping(self, uBase, uHighPointsList):
        waveform = 0
        return np.int16(waveform)