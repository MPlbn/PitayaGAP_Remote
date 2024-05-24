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
import ProgramRunner
from constants import *

class GUI:
    def __init__(self):
        self.PR = ProgramRunner.ProgramRunner()
        self.root = ttk.Window(themename="superhero", size=GUI_DEFAULT_WINDOW_SIZE)
        self.interval: int = GUI_DEFAULT_INTERVAL
        self.thread = thread.Thread(target=self.threadTask)
        self.thread.daemon = True
        self.running: bool = False


    def startGeneratingPress(self):
        self.PR.changeMode(ProgramMode.CONT_START)

    def startGeneratingSteppingPress(self):
        self.PR.changeMode(ProgramMode.STEPPING_START)

    def stopGeneratingPress(self):
        #stopping continous generation in Program Runner work routine
        self.PR.changeMode(ProgramMode.GEN_STOP)

    def lockGeneratingPress(self):
        #locking current voltage value on Continous Generator and pausing autogeneration
        self.PR.pauseContGenerator()
    
    def unlockGeneratingPress(self):
        #unlocking current voltage value on Continous Generator and resuming autogeneration
        self.PR.unpauseContGenerator()

    def stepUpKey(self):
        #Increment step manually
        pass

    def stepDownKey(self):
        #Decrement step manually
        pass

    def setRangesPress(self):

        #collecting data from entries
        tempHRange: float = float(self.hRangeEntry.get()) if self.hRangeEntry.get() != "" else GEN_DEFAULT_HRANGE
        tempLRange: float = float(self.lRangeEntry.get()) if self.lRangeEntry.get() != "" else GEN_DEFAULT_LRANGE
        tempStep: float = float(self.stepEntry.get()) if self.stepEntry.get() != "" else GEN_DEFAULT_STEP
        tempTime: int = int(self.intervalEntry.get()) if self.intervalEntry.get() != "" else GUI_DEFAULT_INTERVAL

        tempMessage: str = ""

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

        #showing error message
        self.errorLabel.configure(text = tempMessage)

        #setting values
        self.PR.setContGeneratorParameters(tempHRange, tempLRange, tempStep)
        self.interval = tempTime

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
        self.settingsAndButtonsFrame = ttk.Frame(self.root)

        #settings
        self.settingsFrame = ttk.Labelframe(self.settingsAndButtonsFrame, bootstyle=INFO, text='settings')
        self.hRangeLabel = ttk.Label(self.settingsFrame, bootstyle=INFO , text='High Range')
        self.lRangeLabel = ttk.Label(self.settingsFrame, bootstyle=INFO, text='Low Range')
        self.stepLabel = ttk.Label(self.settingsFrame, bootstyle=INFO, text='Step value')
        self.intervalLabel = ttk.Label(self.settingsFrame, bootstyle=INFO, text='Speed value')
        self.hRangeEntry = ttk.Entry(self.settingsFrame, bootstyle=INFO, validatecommand=(self.valFloat, '%P'), validate="key")
        self.lRangeEntry = ttk.Entry(self.settingsFrame, bootstyle=INFO, validatecommand=(self.valFloat, '%P'), validate="key")
        self.stepEntry = ttk.Entry(self.settingsFrame, bootstyle=INFO, validatecommand=(self.valPosFloat, '%P'), validate="key")
        self.intervalEntry = ttk.Entry(self.settingsFrame, bootstyle=INFO, validatecommand=(self.valInt, '%P'), validate="key")
        self.setBtn = ttk.Button(self.settingsFrame, text='Set', bootstyle=(INFO,OUTLINE), command=self.setRangesPress)
    
        #Setting default values to entries
        self.hRangeEntry.insert(0, str(GEN_DEFAULT_HRANGE))
        self.lRangeEntry.insert(0, str(GEN_DEFAULT_LRANGE))
        self.stepEntry.insert(0, str(GEN_DEFAULT_STEP))
        self.intervalEntry.insert(0, str(GUI_DEFAULT_INTERVAL))

        #errors
        self.errorFrame = ttk.Frame(self.settingsAndButtonsFrame, width=450)
        self.errorLabel = ttk.Label(self.errorFrame, text="", bootstyle=(DANGER), width=450, font=("Segoe UI", 8))

        #buttons
        self.buttonsFrame = ttk.Frame(self.settingsAndButtonsFrame)
        self.startBtn = ttk.Button(self.buttonsFrame, text='Start', bootstyle=(SUCCESS,OUTLINE), command=self.startGeneratingPress)
        self.stopBtn = ttk.Button(self.buttonsFrame, text='Stop', bootstyle=(DANGER,OUTLINE), command=self.stopGeneratingPress)
        self.lockBtn = ttk.Button(self.buttonsFrame, text='Lock', bootstyle=(PRIMARY,OUTLINE), command=self.lockGeneratingPress)
        self.unlockBtn = ttk.Button(self.buttonsFrame, text='Unlock', bootstyle=(PRIMARY,OUTLINE), command=self.unlockGeneratingPress)
        self.startStepBtn = ttk.Button(self.buttonsFrame, text='Start Step', bootstyle=(SUCCESS,OUTLINE), command=self.startGeneratingSteppingPress)

        #progress
        self.progressFrame = ttk.Frame(self.root)
        self.progressBar = ttk.Progressbar(self.progressFrame, length=300, bootstyle=(PRIMARY))
        self.progressInfoLabel = ttk.Label(self.progressFrame, bootstyle=INFO, text='Current generated value', font=("Segoe UI", 15, "bold"))
        self.progressLabel = ttk.Label(self.progressFrame, bootstyle=PRIMARY, text='0.00', font=("Segoe UI", 20, "bold"))

        #plot
        self.plotFrame = ttk.Frame(self.root)
        self.PR.setPlotterFrame(self.plotFrame)


    def startGUI(self):
        #placing widgets
        self.settingsAndButtonsFrame.pack(padx=20, pady=20)

        self.settingsFrame.grid(row=0, column=0, columnspan=2, rowspan=5, ipadx=20, ipady=20)
        self.hRangeLabel.grid(row=0, column=0, padx=5)
        self.lRangeLabel.grid(row=1, column=0, padx=5)
        self.stepLabel.grid(row=2, column=0, padx=5)
        self.intervalLabel.grid(row=3, column=0, padx=5)
        self.hRangeEntry.grid(row=0, column=1, pady=5)
        self.lRangeEntry.grid(row=1, column=1, pady=5)
        self.stepEntry.grid(row=2, column=1, pady=5)
        self.intervalEntry.grid(row=3, column=1, pady=5)
        self.setBtn.grid(row=4,column=1, pady=10)

        self.errorFrame.grid(row=0, column=3, rowspan=5, columnspan=1, padx=40, sticky=NSEW, pady=20)
        self.errorLabel.grid(row=0,column=0)
        self.errorFrame.grid_propagate(False)

        self.buttonsFrame.grid(row=0, column=4, rowspan=3)
        self.lockBtn.grid(row=0, column=0, pady=5)
        self.unlockBtn.grid(row=1,column=0, pady=5)
        self.stopBtn.grid(row=2,column=0, pady=5)
        self.startBtn.grid(row=3,column=0, pady=5)
        self.startStepBtn.grid(row=4,column=0, pady=5)


        self.progressFrame.pack(padx=20,pady=20)
        self.progressInfoLabel.pack(padx=20)
        self.progressLabel.pack(padx=20, pady=10)
        self.progressBar.pack(padx=20)

        self.plotFrame.pack(padx=20, pady=10, fill=BOTH)

        #plotting done in Plotter class     

        self.thread.start()
        #run gui
        self.root.mainloop()