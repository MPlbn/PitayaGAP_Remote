import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys


import mock


#functions for buttons
def quit():
    sys.exit()

def validateFloat(uEntryValue) -> bool:
    if(uEntryValue == ''):
        return True
    
    if(uEntryValue == '-'):
        return True
    try:
        float(uEntryValue)
        return True
    except ValueError:
        return False   
    
def validatePositiveFloat(uEntryValue) -> bool:
    if(uEntryValue == ''):
        return True
    if(uEntryValue == '-' or uEntryValue[0] == '-'):
        return False
    try:
        float(uEntryValue)
        return True
    except ValueError:
        return False

def validateInt(uEntryValue) -> bool:
    if(uEntryValue == ""):
        return True
    try:
        int(uEntryValue)
        return True
    except ValueError:
        return False


def setRangesPress():
    
    tempHRange: float = float(hRangeEntry.get()) if hRangeEntry.get() != "" else 1.0
    tempLRange: float = float(lRangeEntry.get()) if lRangeEntry.get() != "" else -1.0
    tempStep: float = float(stepEntry.get()) if stepEntry.get() != "" else 0.1
    tempTime: int = int(intervalEntry.get()) if intervalEntry.get() != "" else 50

    tempMessage: str = ""


    if(tempHRange < tempLRange):
        temp = tempLRange
        tempHRange = tempLRange
        tempLRange = temp
        hRangeEntry.delete(0, ttk.END)
        lRangeEntry.delete(0, ttk.END)
        hRangeEntry.insert(0, f'{tempHRange}')
        lRangeEntry.insert(0, f'{tempLRange}')

    if(tempHRange > 5.0):
        tempHRange = 5.0
        hRangeEntry.delete(0, ttk.END)
        hRangeEntry.insert(0, '5.0')
        tempMessage += "Error: Range cannot be higher than 5.0\n"

    if(tempHRange < -5.0):
        tempHRange = -5.0
        hRangeEntry.delete(0, ttk.END)
        hRangeEntry.insert(0, '-5.0')
        tempMessage += "Error: Range cannot be lower than -5.0\n"

    if(tempLRange > 5.0):
        tempLRange = 5.0
        lRangeEntry.delete(0, ttk.END)
        lRangeEntry.insert(0, '5.0')
        tempMessage += "Error: Range cannot be higher than 5.0\n"

    if(tempLRange < -5.0):
        tempLRange = -5.0
        lRangeEntry.delete(0, ttk.END)
        lRangeEntry.insert(0, '-5.0')
        tempMessage += "Error: Range cannot be lower than -5.0\n"    

    if(tempHRange == tempLRange):
        tempHRange = 1.0
        tempLRange = -1.0
        hRangeEntry.delete(0, ttk.END)
        lRangeEntry.delete(0, ttk.END)
        hRangeEntry.insert(0, '1.0')
        lRangeEntry.insert(0, '-1.0')
        tempMessage += "Error: Ranges cannot have the same value - resetting to default range values\n"

    if(tempStep > 1):
        tempStep = 1
        stepEntry.delete(0, ttk.END)
        stepEntry.insert(0, '1.0')
        tempMessage += "Error: Step value cannot be higher than 1.0\n"

    if(tempStep <= 0):
        tempStep = 0.1
        stepEntry.delete(0, ttk.END)
        stepEntry.insert(0, '0.1')
        tempMessage += "Error: Step value cannot be 0 or lower\n"
    
    if(tempTime > 5000):
        tempTime = 5000
        intervalEntry.delete(0, ttk.END)
        intervalEntry.insert(0, '5000')
        tempMessage += "Error: Interval cannot be higher than 5000ms\n"

    if(tempTime < 5):
        tempTime = 5
        intervalEntry.delete(0, ttk.END)
        intervalEntry.insert(0, '5')
        tempMessage += "Error: Interval cannot be lower than 5ms\n"

    
    errorLabel.configure(text = tempMessage)
    GENERATOR.setRanges(tempHRange, tempLRange)
    GENERATOR.setStep(tempStep)
    GENERATOR.setInterval(tempTime)

def startGeneratingPress():
    PLOTTER.start()
    GENERATOR.setGenerating(True)

def stopGeneratingPress():
    PLOTTER.stop()
    GENERATOR.setGenerating(False)

def pauseGeneratingPress():
    GENERATOR.setGenerating(False)


#creating base
root = ttk.Window(themename="superhero", size=(1000, 1000))

#registering validation
valInt = root.register(validateInt)
valFloat = root.register(validateFloat)
valPosFloat = root.register(validatePositiveFloat)

style = ttk.Style()
style.configure('TButton', font=("Segoe UI", 20))
style.configure('info.Outline.TButton', font=("Segoe UI", 12))

#creating widgets
settingsAndButtonsFrame = ttk.Frame(root, style='TFrame')


