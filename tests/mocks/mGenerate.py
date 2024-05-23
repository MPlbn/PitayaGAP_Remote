from mConstants import *
import time

#Generating commands wrapper - obsolete
# class Generator:
#     def __init__(self, uIP):
#         self.RP_S = scpi.scpi(uIP)
        
#     def reset(self):
#         self.RP_S.tx_txt('GEN:RST')

#     def setup(self, uChannelNumber, uWaveform, uFrequency, uAmplitude):
#         self.channelNumber = uChannelNumber
#         self.frequency = uFrequency
#         self.amplitude = uAmplitude
#         self.RP_S.sour_set(uChannelNumber, uWaveform, uAmplitude, uFrequency)

#     def startGenerating(self):
#         self.RP_S.tx_txt(f'OUTPUT{self.channelNumber}:STATE ON')
#         self.RP_S.tx_txt(f'SOUR{self.channelNumber}:TRIG:INT')

#     def stopGenerating(self):
#         self.RP_S.tx_txt(f'OUTPUT{self.channelNumber}:STATE OFF')

#   WIP TODO

class ContGenerator:
    def __init__(self, uIP):
        #self.RP_S = scpi.scpi(uIP)
        self.output: int = DEFAULT_CHANNEL
        self.frequency: int = 1000 #prob not needed
        self.voltageValue: float = GEN_DEFAULT_VOLTAGE
        self.highRange: float = GEN_DEFAULT_HRANGE
        self.lowRange: float = GEN_DEFAULT_LRANGE
        self.step: float = GEN_DEFAULT_STEP
        self.roundingNumber = 1
        self.isPaused: bool = False
        self.GEN_MODE = GeneratorMode.CONT
        self.steppingIndex: int = 0
        self.steppingLevelsIncrement: int = 1

        #for test
        self.steppingRanges = GEN_DEFAULT_STEPPING_RANGES

    def changeMode(self, uNewMode: GeneratorMode):
        self.GEN_MODE = uNewMode
    
    def getNextSteppingLevel(self) -> float:
        if(self.steppingIndex + self.steppingLevelsIncrement > len(self.steppingRanges) - 1 or self.steppingIndex + self.steppingLevelsIncrement < 0):
            self.steppingLevelsIncrement *= -1
        self.steppingIndex += self.steppingLevelsIncrement
        print(self.steppingRanges[self.steppingIndex])
        return self.steppingRanges[self.steppingIndex]

    def setup(self, uChannelNumber = DEFAULT_CHANNEL, uFrequency = 1000, uAmplitude = 0.0):
        self.output = uChannelNumber
        self.frequency = uFrequency
        self.voltageValue = uAmplitude

        #self.RP_S.sour_set(self.output, "dc", self.voltageValue, self.frequency)

    def setRanges(self, uHRange = None, uLRange = None):
        if(uHRange != None):
            self.highRange = uHRange
        if(uLRange != None):    
            self.lowRange = uLRange

    def setBase(self, uBase):
        self.setRanges(uLRange=uBase)

    def setStep(self, uStep):
        self.step = uStep
        self.calculateRoundingNumber()

    def setOutput(self, uOutput):
        self.output = uOutput

    def changeVolt(self, uNewVoltage):
        #self.RP_S.tx_txt(f'SOUR{self.output}:VOLT {abs(uNewVoltage)}')
        time.sleep(MOCK_TIME_SLOW)
        

    def pause(self):
        self.isPaused = True

    def unpause(self):
        self.isPaused = False

    def reset(self):
        #self.RP_S.tx_txt('GEN:RST')
        time.sleep(MOCK_TIME_SLOW)

    def startGen(self):
        # self.RP_S.tx_txt(f'OUTPUT{self.output}:STATE ON')
        # self.RP_S.tx_txt(f'SOUR{self.output}:TRig:INT')
        time.sleep(MOCK_TIME_SLOW)

    def workRoutine(self):
        if(not self.isPaused):
            self.generate()
            self.changeVolt(self.voltageValue)
            

    def generate(self):
        match self.GEN_MODE:
            case GeneratorMode.CONT:
                if(self.voltageValue + self.step > self.highRange):
                    if(self.step > 0):
                        self.step *= -1.0
                if(self.voltageValue + self.step < self.lowRange):
                    if(self.step < 0):
                        self.step *= -1.0
                #temp = self.voltageValue
                self.voltageValue += self.step

                # if(temp*self.voltageValue < 0):
                #     if(self.voltageValue < 0):
                #         self.RP_S.tx_txt(f'SOUR{self.output}:FUNC DC_NEG')
                #     else:
                #         self.RP_S.tx_txt(f'SOUR{self.output}:FUNC DC')

            case GeneratorMode.STEPPING:
                if(self.voltageValue + self.step > self.highRange):
                    if(self.step > 0):
                        self.step *= -1.0
                        self.setRanges(uHRange=self.getNextSteppingLevel())
                if(self.voltageValue + self.step < self.lowRange):
                    if(self.step < 0):
                        self.step *= -1.0
                
                self.voltageValue += self.step

    # for test
    def steppingGenerate(self):
        pass

    def voltageToPercent(self) -> int:
        fullRange: float = self.highRange - self.lowRange
        currentPlace: float = self.voltageValue - self.lowRange
        return (currentPlace / fullRange) * 100
    
    def calculateRoundingNumber(self) -> int:
        try:
            decimalPart = str(self.step).split('.')[1]
        except:
            decimalPart = ""
        self.roundingNumber = len(decimalPart)
    
    def getRoundingNumber(self) -> int:
        return self.roundingNumber

    def stopGen(self):
        # if(self.voltageValue > 0):
        #     if(self.step > 0):
        #         self.step *= -1.0
        # if(self.voltageValue < 0):
        #     if(self.step < 0):
        #         self.step *= -1.0
        

        # while(self.voltageValue > 0.1 or self.voltageValue < -0.1):
        #     self.voltageValue += self.step
        
        #self.RP_S.tx_txt(f"OUTPUT{self.output}:STATE OFF")
        self.voltageValue = 0.0

    def mockedGetGeneratedValue(self) -> float:
        return self.voltageValue
    