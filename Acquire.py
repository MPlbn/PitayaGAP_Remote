import redpitaya_scpi as scpi
import time

from constants import *

#   class responsible for constant, real time data acquisition from RedPitaya.
#   uses SCPI commands
class Acquisitor:
    def __init__(self, uIP):
        self.RP_S = scpi.scpi(uIP)
        self.decimation = 1
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
        self.RP_S.tx_txt(f'ACQ:AVG ON')

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
        tStartTime = time.time()
        buffer_stringVoltage = self.RP_S.rx_txt() #this takes all the time in the world, but why? TODO
        tStopTime = time.time()
        buffer_stringVoltage = buffer_stringVoltage.strip('{}\n\r').replace("  ", "").split(',')
        retListVoltage = list(map(float, buffer_stringVoltage))

        #Acquire current values
        self.RP_S.tx_txt(f'ACQ:SOUR{ACQ_CURRENT_CHANNEL}:DATA:LATest:N? {uSampleSize}')
        buffer_stringCurrent = self.RP_S.rx_txt()
        buffer_stringCurrent = buffer_stringCurrent.strip('{}\n\r').replace("  ", "").split(',')
        retListCurrent = list(map(float, buffer_stringCurrent))

        #Return Voltage and Current in a list
        retList = [retListVoltage, retListCurrent]

        tElapsed = (tStopTime - tStartTime) * 1000
        print(f'Elapsed time: {tElapsed} ms')        
        
        return retList
    
    ## =========== TEST ============ ##
    def setTrig(self):
        self.RP_S.tx_txt('ACQ:TRig:CH2 NOW')

    def AcqRoutine(self):
        self.RP_S.tx_txt('ACQ:SOUR2:DATA:TRig? 0,POST_TRIG')
        retVal = self.RP_S.rx_txt()
        return retVal
    def AcqRoutineFull(self): 
        self.RP_S.tx_txt('ACQ:SOUR2:DATA?')

        tStartTime = time.time()
        retVal = self.RP_S.rx_txt() #It's still 40ms -> bad not really able to do it faster
        tStopTime = time.time()

        tElapsed = (tStopTime - tStartTime) * 1000
        print(f'Elapsed time: {tElapsed} ms') 
        return retVal
    
    def processData(self, uBuffer):
        retList = []
        for element in uBuffer:
            element = element.strip("{}")
            retList.append(float(element))
        return retList
    
    def processDataFull(self, uBuffer):
        uBuffer = uBuffer.strip('{}\n\r').replace("  ", "").split(',')
        uBuffer = list(map(float, uBuffer))
        return uBuffer
        #retVal = sum(uBuffer) / len(uBuffer)
        #return [retVal]