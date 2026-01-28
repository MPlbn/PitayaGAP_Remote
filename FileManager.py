import numpy as np
from datetime import datetime
import csv
from constants import *

class FileManager:
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


### IS THE LOADING EVEN NEEDED? WHAT FOR? SKIP FOR NOW
    #   loading
    # def load(self, uPath):
    #     with open(uPath, 'r', newline='') as csvFile:
    #         reader = csv.reader(csvFile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONNUMERIC)
    #         tempGenData = next(reader)
    #         tempAcqData = next(reader)
    #         return tempGenData, tempAcqData