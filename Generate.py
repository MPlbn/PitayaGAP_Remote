import redpitaya_scpi as scpi
from constants import *

#Fast samples generator
class Generator:
    def __init__(self, uIP):
        self.RP_S = scpi.scpi(uIP)
        self.channelNumber = GEN_DEFAULT_CHANNEL
        self.frequency = F_GEN_DEFAULT_DACRATE
        self.amplitude = 1
        self.waveform = F_GEN_DEFAULT_WAVEFORM
        
    def reset(self):
        self.RP_S.tx_txt('GEN:RST')

    def setup(self, uChannelNumber, uWaveform, uFrequency, uAmplitude):
        self.channelNumber = uChannelNumber
        self.frequency = uFrequency
        self.amplitude = uAmplitude
        self.waveform = uWaveform
        
    def setSCPIsettings(self):
        self.RP_S.sour_set(self.channelNumber, self.waveform, self.amplitude, self.frequency)

    def startGenerating(self):
        self.RP_S.tx_txt(f'OUTPUT{self.channelNumber}:STATE ON')
        self.RP_S.tx_txt(f'SOUR{self.channelNumber}:TRIG:INT')

    def stopGenerating(self):
        self.RP_S.tx_txt(f'OUTPUT{self.channelNumber}:STATE OFF')


