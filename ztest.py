import ProgramRunner

from constants import *

Pr = ProgramRunner.FastProgramRunner()
amplitude = 1
frequency = 1000
waveform = WF_SINE
decimation = 10
samples = 100000

Pr.setup(waveform, amplitude, frequency, decimation, samples)