settingsFrame = ttk.Labelframe(settingsAndButtonsFrame, bootstyle=INFO, text='settings')
hRangeLabel = ttk.Label(settingsFrame, bootstyle=INFO , text='High Range')
lRangeLabel = ttk.Label(settingsFrame, bootstyle=INFO, text='Low Range')
stepLabel = ttk.Label(settingsFrame, bootstyle=INFO, text='Step value')
intervalLabel = ttk.Label(settingsFrame, bootstyle=INFO, text='Speed value')
hRangeEntry = ttk.Entry(settingsFrame, bootstyle=INFO, validatecommand=(valFloat, '%P'), validate="key")
lRangeEntry = ttk.Entry(settingsFrame, bootstyle=INFO, validatecommand=(valFloat, '%P'), validate="key")
stepEntry = ttk.Entry(settingsFrame, bootstyle=INFO, validatecommand=(valPosFloat, '%P'), validate="key")
intervalEntry = ttk.Entry(settingsFrame, bootstyle=INFO, validatecommand=(valInt, '%P'), validate="key")
setBtn = ttk.Button(settingsFrame, text='Set', bootstyle=(INFO,OUTLINE), command=setRangesPress)

hRangeEntry.insert(0, '1.0')
lRangeEntry.insert(0, '-1.0')
stepEntry.insert(0, '0.1')
intervalEntry.insert(0, '50')

errorFrame = ttk.Frame(settingsAndButtonsFrame, width=450)
errorLabel = ttk.Label(errorFrame, text="", bootstyle=(DANGER), width=450, font=("Segoe UI", 8))

buttonsFrame = ttk.Frame(settingsAndButtonsFrame)
startBtn = ttk.Button(buttonsFrame, text='Start', bootstyle=(SUCCESS,OUTLINE), command=startGeneratingPress)
stopBtn = ttk.Button(buttonsFrame, text='Stop', bootstyle=(DANGER,OUTLINE), command=stopGeneratingPress)
lockBtn = ttk.Button(buttonsFrame, text='Lock', bootstyle=(PRIMARY,OUTLINE), command=pauseGeneratingPress)

progressFrame = ttk.Frame(root)
progressBar = ttk.Progressbar(progressFrame, length=300, bootstyle=(PRIMARY))
progressLabel = ttk.Label(progressFrame, bootstyle=PRIMARY, text='0.00', font=("Segoe UI", 20, "bold"))
progressInfoLabel = ttk.Label(progressFrame, bootstyle=INFO, text='Current generated value', font=("Segoe UI", 15, "bold"))

plotFrame = ttk.Frame(root)

def updateGeneration():
    GENERATOR.generate()

    progressLabel.configure(text=str(round(GENERATOR.currentValue, GENERATOR.calculateRoundingNumber())))
    progressBar.configure(value=GENERATOR.convertToPercent())

    PLOTTER.processData(GENERATOR.getGeneratedValue())
    PLOTTER.updatePlot()
    PLOTTER.canvas.draw()
    root.after(GENERATOR.getInterval(), updateGeneration)

#mocked classes
GENERATOR = mock.MockGenerator()
PLOTTER = mock.mockPlotter(plotFrame)

#placing widgets
settingsAndButtonsFrame.pack(padx=20, pady=20)

#settingsFrame.pack(ipadx=20, ipady=20, anchor=NW, side=LEFT)
settingsFrame.grid(row=0, column=0, columnspan=2, rowspan=5, ipadx=20, ipady=20)
hRangeLabel.grid(row=0, column=0, padx=5)
lRangeLabel.grid(row=1, column=0, padx=5)
stepLabel.grid(row=2, column=0, padx=5)
intervalLabel.grid(row=3, column=0, padx=5)
hRangeEntry.grid(row=0, column=1, pady=5)
lRangeEntry.grid(row=1, column=1, pady=5)
stepEntry.grid(row=2, column=1, pady=5)
intervalEntry.grid(row=3, column=1, pady=5)
setBtn.grid(row=4,column=1, pady=10)

#errorFrame.pack(pady=(50, 20), side=TOP, anchor=N)
errorFrame.grid(row=0, column=3, rowspan=5, columnspan=1, padx=40, sticky=NSEW, pady=20)
errorLabel.grid(row=0,column=0)
errorFrame.grid_propagate(False)

#buttonsFrame.pack(padx=(500, 0), pady=(50, 20), anchor=NE, side=RIGHT)
buttonsFrame.grid(row=0, column=4, rowspan=3)
lockBtn.grid(row=0, column=0, pady=5)
stopBtn.grid(row=1,column=0, pady=5)
startBtn.grid(row=2,column=0, pady=5)


progressFrame.pack(padx=20,pady=20)
progressInfoLabel.pack(padx=20)
progressLabel.pack(padx=20, pady=10)
progressBar.pack(padx=20)

plotFrame.pack(padx=20, pady=10, fill=BOTH)

#run gui
updateGeneration()
root.mainloop()