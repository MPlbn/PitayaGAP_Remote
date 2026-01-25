import rp
import numpy as np
from pitConstants import *

class PitAcquisitor:
    def __init__(self, uDec):
        self.decimation = self.getDecimation(int(uDec))
        self.N = BUFF_SIZE

    def getDecimation(uDec):
        return getattr(rp, f'RP_DEC_{uDec}')

    def reset(self):
        rp.rp_AcqReset()

    def setup(self):
        rp.rp_AcqSetDecimation(self.decimation)

    def runAcquisition(self):
        rp.rp_AcqSetTriggerSrc(rp.RP_TRIG_SRC_NOW)

        while 1:
            trig_state = rp.rp_AcqGetTriggerState()[1]
            if trig_state == rp.RP_TRIG_STATE_TRIGGERED:
                break

        while 1:
            if rp.rp_AcqGetBufferFillState()[1]:
                break

        fBuffer = rp.fBuffer(self.N)
        res = rp.rp_AcqGetDataV(DEFAULT_CHANNEL, 0, self.N, fBuffer)

        data_V = np.zeros(self.N, dtype = float)

        #TODO get the data then save it to csv

        #this seems pointless
        for i in range (0, self.N, 1):
            data_V[i] = fBuffer[i]
