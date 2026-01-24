import numpy as np
from datetime import datetime
import csv

class FileManager:
    def __init__(self):
        self.pathPrefix: str = "DATA"
        self.pathPostfix: str = ".csv"
    ### managing CSV data files
    #   saving
    def generatePath(self, uAdditionalNamePart):
        path = datetime.today().strftime('%Y%m%d%H%M%S')
        return str(uAdditionalNamePart + self.pathPrefix + path + self.pathPostfix)

    #   TODO different way to save as a columns, not as a rows

    def saveToFile(self, uGenData, uAcqData, uAdditionalNamePart=""):
        with open(self.generatePath(uAdditionalNamePart), 'w', newline='') as csvFile:
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