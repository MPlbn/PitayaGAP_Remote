#include "generate.h"
#include <cmath>
#include <vector>

Generator::Generator(){}
// ---------------- PRIVATE METHODS ------------------
float Generator::generate(){
    float tempValue = voltageValue + step;
    switch(genMode){
        case GeneratorConstants::GenType::NORMAL:{
            if(tempValue > highRange || tempValue < lowRange){
                step *= -1;
            }
            break;
        }
        case GeneratorConstants::GenType::STEPPING:{
            GeneratorConstants::SteppingBounceType bounceType = isOutOfBounds(tempValue, steppingRanges[steppingIndex], base);
            switch(bounceType){
                case GeneratorConstants::SteppingBounceType::NONE:{
                    break;
                }
                case GeneratorConstants::SteppingBounceType::BASE:{
                    step*= -1;
                    break;
                }
                case GeneratorConstants::SteppingBounceType::LIMIT:{
                    step *= -1;
                    incrementSteppingRange();
                    break;
                }
            }
        }
    }
    return voltageValue += step;
}

void Generator::setMode(GeneratorConstants::GenType uNewMode){
    genMode = uNewMode;
}

void Generator::setRanges(float uHRange, float uLRange){
    highRange = uHRange;
    lowRange = uLRange;
}

void Generator::setLimit(float uLimit){
    limit = uLimit;
}

void Generator::setStep(float uStep){
    step = uStep;
}

void Generator::setBase(float uBase){
    base = uBase;
}

void Generator::setResetVoltage(float uVoltage){
    resetVoltageValue = uVoltage;
}

void Generator::setVoltageValue(float uVoltage){
    voltageValue = uVoltage;
}

void Generator::createSteps(int uNumOfSteps){
    steppingRanges.clear();
    float fullSize = limit - base;
    float stepSize = fullSize / uNumOfSteps;
    float stepValue = base;
    for(int i = 0; i < uNumOfSteps - 1; i++){
        stepValue += stepSize;
        steppingRanges.push_back(stepValue);
    }
    steppingRanges.push_back(limit);
    steppingIndex = 0;
    steppingLevelStepValue = 1;
}

void Generator::setDirection(GeneratorConstants::Direction uDirection){
    direction = uDirection;
}

void Generator::incrementSteppingRange(){
    int nextPotentialIndex = steppingIndex + steppingLevelStepValue;
    if(nextPotentialIndex > (static_cast<int>(steppingRanges.size())-1) || nextPotentialIndex < 0){
        steppingLevelStepValue *= -1;
    }
    steppingIndex += steppingLevelStepValue;
}

GeneratorConstants::SteppingBounceType Generator::isOutOfBounds(float uValue, float uLimit, float uBase){
    if(uLimit > uBase){
        if(uValue > uLimit){
            return GeneratorConstants::SteppingBounceType::LIMIT;
        }
        else if(uValue < uBase){
            return GeneratorConstants::SteppingBounceType::BASE;
        }
    }
    else if(uBase > uLimit){
        if(uValue > uBase){
            return GeneratorConstants::SteppingBounceType::BASE;

        }
        else if(uValue < uLimit){
            return GeneratorConstants::SteppingBounceType::LIMIT;

        }
    }
    return GeneratorConstants::SteppingBounceType::NONE;
}


// ---------------- PUBLIC METHODS -------------------
void Generator::setup(GeneratorConstants::GenType uMode, float uStartingVoltage, float uHRange, float uLRange, float uStep, GeneratorConstants::Direction uDirection){
    setMode(uMode);
    setResetVoltage(uStartingVoltage);
    setVoltageValue(uStartingVoltage);
    setRanges(uHRange, uLRange);
    setStep(uStep);
    setDirection(uDirection);
}

void Generator::setup(GeneratorConstants::GenType uMode, float uBaseVoltage, float uLimit, float uStep, int uNumSteps){
    setMode(uMode);
    setBase(uBaseVoltage);
    setLimit(uLimit);
    setStep(uStep);
    if(uBaseVoltage > uLimit){
        setDirection(GeneratorConstants::Direction::NEGATIVE);
    }
    else{
        setDirection(GeneratorConstants::Direction::POSITIVE);
    }
    createSteps(uNumSteps);
}

float Generator::workRoutine(){
    if(resetFlag){
        voltageValue = resetVoltageValue;
        if(genMode == GeneratorConstants::GenType::STEPPING){
            steppingIndex = 0;
            steppingLevelStepValue = 1;
        }
        switch(direction){
            case GeneratorConstants::Direction::POSITIVE:{
                if(step < 0){
                    flip();
                }
                break;
            }
            case GeneratorConstants::Direction::NEGATIVE:{
                if(step > 0){
                    flip();
                }
                break;
            }
        }
        resetFlag = false;
    }
    else{
        if(!isPaused){
            setVoltageValue(generate());
        }
    }
    return voltageValue;
}

void Generator::reset(){
    resetFlag = true;
}

void Generator::setPause(bool uPaused){
    isPaused = uPaused;
}

void Generator::flip(){
    step *= -1;
}

void Generator::manualChangeVoltage(GeneratorConstants::ManualStepType uChangeType){
    float tempStep;
    switch(uChangeType){
        case GeneratorConstants::ManualStepType::UP:{
            tempStep = std::abs(step);
            break;    
        }
        case GeneratorConstants::ManualStepType::DOWN:{
            tempStep = -std::abs(step);
            break;
        }
    }
    setVoltageValue(voltageValue + tempStep);
}