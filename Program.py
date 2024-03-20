#!/usr/bin/env python3
#Additional libraries to download
import matplotlib.pyplot as pplot

#REDPITAYA LIBRARAY FOR SCPI
import redpitaya_scpi as scpi

#CUSTOM MODULES
import Generate
import Acquire

#TODO change to class
class ProgramRunner:
    def __init__(self, uIP = 'rp-f0ba38.local'):
        self.IP = uIP
        self.PROGRAM_MODE = 0 #not running
        self.Generator = Generate.Generator(self.IP)
        self.Acquisitor = Acquire.Acquisitor(self.IP)

    def setGeneratorConstants(uChannelNumber = 1, uWaveform = 'sine', uAmplitude = 1, uFrequency = 1000):
        pass

    def setAcquisitionConstants(uChannelNumber = 1, uDecimation = 32, uTriggerLevel = 0.5, uTriggerDelay = 0):
        pass

    def run(self):
        match self.PROGRAM_MODE:
            case 0:
                pass
            case 1: #full run
                self.Generator.reset()
                self.Acquisitor.reset()

                #settings
                self.setGeneratorConstants() #Default vals
                self.setAcquisitionConstants() #Default vals

                #Starting generation
                self.Generator.startGenerating()

                #Starting acquisition
                self.dataBuffer = self.Acquisitor.runAcquisition()

            case 2:
                pass
            case 3:
                pass
            case 4:
                pass

    def changeMode():
        pass

    def exit():
        scpi.scpi(self.IP).close()

    def plotFromBuffer(self):
        pplot.plot(self.dataBuffer)
        pplot.ylabe('testWykres')
        pplot.show()