#from appJar import gui
import appJar
import mock
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    PLOTTER.processData(GENERATOR.currentValue)
    PLOTTER.updatePlot(ax, canvas)


#globals
GENERATOR: mock.MockGenerator = mock.MockGenerator()

PLOTTER: mock.mockPlotter = mock.mockPlotter()

#settings
appGui: appJar.gui = appJar.gui("TEST", "fullscreen")

appGui.addLabel("lRange", "Input lower range", 0, 0)
appGui.addNumericEntry("LowRange", 0, 1)

appGui.addLabel("hRange", "Input higher range", 0, 2)
appGui.addNumericEntry("HighRange", 0, 3)

appGui.addLabel("stepLabel", "Input step value", 0, 4)
appGui.addNumericEntry("step", 0, 5)

appGui.addLabel("timeInterval", "Set V/s", 0, 6)
appGui.addNumericEntry("interval", 0, 7)

appGui.addButton("Set Ranges", setRangesPress, 2, 1)
appGui.addButton("Start Generating", startGeneratingPress, 3, 1)
appGui.addButton("Stop Generating", stopGeneratingPress, 3, 2)
appGui.addButton("Lock", pauseGeneratingPress, 3, 3)

appGui.addSplitMeter("generateMeter", 4, 2)
appGui.setMeterFill("generateMeter", ["green", "blue"])
appGui.addLabel("generatedValue", "", 4, 1)

appGui.bindKey("<Escape>", appGui.stop) #close gui
appGui.bindKey("<Return>", press) #dodaje do startu

fig, ax = plt.subplots()
canvas = FigureCanvasTkAgg(fig, appGui.topLevel)
canvas.get_tk_widget().pack(side = "top", fill = "both", expand=True)

appGui.registerEvent(updateGeneration)
appGui.setPollTime(GENERATOR.generatingInterval)

appGui.go()