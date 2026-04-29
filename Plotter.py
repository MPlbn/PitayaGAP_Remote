from PySide6.QtCore import Qt
import pyqtgraph as PGraph
import numpy as np

class Plotter(PGraph.PlotWidget):
    def __init__(self, parent=None, background='default', plotItem=None, **kargs):
        super().__init__(parent, background, plotItem, **kargs)
        self.isRunning = False
        self.ratio = 1.0
        #self.setYRange(-2,2)

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
        self.dataI = []
        self.dataV = []
        self.curve = self.plot(self.dataV, self.dataI, pen="y")

    def updatePlot(self, uDataV, uDataI):
        if(self.isRunning):
            self.dataI = uDataI
            self.dataV = uDataV
            self.curve.setData(self.dataV, self.dataI)

    def clear(self):
        self.dataI = []
        self.dataV = []
        self.curve.setData(self.dataV, self.dataI)

class GenPlotter(Plotter):
    def __init__(self):
        super().__init__()
        self.setTitle("Generated values")
        self.dataV = []
        self.curve = self.plot(self.dataV, pen="y")

    def updatePlot(self, uDataV):
        if(self.isRunning):
            self.dataV = uDataV
            self.curve.setData(self.dataV)

    def clear(self):
        self.dataV = []
        self.curve.setData(self.dataV)

class FAcqPlotter(Plotter):
    def __init__(self):
        super().__init__()
        self.setTitle("I/V")
        self.dataI = []
        self.dataV = []
        self.curveList = []
        self.colorIndex = 0

    def updatePlot(self, uDataV, uDataI):
        self.dataI = uDataI
        self.dataV = uDataV
        hue = (self.colorIndex * 37) % 360
        color = PGraph.intColor(hue)
        pen = PGraph.mkPen(color)

        self.curveList.append(self.plot(self.dataV, pen=pen))
        self.colorIndex += 1

    def clearData(self):
        for curve in self.curveList:
            self.removeItem(curve)

        self.curveList = []
        self.dataI = []
        self.dataV = []
