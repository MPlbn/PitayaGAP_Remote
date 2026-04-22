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
    
    constexpr char GEN_COMMAND = 'B';
    constexpr char START_GEN_COMMAND = 'C';
    constexpr char RESET_GEN_COMMAND = 'D';
    constexpr char STOP_GEN_COMMAND = 'E';
    
    constexpr char ACQ_COMMAND = 'F';
    constexpr char START_ACQ_COMMAND = 'G';
    constexpr char RESET_ACQ_COMMAND = 'H';
    constexpr char STOP_ACQ_COMMAND = 'I';
    
    constexpr char CLOSE_COMMAND = 'Z';
    
    constexpr rp_channel_t CH_1 = RP_CH_1;
    constexpr rp_channel_t CH_2 = RP_CH_2;


    bool processPitayaErrorcode(int errorcode, std::string functionName);
    bool initialize();
    bool close();

    bool sendNextValue(int uClient);
    bool send_all(int sock, const void* buffer, size_t length);
    bool recv_all(int sock, void* buffer, size_t length);

    bool receiveSettings(int uClient, float& hStartVolVal, int32_t& hFreq, rp_acq_decimation_t& hDec, rp_pinState_t& hGain);

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
    bool receiveNewVoltage(int uClient, float& hValue);
    bool changeVoltage(float uNewVoltage);
    bool acquireVoltage(rp_channel_t uChannel, float& Value);
    bool sendVoltageValue(int uClient, float* uBuffer);
}