#!/usr/bin/env python3

#outside imports
import threading as thread
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import sys
import time

#inside imports
import mProgramRunner
from mConstants import *

class GUI:
    def __init__(self):
        self.PR = mProgramRunner.ProgramRunner()
        self.root = ttk.Window(themename="superhero", size=GUI_DEFAULT_WINDOW_SIZE)
        self.interval: int = GUI_DEFAULT_INTERVAL
        self.thread = thread.Thread(target=self.threadTask)
        self.thread.daemon = True
        self.running = False
        self.genMode = "normal"
        self.direction = "anodic"
        self.ratio = "1/1"

    #buttons
    def startGeneratingPress(self):
        #starting continous generation in Program Runner work routine
        match self.genMode:
            case "normal":
                self.PR.changeMode(ProgramMode.CONT_START)
            case "stepping":
                self.PR.changeMode(ProgramMode.STEPPING_START)

        self.startBtn.state(GUI_DISABLED)
        self.stopBtn.state(GUI_ENABLED)
        self.lockBtn.state(GUI_ENABLED)

    def stopGeneratingPress(self):
        #stopping continous generation in Program Runner work routine
        self.PR.changeMode(ProgramMode.GEN_STOP)
        self.stopBtn.state(GUI_DISABLED)
        self.startBtn.state(GUI_ENABLED)
        self.lockBtn.state(GUI_DISABLED)
        self.unlockBtn.state(GUI_DISABLED)

    def lockGeneratingPress(self):
        #locking current voltage value on Continous Generator and pausing autogeneration
        self.PR.pauseContGenerator()
        self.lockBtn.state(GUI_DISABLED)
        self.unlockBtn.state(GUI_ENABLED)
    
    def unlockGeneratingPress(self):
        #unlocking current voltage value on Continous Generator and resuming autogeneration
        self.PR.unpauseContGenerator()
        self.unlockBtn.state(GUI_DISABLED)
        self.lockBtn.state(GUI_ENABLED)

    def savePress(self):
        self.PR.saveDataToCSV()

    def resetGeneratingPress(self):
        self.PR.resetGenerator()

    def flipGeneratingPress(self):
        self.PR.flipGenStep()

    def comboboxCallback(self, value):
        self.genMode = str(self.genModeCombobox.get())
        self.FRAME_LIST[str(self.genModeCombobox.get())].tkraise()

    def dirComboboxCallback(self, value):
        self.direction = str(self.directionCombobox.get())
        
    def ratioComboboxCallback(self, value):
        self.ratio = str(self.IVratioCombobox.get())    

    def stepUpKey(self, event=None):
        if(self.PR.getContGeneratorPauseState()):
            self.PR.manualChangeGenVoltage(GUI_INCREMENT_STEP)

    def stepDownKey(self, event=None):
        if(self.PR.getContGeneratorPauseState()):
            self.PR.manualChangeGenVoltage(GUI_DECREMENT_STEP)

    def exitFullscreenKey(self, event=None):
        self.root.attributes('-fullscreen', False)
    
    def enterFullscreenKey(self, event=None):
        self.root.attributes('-fullscreen', True)

    def passRatio(self):
        self.PR.setDataRatio(self.ratio)

    def setRangesPress(self):
        tempMessage: str = ""
        tempStep: float = float(self.stepEntry.get()) if self.stepEntry.get() != "" else GEN_DEFAULT_STEP
        tempTime: int = int(self.intervalEntry.get()) if self.intervalEntry.get() != "" else GUI_DEFAULT_INTERVAL

        print(self.direction)

        if(tempStep > GEN_MAX_STEP):
            tempStep = GEN_MAX_STEP
            self.stepEntry.delete(0, ttk.END)
            self.stepEntry.insert(0, str(GEN_MAX_STEP))
            tempMessage += f"Error: Step value cannot be higher than {GEN_MAX_STEP}\n"

        if(tempStep <= 0):
            tempStep = GEN_DEFAULT_STEP
            self.stepEntry.delete(0, ttk.END)
            self.stepEntry.insert(0, str(GEN_DEFAULT_STEP))
            tempMessage += "Error: Step value cannot be 0 or lower\n"
        
        if(tempTime > GUI_MAX_INTERVAL):
            tempTime = GUI_MAX_INTERVAL
            self.intervalEntry.delete(0, ttk.END)
            self.intervalEntry.insert(0, str(GUI_MAX_INTERVAL))
            tempMessage += f"Error: Interval cannot be higher than {GUI_MAX_INTERVAL}ms\n"

        if(tempTime < GUI_MIN_INTERVAL):
            tempTime = GUI_MIN_INTERVAL
            self.intervalEntry.delete(0, ttk.END)
            self.intervalEntry.insert(0, str(GUI_MIN_INTERVAL))
            tempMessage += f"Error: Interval cannot be lower than {GUI_MIN_INTERVAL}ms\n"


        match self.genMode:
            case "normal":
                #collecting data from entries
                tempHRange: float = float(self.hRangeEntry.get()) if self.hRangeEntry.get() != "" else GEN_DEFAULT_HRANGE
                tempLRange: float = float(self.lRangeEntry.get()) if self.lRangeEntry.get() != "" else GEN_DEFAULT_LRANGE
                tempStPoint: float = float(self.startingPointEntry.get()) if self.startingPointEntry != "" else GEN_DEFAULT_VOLTAGE


                #validations
                if(tempHRange < tempLRange):
                    temp = tempLRange
                    tempHRange = tempLRange
                    tempLRange = temp
                    self.hRangeEntry.delete(0, ttk.END)
                    self.lRangeEntry.delete(0, ttk.END)
                    self.hRangeEntry.insert(0, f'{tempHRange}')
                    self.lRangeEntry.insert(0, f'{tempLRange}')

                if(tempHRange > GEN_MAX_RANGE):
                    tempHRange = GEN_MAX_RANGE
                    self.hRangeEntry.delete(0, ttk.END)
                    self.hRangeEntry.insert(0, str(GEN_MAX_RANGE))
                    tempMessage += f"Error: Range cannot be higher than {GEN_MAX_RANGE}\n"

                if(tempHRange < GEN_MIN_RANGE):
                    tempHRange = GEN_MIN_RANGE
                    self.hRangeEntry.delete(0, ttk.END)
                    self.hRangeEntry.insert(0, str(GEN_MIN_RANGE))
                    tempMessage += f"Error: Range cannot be lower than {GEN_MIN_RANGE}\n"

                if(tempLRange > GEN_MAX_RANGE):
                    tempLRange = GEN_MAX_RANGE
                    self.lRangeEntry.delete(0, ttk.END)
                    self.lRangeEntry.insert(0, str(GEN_MAX_RANGE))
                    tempMessage += f"Error: Range cannot be higher than {GEN_MAX_RANGE}\n"

                if(tempLRange < GEN_MIN_RANGE):
                    tempLRange = GEN_MIN_RANGE
                    self.lRangeEntry.delete(0, ttk.END)
                    self.lRangeEntry.insert(0, str(GEN_MIN_RANGE))
                    tempMessage += f"Error: Range cannot be lower than {GEN_MIN_RANGE}\n"    

                if(tempHRange == tempLRange):
                    tempHRange = GEN_DEFAULT_HRANGE
                    tempLRange = GEN_DEFAULT_LRANGE
                    self.hRangeEntry.delete(0, ttk.END)
                    self.lRangeEntry.delete(0, ttk.END)
                    self.hRangeEntry.insert(0, str(GEN_DEFAULT_HRANGE))
                    self.lRangeEntry.insert(0, str(GEN_DEFAULT_LRANGE))
                    tempMessage += f"Error: Ranges cannot have the same value - resetting to default range values\n"

                if(tempStPoint > GEN_MAX_RANGE or
                    tempStPoint < GEN_MIN_RANGE):
                        self.startingPointEntry.delete(0, ttk.END)
                        self.startingPointEntry.insert(0, str(GEN_DEFAULT_VOLTAGE))
                        tempMessage += f"Error: Starting point cannot have value outside of bounds - resseting to 0.0V\n"

                # if(tempStPoint > tempHRange):
                #     pass

                # if(tempStPoint < tempLRange):
                #     pass

                self.PR.setContGeneratorParameters(tempHRange, tempLRange, tempStep, self.direction, tempStPoint)
            case "stepping":
                #collecting values
                tempLimit : float = float(self.maxRangeEntry.get()) if self.maxRangeEntry.get() != "" else GEN_DEFAULT_HRANGE 
                tempBase: float = float(self.baseEntry.get()) if self.baseEntry.get() != "" else GEN_DEFAULT_VOLTAGE
                tempNumOfSteps: int = int(self.numOfStepsEntry.get()) if self.numOfStepsEntry.get() != "" else GEN_DEFAULT_NUM_STEPS

                if(tempLimit > GEN_MAX_RANGE):
                    tempLimit = GEN_MAX_RANGE
                    self.baseEntry.delete(0, ttk.END)
                    self.baseEntry.insert(0, str(GEN_MIN_RANGE))
                    tempMessage += f"Error: Upper limit cannot be higher than {GEN_MAX_RANGE}"

                if(tempLimit < GEN_MIN_RANGE):
                    tempLimit = GEN_MIN_RANGE
                    self.maxRangeEntry.delete(0, ttk.END)
                    self.maxRangeEntry.insert(0, str(GEN_MIN_RANGE))
                    tempMessage += f"Error: Upper limit cannot be lower than {GEN_MIN_RANGE}"

                if(tempBase > GEN_MAX_RANGE):
                    tempBase = GEN_MAX_RANGE
                    self.baseEntry.delete(0, ttk.END)
                    self.baseEntry.insert(0, str(GEN_MAX_RANGE))
                    tempMessage += f"Error: Base voltage cannot be higher than {GEN_MAX_RANGE}"
                
                if(tempBase < GEN_MIN_RANGE):
                    tempBase = GEN_MIN_RANGE
                    self.baseEntry.delete(0, ttk.END)
                    self.baseEntry.insert(0, str(GEN_MIN_RANGE))
                    tempMessage += f"Error: Base voltage cannot be lower than {GEN_MIN_RANGE}"

                if(tempBase == tempLimit):
                    tempBase = GEN_DEFAULT_VOLTAGE
                    tempLimit = GEN_MAX_RANGE

                    self.baseEntry.delete(0, ttk.END)
                    self.baseEntry.insert(0, str(GEN_DEFAULT_VOLTAGE))
                    self.maxRangeEntry.delete(0, ttk.END)
                    self.maxRangeEntry.insert(0, str(GEN_MAX_RANGE))
                    tempMessage += f"Error: Base voltage and upper limit cannot be tha same - resetting values"

                #Temporary, for sure to change TODO
                # if(tempBase > tempMaxRange):
                #     temp = tempBase
                #     tempBase = tempMaxRange
                #     tempMaxRange = temp
                #     self.baseEntry.delete(0, ttk.END)
                #     self.baseEntry.insert(0, str(tempBase))
                #     self.maxRangeEntry.delete(0, ttk.END)
                #     self.maxRangeEntry.insert(0, str(tempMaxRange))

                if(tempNumOfSteps < 2):
                    tempNumOfSteps = 2
                    self.numOfStepsEntry.delete(0, ttk.END)
                    self.numOfStepsEntry.insert(0, str(2))
                    tempMessage += f"Error: Number of steps cannot be lower than 2"

                if(tempNumOfSteps > 30):
                    tempNumOfSteps = 30
                    self.numOfStepsEntry.delete(0, ttk.END)
                    self.numOfStepsEntry.insert(0, str(30))
                    tempMessage += f"Error: Number of steps cannot be higher than 30"

                self.PR.setSteppingGeneratorParameters(tempLimit, tempBase, tempStep, tempNumOfSteps)

        #showing error message
        self.errorLabel.configure(text = tempMessage)

        #setting values
        self.interval = tempTime
        self.passRatio()

    def threadTask(self):
        while True:
            self.PR.run()
            self.root.after(0, self.updateFun)
            time.sleep(self.interval/1000)
    
    def updateFun(self):
        self.PR.updateGUIElements(self.progressBar, self.progressLabel)
        

    def stopGUI(self):
        #Close ProgramRunner and gui
        self.PR.exit()
        sys.exit()

    # VALIDATION FUNCTIONS

    def validateInt(self, uEntryValue) -> bool:
        if(uEntryValue == ""):
            return True
        try:
            int(uEntryValue)
            return True
        except ValueError:
            return False

    def validateFloat(self, uEntryValue) -> bool:
        if(uEntryValue == ''):
            return True
    
        if(uEntryValue == '-'):
            return True
        try:
            float(uEntryValue)
            return True
        except ValueError:
            return False 

    def validatePositiveFloat(self, uEntryValue) -> bool:
        if(uEntryValue == ''):
            return True
        if(uEntryValue == '-' or uEntryValue[0] == '-'):
            return False
        try:
            float(uEntryValue)
            return True
        except ValueError:
            return False


    def initGUI(self):
        ####style configuration
        self.style = ttk.Style()
        self.style.configure('TButton', font=("Segoe UI", 20))
        self.style.configure('info.Outline.TButton', font=("Segoe UI", 12))

        ####registering validation functions
        self.valInt = self.root.register(self.validateInt)
        self.valFloat = self.root.register(self.validateFloat)
        self.valPosFloat = self.root.register(self.validatePositiveFloat)

        ####creating widgets
        #main frame containing top row of widgets
        #self.settingsAndButtonsFrame = ttk.Frame(self.root)
        #progress and generator frame
        self.genProgFrame = ttk.Frame(self.root)

        #settings
        self.settingsFrame = ttk.Labelframe(self.genProgFrame, bootstyle=INFO, text='settings')
        self.genModeCombobox = ttk.Combobox(self.settingsFrame, bootstyle=INFO, state=READONLY)

        #standard settings used everytime
        self.standardSetFrame = ttk.Frame(self.settingsFrame)
        self.stepLabel = ttk.Label(self.standardSetFrame , bootstyle=INFO, text='Step value [V]')
        self.intervalLabel = ttk.Label(self.standardSetFrame , bootstyle=INFO, text='Speed value')
        self.stepEntry = ttk.Entry(self.standardSetFrame , bootstyle=INFO, validatecommand=(self.valPosFloat, '%P'), validate="key")
        self.intervalEntry = ttk.Entry(self.standardSetFrame, bootstyle=INFO, validatecommand=(self.valInt, '%P'), validate="key")
        self.setBtn = ttk.Button(self.standardSetFrame , text='Set', bootstyle=(INFO,OUTLINE), command=self.setRangesPress)
        self.IVratioLabel = ttk.Label(self.standardSetFrame, bootstyle=INFO, text='I/V [A/mV]')
        self.IVratioCombobox = ttk.Combobox(self.standardSetFrame, bootstyle=INFO, state=READONLY)

        #normal settings
        self.normalSetFrame = ttk.Frame(self.settingsFrame, width=350, height=170)
        self.hRangeLabel = ttk.Label(self.normalSetFrame , bootstyle=INFO , text='High Range [V]')
        self.lRangeLabel = ttk.Label(self.normalSetFrame , bootstyle=INFO, text='Low Range [V]')
        self.directionLabel = ttk.Label(self.normalSetFrame, bootstyle=INFO, text='Direction')
        self.startingPointLabel = ttk.Label(self.normalSetFrame, bootstyle=INFO, text='Starting voltage [V]')
        self.hRangeEntry = ttk.Entry(self.normalSetFrame , bootstyle=INFO, validatecommand=(self.valFloat, '%P'), validate="key")
        self.lRangeEntry = ttk.Entry(self.normalSetFrame , bootstyle=INFO, validatecommand=(self.valFloat, '%P'), validate="key")
        self.directionCombobox = ttk.Combobox(self.normalSetFrame, bootstyle=INFO, state=READONLY, width=10)
        self.startingPointEntry = ttk.Entry(self.normalSetFrame, bootstyle=INFO, validatecommand=(self.valFloat, '%P'), validate="key")
    
        #stepping settings
        self.steppingSetFrame = ttk.Frame(self.settingsFrame, width=350, height=170)
        self.baseLabel = ttk.Label(self.steppingSetFrame, bootstyle=INFO, text='Base level [V]')
        self.maxRangeLabel = ttk.Label(self.steppingSetFrame, bootstyle=INFO, text='Limit value [V]')
        self.numOfStepsLabel = ttk.Label(self.steppingSetFrame, bootstyle=INFO, text='No. of steps')
        self.baseEntry = ttk.Entry(self.steppingSetFrame, bootstyle=INFO, validatecommand=(self.valFloat, '%P'), validate="key")
        self.maxRangeEntry = ttk.Entry(self.steppingSetFrame, bootstyle=INFO, validatecommand=(self.valFloat, '%P'), validate="key")
        self.numOfStepsEntry = ttk.Entry(self.steppingSetFrame, bootstyle=INFO, validatecommand=(self.valInt, '%P'), validate="key")

        #Setting combobox values
        self.genModeCombobox['values'] = GUI_COMBOBOX_VALUES
        self.genModeCombobox.set(GUI_COMBOBOX_VALUES[0])
        self.genModeCombobox.bind('<<ComboboxSelected>>', self.comboboxCallback)

        self.directionCombobox['values'] = GUI_DIR_COMBOBOX_VALUES 
        self.directionCombobox.set(GUI_DIR_COMBOBOX_VALUES[0])
        self.directionCombobox.bind('<<ComboboxSelected>>', self.dirComboboxCallback)

        self.IVratioCombobox['values'] = GUI_RATIO_COMBOBOX_VALUES
        self.IVratioCombobox.set(GUI_RATIO_COMBOBOX_VALUES[0])
        self.IVratioCombobox.bind('<<ComboboxSelected>>', self.ratioComboboxCallback)

        #Setting default values to entries
        self.hRangeEntry.insert(0, str(GEN_DEFAULT_HRANGE))
        self.lRangeEntry.insert(0, str(GEN_DEFAULT_LRANGE))
        self.stepEntry.insert(0, str(GEN_DEFAULT_STEP))
        self.intervalEntry.insert(0, str(GUI_DEFAULT_INTERVAL))
        self.startingPointEntry.insert(0, str(GEN_DEFAULT_VOLTAGE))

        self.baseEntry.insert(0, str(GEN_DEFAULT_VOLTAGE))
        self.maxRangeEntry.insert(0, str(GEN_DEFAULT_HRANGE))
        self.numOfStepsEntry.insert(0, str(GEN_DEFAULT_NUM_STEPS))

        #errors
        self.errorFrame = ttk.LabelFrame(self.root, width=50, height=50, text='errors', bootstyle=INFO)
        self.errorLabel = ttk.Label(self.errorFrame, text="", bootstyle=(DANGER), width=50, font=("Segoe UI", 8))

        #buttons
        self.buttonsFrame = ttk.Frame(self.root)
        self.startBtn = ttk.Button(self.buttonsFrame, text='Start', bootstyle=(SUCCESS,OUTLINE), command=self.startGeneratingPress)
        self.stopBtn = ttk.Button(self.buttonsFrame, text='Stop', bootstyle=(DANGER,OUTLINE), command=self.stopGeneratingPress) #Should not reset the generation TODO
        self.lockBtn = ttk.Button(self.buttonsFrame, text='Lock', bootstyle=(PRIMARY,OUTLINE), command=self.lockGeneratingPress)
        self.unlockBtn = ttk.Button(self.buttonsFrame, text='Unlock', bootstyle=(PRIMARY,OUTLINE), command=self.unlockGeneratingPress)
        self.saveBtn = ttk.Button(self.buttonsFrame, text='Save Data', bootstyle=(PRIMARY,OUTLINE), command=self.savePress)
        self.resetBtn = ttk.Button(self.buttonsFrame, text='Reset', bootstyle=(DANGER,OUTLINE), command=self.resetGeneratingPress)
        self.flipBtn = ttk.Button(self.buttonsFrame, text="Flip", bootstyle=(PRIMARY,OUTLINE), command=self.flipGeneratingPress)

        self.stopBtn.state(GUI_DISABLED)
        self.lockBtn.state(GUI_DISABLED)
        self.unlockBtn.state(GUI_DISABLED)


        #progress
        self.progressFrame = ttk.Frame(self.genProgFrame)
        self.progressBar = ttk.Progressbar(self.progressFrame, length=300, bootstyle=(PRIMARY))
        self.progressInfoLabel = ttk.Label(self.progressFrame, bootstyle=INFO, text='Current generated value', font=("Segoe UI", 15, "bold"))
        self.progressLabel = ttk.Label(self.progressFrame, bootstyle=PRIMARY, text='0.00', font=("Segoe UI", 20, "bold"))

        #plot
        self.plotFrame = ttk.Frame(self.root, width=1000, height=700, border=5, relief="sunken", bootstyle=SECONDARY)
        self.PR.setPlotterFrame(self.plotFrame, PlotType.ACQ)

        #generation plot
        self.genPlotFrame = ttk.Frame(self.genProgFrame, border=5, relief="sunken", bootstyle=SECONDARY)
        self.PR.setPlotterFrame(self.genPlotFrame, PlotType.GEN)

        #frame list
        self.FRAME_LIST = {"normal" : self.normalSetFrame, "stepping" : self.steppingSetFrame}

        #binding keyboard keys to their functionality
        #temporary without numpad
        self.root.bind('[', self.stepUpKey)
        self.root.bind(']', self.stepDownKey)
        
        #should work, don't have a numpad to check out
        #self.root.bind('KP_Add', self.stepUpKey)
        #self.root.bind('KP_Substract', self.stepDownKey)
        self.root.bind('f', self.enterFullscreenKey)
        self.root.bind('<Escape>', self.exitFullscreenKey)


    def startGUI(self):
        #placing widgets
        #self.settingsAndButtonsFrame.pack(padx=20, pady=20)
        self.genProgFrame.pack(side=LEFT, anchor=N)
        self.plotFrame.pack(padx=20, pady=10, anchor=NE)#, fill=BOTH)
        self.plotFrame.pack_propagate(False)

        self.settingsFrame.pack(padx=20, pady=20, ipadx=20)   #grid(row=0, column=0, columnspan=2, rowspan=5, ipadx=20, ipady=20)
        self.genModeCombobox.grid(row=0, column=0)

        self.normalSetFrame.grid(row=1, column=0, sticky=NSEW)
        self.normalSetFrame.grid_propagate(False)
        self.hRangeLabel.grid(row=0, column=0, padx=5)
        self.lRangeLabel.grid(row=1, column=0, padx=5)
        self.directionLabel.grid(row=2, column=0, padx=5)
        self.startingPointLabel.grid(row=3, column=0, padx=5)
        self.hRangeEntry.grid(row=0, column=1, pady=5)
        self.lRangeEntry.grid(row=1, column=1, pady=5)
        self.directionCombobox.grid(row=2, column=1, pady=5, sticky=W)
        self.startingPointEntry.grid(row=3, column=1, pady=5)
        
        self.steppingSetFrame.grid(row=1, column=0, sticky=NSEW)
        self.steppingSetFrame.grid_propagate(False)
        self.baseLabel.grid(row=0, column=0, padx=5)
        self.maxRangeLabel.grid(row=1, column=0, padx=5)
        self.numOfStepsLabel.grid(row=2, column=0, padx=5)
        self.baseEntry.grid(row=0, column=1, pady=5)
        self.maxRangeEntry.grid(row=1, column=1, pady=5)
        self.numOfStepsEntry.grid(row=2, column=1, pady=5)

        self.standardSetFrame.grid(row=2,column=0)
        self.stepLabel.grid(row=1, column=0, padx=5)
        self.intervalLabel.grid(row=2, column=0, padx=5)
        self.IVratioLabel.grid(row=3, column=0, padx=5)
        self.stepEntry.grid(row=1, column=1, pady=5)
        self.intervalEntry.grid(row=2, column=1, pady=5)
        self.IVratioCombobox.grid(row=3, column=1, pady=5)
        self.setBtn.grid(row=5,column=1, pady=10)



        self.buttonsFrame.pack()#grid(row=0, column=4, rowspan=3)
        self.startBtn.grid( row=0, column=0, pady=5, padx=5)
        self.stopBtn.grid(  row=0, column=1, pady=5, padx=5)
        self.resetBtn.grid( row=0, column=2, pady=5, padx=5)
        self.lockBtn.grid(  row=1, column=0, pady=5, padx=5)
        self.unlockBtn.grid(row=1, column=1, pady=5, padx=5)
        self.flipBtn.grid(  row=1, column=2, pady=5, padx=5)
        self.saveBtn.grid(  row=2, column=0, pady=5, padx=5)

        self.errorFrame.pack()#grid(row=0, column=3, rowspan=5, columnspan=1, padx=40, sticky=NSEW, pady=20)
        self.errorLabel.grid(row=0,column=0)
        self.errorFrame.pack_propagate(False)

        self.progressFrame.pack(padx=20,pady=20)
        self.progressInfoLabel.pack(padx=20)
        self.progressLabel.pack(padx=20, pady=10)
        self.progressBar.pack(padx=20)

        self.genPlotFrame.pack(padx=5)

        self.normalSetFrame.tkraise()

        #plotting done in Plotter class     

        self.thread.start()
        #run gui
        self.root.mainloop()

