#from appJar import gui
import appJar
import mock
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ttkthemes


def press(button):
    print(appGui.getEntry("Amplituda"))

def setRangesPress(button):
    tempHighRange: float = appGui.getEntry("HighRange")
    tempLowRange: float = appGui.getEntry("LowRange")
    tempStep: float = appGui.getEntry("step")
    tempTime: int = appGui.getEntry("interval")
    
    GENERATOR.setRanges(tempHighRange, tempLowRange)
    GENERATOR.setStep(tempStep)
    GENERATOR.setInterval(tempTime)


def startGeneratingPress(button):
    PLOTTER.start()
    GENERATOR.setGenerating(True)


def stopGeneratingPress(button):
    PLOTTER.stop()
    GENERATOR.setGenerating(False)
    
def pauseGeneratingPress(button):
    GENERATOR.setGenerating(False)

def updateGeneration():
    GENERATOR.generate()
    appGui.setLabel("generatedValue", str(round(GENERATOR.currentValue, GENERATOR.calculateRoundingNumber())))
    appGui.setMeter("generateMeter", GENERATOR.convertToPercent(), str(round(GENERATOR.currentValue, GENERATOR.calculateRoundingNumber())))
    PLOTTER.processData(GENERATOR.getGeneratedValue())
    PLOTTER.updatePlot()
    PLOTTER.canvas.draw()


#globals
appGui: appJar.gui = appJar.gui("TEST", useTtk=True)
appGui.setResizable(False)
appGui.setTtkTheme("breeze")

GENERATOR: mock.MockGenerator = mock.MockGenerator()

PLOTTER: mock.mockPlotter = mock.mockPlotter(appGui)

#settings
with appGui.labelFrame("settings", 0, 0, rowspan=5, colspan=2, sticky=""):

    appGui.label("lRange", "Input lower range", row=0, column=0)
    appGui.entry("LowRange", row=0, column=1, kind='numeric')

    appGui.label("hRange", "Input higher range", row=1, column=0)
    appGui.entry("HighRange", row=1, column=1, kind='numeric')

    appGui.label("stepLabel", "Input step value", row=2, column=0)
    appGui.entry("step", row=2, column=1, kind='numeric')

    appGui.label("timeInterval", "Set V/s", row=3, column=0)
    appGui.entry("interval", row=3, column=1, kind='numeric')

    appGui.button("Set Ranges", value=setRangesPress, row=4, column=1)

appGui.label("mt1", "", row=0, column=3)
appGui.label("mt2", "", row=0, column=4)
appGui.label("mt3", "", row=0, column=5)
appGui.label("mt4", "", row=0, column=6)
appGui.label("mt5", "", row=0, column=7)
appGui.label("mt6", "", row=0, column=8)
appGui.label("mt7", "", row=0, column=9)

with appGui.frame("buttons", 0, 10, rowspan=3, colspan=1, sticky='news'):

    appGui.button("Start Generating", value=startGeneratingPress, row=0, column=0)
    appGui.button("Stop Generating", value=stopGeneratingPress, row=1, column=0)
    appGui.button("Lock", value=pauseGeneratingPress, row=2, column=0)



appGui.addSplitMeter("generateMeter", 5, 0)
appGui.setMeterFill("generateMeter", ["green", "blue"])
appGui.addLabel("generatedValue", "", 5, 1)

appGui.bindKey("<Escape>", appGui.stop) #close gui
appGui.bindKey("<Return>", press) #dodaje do startu

# fig, ax = plt.subplots() #TODO get from plotter
# canvas = FigureCanvasTkAgg(fig, appGui.topLevel)
# canvas.get_tk_widget().pack(side = "top", fill = "both", expand=True)

appGui.registerEvent(updateGeneration)
appGui.setPollTime(GENERATOR.generatingInterval)

appGui.go()