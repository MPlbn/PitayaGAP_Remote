import redpitaya_scpi as scpi

#Generating commands wrapper 
class Generator:
    def __init__(self, uIP):
        self.RP_S = scpi.scpi(uIP)
        
    def reset(self):
        self.RP_S.tx_txt('GEN:RST')

    def setup(self, uChannelNumber, uWaveform, uFrequency, uAmplitude):
        self.channelNumber = uChannelNumber
        self.frequency = uFrequency
        self.amplitude = uAmplitude
        self.RP_S.sour_set(uChannelNumber, uWaveform, uFrequency, uAmplitude)

    def startGenerating(self):
        self.RP_S.tx_txt(f'OUTPUT{self.channelNumber}:STATE ON')
        self.RP_S.tx_txt(f'SOUR{self.channelNumber}:TRIG:INT')

    #TODO
    def lockOnCurrentVoltage(self):
        #TODO current value how to get it
        self.reset()
        currentAmplitude = self.amplitude #TODO How to set starting value
        self.setup(self.channelNumber, 'constant', self.frequency, currentAmplitude)
        self.startGenerating()
   
    #TODO
    def unlock(self):
        pass