class fastGUI:
    def __init__(self):
        self.root = (ttk.Window(themename="superhero", size=F_GUI_DEFAULT_WINDOW_SIZE))
        self.PR = mProgramRunner.ProgramRunner()
        self.waveForm = F_GEN_DEFAULT_WAVEFORM
        self.decimation = F_GEN_DEFAULT_DEC

    def validateInt(self, uEntryValue) -> bool:
        if(uEntryValue == ""):
            return True
        try:
            int(uEntryValue)
            return True
        except ValueError:
            return False

    def validateFloat(self, uEntryValue) -> bool:
        if(uEntryValue == ''):
            return True
    
        if(uEntryValue == '-'):
            return True
        try:
            float(uEntryValue)
            return True
        except ValueError:
            return False 

    def waveFormComboboxCallback(self, value):
        self.waveForm = str(self.waveFormCB.get())

    def decComboboxCallback(self, value):
        self.decimation = int(self.decCB.get())

    def initGUI(self):
        ##style configuration
        self.style = ttk.Style()
        self.style.configure('TButton', font=("Segoe UI", 20))
        self.style.configure('info.Outline.TButton', font=("Segoe UI", 12))

        self.valInt = self.root.register(self.validateInt)
        self.valFloat = self.root.register(self.validateFloat)    

        #main Setttings frame
        self.settingsFrame = ttk.LabelFrame(self.root, bootstyle=INFO, text='setting DBG')

        #genSettings frame
        self.genSettingsFrame = ttk.Labelframe(self.settingsFrame, bootstyle=INFO, text='Generator')
        self.waveFormCB = ttk.Combobox(self.genSettingsFrame, bootstyle=INFO, state=READONLY)
        self.ampEntry = ttk.Entry(self.genSettingsFrame , bootstyle=INFO, validatecommand=(self.valFloat, '%P'), validate="key")
        self.freqEntry = ttk.Entry(self.genSettingsFrame, bootstyle=INFO, validatecommand=(self.valInt, '%P'), validate="key")

        self.waveFormLabel = ttk.Label(self.genSettingsFrame, bootstyle=INFO, text='Waveform type')
        self.ampLabel = ttk.Label(self.genSettingsFrame, bootstyle=INFO, text='Amplitude')
        self.freqLabel = ttk.Label(self.genSettingsFrame, bootstyle=INFO, text='Frequency')

        #acqSettings frame
        self.acqSettingsFrame = ttk.Labelframe(self.settingsFrame, bootstyle=INFO, text='Acquisitor')
        self.decCB = ttk.Combobox(self.acqSettingsFrame, bootstyle=INFO, state=READONLY)
        self.samplesEntry = ttk.Entry(self.acqSettingsFrame, bootstyle=INFO, validatecommand=(self.valInt, '%P'), validate="key")

        self.decLabel = ttk.Label(self.acqSettingsFrame, bootstyle=INFO, text='Decimation')
        self.samplesLabel = ttk.Label(self.acqSettingsFrame, bootstyle=INFO, text='Number of samples to collect')

        #buttons frame
        self.buttonsFrame = ttk.Frame(self.root)
        self.runBtn = ttk.Button(self.buttonsFrame, text='RUN', bootstyle=(INFO,OUTLINE), command=self.run)
        self.exitBtn = ttk.Button(self.buttonsFrame, text='EXIT', bootstyle=(DANGER,OUTLINE), command=self.stopGUI)

        #setting combobox values
        self.waveFormCB['values'] = F_GUI_WF_COMBOBOX_VALUES
        self.waveFormCB.set(F_GUI_WF_COMBOBOX_VALUES[0])
        self.waveFormCB.bind('<<ComboboxSelected>>', self.waveFormComboboxCallback)

        self.decCB['values'] = F_GUI_DEC_COMBOBOX_VALUES
        self.decCB.set(F_GUI_DEC_COMBOBOX_VALUES[0])
        self.decCB.bind('<<ComboboxSelected>>', self.decComboboxCallback)

        #setting other values
        self.ampEntry.insert(0, str(F_GEN_DEFAULT_AMPLITUDE))
        self.freqEntry.insert(0, str(F_GEN_DEFAULT_FREQ))
        self.samplesEntry.insert(0, str(F_GEN_DEFAULT_SAMPLES))

    def startGUI(self):
        #settings frame placement
        self.settingsFrame.pack(side=LEFT, anchor=W, padx=30, pady=30)

        #gen settings
        self.genSettingsFrame.pack(anchor=W, padx=10, pady=10)
        self.waveFormCB.grid(row=0, column=1, padx=10, pady=10)
        self.ampEntry.grid(row=1, column=1, padx=10, pady=10)
        self.freqEntry.grid(row=2, column=1, padx=10, pady=10)

        self.waveFormLabel.grid(row=0, column=0, padx=10, pady=10)
        self.ampLabel.grid(row=1, column=0, padx=10, pady=10)
        self.freqLabel.grid(row=2, column=0, padx=10, pady=10)

        #acq settings
        self.acqSettingsFrame.pack(anchor=W, padx=10, pady=10)
        self.decCB.grid(row=0, column=1, padx=10, pady=10)
        self.samplesEntry.grid(row=1, column=1, padx=10, pady=10)

        self.decLabel.grid(row=0, column=0, padx=10, pady=10)
        self.samplesLabel.grid(row=1, column=0, padx=10, pady=10)

        #Buttons frame placement
        self.buttonsFrame.pack(side=RIGHT, anchor=E, padx=30, pady=30)
        self.runBtn.grid(row=0, column=0, padx=10, pady=10)
        self.exitBtn.grid(row=1, column=0, padx=10, pady=10)

        self.root.mainloop()

    def stopGUI(self):
        #Close ProgramRunner and gui
        #subprocess.Popen([sys.executable, 'runVolGen.py'])
        sys.exit()

    def run(self):

        #TODO field validation
        tempWaveForm = self.waveForm
        tempAmp = self.ampEntry.get()
        tempFreq = self.freqEntry.get()

        tempDec = self.decimation
        tempSamples = self.samplesEntry.get()
        self.PR.fastFullRun(tempWaveForm, tempAmp, tempFreq, tempDec, tempSamples)

