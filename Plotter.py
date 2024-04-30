import numpy as np

#TODO Change to animation cause it's super slow

class Plotter:
    def __init__(self):
        self.isInContMode = False

    def start(self):
        self.isInContMode = True

    def stop(self):
        self.isInContMode = False

    def plot(self, uData, ax, canvas):
        x = np.linspace(1, len(uData), len(uData))
        ax.clear()
        ax.plot(x, uData)
        canvas.draw()

    #TODO

    def testAnimPlot(self, uData, ax, canvas):
        pass
            
