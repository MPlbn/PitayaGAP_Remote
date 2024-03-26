import redpitaya_scpi as scpi

#Acquisition commands wrapper
class Acquisitor:
    def __init__(self, uIP):
        self.RP_S = scpi.scpi(uIP)
        self.channelNumber = 1

    def reset(self):
        self.RP_S.tx_txt('ACQ:RST')
    
    def setup(self, uDecimation = 32, uTriggerLevel = 0, uTriggerDelay = 0):
        self.RP_S.acq_set(uDecimation, uTriggerLevel, uTriggerDelay)

    def runAcquisition(self):
        self.RP_S.tx_txt('ACQ:START')
        self.RP_S.tx_txt(f'ACQ:TRIG CH{self.channelNumber}_PE')
        while True:
            self.RP_S.tx_txt('ACQ:TRIG:FILL?')
            if self.RP_S.rx_txt() == '1':
                break
        return self.RP_S.acq_data(self.channelNumber, convert=True)
    
    def stopAcquisition(self):
        self.RP_S.tx_txt('ACQ:STOP')
