import numpy as np
from datetime import datetime
import csv
from scipy.io import wavfile
import struct
from abc import ABC, abstractmethod
from constants import *
import os

class FileManager(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generatePath():
        pass

    @abstractmethod
    def saveToFile():
        pass

class CSVFileManager(FileManager):
    def __init__(self):
        self.pathPrefix: str = "DATA"
        self.pathPostfix: str = ".csv"
        self.currentPath: str = ""
    ### managing CSV data files
    #   saving
    def generatePath(self, uAdditionalNamePart):
        path = datetime.today().strftime('%Y%m%d%H%M%S')
        return str(uAdditionalNamePart + self.pathPrefix + path + self.pathPostfix)

    def createFile(self, uAdditionalNamePart=""):
        self.currentPath = self.generatePath(uAdditionalNamePart)
        with open(self.currentPath, 'w', newline='') as emptyCSV:
            pass
    
    def saveToFile(self, uVData, uIData = [], uIsMock = False):
        if(uIsMock):
            with open(self.currentPath, 'a', newline='') as csvFile:
                writer = csv.writer(csvFile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONNUMERIC)
                for i in range(0, len(uVData)):
                    writer.writerow([uVData[i], uVData[i]])
        else:
            with open(self.currentPath, 'a', newline='') as csvFile:
                writer = csv.writer(csvFile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONNUMERIC)
                for i in range(0, len(uVData)):
                    writer.writerow([uIData[i], uVData[i]])


class WAVFileManager(FileManager):
    def __init__(self):
        self.pathPrefix: str = "arb_custom_"
        self.pathPostfix: str = ".wav"
        self.currentPath: str = ""
    
    def generatePath(self, uWaveform):
        return str(self.pathPrefix + str(uWaveform) + self.pathPostfix)

    def getCurrentPath(self):
        return self.currentPath

    def saveToFile(self, uWaveform, uWFValues, uSampleRate):
        self.currentPath = self.generatePath(uWaveform)
        wavfile.write(self.currentPath, uSampleRate, uWFValues)

    def openFile(self, uPath):
        samplingRate, data = wavfile.read(uPath)
        return data

    def deleteFile(self, uPath):
        if(os.path.exists(uPath)):
            os.remove(uPath)
        else:
            print(f'The file: {uPath} does not exist.')
