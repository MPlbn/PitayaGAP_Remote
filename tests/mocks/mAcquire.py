
import time

import numpy as np

from mConstants import *
#Acquisition commands wrapper - WIP TODO
class Acquisitor:
    def __init__(self, uIP):
        #self.RP_S = scpi.scpi(uIP)
        self.channelNumber = 1
        self.decimation = 4
        self.Data = []

    def reset(self):
        #self.RP_S.tx_txt('ACQ:RST')
        time.sleep(0.1)

    def setup(self):
        #self.RP_S.tx_txt(f'ACQ:DEC {self.decimation}')
        time.sleep(0.1)

    def start(self):
        # self.RP_S.tx_txt('ACQ:START')
        time.sleep(0.1)

    def stop(self):
        # self.RP_S.tx_txt('ACQ:STOP')
        time.sleep(0.1)

    def run(self):
        # self.RP_S.tx_txt('ACQ:TRig NOW')

        # while True:
        #     self.RP_S.tx_txt('ACQ:TRig:FILL?')
        #     if(self.RP_S.rx_txt() == '1'):
        #         break
        time.sleep(0.3)

    def getBuff(self):
        #return self.RP_S.acq_data(self.channelNumber, convert=True)[ACQ_BUFFER_SIZE-ACQ_SAMPLE_SIZE:ACQ_BUFFER_SIZE]
        return np.full(50, self.Data)
    
    def mockedSetBuff(self, uData):
        self.Data = uData

    # def setup(self, uDecimation = 1, uTriggerLevel = 0, uTriggerDelay = 0):
    #     self.RP_S.acq_set(uDecimation, uTriggerLevel, uTriggerDelay)

    # def startAcquisition(self):
    #     self.RP_S.tx_txt('ACQ:START')

    # def runAcquisition(self):
    #     self.RP_S.tx_txt('ACQ:START')
    #     self.RP_S.tx_txt(f'ACQ:TRIG NOW')
    #     while True:
    #         self.RP_S.tx_txt('ACQ:TRIG:FILL?')
    #         if self.RP_S.rx_txt() == '1':
    #             break
    #     x = self.RP_S.acq_data(self.channelNumber, convert=True)
    #     return x
    
    # def triggerContAcquisition(self):
    #     self.RP_S.tx_txt('ACQ:TRIG NOW')

    # def runContAcquisition(self):
    #     while True:
    #         self.RP_S.tx_txt('ACQ:TRIG:FILL?')
    #         if self.RP_S.rx_txt() == '1':
    #             break
    #     return self.RP_S.acq_data(self.channelNumber, convert=True, lat=True, num_samples=1)
    
    # def getContVoltage(self):
    #     #here something else
    #     print("Tutaj?")
    #     return

    # def stopAcquisition(self):
    #     self.RP_S.tx_txt('ACQ:STOP')
