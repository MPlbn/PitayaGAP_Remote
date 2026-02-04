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
import CMDManager
import WaveCreator
import psutil
from constants import *
from commands import *

#   class responsible for work routine of a program

class ProgramRunner:
    def __init__(self, uIP = 'rp-f0ba38.local'):
        self.IP = uIP
        self.PROGRAM_MODE = ProgramMode.IDLE
        self.ContGenerator = Generate.ContGenerator(self.IP)
        self.FastGenerator = Generate.Generator(self.IP)
        self.Acquisitor = Acquire.Acquisitor(self.IP)
        self.isRunningContinous = False
        self.dataBuffer = [] #not used for now
        self.AcqPlotter = Plotter.AcqPlotter()
        self.GenPlotter = Plotter.GenPlotter()
        self.CSVFileManager = FileManager.CSVFileManager()
        self.CMDManager = CMDManager.CMDManager(uIP)


    def connect(self):
        if (self.CMDManager.connectToPitaya() is not None):
            return True
        else:
            return False

    def disconnect(self):
        self.CMDManager.disconnectFromPitaya()

    #TODO
    def startSCPIServer(self):
        pass

    def stopSCPIServer(self):
        pass

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

    def setContGeneratorParameters(self, uHighRange, uLowRange, uStep, uDirection, uStartingValue = 0.0):
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

    #   setting acquisitor parameters passed form GUI
    #   uGain: string - gain mode (HV/LV)
    #   uDecimation: int - decimation value (how many samples are skipped between acquiring another one)

    def setAcquisitorParameters(self, uGain, uDecimation = 4):
        self.Acquisitor.setup(uDecimation=uDecimation, uGain=uGain)

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

    def startSaveProcess(self):
        if(self.PROGRAM_MODE == ProgramMode.IDLE):
            self.changeMode(ProgramMode.CSV_WORK_ROUTINE_TO_IDLE)
        else:
            self.changeMode(ProgramMode.CSV_WORK_ROUTINE_TO_GEN)

    #   dataI: np.array() - Filled with value of the current
    #   dataV: np.array() - Filled with value of the voltages
    def saveDataToCSV(self, dataI = [], dataV = []):
            self.CSVFileManager.saveToFile(uVData=dataV, uIData=dataI, uIsMock=True)

    #   resets the current voltage value to the set starting voltage value
    def resetGenerator(self):
        self.ContGenerator.resetGenValue()

    #   flips the step value (*-1) of continouous generator
    def flipGenStep(self):
        self.ContGenerator.flipDirection()

    #   clears the data from both plotters
    def clearPlot(self):
        self.AcqPlotter.clear()
        self.GenPlotter.clear()

    #   main work routine of program runner

    def run(self):
        match self.PROGRAM_MODE:
            case ProgramMode.IDLE: #idle state
                pass

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
                self.Acquisitor.setSCPIsettings()
                self.Acquisitor.start()
                buffer = self.Acquisitor.getBuff(ACQ_SAMPLE_SIZE)
                Vbuffer = np.array(buffer[0])
                Ibuffer = np.array(buffer[1])
                self.processDataBuffer(Vbuffer, PlotType.ACQ, Ibuffer)
                self.Acquisitor.stop()
                
                #Time check
                tStopTime = time.time()
                tElapsed = (tStopTime - tStartTime) * 1000
                print(f'Elapsed time: {tElapsed} ms')
                
            case ProgramMode.STEPPING_START:
                self.ContGenerator.changeMode(GeneratorMode.STEPPING)
                self.ContGenerator.reset()
                self.ContGenerator.setup()
                self.ContGenerator.setRanges(uHRange=self.ContGenerator.steppingRanges[0], uLRange=GEN_DEFAULT_VOLTAGE) #TODO something to check here
                self.ContGenerator.startGen()
                self.AcqPlotter.start()
                self.GenPlotter.start()
                self.changeMode(ProgramMode.PRE_WORK_ROUTINE)
            
            case ProgramMode.PRE_WORK_ROUTINE:
                self.processDataBuffer(self.ContGenerator.voltageValue, PlotType.GEN)
                self.Acquisitor.reset()
                self.Acquisitor.setSCPIsettings()
                self.Acquisitor.start()
                buffer = self.Acquisitor.getBuff(ACQ_SAMPLE_SIZE)
                Vbuffer = np.array(buffer[0])
                Ibuffer = np.array(buffer[1])
                self.processDataBuffer(Vbuffer, PlotType.ACQ, Ibuffer)
                self.Acquisitor.stop()
                self.changeMode(ProgramMode.GEN_WORK_ROUTINE)
            
            case ProgramMode.CSV_WORK_ROUTINE_TO_GEN:
                self.ContGenerator.stopGen(StopType.STOP_KEEP)
                self.AcqPlotter.stop()
                self.GenPlotter.stop()
                self.CSVFileManager.createFile()
                self.saveDataToCSV(dataV=self.AcqPlotter.getData())
                self.ContGenerator.startGen()
                self.AcqPlotter.start()
                self.GenPlotter.start()
                self.changeMode(ProgramMode.GEN_WORK_ROUTINE)

            case ProgramMode.CSV_WORK_ROUTINE_TO_IDLE:
                self.ContGenerator.stopGen(StopType.STOP_KEEP)
                self.AcqPlotter.stop()
                self.GenPlotter.stop()
                self.CSVFileManager.createFile()
                self.saveDataToCSV(dataV=self.AcqPlotter.getData())
                self.ContGenerator.startGen()
                self.AcqPlotter.start()
                self.GenPlotter.start()
                self.changeMode(ProgramMode.IDLE)

            
            
            
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
    
    def processDataBuffer(self, uBuffer, uPlotterType, uBufferCurrent=[]):
        match uPlotterType:
            case PlotType.ACQ:
                self.AcqPlotter.processData(uBufferCurrent, uBuffer)
            case PlotType.GEN:
                self.GenPlotter.processData(uBuffer)
    
    #   closing the scpi connection

    def exit(self):
        self.changeMode(ProgramMode.GEN_STOP)
        scpi.scpi(self.IP).close()


