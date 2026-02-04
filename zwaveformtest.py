import WaveCreator
import FileManager
import matplotlib.pyplot as plt
from constants import *
import numpy as np


WCreator = WaveCreator.WaveCreator()
FManager = FileManager.WAVFileManager() 
amplitude = 1
frequency = 1000
waveform = WF_SINE
path = "dataLogs/data_file_10.42.0.63_2026-02-04_13-19-25.wav"


#y_Values = WCreator.create(waveform)
#FManager.saveToFile(waveform, y_Values, WCreator.getSampleRate())
data = FManager.openFile(path)

plt.plot(data)
plt.show()
#print(np.iinfo(np.int16).max)