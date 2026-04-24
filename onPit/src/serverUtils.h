#ifndef SERVERUTILS_H
#define SERVERUTILS_H

#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/tcp.h>
#include <cstring>
#include <iostream>
#include <cstdint>
#include <cmath>
#include <chrono>
#include "rp.h"

namespace PitayaServerUtils{
    constexpr int PORT = 5000;
    constexpr char SETUP_COMMAND = 'A';
    constexpr char SETUP_C_GEN_COMMAND = 'B'
    
    constexpr char START_ACQ_COMMAND = 'C';
    constexpr char START_GEN_COMMAND = 'D';
    
    constexpr char RESET_GEN_COMMAND = 'E';
    constexpr char RESET_ACQ_COMMAND = 'F';
    
    constexpr char STOP_GEN_COMMAND = 'G';
    constexpr char STOP_ACQ_COMMAND = 'H';

    constexpr char PAUSE_C_GEN_COMMAND = 'I';
    constexpr char UNPAUSE_C_GEN_COMMAND = 'J';
    constexpr char RESET_C_GEN_COMMAND = 'K';
    constexpr char FLIP_C_GEN_COMMAND = 'L';

    constexpr char FULL_CYCLE_COMMAND = 'M';

    constexpr char CLOSE_COMMAND = 'Z';
    
    constexpr rp_channel_t CH_1 = RP_CH_1;
    constexpr rp_channel_t CH_2 = RP_CH_2;


    bool processPitayaErrorcode(int errorcode, std::string functionName);
    bool initialize();
    bool close();

    bool sendNextValue(int uClient);
    bool send_all(int sock, const void* buffer, size_t length);
    bool recv_all(int sock, void* buffer, size_t length);

    bool receiveSettings(int uClient, float& uStartVolVal, int32_t& uFreq, rp_acq_decimation_t& uDec, rp_pinState_t& uGain);
    bool receiveGenType(int uClient, GeneratorConstants::GenType& uGenType);
    bool receiveGenSettings(int uClient, float& uStartingValue, float& uHRange, float& uLRange, float& uStep, GeneratorConstants::Direction& uDirection);
    bool receiveGenSettings(int uClient, float& uBaseVoltage, float& uLimit, float& uStep, int32_t& uNumSteps);

    bool resetGen();
    bool startGen();
    bool stopGen();
    bool setGenSettings(float uStartVolVal, int uFreq);

    bool resetAcq();
    bool startAcq();
    bool triggerAcq();
    bool isBufferFilled();
    bool stopAcq();
    bool setAcqSettings(rp_acq_decimation_t uDec, rp_pinState_t uGain);

    //bool sendPleaseKindlyRepeatTheLastData(int uClient);
    bool sendReady(int uClient);
    bool receiveNewVoltage(int uClient, float& uValue);
    bool changeVoltage(float uNewVoltage, float uCurrentVoltageValue);
    bool acquireVoltage(rp_channel_t uChannel, float& uValue);
    bool sendVoltageValue(int uClient, float* uBuffer);
}
#endif