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
        self.isRunningContinous = False
        self.continousData = []
        self.currentGeneratedValue = 0
        self.currentGeneratedValueStep = 0.00001

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
                self.setGeneratorConstants(uWaveform="arbitrary") #Default vals
                self.setGeneratorArbitraryValue(0.3)
                self.setAcquisitionConstants() #Default vals

                #Starting generation
                self.Generator.startGenerating()

                #Starting acquisition
                self.dataBuffer = self.Acquisitor.runAcquisition()

            case 2: #Continous run
                    self.Generator.reset()
                    self.Acquisitor.reset()
                    self.generateContinousValue()
                    self.setAcquisitionConstants(1, 16384, 0, 0)
                    self.setGeneratorConstants(1, 'dc', self.currentGeneratedValue, 1000000)
                    self.Generator.startGenerating() 
                    self.dataBuffer = self.Acquisitor.runAcquisition() 
                    self.continousData.append(self.dataBuffer)    
                    self.plotContinous()             
                        

            case 3:
                pass
            case 4:
                pass

    def changeMode(self, newMode):
        if newMode >= 0 and newMode < 3:
            self.PROGRAM_MODE = newMode
        else:
            print("Error: Invalid mode number")

    def exit(self):
        scpi.scpi(self.IP).close()
    
    def generateContinousValue(self):
        if self.currentGeneratedValue >= 1 or self.currentGeneratedValue <= -1:
            self.currentGeneratedValueStep *= -1
        self.currentGeneratedValue += self.currentGeneratedValueStep


    def plotFromBuffer(self):
        pplot.plot(self.dataBuffer)
        pplot.ylabel('testWykres')
        pplot.show()

    def plotContinous(self):
        pplot.plot(self.continousData)
        pplot.ylabel('testWykresCiag')
        pplot.show()