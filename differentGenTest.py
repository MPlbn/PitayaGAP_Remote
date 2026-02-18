import Generate
import paramiko
import CMDManager
import WaveCreator
import FileManager
import ProgramRunner

from commands import *
from constants import *
# ===================== THIS IS BAD, RESETS TO 0 AFTER EACH STEP =====================
PR = ProgramRunner.ProgramRunner()
#first connect
PR.connect()
PR.TEST_START_CMD()
PR.TEST_CMD_GENERATION()
PR.disconnect()