class ContGenerator:
    def __init__(self, uIP):
        self.RP_S = scpi.scpi(uIP)
        self.output: int = GEN_DEFAULT_CHANNEL
        self.frequency: int = 1000 #prob not needed
        self.voltageValue: float = GEN_DEFAULT_VOLTAGE
        self.resetVoltageValue: float = GEN_DEFAULT_VOLTAGE
        self.resetFlag: bool = False
        self.highRange: float = GEN_DEFAULT_HRANGE
        self.lowRange: float = GEN_DEFAULT_LRANGE
        self.step: float = GEN_DEFAULT_STEP
        self.roundingNumber: int = 1
        self.isPaused: bool = False
        self.GEN_MODE = GeneratorMode.CONT
        self.steppingIndex: int = 0
        self.steppingLevelsIncrement: int = 1
        self.base: float = GEN_DEFAULT_VOLTAGE
        self.limit: float = GEN_DEFAULT_HRANGE
        self.direction = "anodic"

        #for test
        self.steppingRanges = []

    def loadValue(self, uValue):
        self.voltageValue = uValue

    def changeMode(self, uNewMode: GeneratorMode):
        self.GEN_MODE = uNewMode

    def manualChangeVoltage(self, uChangeType):
        tempValue = self.voltageValue + (uChangeType * abs(self.step))
        match self.GEN_MODE:
            case GeneratorMode.CONT:
                if(tempValue < self.lowRange or
                   tempValue > self.highRange):
                    pass
                else:
                    self.voltageValue = tempValue
            case GeneratorMode.STEPPING:
                if(tempValue > self.base or
                   tempValue < self.base or
                   tempValue > self.limit or
                   tempValue < self.limit):
                    pass
                else:
                    self.voltageValue = tempValue
        self.changeVolt(self.voltageValue)

    def getNextSteppingLevel(self) -> float:
        if(self.steppingIndex + self.steppingLevelsIncrement > len(self.steppingRanges) - 1 or self.steppingIndex + self.steppingLevelsIncrement < 0):
            self.steppingLevelsIncrement *= -1
        self.steppingIndex += self.steppingLevelsIncrement
        return self.steppingRanges[self.steppingIndex]

    def setup(self, uChannelNumber = GEN_DEFAULT_CHANNEL, uFrequency = 1000, uAmplitude = 0.0):
        self.output = uChannelNumber
        self.frequency = uFrequency
        self.voltageValue = uAmplitude

        self.RP_S.sour_set(self.output, "dc", self.voltageValue, self.frequency)

    def setRanges(self, uHRange = None, uLRange = None):
        if(uHRange != None):
            self.highRange = uHRange
        if(uLRange != None):
            self.lowRange = uLRange

    def setStartingValue(self, uStartingValue):
        self.resetVoltageValue = uStartingValue
        self.voltageValue = uStartingValue

    def setSteppingRanges(self, uLimit, uBase = None):
        if(uBase != None):
            if(uBase > uLimit):
                self.direction = "kathodic"
            else:
                self.direction = "anodic"
            self.applyDirection()
            self.base = uBase
            self.voltageValue = uBase
        self.limit = uLimit

    def createSteps(self, uNumOfSteps):    
        fullSize = self.limit - self.base
        stepSize = fullSize / uNumOfSteps
        self.steppingRanges = []
        stepValue = self.base
        for _ in range(0, uNumOfSteps):
            stepValue += stepSize
            self.steppingRanges.append(stepValue)
        self.limit = self.steppingRanges[0]

    def setStep(self, uStep):
        if(self.step < 0):
            self.step = -uStep
        else:
            self.step = uStep
        self.calculateRoundingNumber()

    def setDirection(self, uDirection):
        self.direction = uDirection

    def applyDirection(self):
        match self.direction:
            case "anodic":
                pass
            case "kathodic":
                self.step *= -1.0

    def setOutput(self, uOutput):
        self.output = uOutput

    def changeVolt(self, uNewVoltage):
        self.RP_S.tx_txt(f'SOUR{self.output}:VOLT {abs(uNewVoltage)}')
        
    def pause(self):
        self.isPaused = True

    def unpause(self):
        self.isPaused = False

    def getPause(self) -> bool:
        return self.isPaused

    def reset(self):
        self.RP_S.tx_txt('GEN:RST')

    def startGen(self):
        self.RP_S.tx_txt(f'OUTPUT{self.output}:STATE ON')
        self.RP_S.tx_txt(f'SOUR{self.output}:TRig:INT')

    def flipDirection(self):
        self.step *= -1.0

    def workRoutine(self):
        if(self.resetFlag):
            self.voltageValue = self.resetVoltageValue
            self.changeVolt(self.resetVoltageValue)
            match self.direction:
                case "anodic":
                    if(self.step < 0):
                        self.flipDirection()
                    else:
                        pass
                case "kathodic":
                    if(self.step > 0):
                        self.flipDirection()
                    else:
                        pass
            self.resetFlag = False
            if(self.GEN_MODE == GeneratorMode.STEPPING):
                self.steppingIndex = 0
                self.setSteppingRanges(uLimit=self.steppingRanges[self.steppingIndex])
        else:
            if(not self.isPaused):
                self.generate()
                self.changeVolt(self.voltageValue)
            
    def resetGenValue(self):
        self.resetFlag = True

    def generate(self):
        match self.GEN_MODE:
            case GeneratorMode.CONT:
                if(self.voltageValue + self.step > self.highRange):
                    if(self.step > 0):
                        self.step *= -1.0
                if(self.voltageValue + self.step < self.lowRange):
                    if(self.step < 0):
                        self.step *= -1.0  

            case GeneratorMode.STEPPING:
                tempValue = self.voltageValue + self.step
                match self.direction:
                    case "anodic":
                        if(tempValue > self.limit):
                            if(self.step > 0):
                                self.step *= -1.0
                                self.setSteppingRanges(uLimit=self.getNextSteppingLevel())
                        if(tempValue < self.base):
                            if(self.step < 0):
                                self.step *= -1.0
                    case "kathodic":
                        if(tempValue < self.limit):
                            if(self.step < 0):
                                self.step *= -1.0
                                self.setSteppingRanges(uLimit=self.getNextSteppingLevel())
                        if(tempValue > self.base):
                            if(self.step > 0):
                                self.step *= -1.0
        temp = self.voltageValue
        self.voltageValue += self.step
        if(temp*self.voltageValue <= 0):
            if(self.voltageValue < 0):
                self.RP_S.tx_txt(f'SOUR{self.output}:FUNC DC_NEG')
            else:
                self.RP_S.tx_txt(f'SOUR{self.output}:FUNC DC')
                    
                
   
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

    #Smooth change if needed
    def stopGen(self, uStopType: StopType):
        # if(self.voltageValue > 0):
        #     if(self.step > 0):
        #         self.step *= -1.0
        # if(self.voltageValue < 0):
        #     if(self.step < 0):
        #         self.step *= -1.0
        

        # while(self.voltageValue > 0.1 or self.voltageValue < -0.1):
        #     self.voltageValue += self.step
        match uStopType:
            case StopType.STOP_RESET:
                self.RP_S.tx_txt(f"OUTPUT{self.output}:STATE OFF")
                self.voltageValue = 0.0
                self.resetFlag = True
            case StopType.STOP_KEEP:
                self.RP_S.tx_txt(f'OUTPUT{self.output}:STATE OFF')