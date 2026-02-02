import redpitaya_scpi as scpi
import time

from constants import *

#   class responsible for constant, real time data acquisition from RedPitaya.
#   uses SCPI commands
class Acquisitor:
    def __init__(self, uIP):
        self.RP_S = scpi.scpi(uIP)
        self.decimation = 4
        self.gain = ACQ_DEFAULT_GAIN

    #   resets acquisition
    def reset(self):
        self.RP_S.tx_txt('ACQ:RST')

    #   acquisition settings
    def setup(self, uDecimation, uGain):
        self.decimation = uDecimation
        self.gain = uGain

    #   sends the settings to SCPI
    def setSCPIsettings(self):
        self.RP_S.tx_txt(f'ACQ:DEC {self.decimation}')
        self.RP_S.tx_txt(f'ACQ:DATA:Units {ACQ_UNITS}')
        self.RP_S.tx_txt(f'ACQ:DATA:FORMAT {ACQ_DATA_FORMAT}')
        self.RP_S.tx_txt(f'ACQ:SOUR{ACQ_VOLTAGE_CHANNEL}:GAIN {self.gain}')
        self.RP_S.tx_txt(f'ACQ:SOUR{ACQ_CURRENT_CHANNEL}:GAIN {self.gain}')

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
        #Acquire Voltage values
        self.RP_S.tx_txt(f'ACQ:SOUR{ACQ_VOLTAGE_CHANNEL}:DATA:LATest:N? {uSampleSize}')
        buffer_stringVoltage = self.RP_S.rx_txt()
        buffer_stringVoltage = buffer_stringVoltage.strip('{}\n\r').replace("  ", "").split(',')
        retListVoltage = list(map(float, buffer_stringVoltage))

        #Acquire current values
        self.RP_S.tx_txt(f'ACQ:SOUR{ACQ_CURRENT_CHANNEL}:DATA:LATest:N? {uSampleSize}')
        buffer_stringCurrent = self.RP_S.rx_txt()
        buffer_stringCurrent = buffer_stringCurrent.strip('{}\n\r').replace("  ", "").split(',')
        retListCurrent = list(map(float, buffer_stringCurrent))

        #Return Voltage and Current in a list
        retList = [retListVoltage, retListCurrent]
        return retList