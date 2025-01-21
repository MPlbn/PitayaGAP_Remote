import redpitaya_scpi as scpi
import time


from constants import *
#Acquisition commands wrapper - WIP TODO
class Acquisitor:
    def __init__(self, uIP):
        self.RP_S = scpi.scpi(uIP)
        self.channelNumber = DEFAULT_CHANNEL
        self.decimation = 4

    def reset(self):
        self.RP_S.tx_txt('ACQ:RST')

    def setup(self):
        self.RP_S.tx_txt(f'ACQ:DEC {self.decimation}')

    def start(self):
        self.RP_S.tx_txt('ACQ:START')

    def stop(self):
        self.RP_S.tx_txt('ACQ:STOP')

    def run(self):
        self.RP_S.tx_txt('ACQ:TRig NOW')

        while True:
            self.RP_S.tx_txt('ACQ:TRig:FILL?')
            if(self.RP_S.rx_txt() == '1'):
                break

    #def getBuff(self) -> list:
        #return self.RP_S.acq_data(self.channelNumber, convert=True)[ACQ_BUFFER_SIZE-ACQ_SAMPLE_SIZE:ACQ_BUFFER_SIZE] #Tutaj jest głupio, musi zbierać mniej a nie zbierać całości i wycinać, tutaj duże spadki czasowe

    def getBuff(self) -> list:
        self.RP_S.tx_txt(f'ACQ:SOUR{self.channelNumber}:DATA:LATest:N? 10') #To juz dziala, max spadlo do 45ms co ruch
        buffer_string = self.RP_S.rx_txt()
        buffer_string = buffer_string.strip('{}\n\r').replace("  ", "").split(',')
        retList = list(map(float, buffer_string))
        return retList

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
