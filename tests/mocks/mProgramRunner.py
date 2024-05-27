#!/usr/bin/env python3
#Required libraries to download
import numpy as np
import ttkbootstrap

#Standard libraries
import time

#Custom modules
import mGenerate
import mAcquire
import mPlotter
from mConstants import *


#   class responsible for work routine of a program

class ProgramRunner:
    def __init__(self, uIP = "mockedIP"):
        self.IP = uIP
        self.PROGRAM_MODE = ProgramMode.IDLE
        #self.Generator = mGenerate.Generator(self.IP)
        self.ContGenerator = mGenerate.ContGenerator(self.IP)
        self.Acquisitor = mAcquire.Acquisitor(self.IP)
        self.isRunningContinous = False
        self.dataBuffer = [] #not used for now
        self.Plotter = mPlotter.Plotter()

    #   passing frame to plotter class to place the drawn plot
    #   uPlotterFrame: ttk.Frame - gui frame from GUI class

    def setPlotterFrame(self, uPlotterFrame):
        self.Plotter.setFrame(uPlotterFrame)
        self.Plotter.initVisuals()

    #   setting generator parameters passed from GUI
    #   uHighRange: float - ceiling voltage value which won't be passed while generating
    #   uLowRange: float - floor voltage value which won't be passed while generating
    #   uStep: float - value by which voltage output will change each step

    def setContGeneratorParameters(self, uHighRange, uLowRange, uStep):
        self.ContGenerator.setRanges(uHighRange, uLowRange)
        self.ContGenerator.setStep(uStep)

    def setSteppingGeneratorParameters(self, uMaxRange, uBase, uStep, uNumOfSteps):
        self.ContGenerator.setBase(uBase)
        self.ContGenerator.setRanges(uHRange=uMaxRange)
        self.ContGenerator.createSteps(uNumOfSteps)
        self.ContGenerator.setStep(uStep)

    #   handler of acquisition values
    #   uChannelNumber: int - channel that acquisition will be performed on - [1,2]
    #   uDecimation: int - decimation value (how many samples are skipped between acquiring another one)
    #   uTriggerLevel: float - level that at which trigger will start acquisition
    #   uTriggerDelay: float - time needed after trigger to start acquisition 

    def setAcquisitionConstants(self, uChannelNumber = DEFAULT_CHANNEL, uDecimation = 32, uTriggerLevel = 0.5, uTriggerDelay = 0):
        self.Acquisitor.setup(uDecimation, uTriggerLevel, uTriggerDelay)
        self.Acquisitor.channelNumber = uChannelNumber


    #   pausing generation of continous generator

    def pauseContGenerator(self):
        self.ContGenerator.pause()


    #   unpausing generation of continous generator

    def unpauseContGenerator(self):
        self.ContGenerator.unpause()

    ##HELPER

    def updateGUIElements(self, uProgressBar, uProgressLabel):
        uProgressBar.configure(value = self.ContGenerator.voltageToPercent())
        uProgressLabel.configure(text=str(round(self.ContGenerator.voltageValue, self.ContGenerator.getRoundingNumber())))
        self.Plotter.updatePlot()
        self.Plotter.canvas.draw()


    #   main work routine of program runner
    #   uProgressBar - progress bar passed from GUI to be updated
    #   uProgressLabel - label showing current voltage value, passed from GUI to be updated 

    def run(self):
        match self.PROGRAM_MODE:
            case ProgramMode.IDLE: #idle state
                pass
            case ProgramMode.FULL_RUN: #full run
                pass
                # self.Generator.reset()
                # self.Acquisitor.reset()

                # #settings
                # self.setGeneratorConstants(uWaveform="sine") #Default vals
                # self.setAcquisitionConstants() #Default vals

                # #Starting generation
                # self.Generator.startGenerating()

                # #wait to limit initial junk data
                # time.sleep(1)

                # #Starting acquisition
                # self.dataBuffer = self.Acquisitor.runAcquisition() #sth is broken
                
                # #stopping acquisition and generation
                # self.Acquisitor.stopAcquisition()
                # self.Generator.stopGenerating()
                # self.Plotter.plot(self.dataBuffer, uAx, uCanvas)
                # #back to idle

                #Maybe clear dataBuffer?? TODO
                #self.changeMode(0)

            case ProgramMode.CONT_START: #Continous run start
                self.ContGenerator.changeMode(GeneratorMode.CONT)
                self.ContGenerator.reset()
                self.ContGenerator.setup()
                self.ContGenerator.startGen()
                self.Plotter.start()
                self.changeMode(ProgramMode.GEN_WORK_ROUTINE) 
    
            case ProgramMode.GEN_STOP: #Stop continous
                #run to 0 and stop
                self.ContGenerator.stopGen()
                self.Plotter.stop()
                self.changeMode(ProgramMode.IDLE)

            case ProgramMode.GEN_WORK_ROUTINE:
                self.ContGenerator.workRoutine()
                self.Acquisitor.reset()
                self.Acquisitor.setup()
                self.Acquisitor.start()
                self.Acquisitor.mockedSetBuff(self.ContGenerator.mockedGetGeneratedValue())
                buffer = self.Acquisitor.getBuff() 
                self.processAcqBuffer(buffer)
                self.Acquisitor.stop()
                
            case ProgramMode.STEPPING_START:
                self.ContGenerator.changeMode(GeneratorMode.STEPPING)
                self.ContGenerator.reset()
                self.ContGenerator.setup() 
                self.ContGenerator.setRanges(uHRange=self.ContGenerator.steppingRanges[0], uLRange=GEN_DEFAULT_VOLTAGE) # value for test
                self.ContGenerator.startGen()
                self.Plotter.start()
                self.changeMode(ProgramMode.GEN_WORK_ROUTINE)

    #   Changing the work routine
    #   newMode: int - new mode to be set

    def changeMode(self, newMode: ProgramMode):
        if newMode.value >= FIRST_MODE and newMode.value <= LAST_MODE:
            self.PROGRAM_MODE = newMode
        else:
            print("Error: Invalid mode number")
    
    #   Passing data to plotter processing function
    #   uBuffer: array of floats - buffer returned from aqcuisition

    def processAcqBuffer(self, uBuffer):
        self.Plotter.processData(uBuffer)
    
    #   closing the scpi connection

    def exit(self):
        self.changeMode(ProgramMode.CONT_STOP)
    