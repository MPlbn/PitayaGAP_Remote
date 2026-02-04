import ProgramRunner
import CMDManager

from constants import *
from commands import *

Pr = ProgramRunner.FastProgramRunner()
amplitude = 1
frequency = 10000
waveform = WF_SINE
decimation = 10
samples = 100000

Pr.connect()
Pr.setup(waveform, amplitude, frequency, decimation, samples)
Pr.runStreamingServer()
Pr.pushConfig()
Pr.runGeneration()
