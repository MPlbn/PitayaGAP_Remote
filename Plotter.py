from PySide6.QtCore import Qt
import pyqtgraph as PGraph
import numpy as np

class Plotter(PGraph.PlotWidget):
    def __init__(self, parent=None, background='default', plotItem=None, **kargs):
        super().__init__(parent, background, plotItem, **kargs)
        self.isRunning = False
        self.ratio = 1.0
        self.setYRange(-1,1)

    def stop(self):
        self.isRunning = False

    def start(self):
        self.isRunning = True
    
    def getIsRunning(self):
        return self.isRunning
    
    def setRatio(self, uRatio):
        self.ratio = uRatio

    def getRatio(self):
        return self.ratio

class AcqPlotter(Plotter):
    def __init__(self):
        super().__init__()
        self.setTitle("I/V")
        self.dataI = [0]
        self.dataV = [0]
        self.curve = self.plot(self.dataV, self.dataI, pen="y")

    def updatePlot(self, uDataV, uDataI):
        if(self.isRunning):
            self.dataI = uDataI
            self.dataV = uDataV
            self.curve.setData(self.dataV, self.DataI)

class GenPlotter(Plotter):
    def __init__(self):
        super().__init__()
        self.setTitle("Generated values")
        self.dataV = [0]
        self.curve = self.plot(self.dataV, pen="y")

    def updatePlot(self, uDataV):
        if(self.isRunning):
            self.dataV = uDataV
            self.curve.setData(self.dataV)