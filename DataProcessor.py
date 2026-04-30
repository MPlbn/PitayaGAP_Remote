import numpy as np
from abc import ABC, abstractmethod

from constants import *

class DataProcessor(ABC):
    def __init__(self):
        self.dataLimit: int = None
        self.sampleSize: int = None
        
    def setDataLimit(self, uNewDataLimit: int):
        self.dataLimit = uNewDataLimit

    def getDataLimit(self) -> int:
        return self.dataLimit
    
    def setSampleSize(self, uNewSampleSize: int):
        self.sampleSize = uNewSampleSize

    def getSampleSize(self) -> int:
        return self.sampleSize
    
    @abstractmethod    
    def processData(self, uNewDataBuffer):
        pass

    @abstractmethod
    def clear(self):
        pass

class GeneratorDataProcessor(DataProcessor):
    def __init__(self):
        super().__init__()
        self.dataV = []
        self.setDataLimit(MAX_DATA_SIZE_GEN)
        self.setSampleSize(1)

    def processData(self, uNewData:float):
        if(len(self.dataV) >= self.dataLimit):
            self.dataV = self.dataV[self.sampleSize:]
        self.dataV = np.append(self.dataV, uNewData*MV_TO_V_VALUE)

    def getData(self):
        return self.dataV
    
    def clear(self):
        self.dataV = []
    
class AcquisitorDataProcessor(DataProcessor):
    def __init__(self):
        super().__init__()
        self.dataV = []
        self.dataI = []
        self.setDataLimit(MAX_DATA_SIZE)
        self.setSampleSize(ACQ_SAMPLE_SIZE)

    def processData(self, uNewDataBuffer):
        if(len(self.dataV) >= self.dataLimit):
            self.dataV = self.dataV[self.sampleSize:]
        self.dataV = np.append(self.dataV, uNewDataBuffer[0]*MV_TO_V_VALUE)
        if(len(self.dataI) >= self.dataLimit):
            self.dataI = self.dataI[self.sampleSize:]
        self.dataI = np.append(self.dataI, uNewDataBuffer[1]*MV_TO_V_VALUE)

    def getDataV(self):
        return self.dataV
    
    def getDataI(self):
        return self.dataI
    
    def clear(self):
        self.dataV = []
        self.dataI = []
    
def processRatio(uRatio: str) -> float:
    numerator, denominator = map(int, uRatio.split('/'))
    result: float = numerator/denominator 
    return result
    
    