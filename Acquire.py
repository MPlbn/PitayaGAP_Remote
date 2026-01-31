import redpitaya_scpi as scpi
import time

from constants import *

#   class responsible for constant, real time data acquisition from RedPitaya.
#   uses SCPI commands
class Acquisitor:
    def __init__(self, uIP):
        self.RP_S = scpi.scpi(uIP)
        self.channelNumber = ACQ_DEFAULT_CHANNEL
        self.decimation = 4

    #   resets acquisition
    def reset(self):
        self.RP_S.tx_txt('ACQ:RST')

    #   acquisition settings
    def setup(self, uDecimation):
        self.decimation = uDecimation

    #   sends the settings to SCPI
    def setSCPIsettings(self):
        self.RP_S.tx_txt(f'ACQ:DEC {self.decimation}')
        self.RP_S.tx_txt(f'ACQ:DATA:Units {ACQ_UNITS}')
        self.RP_S.tx_txt(f'ACQ:DATA:FORMAT {ACQ_DATA_FORMAT}')
        self.RP_S.tx_txt(f'ACQ:SOUR{self.channelNumber}:GAIN {ACQ_GAIN}')

    #   starts acquisition
    def start(self):
        self.RP_S.tx_txt('ACQ:START')

    #   stops acquisition
    def stop(self):
        self.RP_S.tx_txt('ACQ:STOP')

    #   runs acquisition by setting trigger to be instant and waiting for buffer to fill
    def run(self):
        self.RP_S.tx_txt('ACQ:TRig NOW')

        while True:
            self.RP_S.tx_txt('ACQ:TRig:FILL?')
            if(self.RP_S.rx_txt() == '1'):
                break
    
    #   transfers acquired data from redpitaya to the PC and returns the values as a list of floats
    def getBuff(self, uSampleSize) -> list:
        self.RP_S.tx_txt(f'ACQ:SOUR{self.channelNumber}:DATA:LATest:N? {uSampleSize}') #To juz dziala, max spadlo do 42ms co ruch
        buffer_string = self.RP_S.rx_txt()
        buffer_string = buffer_string.strip('{}\n\r').replace("  ", "").split(',')
        retList = list(map(float, buffer_string))
        return retList