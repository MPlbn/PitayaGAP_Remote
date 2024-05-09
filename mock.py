import time
from appJar import gui
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation as FAnim
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
        return np.full(50, self.currentValue)
    
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
    def __init__(self, app):
        self.data = np.array([]) #max size: 1000
        self.maxDataSize = 10000
        self.isRunning = False
        self.fig, self.ax = pyplot.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=app.getFrame())
        self.canvas.get_tk_widget().pack(side = "top", fill = "both", expand = True)
        self.line, = self.ax.plot([], [], lw=2)


    def processData(self, uNewData):
        if(self.isRunning):
            if(len(self.data) >= self.maxDataSize):
                self.data = self.data[50:]
            self.data = np.append(self.data, uNewData)
            
        
    def start(self):
        self.isRunning = True
    
    def stop(self):
        self.isRunning = False

    def updatePlot(self):
        if(self.isRunning):
            x = np.linspace(0, self.maxDataSize - 1, len(self.data))
            self.line.set_data(x, self.data)
            self.ax.relim()
            self.ax.autoscale_view()

    
    def getAX(self):
        return self.ax
    
    def animate(self):
        animation = FAnim(self.fig, self.updatePlot, frames=100, blit=True)
        pyplot.show()