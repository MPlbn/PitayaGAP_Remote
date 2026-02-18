import Generate
import paramiko
import CMDManager
import WaveCreator
import FileManager
import ProgramRunner

from commands import *
from constants import *

PR = ProgramRunner.FastProgramRunner()
# ============ THIS WAY ALSO BAD, RESETS TO 0 ================
# ============ plus delay on change is abysmal - nearly 1 second on setting new waveform change ===============
#first connect
PR.connect()
PR.runStreamingServer()
PR.TEST_STREAMING_GENERATION()
PR.stopStreaming()
PR.disconnect()
#generate for 20 sec