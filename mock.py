import time
from appJar import gui
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class MockGenerator:
    def __init__(self):
        self.hRange: float = 1.0
        self.lRange: float = -1.0
        self.currentValue: float = 0.0
        self.step: float = 0.01
        self.isGenerating: bool = False
        self.generatingInterval: int = 50
    
    def setRanges(self, uHRange, uLRange):
        self.hRange = uHRange
        self.lRange = uLRange

    def setStep(self, uStep):
        self.step = uStep

    def setGenerating(self, uIsGenerating):
        self.isGenerating = uIsGenerating

    def setInterval(self, uInterval):
        self.generatingInterval = int(uInterval)

    def calculateRoundingNumber(self):
        decimalPart = str(self.step).split('.')[1]
        return len(decimalPart)

    def getGenerating(self):
        return self.isGenerating
    
    def getGeneratedValue(self):
        return self.currentValue
    
    def convertToPercent(self):
        fullRange: float = self.hRange - self.lRange
        currentPlace: float = self.currentValue - self.lRange
        return (currentPlace / fullRange) * 100

    def generate(self):
        if self.isGenerating:    
            if self.currentValue > self.hRange:
                if(self.step > 0):
                    self.step *= -1
            if self.currentValue < self.lRange:
                if(self.step < 0):
                    self.step *= -1

            self.currentValue += self.step
            

class mockPlotter:
    def __init__(self):
        self.data = [] #max size: 1000
        self.maxDataSize = 1000
        self.isRunning = False

    def processData(self, uNewData):
        if(self.isRunning):
            if(len(self.data) >= self.maxDataSize):
                self.data.pop()
            self.data.append(uNewData)
        
    def start(self):
        self.isRunning = True
    
    def stop(self):
        self.isRunning = False

    def updatePlot(self, ax, canvas):
        if(self.isRunning):
            x = np.linspace(0, 999, len(self.data))
            y = self.data
            ax.clear()
            ax.plot(x,y)
            canvas.draw()
    