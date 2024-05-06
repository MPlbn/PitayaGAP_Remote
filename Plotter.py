import numpy as np
import matplotlib.animation as anim
import matplotlib.pyplot as plt

class Plotter:
    def __init__(self, uData):
        self.isInContMode = False
        self.INDEX = 0

    def start(self):
        self.isInContMode = True

    def stop(self):
        self.isInContMode = False

    def plot(self, uData, ax, canvas):
        x = np.linspace(1, len(uData), len(uData))
        ax.clear()
        ax.plot(x, uData)
        canvas.draw()
