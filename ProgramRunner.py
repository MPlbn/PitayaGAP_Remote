#!/usr/bin/env python3
#Required libraries to download
import numpy as np

#Standard libraries
import time
import psutil
import socket
import os
import shutil

#Custom modules
import Acquire
import FileManager
import CMDManager
import WaveCreator
import DataProcessor
from constants import *
from commands import *

#   class responsible for work routine of a program

class ProgramRunner:
    def __init__(self, uIP = RED_PITAYA_IP):
        self.IP = uIP
        self.SCPI_IP = RED_PITAYA_IP
        self.PROGRAM_MODE = ProgramMode.IDLE
        self.socket = None
        self.genPauseState = False
        self.Acquisitor = Acquire.Acquisitor()
        self.isRunningContinous = False
        self.AcqDataProcessor = DataProcessor.AcquisitorDataProcessor()
        self.GenDataProcessor = DataProcessor.GeneratorDataProcessor()
        self.CSVFileManager = FileManager.CSVFileManager()
        self.CMDManager = CMDManager.CMDManager(self.IP)
        self.sendEvent = None
        self.currentCommand = None
        self.lastMode = None
        # self.stopPlotters = uSignalList[0]      
        # self.startPlotters = uSignalList[1]
        # self.updateProgressElements = uSignalList[2]

    def setEventFunction(self, uEventHandlerFunction):
        self.sendEvent = uEventHandlerFunction

    #   Connect to pitaya via ssh

    def connect(self):
        if (self.CMDManager.connectToPitaya() is not None):
            return True
        else:
            return False

    #   Disconnect from pitaya ssh

    def disconnect(self):
        self.CMDManager.disconnectFromPitaya()

    #   Startup routine used at the start of GUI

    def startupRoutine(self):
        isConnected = self.connect()
        if(not isConnected):
            print('Error, cannot connect...')
            for i in range(0,10):
                print(f' [{i}]Trying to connect to {self.IP} ...')
                isConnected = self.connect()
                if(isConnected):
                    break
                else:
                    time.sleep(2)
        if(isConnected):
            time.sleep(1)
            self.startCustomServer()
            self.disconnect()
            
        isTCPconnected = self.connectToServer()
        if(isTCPconnected):
            self.Acquisitor.setSocket(self.socket)
        else:
            print('Error connecting: TCP')
        
        return isConnected and isTCPconnected
        
    #   remotely loading the correct FPGA overlay and running the custom server used for live gen/acq

    def startCustomServer(self):
        stdout, stderr, status = self.CMDManager.executeCommand(CMD_LOAD_STANDARD_FPGA)
        time.sleep(1)
        stdout, stderr, status = self.CMDManager.executeCommand(CMD_START_CUSTOM_SERVER)
        time.sleep(1)

    #   connect to custom server via TCP socket

    def connectToServer(self):
        isConnected = False
        for _ in range(5):
            try:
                sock = socket.create_connection((RED_PITAYA_IP, 5000))
                isConnected = True
                break
            except ConnectionRefusedError:
                time.sleep(0.5)

        if(isConnected):
            sock.setsockopt(socket.IPPROTO_IP, socket.TCP_NODELAY, 1)
            self.socket = sock
        return isConnected
    
    def disconnectFromServer(self):
        self.socket.sendall(CLOSE_COMMAND)
        time.sleep(0.2)
        self.socket.close()
      
    #   Setting generator parameters passed from GUI when in normal mode
    #   uHighRange: float - ceiling voltage value which won't be passed while generating
    #   uLowRange: float - floor voltage value which won't be passed while generating
    #   uStep: float - value by which voltage output will change each step
    #   uDirection: string - anodic/kathodic
    #   uFrequency: int - frequency value
    #   uStartingValue: float - starting generator voltage

    def setContGeneratorParameters(self, uHighRange:float, uLowRange:float, uStep:float, uDirection:str, uStartingValue:float = 0.0):
        direction = 0
        if(uDirection == 'kathodic'):
            direction = 1

        CMDManager.executeTCPCommand(self.socket, SETUP_C_GEN_COMMAND)
        if(not CMDManager.readTCPReadyState(self.socket)):
            print("error: setContGeneratorParameters: ready state")
            return
        CMDManager.sendTCPGenMode(self.socket, GenModeGUI.NORMAL)
        CMDManager.sendTCPCGenSetupValues(self.socket, uStartingValue, uHighRange, uLowRange, uStep, direction)
        if(not CMDManager.readTCPReadyState(self.socket)):
            print("error: setSteppingGeneratorParameters: sendValues ready state")

    #   Setting generator parameters passed from GUI when in stepping mode
    #   uLimit: float - upper/lower voltage limit which won't be passed while generating
    #   uBase: float - base voltage that will be the starting point for each peak run while generating
    #   uStep: float - value by which voltage output will change each step
    #   uNumOfSteps: int - number of different voltage peaks to be created
    #   uFrequency: int - frequency value
    #   uStartingValue: float - starting generator voltage

    def setSteppingGeneratorParameters(self, uLimit:float, uBase:float, uStep:float, uNumOfSteps:int, uStartingValue:float = 0.0):
        CMDManager.executeTCPCommand(self.socket, SETUP_C_GEN_COMMAND)
        if(not CMDManager.readTCPReadyState(self.socket)):
            print("error: setContGeneratorParameters: ready state")
            return
        CMDManager.sendTCPGenMode(self.socket, GenModeGUI.STEP)
        CMDManager.sendTCPCGenStepSetupValues(self.socket, uBase, uLimit, uStep, uNumOfSteps)
        if(not CMDManager.readTCPReadyState(self.socket)):
            print("error: setSteppingGeneratorParameters: sendValues ready state")
        

    #   Setting acquisitor parameters passed form GUI
    #   uGain: string - gain mode (HV/LV)
    #   uDecimation: int - decimation value (how many samples are skipped between acquiring another one)

    def setAcquisitorParameters(self, uGain, uDecimation = 1):
        self.Acquisitor.setup(uDecimation=uDecimation, uGain=uGain)

    #   Converting ratio from combobox string to float ratio and passing it to dataProcessor
    #   uRatio: str - text acquired from combobox
    def processRatio(self, uRatio: str) -> float:
        return DataProcessor.processRatio(uRatio)

    #   Pausing generation of continous generator

    def pauseContGenerator(self):
        self.currentCommand = PAUSE_C_GEN_COMMAND
        self.lastMode = self.PROGRAM_MODE
        self.genPauseState = True
        self.changeMode(ProgramMode.GEN_COMMAND_SEND)

    #   Unpausing generation of continous generator

    def unpauseContGenerator(self):
        self.currentCommand = UNPAUSE_C_GEN_COMMAND
        self.lastMode = self.PROGRAM_MODE
        self.genPauseState = False
        self.changeMode(ProgramMode.GEN_COMMAND_SEND)

    def clearData(self):
        self.lastMode = self.PROGRAM_MODE
        self.changeMode(ProgramMode.IDLE)
        self.AcqDataProcessor.clear()
        self.GenDataProcessor.clear()

        self.changeMode(self.lastMode)
    #   Getter for current generator pause state

    def getContGeneratorPauseState(self):
        return self.genPauseState

    def sendSetup(self):
        frequency = 1000 # default value not changed
        decimation = self.Acquisitor.getDecimation()
        gain = self.Acquisitor.getGain()

        CMDManager.executeTCPCommand(self.socket, SETUP_COMMAND)
        if(not CMDManager.readTCPReadyState(self.socket)):
            print('error: ProgramRunner.sendSetup:Runing the command')
        CMDManager.sendTCPSetupValues(self.socket, frequency, decimation, gain)
        if(not CMDManager.readTCPReadyState(self.socket)):
            print('error: ProgramRunner.sendSetup:Setting the values')        

    # Change program mode to correctly run the CSV file saving

    def startSaveProcess(self):
            self.lastMode = self.PROGRAM_MODE
            self.changeMode(ProgramMode.CSV_WORK_ROUTINE)

    #   Save data to CSV file
    #   dataI: np.array() - Filled with value of the current
    #   dataV: np.array() - Filled with value of the voltages

    def saveDataToCSV(self, dataI = [], dataV = []):
        self.CSVFileManager.saveToFile(uVData=dataV, uIData=dataI)

    #   Resets the current voltage value to the set starting voltage value

    def resetGeneratorValue(self):
        CMDManager.executeTCPCommand(self.socket, RESET_C_GEN_COMMAND)

    def resetGenerator(self):
        CMDManager.executeTCPCommand(self.socket, RESET_GEN_COMMAND)
        if(not CMDManager.readTCPReadyState(self.socket)):
            print("error: resetGenerator()")

    def startGenerator(self):
        CMDManager.executeTCPCommand(self.socket, START_GEN_COMMAND)
        if(not CMDManager.readTCPReadyState(self.socket)):
            print("error: startGenerator()")
    #   Flips the step value (*-1) of continouous generator

    def flipGenStep(self):
        self.currentCommand = FLIP_C_GEN_COMMAND
        self.lastMode = self.PROGRAM_MODE
        self.changeMode(ProgramMode.GEN_COMMAND_SEND)

    def stopGen(self, uStopType: StopType):
        match uStopType:
            case StopType.STOP_RESET:
                CMDManager.executeTCPCommand(self.socket, STOP_GEN_COMMAND)
                CMDManager.executeTCPCommand(self.socket, RESET_C_GEN_COMMAND)
            case StopType.STOP_KEEP:
                CMDManager.executeTCPCommand(self.socket, STOP_GEN_COMMAND)
        if(not CMDManager.readTCPReadyState(self.socket)):
            print("error: Generator.stop")

    def genWorkRoutine(self):
        CMDManager.executeTCPCommand(self.socket, GEN_COMMAND)
        if(not CMDManager.readTCPReadyState(self.socket)):
            print("Error: genWorkRoutine()")

    #   Main work routine of program runner

    def run(self):
        match self.PROGRAM_MODE:
            case ProgramMode.IDLE:
                pass

            case ProgramMode.START:
                self.resetGenerator()
                self.Acquisitor.reset()
                self.sendSetup()
                self.startGenerator()
                self.Acquisitor.start()
                self.changeMode(ProgramMode.GEN_WORK_ROUTINE)
    
            case ProgramMode.PRE_WORK_ROUTINE: 
                self.Acquisitor.workRoutine()
                Vbuffer = self.Acquisitor.getCurrentV()
                Ibuffer = self.Acquisitor.getCurrentI()
                genVal = self.Acquisitor.getGenVal()
                self.processDataBuffer(genVal, DataType.GEN)
                self.processDataBuffer([Vbuffer, Ibuffer], DataType.ACQ)
                self.changeMode(ProgramMode.GEN_WORK_ROUTINE)

            case ProgramMode.GEN_WORK_ROUTINE: 
                self.genWorkRoutine()
                self.Acquisitor.workRoutine()
                Vbuffer = self.Acquisitor.getCurrentV()
                Ibuffer = self.Acquisitor.getCurrentI()
                genVal = self.Acquisitor.getGenVal()
                self.processDataBuffer(genVal, DataType.GEN)
                self.processDataBuffer([Vbuffer, Ibuffer], DataType.ACQ)
           
            case ProgramMode.CSV_WORK_ROUTINE:
                self.stopGen(StopType.STOP_KEEP) 
                self.Acquisitor.stop()
                self.CSVFileManager.createFile()
                self.saveDataToCSV(dataV=self.AcqDataProcessor.getDataV(), dataI=self.AcqDataProcessor.getDataI())
                self.startGenerator()
                self.Acquisitor.start()
                self.changeMode(self.lastMode)

            case ProgramMode.GEN_COMMAND_SEND:
                CMDManager.executeTCPCommand(self.socket, self.currentCommand)
                self.changeMode(self.lastMode)

            case ProgramMode.GEN_STOP:
                self.stopGen(StopType.STOP_RESET)
                self.Acquisitor.stop()

                if(self.genPauseState):
                    self.unpauseContGenerator()
                
                self.changeMode(ProgramMode.IDLE)

            case ProgramMode.EXIT:
                self.stopGen(StopType.STOP_RESET)
                self.Acquisitor.stop()
                
                if(self.genPauseState):
                    self.unpauseContGenerator()
                
                self.disconnectFromServer()
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
        pass

    #   Passing data to data processor processing function
    #   uBuffer: array of floats - buffer = [V, I] for ACQ, buffer = [V] for Gen
    #   uDataType: DataType - determines which data processor should take care of data buffer
    
    def processDataBuffer(self, uBuffer, uDataType):
        match uDataType:
            case DataType.ACQ:
                self.AcqDataProcessor.processData(uBuffer)
            case DataType.GEN:
                self.GenDataProcessor.processData(uBuffer)

    #   Closing the custom server connection

    def exit(self):
        self.changeMode(ProgramMode.EXIT)

