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

    def start(self):
        self.isRunning = True

    def stop(self):
        self.isRunning = False


    def animate(self):
        animation = FAnim(self.fig, self.updatePlot, frames=100, blit=True)
        plt.show()

    def loadData(self, uData):
        self.data = uData

    def getData(self):
        return self.data
    
    def clear(self):
        self.data = np.array([])
        if(not self.isRunning):
            self.isRunning = True
            self.updatePlot()
            self.isRunning = False

    @abstractmethod
    def updatePlot(self):
        pass
    
    @abstractmethod
    def initVisuals(self):
        pass

    @abstractmethod
    def processData(self, uNewData):
        pass

#   PLOTTER FOR ACQUIRED DATA
class AcqPlotter(Plotter):
    def __init__(self):
        self.dataI = np.array([])
        self.dataV = np.array([])
        self.isRunning: bool = False
        self.fig, self.ax = plt.subplots()
        self.ratio = PLOT_DEFAULT_RATIO


    def initVisuals(self):
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.set_xlabel("U (voltage)")
        self.ax.set_ylabel("I (current)")

    def setRatio(self, uRatio: float):
        self.ratio = uRatio

    def processData(self, uNewDataI, uNewDataV):
        print(uNewDataI[0]*PLOT_DEFAULT_RATIO)
        if(self.isRunning):
            if(len(self.dataI) >= PLOT_MAX_DATA_SIZE):
                self.dataI = self.dataI[ACQ_SAMPLE_SIZE:]
            self.dataI = np.append(self.dataI, uNewDataI*MV_TO_V_VALUE)
            if(len(self.dataV) >= PLOT_MAX_DATA_SIZE):
                self.dataV = self.dataV[ACQ_SAMPLE_SIZE:]
            self.dataV = np.append(self.dataV, uNewDataV*self.ratio*MV_TO_V_VALUE)
    
    def updatePlot(self):
        if(self.isRunning):
            self.line.set_data(self.dataV, self.dataI)
            self.ax.relim()
            self.ax.autoscale_view()


#   PLOTTER FOR GENERATOR DATA
class GenPlotter(Plotter):

    def initVisuals(self):
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        self.line, = self.ax.plot([], [], lw=2)
        self.ax.set_xlabel("No. of Samples")
        self.ax.set_ylabel("U (Voltage)")

    def processData(self, uNewData):
        if(self.isRunning):
            if(len(self.data) >= PLOT_GEN_MAX_DATA_SIZE):
                self.data = self.data[1:]
            self.data = np.append(self.data, uNewData*MV_TO_V_VALUE)

    def updatePlot(self):
        if(self.isRunning):
            x = np.linspace(0, PLOT_MAX_DATA_SIZE - 1, len(self.data))
            self.line.set_data(x, self.data)
            self.ax.relim()
            self.ax.autoscale_view()