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
        self.ContGenerator = Generate.ContGenerator(self.IP)
        self.Acquisitor = Acquire.Acquisitor(self.IP)
        self.isRunningContinous = False
        self.continousData = []
        self.dataBuffer = []

    def setGeneratorConstants(self, uChannelNumber = 1, uWaveform = 'sine', uAmplitude = 1, uFrequency = 1000):
        self.Generator.setup(uChannelNumber, uWaveform, uAmplitude, uFrequency)

    def setAcquisitionConstants(self, uChannelNumber = 1, uDecimation = 32, uTriggerLevel = 0.5, uTriggerDelay = 0):
        self.Acquisitor.setup(uDecimation, uTriggerLevel, uTriggerDelay)
        self.Acquisitor.channelNumber = uChannelNumber

    def setGeneratorArbitraryValue(uValue):
        pass

    def run(self):
        match self.PROGRAM_MODE:
            case 0:
                pass
            case 1: #full run
                self.Generator.reset()
                self.Acquisitor.reset()
                #settings
                self.setGeneratorConstants(uWaveform="sine") #Default vals
                self.setAcquisitionConstants() #Default vals

                #Starting generation
                self.Generator.startGenerating()

                #Starting acquisition
                self.dataBuffer = self.Acquisitor.runAcquisition() #sth is broken

            case 2: #Continous run start
                    self.Acquisitor.reset()
                    self.setAcquisitionConstants(1, 1024, 0, 0)
                    self.ContGenerator.startGen()
                    #self.Acquisitor.startAcquisition()
                    self.changeMode(4)           

            case 3: #Stop continous
                #run to 0 and stop
                self.Acquisitor.stopAcquisition()
                self.ContGenerator.stopGen()

            case 4:
                self.ContGenerator.workRoutine()
                voltage = self.Acquisitor.runContAcquisition()
                self.continousData.append(voltage)

    def changeMode(self, newMode):
        if newMode >= 0 and newMode <= 4:
            self.PROGRAM_MODE = newMode
        else:
            print("Error: Invalid mode number")

    def exit(self):
        scpi.scpi(self.IP).close()
    
    def plotFromBuffer(self):
        pplot.plot(self.dataBuffer)
        pplot.ylabel('testWykres')
        pplot.show()

    def plotContinous(self):
        pplot.plot(self.continousData)
        pplot.ylabel('testWykresCiag')
        pplot.show()