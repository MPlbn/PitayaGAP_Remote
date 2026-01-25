import numpy as np
    
# file save mock
#   TODO change the GUI from "LOAD" to "SAVE" accordingly, also make room for periodic saves?
from datetime import datetime
import csv

class FileManager:
    def __init__(self):
        self.pathPrefix: str = "DATA"
        self.pathPostfix: str = ".csv"
    ### managing CSV data files
    #   saving
    def generatePath(self):
        path = datetime.today().strftime('%Y%m%d%H%M%S')
        return str(self.pathPrefix + path + self.pathPostfix)

    def saveToFile(self, uGenData, uAcqData):
        with open(self.generatePath(), 'w', newline='') as csvFile:
            writer = csv.writer(csvFile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow(uGenData)
            writer.writerow(uAcqData)
### IS THE LOADING EVEN NEEDED? WHAT FOR? SKIP FOR NOW
    #   loading
    # def load(self, uPath):
    #     with open(uPath, 'r', newline='') as csvFile:
    #         reader = csv.reader(csvFile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_NONNUMERIC)
    #         tempGenData = next(reader)
    #         tempAcqData = next(reader)
    #         return tempGenData, tempAcqData