import redpitaya_scpi as scpi

#Generating commands wrapper - obsolete
class Generator:
    def __init__(self, uIP):
        self.RP_S = scpi.scpi(uIP)
        
    def reset(self):
        self.RP_S.tx_txt('GEN:RST')

    def setup(self, uChannelNumber, uWaveform, uFrequency, uAmplitude):
        self.channelNumber = uChannelNumber
        self.frequency = uFrequency
        self.amplitude = uAmplitude
        self.RP_S.sour_set(uChannelNumber, uWaveform, uAmplitude, uFrequency)

    def startGenerating(self):
        self.RP_S.tx_txt(f'OUTPUT{self.channelNumber}:STATE ON')
        self.RP_S.tx_txt(f'SOUR{self.channelNumber}:TRIG:INT')

    def stopGenerating(self):
        self.RP_S.tx_txt(f'OUTPUT{self.channelNumber}:STATE OFF')

#   WIP TODO

class ContGenerator:
    ## TODO Possibly doable with dc waveform and changing the amplitude without resetting generator
    def __init__(self, uIP):
        self.RP_S = scpi.scpi(uIP)
        self.output: int = 1
        self.voltageValue: float = 0.5
        self.step: float = 0.1
        self.interval: int = 50
        self.lowRange: float = -0.9
        self.highRange: float = 0.9
        self.isPaused: bool = False

    def setup(self, uChannelNumber = 1, uFrequency = 0, uAmplitude = 0.2):
        self.channelNumber = uChannelNumber
        self.frequency = uFrequency
        self.amplitude = uAmplitude
        self.RP_S.sour_set(uChannelNumber, "triangle", uAmplitude, uFrequency) #sth wrong here too, it doesn't do what i need it to, always outputs 0.73...

    def setRanges(self, uHRange, uLRange):
        self.lowRange = uLRange
        self.highRange = uHRange

    def setInteval(self, uInterval):
        #TODO Pewnie jakies zmiany
        self.interval = uInterval

    def setStep(self, uStep):
        self.step = uStep

    def setOutput(self, uOutput):
        self.output = uOutput

    def changeVolt(self, uNewVoltage):
        #This doesn't change anything
        # self.RP_S.tx_txt(f'OUTPUT{self.output}:STATE OFF')
        # self.reset()
        # self.setup(uAmplitude=uNewVoltage)
        # self.startGen()
        self.RP_S.tx_txt(f'SOUR{self.output}:VOLT {uNewVoltage}')
        # self.RP_S.tx_txt(f'OUTPUT{self.output}:STATE ON')
        

    def pause(self):
        self.isPaused = True

    def unpause(self):
        self.isPaused = False

    def reset(self):
        self.RP_S.tx_txt('GEN:RST')

    def startGen(self):
        self.RP_S.tx_txt(f'OUTPUT{self.output}:STATE ON')
        self.RP_S.tx_txt(f'SOUR{self.output}:TRIG:INT')

    def workRoutine(self):
        if(not self.isPaused):
            self.generate()
            self.changeVolt(self.voltageValue)
            

    def generate(self):
        if(self.voltageValue > self.highRange):
            if(self.step > 0):
                self.step *= -1.0
        if(self.voltageValue < self.lowRange):
            if(self.step < 0):
                self.step *= -1.0
        self.voltageValue += self.step
   
    def stopGen(self):
        # if(self.voltageValue > 0):
        #     if(self.step > 0):
        #         self.step *= -1.0
        # if(self.voltageValue < 0):
        #     if(self.step < 0):
        #         self.step *= -1.0
        

        # while(self.voltageValue > 0.1 or self.voltageValue < -0.1):
        #     self.voltageValue += self.step
        
        self.RP_S.tx_txt(f"OUTPUT{self.output}:STATE OFF")
        self.voltageValue = 0.0