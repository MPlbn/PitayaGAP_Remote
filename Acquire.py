import redpitaya_scpi as scpi
import time

#Acquisition commands wrapper - WIP TODO
class Acquisitor:
    def __init__(self, uIP):
        self.RP_S = scpi.scpi(uIP)
        self.channelNumber = 1

    def reset(self):
        self.RP_S.tx_txt('ACQ:RST')
    
    def setup(self, uDecimation = 1, uTriggerLevel = 0, uTriggerDelay = 0):
        self.RP_S.acq_set(uDecimation, uTriggerLevel, uTriggerDelay)

    def startAcquisition(self):
        self.RP_S.tx_txt('ACQ:START')

    def runAcquisition(self):
        self.RP_S.tx_txt('ACQ:START')
        self.RP_S.tx_txt(f'ACQ:TRIG NOW')
        # while True:
        #     self.RP_S.tx_txt('ACQ:TRIG:FILL?')
        #     if self.RP_S.rx_txt() == '1':
        #         print("tutaj")
        #         break
        x = self.RP_S.acq_data(self.channelNumber, convert=True)
        print(len(x))
        return x
    
    def runContAcquisition(self):
        time.sleep(1)
        self.RP_S.tx_txt(f'ACQ:TRIG NOW')
        while True:
            self.RP_S.tx_txt('ACQ:TRIG:FILL?')
            if self.RP_S.rx_txt() == '1':
                break
        return self.RP_S.acq_data(self.channelNumber, convert=True, start = 0, old=True)
    
    # def getContVoltage(self):
    #     #here something else
    #     print("Tutaj?")
    #     return

    def stopAcquisition(self):
        self.RP_S.tx_txt('ACQ:STOP')
