import WaveCreator
import FileManager
import matplotlib.pyplot as plt
from constants import *


WCreator = WaveCreator.WaveCreator()
FManager = FileManager.WAVFileManager() 
amplitude = 1
frequency = 1000
waveform = WF_SINE

y_Values = WCreator.create(waveform)
FManager.saveToFile(waveform, y_Values, WCreator.getSampleRate())
data = FManager.openFile(FManager.getCurrentPath())

plt.plot(data)
plt.show()
print("delete")
FManager.deleteFile(FManager.getCurrentPath())