class startupGUI:
    def __init__(self):
        self.root = (ttk.Window(themename="superhero", size=S_GUI_DEFAULT_WINDOW_SIZE))

    def chooseFast(self):
        #subprocess.Popen([sys.executable, 'runFast.py'])
        sys.exit()
    
    def chooseSlow(self):
        #subprocess.Popen([sys.executable, 'runRealTime.py'])
        sys.exit()
    
    def exit(self):
        sys.exit()

    def initGUI(self):
        ###style configuration
        self.style = ttk.Style()
        self.style.configure('TButton', font=("Segoe UI", 20))
        self.style.configure('info.Outline.TButton', font=("Segoe UI", 12))

        #choice buttons
        self.buttonsFrame = ttk.Frame(self.root)
        self.fastBtn = ttk.Button(self.buttonsFrame, text = 'N Samples', bootstyle=(PRIMARY,OUTLINE), command=self.chooseFast)
        self.slowBtn = ttk.Button(self.buttonsFrame, text = 'Real Time', bootstyle=(PRIMARY,OUTLINE), command=self.chooseSlow)

        #close button
        self.closeFrame = ttk.Frame(self.root)
        self.exitBtn = ttk.Button(self.closeFrame, text='EXIT', bootstyle=(DANGER,OUTLINE), command=self.exit)

    def startGUI(self):
        self.buttonsFrame.pack(side=TOP, anchor=N, padx=30, pady=30)
        self.fastBtn.grid(row = 0, column = 0, padx=5)
        self.slowBtn.grid(row = 0, column = 1, padx=5)

        self.closeFrame.pack(side=BOTTOM, anchor=S, padx=30, pady=30)
        self.exitBtn.grid(row = 0, column = 0, padx = 5)

        self.root.mainloop()