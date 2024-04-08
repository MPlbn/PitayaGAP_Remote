from appJar import gui
import mock

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
    GENERATOR.setGenerating(True)
    GENERATOR.generate(appGui)  # Start generating values with the GUI instance

def stopGeneratingPress(button):
    GENERATOR.setGenerating(False)


#globals
GENERATOR: mock.MockGenerator = mock.MockGenerator()

#settings
appGui: gui = gui("TEST", "1000x1000")

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

appGui.addSplitMeter("generateMeter", 4, 2)
appGui.setMeterFill("generateMeter", ["green", "blue"])
appGui.addLabel("generatedValue", "", 4, 1)

appGui.bindKey("<Escape>", appGui.stop) #close gui
appGui.bindKey("<Return>", press) #dodaje do startu

appGui.go()