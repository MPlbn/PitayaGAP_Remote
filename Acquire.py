import redpitaya_scpi as scpi
import time

from constants import *

#   class responsible for constant, real time data acquisition from RedPitaya.
#   uses SCPI commands
class Acquisitor:
    def __init__(self, uIP):
        self.RP_S = scpi.scpi(uIP)
        self.channelNumber = DEFAULT_CHANNEL
        self.decimation = 4

    #   resets acquisition
    def reset(self):
        self.RP_S.tx_txt('ACQ:RST')

    #   sets up additional parameters (currently only decimation, no problem adding other parameters if needed)
    def setup(self):
        self.RP_S.tx_txt(f'ACQ:DEC {self.decimation}')

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
    def getBuff(self) -> list:
        self.RP_S.tx_txt(f'ACQ:SOUR{self.channelNumber}:DATA:LATest:N? {ACQ_SAMPLE_SIZE}') #To juz dziala, max spadlo do 42ms co ruch
        buffer_string = self.RP_S.rx_txt()
        buffer_string = buffer_string.strip('{}\n\r').replace("  ", "").split(',')
        retList = list(map(float, buffer_string))
        return retList