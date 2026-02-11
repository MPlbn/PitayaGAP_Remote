import WaveCreator
import FileManager
import matplotlib.pyplot as plt
from constants import *
import numpy as np
from scipy.io import wavfile


WCreator = WaveCreator.WaveCreator()
FManager = FileManager.WAVFileManager() 
hVal = 0.8
lVal = -0.5
startVal = 0.6
frequency = 1
waveform = WF_TRI
path = "./streaming_app/arb_custom_Triangle.wav"


y_Values = WCreator.create(waveform, hVal, lVal, startVal, frequency)
FManager.saveToFile(waveform, y_Values, WCreator.getSampleRate())
#data = FManager.openFile(path)
fs, data = wavfile.read(path)
print("Sample rate:", fs)
print("Number of samples:", len(data))
print("First 5 samples:", data[:5])
print("Last 5 samples:", data[-5:])

plt.plot(data)
plt.show()
#print(data[0], data[-1])
#print(np.iinfo(np.int16).max)