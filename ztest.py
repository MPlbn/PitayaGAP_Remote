import ProgramRunner
import CMDManager

from constants import *
from commands import *

Pr = ProgramRunner.FastProgramRunner()
amplitude = 0.5
frequency = 10000
waveform = WF_SINE
decimation = 10
samples = 100000

Pr.connect()
Pr.setup(waveform, amplitude, frequency, decimation, samples)
Pr.runAcquisition(samples)
