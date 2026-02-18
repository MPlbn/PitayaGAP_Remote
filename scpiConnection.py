import redpitaya_scpi as scpi
import ProgramRunner
import time
from commands import *

PR = ProgramRunner.ProgramRunner()

ip = [
    '169.254.49.194',
    'rp-f0ba38.local',
    '192.168.1.100',
]

PR.connect()
stdout, stderr, status = PR.CMDManager.executeCommand(CMD_LOAD_SCPI_FPGA)
time.sleep(1)

stdout, stderr, status = PR.CMDManager.executeCommand(CMD_START_SCPI_SERVER)
time.sleep(1)
PR.initialize()
PR.generateStuff()
PR.disconnect()
