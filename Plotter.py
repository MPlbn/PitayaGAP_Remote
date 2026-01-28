import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation as FAnim
from abc import ABC, abstractmethod

from constants import *

#   BASE CLASS 
class Plotter(ABC):
    def __init__(self):
        self.data = np.array([])
        self.isRunning: bool = False
        self.fig, self.ax = plt.subplots()

    def setFrame(self, uFrame):
        self.frame = uFrame

    def initVisuals(self):
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.line, = self.ax.plot([], [], lw=2)

    def start(self):
        self.isRunning = True

    def stop(self):
        self.isRunning = False

    def updatePlot(self):
        if(self.isRunning):
            x = np.linspace(0, PLOT_MAX_DATA_SIZE - 1, len(self.data))
            self.line.set_data(x, self.data)
            self.ax.relim()
            self.ax.autoscale_view()

    def animate(self):
        animation = FAnim(self.fig, self.updatePlot, frames=100, blit=True)
        plt.show()

    def loadData(self, uData):
        self.data = uData

    def getData(self):
        return self.data
    
    def clear(self):
        self.data = np.array([])
    
    @abstractmethod
    def processData(self, uNewData):
        pass

#   PLOTTER FOR ACQUIRED DATA
class AcqPlotter(Plotter):
    def __init__(self):
        self.data = np.array([])
        self.isRunning: bool = False
        self.fig, self.ax = plt.subplots()
        self.ratio = PLOT_DEFAULT_RATIO

    def setRatio(self, uRatio: float):
        self.ratio = uRatio

    def processData(self, uNewData):
        if(self.isRunning):
            if(len(self.data) >= PLOT_MAX_DATA_SIZE):
                self.data = self.data[ACQ_SAMPLE_SIZE:]
            self.data = np.append(self.data, uNewData*self.ratio)

#   PLOTTER FOR GENERATOR DATA
class GenPlotter(Plotter):
    def processData(self, uNewData):
        if(self.isRunning):
            if(len(self.data) >= PLOT_GEN_MAX_DATA_SIZE):
                self.data = self.data[1:]
            self.data = np.append(self.data, uNewData)