from constants import *
from commands import ACQ_COMMAND, START_ACQ_COMMAND, RESET_ACQ_COMMAND, STOP_ACQ_COMMAND
from CMDManager import executeTCPCommand, readTCPReadyState, readTCPAcqValues

#   class responsible for constant, real time data acquisition from RedPitaya.
#   uses Custom Server
class Acquisitor:
    def __init__(self):
        self.socket = None
        self.decimation = 1
        self.gain = ACQ_DEFAULT_GAIN
        self.currentValues = [0.0, 0.0]

    def setSocket(self, uSocket):
        self.socket = uSocket

    #   resets acquisition
    def reset(self):
        executeTCPCommand(self.socket, RESET_ACQ_COMMAND)
        if(not readTCPReadyState(self.socket)):
            print("error: Acquisitor.reset")

    #   acquisition settings
    def setup(self, uDecimation, uGain):
        self.decimation = uDecimation
        self.gain = uGain

    #   returns decimation
    def getDecimation(self):
        return self.decimation
    
    #   returns gain
    def getGain(self):
        if self.gain == "HV":
            return True
        else:
            return False
        

    #   starts acquisition
    def start(self):
        executeTCPCommand(self.socket, START_ACQ_COMMAND)
        if(not readTCPReadyState(self.socket)):
            print("error: Acquisitor.start")

    #   stops acquisition
    def stop(self):
        executeTCPCommand(self.socket, STOP_ACQ_COMMAND)
        if(not readTCPReadyState(self.socket)):
            print("error: Acquisitor.stop")

    def workRoutine(self):
        executeTCPCommand(self.socket, ACQ_COMMAND)
        self.currentValues = readTCPAcqValues(self.socket)

    def getCurrentV(self):
        return self.currentValues[0]

    def getCurrentI(self):
        return self.currentValues[1]
        