class FastProgramRunner:
    def __init__(self, uIP = 'rp-f0ba38.local'):
        self.ip = uIP
        self.WAVFileManager = FileManager.WAVFileManager()
        self.JSONFileManager = FileManager.JSONFileManager()
        self.CMDManager = CMDManager.CMDManager(self.ip)
        self.WaveCreator = WaveCreator.WaveCreator()

    def connect(self) -> bool:
        if (self.CMDManager.connectToPitaya() is not None):
            return True
        else:
            return False
        
    def disconnect(self):
        self.CMDManager.disconnectFromPitaya()

    def runStreamingServer(self):
        stdout, stderr, status = self.CMDManager.executeCommand(CMD_LOAD_STREAMING_FPGA)
        time.sleep(1)
        stodut, stderr, status = self.CMDManager.executeCommand(CMD_START_STREAMING_SERVER)

    #   calculates number of loops + leftover samples that are needed for fast acquisition
    #   uSamplesNumber: int - number of samples needed for full run
    def processNumberOfSamples(self, uSamplesNumber):
        loopNumber = int(uSamplesNumber / WF_SAMPLES_IN_PERIOD)
        leftoverSamples = uSamplesNumber - (WF_SAMPLES_IN_PERIOD * loopNumber)
        return [loopNumber, leftoverSamples]

    def processWaveForm(self, uWaveForm, uAmplitude):
        waveFormValues = self.WaveCreator.create(uWaveForm, uAmplitude)
        self.WAVFileManager.saveToFile(uWaveForm, waveFormValues, self.WaveCreator.getSampleRate())


    def setConfig(self, uFrequency, uDecimation, uCH1, uCH2):
        configData = self.JSONFileManager.getFileValue()
        # changing the values
        configData[CONFIG_ACQ][CONFIG_ACQ_CH1] = uCH1
        configData[CONFIG_ACQ][CONFIG_ACQ_CH2] = uCH2
        configData[CONFIG_ACQ][CONFIG_DEC] = uDecimation
        configData[CONFIG_GEN][CONFIG_GEN_RATE] = uFrequency

        self.JSONFileManager.saveToFile(configData)

    def pushConfig(self):
        self.CMDManager.executeLocalCommand(CMD_UPLOAD_CONFIG)
        
     
    def runGeneration(self):
        command = CMD_START_STREAMING_DAC
        command[5] = self.WAVFileManager.getCurrentPath()
        self.CMDManager.executeLocalCommand(command)

    def stopStreaming(self):
        #kill the process on PC
        processName = PROC_NAME
        for process in psutil.process_iter():
            if(process.name() == processName):
                process.kill() 
        #kill the process on pitaya
        self.CMDManager.executeCommand(CMD_LIST_PROCESS)
        output = self.CMDManager.getOutput()
        pids = [int(line.split()[0]) for line in output.strip().splitlines()]
        for pid in pids:
            self.CMDManager.executeCommand(f'{CMD_STOP_STREAMING_SERVER}+{pid}')

    
    def runAcquisition(self, uSamples):
        command = CMD_START_STREAMING_ADC
        command[7] = str(uSamples) 
        self.CMDManager.executeLocalCommand(command)

    #   Running full run for fast samples
    #   uWaveForm: string - type of waveform
    #   uAmplitude: float - amplitude
    #   uFrequency: int - frequency
    #   uDecimation: int - chosen decimation
    #   uSamples: int - how many samples to collect before closing 
    #   uGain: string - type of acq gain (HV/LV)

    def setup(self, uWaveForm, uAmplitude, uFrequency, uDecimation, uCH1, uCH2):
        #Setups - this will be done differently
        self.setConfig(uFrequency, uDecimation, uCH1, uCH2)
        self.processWaveForm(uWaveForm, uAmplitude)

        #load fpga, start server, push the config command
        self.runStreamingServer()
        self.pushConfig()

    def startupRoutine(self):
        isConnected = self.connect()
        if(not isConnected):
            print('Error, cannot connect...')
            for i in range(0,10):
                print(f' [{i}]Trying to connect to {self.ip} ...')
                isConnected = self.connect()
                if(isConnected):
                    break
                else:
                    time.sleep(2)
        return isConnected
        

    def run(self, uWaveForm, uAmplitude, uFrequency, uDecimation, uSamples, uCH1, uCH2):

        self.setup(uWaveForm, uAmplitude, uFrequency, uDecimation, uCH1, uCH2)
        self.runGeneration()
        self.runAcquisition(uSamples)
        self.stopStreaming()
    