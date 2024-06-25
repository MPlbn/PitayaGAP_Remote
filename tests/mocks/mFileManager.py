import numpy as np

class FileManager:
    def __init_(self, fp = "/data"):
        self.filepath: str = fp + "/last_state.npz" 
        self.genData = np.array([])
        self.acqData = np.array([])
        self.currentVoltage: float = None

    def save(self):
        np.savez(self.filepath, gen_data=self.genData, acq_data=self.acqData, cVoltage=self.currentVoltage)
        print(f'data saved to {self.filepath}')

    def load(self):
        data = np.load(self.filepath)
        self.genData = data['gen_data']
        self.acqData = data['acq_data']
        self.currentVoltage = data['cVoltage']

    def setData(self, uGenData, uAcqData, uCurrentVoltage):
        self.genData = uGenData
        self.acqData = uAcqData
        self.currentVoltage = uCurrentVoltage

    def getData(self):
        dataDict = {
            'genData' : self.genData,
            'acqData' : self.acqData,
            'currentVoltage' : self.currentVoltage
        }

        return dataDict