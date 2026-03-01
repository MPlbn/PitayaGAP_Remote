import redpitaya_scpi as scpi
import ProgramRunner
import Plotter
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
# data = []
# plotter = Plotter.FAcqPlotter()
# PR.Acquisitor.reset()
# PR.Acquisitor.setSCPIsettings()
# for i in range(5):
#     start = time.time()
#     data += PR.doStuffAcq()
#     end = time.time()
#     elapsed = end-start
#     print(f'step time: {elapsed} ms')
# PR.Acquisitor.stop()
# #data = PR.Acquisitor.processDataFull(data)
# plotter.testPlot(data)

PR.doStuff()
PR.disconnect()