class FastProgramRunner:
    def __init__(self, uIP = RED_PITAYA_IP):
        self.ip = uIP
        self.WAVFileManager = FileManager.WAVFileManager()
        self.JSONFileManager = FileManager.JSONFileManager()
        self.CSVFileManager = FileManager.CSVFileManager()
        self.CMDManager = CMDManager.CMDManager(self.ip)
        self.WaveCreator = WaveCreator.WaveCreator()
        self.data = [[], []]

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
        time.sleep(1)

    #   calculates number of loops + leftover samples that are needed for fast acquisition
    #   uSamplesNumber: int - number of samples needed for full run

    def processNumberOfSamples(self, uSamplesNumber):
        loopNumber = int(uSamplesNumber / WF_FULL_SIZE)
        leftoverSamples = uSamplesNumber - (WF_FULL_SIZE * loopNumber)
        return [loopNumber, leftoverSamples]

    def processWaveForm(self, uWaveForm, uHighPoint, uLowPoint, uStartPoint, uFrequency):
        waveFormValues = self.WaveCreator.create(uWaveForm, uHighPoint, uLowPoint, uStartPoint, uFrequency)
        self.WAVFileManager.saveToFile(uWaveForm, waveFormValues, self.WaveCreator.getSampleRate())
        if(uFrequency < 10):
            dacRate = F_GEN_DEFAULT_DACRATE
        else:
            dacRate = uFrequency * 1000
        return dacRate 


    def setConfig(self, uDacRate, uDecimation, uCH1, uCH2):
        configData = self.JSONFileManager.getFileValue()
        # changing the values
        configData[CONFIG_ACQ][CONFIG_ACQ_CH1] = uCH1
        configData[CONFIG_ACQ][CONFIG_ACQ_CH2] = uCH2
        configData[CONFIG_ACQ][CONFIG_DEC] = uDecimation
        configData[CONFIG_GEN][CONFIG_GEN_RATE] = uDacRate

        self.JSONFileManager.saveToFile(configData)

    def pushConfig(self):
        self.CMDManager.executeLocalCommand(CMD_UPLOAD_CONFIG())
        
     
    def runGeneration(self):
        command = CMD_START_STREAMING_DAC()
        command[7] = self.WAVFileManager.getCurrentPath()
        print(command)
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
            self.CMDManager.executeCommand(f'{CMD_STOP_PROCESS}+{pid}')

    
    def runAcquisition(self, uSamples, uFileType):
        command = CMD_START_STREAMING_ADC()
        command[5] = str(uFileType)
        command[9] = str(uSamples) 
        print(command)
        self.CMDManager.executeLocalCommand(command)

    #   Running full run for fast samples
    #   uWaveForm: string - type of waveform
    #   uAmplitude: float - amplitude
    #   uFrequency: int - frequency
    #   uDecimation: int - chosen decimation
    #   uSamples: int - how many samples to collect before closing 
    #   uGain: string - type of acq gain (HV/LV)

    def setup(self, uWaveForm, uHighPoint, uLowPoint, uStartPoint, uFrequency, uDecimation, uCH1, uCH2):
        #Setups - this will be done differently
        dacRate = self.processWaveForm(uWaveForm, uHighPoint, uLowPoint, uStartPoint, uFrequency)
        self.setConfig(dacRate,uDecimation, uCH1, uCH2)
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
    
    def dataLogsCleanup(self):
        folder = "dataLogs"
        for item in os.listdir(folder):
            item_path = os.path.join(folder, item)

            if(os.path.isfile(item_path) or os.path.islink(item_path)):
                os.remove(item_path)
            elif(os.path.isdir(item_path)):
                shutil.rmtree(item_path)
        
    def cleanup(self):
        self.outputFix()
        self.WAVFileManager.cleanup()
        self.dataLogsCleanup()

    def runCleanupGeneration(self):
        waveformValues = self.WaveCreator.createZero()
        self.WAVFileManager.saveZeroWave(waveformValues, self.WaveCreator.getSampleRate())
        command = CMD_START_STREAMING_DAC()
        command[7] = self.WAVFileManager.getZeroWavePath()   
        command[9] = "1"
        self.CMDManager.executeLocalCommand(command)     

    def outputFix(self):
        self.runCleanupGeneration()

    def getLatestData(self):
        return self.data
        
    def saveToCSV(self):
        self.data = self.CSVFileManager.rawToVolt()
        self.CSVFileManager.createFile("FAST_")
        self.CSVFileManager.saveToFile(self.data[0], self.data[1])

    def run(self, uWaveForm, uHighPoint, uLowPoint, uStartPoint, uFrequency, uDecimation, uSamples, uCH1, uCH2, uFileType):
        self.setup(uWaveForm, uHighPoint, uLowPoint, uStartPoint, uFrequency, uDecimation, uCH1, uCH2)
        self.runGeneration()
        self.runAcquisition(uSamples, uFileType)
        self.saveToCSV()
        self.cleanup()

        