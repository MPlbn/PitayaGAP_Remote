#!/usr/bin/env python3

from appJar import gui
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import ProgramRunner

#   Making it prettier and full functional TODO

class GUI:
    def __init__(self):
        self.PR: ProgramRunner.ProgramRunner = ProgramRunner.ProgramRunner()
        self.appGui: gui = gui("DO ZMIANY", "fullscreen")
        self.startGUI()
        self.interval = 50

    #buttons
    def startGeneratingPress(self, button):
        #starting continous generation in Program Runner work routine
        self.PR.changeMode(2)

    def stopGeneratingPress(self, button):
        #stopping continous generation in Program Runner work routine
        self.PR.changeMode(3)

    def lockGeneratingPress(self, button):
        #locking current voltage value on Continous Generator and pausing autogeneration
        self.PR.pauseContGenerator()
    
    def unlockGeneratingPress(self, button):
        #unlocking current voltage value on Continous Generator and resuming autogeneration
        self.PR.unpauseContGenerator()

    def stepUpKey(self):
        #Increment step manually
        pass

    def stepDownKey(self):
        #Decrement step manually
        pass

    def setRangesPress(self, button):
        #Set voltage ranges, step value and speed
        pass

    def setIntervalPress(self, button):
        #Change main loop interval
        pass

    def mainLoopEvent(self):
        #Running the program runner routine
        self.PR.run(self.ax, self.canvas)

    def stopGUI(self):
        #Close ProgramRunner and gui
        self.PR.exit()
        self.appGui.stop()

    def startGUI(self):
        #adding gui elements
        self.appGui.addLabel("lRange", "Input lower range", 0, 0)
        self.appGui.addNumericEntry("LowRange", 0, 1)

        self.appGui.addLabel("hRange", "Input higher range", 0, 2)
        self.appGui.addNumericEntry("HighRange", 0, 3)

        self.appGui.addLabel("stepLabel", "Input step value", 0, 4)
        self.appGui.addNumericEntry("step", 0, 5)

        self.appGui.addLabel("timeInterval", "Set V/s", 0, 6)
        self.appGui.addNumericEntry("interval", 0, 7)

        self.appGui.addButton("Set Ranges", self.setRangesPress, 2, 1)
        self.appGui.addButton("Set Interval", self.setIntervalPress, 2, 2) 
        self.appGui.addButton("Start Generating", self.startGeneratingPress, 3, 1)
        self.appGui.addButton("Stop Generating", self.stopGeneratingPress, 3, 2)
        self.appGui.addButton("Lock", self.lockGeneratingPress, 3, 3)
        self.appGui.addButton("Unlock", self.unlockGeneratingPress, 3, 4)

        self.appGui.addSplitMeter("generateMeter", 4, 2)
        self.appGui.setMeterFill("generateMeter", ["green", "blue"])
        self.appGui.addLabel("generatedValue", "", 4, 1)

        #preparing keyboard binds
        self.appGui.bindKey("<Escape>", self.stopGUI) #close gui
        self.appGui.bindKey("<+>", self.stepUpKey)
        self.appGui.bindKey("<->", self.stepDownKey)

        #preparing the plotting inside gui
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, self.appGui.topLevel)
        self.canvas.get_tk_widget().pack(side = "top", fill = "both", expand=True)

        #main loop event register
        self.appGui.registerEvent(self.mainLoopEvent)
        self.appGui.setPollTime(self.interval)

        #run gui
        self.appGui.go()