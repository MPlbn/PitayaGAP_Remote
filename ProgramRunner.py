#!/usr/bin/env python3
#Required libraries to download
import matplotlib.pyplot as pplot
import numpy as np
import time

#Redpitaya module for scpi connection and communication
import redpitaya_scpi as scpi

#Custom modules
import Generate
import Acquire
import Plotter


#   class responsible for work routine of a program

class ProgramRunner:
    def __init__(self, uIP = 'rp-f0ba38.local'):
        self.IP = uIP
        self.PROGRAM_MODE = 0 #not running
        self.Generator = Generate.Generator(self.IP)
        self.ContGenerator = Generate.ContGenerator(self.IP)
        self.Acquisitor = Acquire.Acquisitor(self.IP)
        self.Plotter = Plotter.Plotter()
        self.isRunningContinous = False
        self.continousData = []
        self.dataBuffer = []
        self.LAST_BUFFER_VALUE = 16000 #To verify number


    #   handler of generation values
    #   uChannelNumber: int - channel that generation will be performed on - [1,2]
    #   uWaveForm: string - type of signal to be generated - [sine, dc, saw, square, triangle, arbitrary]
    #   uAmplitude: float - amplitude of signal, in case of dc: value of constant
    #   uFrequency: int - frequency of signal, in Hz

    def setGeneratorConstants(self, uChannelNumber = 1, uWaveform = 'sine', uAmplitude = 1, uFrequency = 1000):
        self.Generator.setup(uChannelNumber, uWaveform, uFrequency, uAmplitude)


    #   handler of acquisition values
    #   uChannelNumber: int - channel that acquisition will be performed on - [1,2]
    #   uDecimation: int - decimation value (how many samples are skipped between acquiring another one)
    #   uTriggerLevel: float - level that at which trigger will start acquisition
    #   uTriggerDelay: float - time needed after trigger to start acquisition 

    def setAcquisitionConstants(self, uChannelNumber = 1, uDecimation = 32, uTriggerLevel = 0.5, uTriggerDelay = 0):
        self.Acquisitor.setup(uDecimation, uTriggerLevel, uTriggerDelay)
        self.Acquisitor.channelNumber = uChannelNumber


    #   pausing generation of continous generator

    def pauseContGenerator(self):
        self.ContGenerator.pause()


    #   unpausing generation of continous generator

    def unpauseContGenerator(self):
        self.ContGenerator.unpause()


    #   main work routine of program runner

    def run(self, uAx, uCanvas):
        match self.PROGRAM_MODE:
            case 0: #idle state
                pass
            case 1: #full run
                self.Generator.reset()
                self.Acquisitor.reset()

                #settings
                self.setGeneratorConstants(uWaveform="sine") #Default vals
                self.setAcquisitionConstants() #Default vals

                #Starting generation
                self.Generator.startGenerating()

                #wait to limit initial junk data
                time.sleep(1)

                #Starting acquisition
                self.dataBuffer = self.Acquisitor.runAcquisition() #sth is broken
                
                #stopping acquisition and generation
                self.Acquisitor.stopAcquisition()
                self.Generator.stopGenerating()
                self.Plotter.plot(self.dataBuffer, uAx, uCanvas)
                #back to idle

                #Maybe clear dataBuffer?? TODO
                self.changeMode(0)

            case 2: #Continous run start
                   # self.Acquisitor.reset()
                    self.ContGenerator.reset()
                    #self.setAcquisitionConstants(1, 0, 0, 0) 
                    self.ContGenerator.setup(uAmplitude=0)
                    self.ContGenerator.startGen()
                    #self.Acquisitor.startAcquisition()
                    self.changeMode(4)           

            case 3: #Stop continous
                #run to 0 and stop
                self.Acquisitor.stopAcquisition()
                self.ContGenerator.stopGen()
                self.changeMode(0)

            case 4:
                self.ContGenerator.workRoutine()
                #time.sleep(1)
                #voltage = self.Acquisitor.runContAcquisition()[self.LAST_BUFFER_VALUE-500] #test the last value and check performance, maybe switching to C needed
                #print(voltage)
                #self.continousData.append(voltage)
                #self.Plotter.plot(self.continousData, uAx, uCanvas)

            # TEST MODES
            case 5:
                self.Acquisitor.reset()
                self.ContGenerator.reset()
                
                self.setGeneratorConstants(uFrequency=7)
                #self.setAcquisitionConstants()
                self.Generator.startGenerating()

                # self.Acquisitor.setup()
                # print("odpalanie akwizycji")
                # self.ContGenerator.setupTEST()
                # print("setup generatora")
                # self.ContGenerator.startGen()
                # print("Start generatora")
                # self.Acquisitor.startAcquisition()
                #self.changeMode(0)
                #print("zmiana trybu")
            
            case 6:
                self.Acquisitor.startAcquisition()
                self.dataBuffer = self.Acquisitor.runAcquisition()
                self.Acquisitor.stopAcquisition()
                self.Plotter.plot(self.dataBuffer, uAx, uCanvas)

                # print("Wykonywanie rutyny")
                # self.ContGenerator.workRoutineTEST()
                # time.sleep(1)
                # print("odbieranie danych")
                # self.Acquisitor.triggerContAcquisition()
                # voltage = self.Acquisitor.runContAcquisition()
                # print(voltage)
                # self.continousData.append(voltage)
                # self.Plotter.plot(self.continousData, uAx, uCanvas)

    #   Changing the work routine
    #   newMode: int - new mode to be set

    def changeMode(self, newMode):
        if newMode >= 0 and newMode <= 6:
            self.PROGRAM_MODE = newMode
        else:
            print("Error: Invalid mode number")
    

    #   closing the scpi connection

    def exit(self):
        scpi.scpi(self.IP).close()
    