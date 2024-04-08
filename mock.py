import time
from appJar import gui

class MockGenerator:
    def __init__(self):
        self.hRange: float = 1.0
        self.lRange: float = -1.0
        self.currentValue: float = 0.0
        self.step: float = 0.01
        self.isGenerating: bool = False
        self.generatingInterval: int = 50
    
    def setRanges(self, uHRange, uLRange):
        self.hRange = uHRange
        self.lRange = uLRange

    def setStep(self, uStep):
        self.step = uStep

    def setGenerating(self, uIsGenerating):
        self.isGenerating = uIsGenerating

    def setInterval(self, uInterval):
        self.generatingInterval = int(uInterval)

    def calculateRoundingNumber(self):
        decimalPart = str(self.step).split('.')[1]
        return len(decimalPart)

    def getGenerating(self):
        return self.isGenerating
    
    def getGeneratedValue(self):
        return self.currentValue
    
    def convertToPercent(self):
        fullRange: float = self.hRange - self.lRange
        currentPlace: float = self.currentValue - self.lRange
        return (currentPlace / fullRange) * 100

    def generate(self, appGui):
        if self.isGenerating:    
            if self.currentValue > self.hRange:
                if(self.step > 0):
                    self.step *= -1
            if self.currentValue < self.lRange:
                if(self.step < 0):
                    self.step *= -1

            self.currentValue += self.step
            appGui.setLabel("generatedValue", str(round(self.currentValue, self.calculateRoundingNumber())))
            appGui.setMeter("generateMeter", self.convertToPercent(), str(round(self.currentValue, self.calculateRoundingNumber())))
            appGui.after(self.generatingInterval, self.generate, appGui)