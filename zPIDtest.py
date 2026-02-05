from constants import *
from commands import *
import ProgramRunner
import time

Pr = ProgramRunner.FastProgramRunner()
Pr.connect()
Pr.runStreamingServer()
command = CMD_LIST_PROCESS
time.sleep(1)
stdout, stderr, status = Pr.CMDManager.executeCommand(command)
output = Pr.CMDManager.getOutput()
pids = [int(line.split()[0]) for line in output.strip().splitlines()]
for pid in pids:
            Pr.CMDManager.executeCommand(f'{CMD_STOP_PROCESS}+{pid}')
Pr.disconnect()