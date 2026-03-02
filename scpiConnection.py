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
data = []
plotter = Plotter.FAcqPlotter()

voltage = 0
step = 0.5
hBound = 1
lBound = -1
finBuff = []
PR.ContGenerator.reset()
PR.Acquisitor.reset()
PR.Acquisitor.setSCPIsettings()
PR.ContGenerator.startGen()
for i in range(5):
    PR.ContGenerator.changeVolt(voltage)
    if(voltage + step > hBound or voltage + step < lBound):
        step *= -1
    voltage += step
    time.sleep(0.01)
    data += PR.doStuffAcq()
PR.Acquisitor.stop()
PR.ContGenerator.stopGen(StopType.STOP_RESET)
#data = PR.Acquisitor.processDataFull(data)
plotter.testPlot(data)

#PR.doStuff()
PR.disconnect()
