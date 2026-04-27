#ifndef GENERATE_H
#define GENERATE_H
#include <cmath>
#include <vector>

namespace GeneratorConstants{
    constexpr float DEFAULT_VOLTAGE = 0.0;
    constexpr auto DEFAULT_CHANNEL = 1;
    constexpr int DEFAULT_RP_FREQUENCY = 1000;
    constexpr float DEFAULT_HRANGE = 1.0;
    constexpr float DEFAULT_LRANGE = -1.0;
    constexpr float DEFAULT_STEP = 0.001;

    enum class GenType{
        NORMAL,
        STEPPING
    };

    enum class Direction{
        POSITIVE,
        NEGATIVE
    };

    enum class ManualStepType{
        UP,
        DOWN
    };

    enum class SteppingBounceType{
        NONE,
        LIMIT,
        BASE
    };

    constexpr GenType DEFAULT_MODE = GenType::NORMAL;
    constexpr Direction DEFAULT_DIRECTION = Direction::POSITIVE;
}

class Generator{
    private:
    float voltageValue = GeneratorConstants::DEFAULT_VOLTAGE;
    float resetVoltageValue = GeneratorConstants::DEFAULT_VOLTAGE;
    bool resetFlag = false;
    float highRange = GeneratorConstants::DEFAULT_HRANGE;
    float lowRange = GeneratorConstants::DEFAULT_LRANGE;
    float step = GeneratorConstants::DEFAULT_STEP;
    bool isPaused = false;
    GeneratorConstants::GenType genMode = GeneratorConstants::DEFAULT_MODE;
    int steppingIndex = 0;
    int steppingLevelStepValue = 1;
    float base = GeneratorConstants::DEFAULT_VOLTAGE;
    float limit = GeneratorConstants::DEFAULT_HRANGE;
    GeneratorConstants::Direction direction = GeneratorConstants::DEFAULT_DIRECTION;
    std::vector<float> steppingRanges;
        
    float generate();
    void setMode(GeneratorConstants::GenType uNewMode);
    void setRanges(float uHRange, float uLRange);
    void setLimit(float uLimit);
    void setStep(float uStep);
    void setBase(float uBase);
    void setResetVoltage(float uVoltage);
    void setVoltageValue(float uVoltage);
    void createSteps(int uNumOfSteps);
    void setDirection(GeneratorConstants::Direction uDirection);
    void incrementSteppingRange();
    GeneratorConstants::SteppingBounceType isOutOfBounds(float uValue, float uLimit, float uBase);

    public:
    Generator();
    void setup(GeneratorConstants::GenType uMode, float uStartingVoltage, float uHRange, float uLRange, float uStep, GeneratorConstants::Direction uDirection);
    void setup(GeneratorConstants::GenType uMode, float uBaseVoltage, float uLimit, float uStep, int uNumSteps);
    float workRoutine();
    void reset();
    void setPause(bool uPaused);
    void flip();
    void manualChangeVoltage(GeneratorConstants::ManualStepType uChangeType);
};
#endif