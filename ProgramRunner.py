#!/usr/bin/env python3
#Required libraries to download
import numpy as np
import ttkbootstrap

#Standard libraries
import time

#Redpitaya module for scpi connection and communication
import redpitaya_scpi as scpi

#Custom modules
import Generate
import Acquire
import Plotter
import FileManager
from constants import *


#TODO Stop resets lock/unlock

#   class responsible for work routine of a program

class ProgramRunner:
    def __init__(self, uIP = 'rp-f0ba38.local'):
        self.IP = uIP
        self.PROGRAM_MODE = ProgramMode.IDLE
        self.ContGenerator = Generate.ContGenerator(self.IP)
        self.Acquisitor = Acquire.Acquisitor(self.IP)
        self.isRunningContinous = False
        self.dataBuffer = [] #not used for now
        self.AcqPlotter = Plotter.AcqPlotter()
        self.GenPlotter = Plotter.GenPlotter()
        self.FileManager = FileManager.FileManager()

    #   passing frame to plotter class to place the drawn plot
    #   uPlotterFrame: ttk.Frame - gui frame from GUI class
    #   uPlotterType: PlotType - determines which Plotter is to be configured

    def setPlotterFrame(self, uPlotterFrame, uPlotterType):
        match uPlotterType:
            case PlotType.ACQ:
                self.AcqPlotter.setFrame(uPlotterFrame)
                self.AcqPlotter.initVisuals()
            case PlotType.GEN:
                self.GenPlotter.setFrame(uPlotterFrame)
                self.GenPlotter.initVisuals()        

    #   handler of generation values
    #   uChannelNumber: int - channel that generation will be performed on - [1,2]
    #   uWaveForm: string - type of signal to be generated - [sine, dc, saw, square, triangle, arbitrary]
    #   uAmplitude: float - amplitude of signal, in case of dc: value of constant
    #   uFrequency: int - frequency of signal, in Hz
    #   NOT USED NOT USED NOT USED NOT USED NOT USED

    # def setGeneratorConstants(self, uChannelNumber = DEFAULT_CHANNEL, uWaveform = 'sine', uAmplitude = 1, uFrequency = 1000):
    #     self.Generator.setup(uChannelNumber, uWaveform, uFrequency, uAmplitude)

    #   setting generator parameters passed from GUI when in normal mode
    #   uHighRange: float - ceiling voltage value which won't be passed while generating
    #   uLowRange: float - floor voltage value which won't be passed while generating
    #   uStep: float - value by which voltage output will change each step

    def setContGeneratorParameters(self, uHighRange, uLowRange, uStep, uDirection, uStartingValue):
        self.ContGenerator.setRanges(uHighRange, uLowRange)
        self.ContGenerator.setStep(uStep)
        self.ContGenerator.setDirection(uDirection)
        self.ContGenerator.setStartingValue(uStartingValue)

    #   setting generator parameters passed from GUI when in stepping mode
    #   uLimit: float - upper/lower voltage limit which won't be passed while generating
    #   uBase: float - base voltage that will be the starting point for each peak run while generating
    #   uStep: float - value by which voltage output will change each step
    #   uNumofSteps: int - number of different voltage peaks to be created

    def setSteppingGeneratorParameters(self, uLimit, uBase, uStep, uNumOfSteps):
        self.ContGenerator.setSteppingRanges(uLimit, uBase)
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

    #   converting ratio from combobox string to float ratio and passing it to plotter
    #   uRatio: str - text acquired from combobox

    def setDataRatio(self, uRatio: str):
        numerator, denominator = map(int, uRatio.split('/'))
        result: float = numerator/denominator
        self.AcqPlotter.setRatio(result)    

    #   pausing generation of continous generator

    def pauseContGenerator(self):
        self.ContGenerator.pause()

    #   unpausing generation of continous generator

    def unpauseContGenerator(self):
        self.ContGenerator.unpause()

    #   getter for current generator pause state
    def getContGeneratorPauseState(self):
        return self.ContGenerator.getPause()

    #   updates GUI elements - progress bar, progress label and plots
    #   uProgressBar - progress bar passed from GUI
    #   uProgressLabel - progress label passed from GUI

    def updateGUIElements(self, uProgressBar, uProgressLabel):
        uProgressBar.configure(value = self.ContGenerator.voltageToPercent())
        uProgressLabel.configure(text=str(round(self.ContGenerator.voltageValue, self.ContGenerator.getRoundingNumber())))
        self.AcqPlotter.updatePlot()
        self.AcqPlotter.canvas.draw()
        self.GenPlotter.updatePlot()
        self.GenPlotter.canvas.draw()

    #   saves the current plots displayed data to as CSV file - to be changed to save real data
    def saveDataToCSV(self):
        self.changeMode(ProgramMode.PAUSE)
        self.FileManager.saveToFile(self.GenPlotter.getData(),
                                    self.AcqPlotter.getData())
        self.changeMode(ProgramMode.UNPAUSE)

    #   resets the current voltage value to the set starting voltage value
    def resetGenerator(self):
        self.ContGenerator.resetGenValue()

    #   flips the step value (*-1) of continouous generator
    def flipGenStep(self):
        self.ContGenerator.flipDirection()

    #   main work routine of program runner

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
                self.AcqPlotter.start()
                self.GenPlotter.start()
                self.ContGenerator.applyDirection()
                self.changeMode(ProgramMode.PRE_WORK_ROUTINE) 
    
            case ProgramMode.GEN_STOP: #Stop continous
                #run to 0 and stop
                self.ContGenerator.stopGen(StopType.STOP_RESET)

                if(self.ContGenerator.getPause()):
                    self.ContGenerator.unpause()
                
                self.AcqPlotter.stop()
                self.GenPlotter.stop()
                self.changeMode(ProgramMode.IDLE)

            case ProgramMode.GEN_WORK_ROUTINE:
                tStartTime = time.time()

                self.ContGenerator.workRoutine()
                self.processDataBuffer(self.ContGenerator.voltageValue, PlotType.GEN)
                self.Acquisitor.reset()
                self.Acquisitor.setup()
                self.Acquisitor.start()
                buffer = np.array(self.Acquisitor.getBuff())
                self.processDataBuffer(buffer, PlotType.ACQ)
                self.Acquisitor.stop()
                
                #Time check
                tStopTime = time.time()
                tElapsed = (tStopTime - tStartTime) * 1000
                print(f'Elapsed time: {tElapsed} ms')
                
            case ProgramMode.STEPPING_START:
                self.ContGenerator.changeMode(GeneratorMode.STEPPING)
                self.ContGenerator.reset()
                self.ContGenerator.setup()
                self.ContGenerator.setRanges(uHRange=self.ContGenerator.steppingRanges[0], uLRange=GEN_DEFAULT_VOLTAGE) #here to change
                self.ContGenerator.startGen()
                self.AcqPlotter.start()
                self.GenPlotter.start()
                self.changeMode(ProgramMode.PRE_WORK_ROUTINE)
            
            case ProgramMode.PRE_WORK_ROUTINE:
                self.processDataBuffer(self.ContGenerator.voltageValue, PlotType.GEN)
                self.Acquisitor.reset()
                self.Acquisitor.setup()
                self.Acquisitor.start()
                buffer = np.array(self.Acquisitor.getBuff())
                self.processDataBuffer(buffer, PlotType.ACQ)
                self.Acquisitor.stop()
                self.changeMode(ProgramMode.GEN_WORK_ROUTINE)
            
            case ProgramMode.PAUSE:
                self.ContGenerator.stopGen(StopType.STOP_KEEP)
                self.AcqPlotter.stop()
                self.GenPlotter.stop()
                self.changeMode(ProgramMode.IDLE)
            
            case ProgramMode.UNPAUSE:
                self.ContGenerator.startGen()
                self.AcqPlotter.start()
                self.GenPlotter.start()
                self.changeMode(ProgramMode.GEN_WORK_ROUTINE)
            
    #   Changing the work routine
    #   newMode: int - new mode to be set

    def changeMode(self, newMode: ProgramMode):
        if newMode.value >= FIRST_MODE and newMode.value <= LAST_MODE:
            self.PROGRAM_MODE = newMode
        else:
            print("Error: Invalid mode number")
    
    #   Step increment/decrement handler
    #   uChangeType: int = modifier to step value

    def manualChangeGenVoltage(self, uChangeType):
        self.ContGenerator.manualChangeVoltage(uChangeType)

    #   Passing data to plotter processing function
    #   uBuffer: array of floats - buffer returned from aqcuisition
    #   uPlotterType: PlotType - determines which plotter should take care of data buffer
    
    def processDataBuffer(self, uBuffer, uPlotterType):
        match uPlotterType:
            case PlotType.ACQ:
                self.AcqPlotter.processData(uBuffer)
            case PlotType.GEN:
                self.GenPlotter.processData(uBuffer)
    
    #   closing the scpi connection

    def exit(self):
        self.changeMode(ProgramMode.GEN_STOP)
        scpi.scpi(self.IP).close()

#   class responsible for work routine of N samples variant of the program
class fastProgramRunner:
    def __init__(self):
        pass

    def exit(self):
        pass