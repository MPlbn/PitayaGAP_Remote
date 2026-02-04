import ProgramRunner
import CMDManager

from constants import *
from commands import *
import threading

Pr = ProgramRunner.FastProgramRunner()
amplitude = 0.5
frequency = 100000
waveform = WF_TRI
decimation = 10
samples = 30000

Pr.connect()
Pr.setup(waveform, amplitude, frequency, decimation)
Pr.runGeneration()
Pr.runAcquisition(samples)
print("I'm here")
Pr.stopStreaming()
print("im after streaming")
Pr.disconnect()