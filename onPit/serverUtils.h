#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/tcp.h>
#include <cstring>
#include <iostream>
#include "rp.h"

namespace PitayaServerUtils{
    constexpr int PORT = 5000;
    constexpr char SETUP_COMMAND = 'S';
    constexpr char ACQ_COMMAND = 'A';
    constexpr char GEN_COMMAND = 'G';
    constexpr char CLOSE_COMMAND = 'C';
    constexpr rp_channel_t CH_1 = RP_CH_1;
    constexpr rp_channel_t CH_2 = RP_CH_2;

    bool sendNextValue(int uClient);
    bool send_all(int sock, const void* buffer, size_t length);
    bool recv_all(int sock, void* buffer, size_t length);

    bool resetGen();
    bool startGen();
    bool stopGen();
    bool receiveGenSettings(int uClient, float& hStartVolVal, int& hFreq);
    bool setGenSettings(float uStartVolVal, int uFreq);

    bool resetAcq();
    bool startAcq();
    bool stopAcq();
    bool receiveAcqSettings(int uClient, rp_acq_decimation_t& hDec, rp_pinState_t& hGain);
    bool setAcqSettings(rp_acq_decimation_t uDec, rp_pinState_t uGain);

    //bool sendPleaseKindlyRepeatTheLastData(int uClient);
    bool sendReady(int uClient);
    bool receiveNewVoltage(int uClient, float& hValue);
    bool changeVoltage(float uNewVoltage);
    bool acquireVoltage(rp_channel_t uChannel, float& hValue);
    bool sendVoltageValue(int uClient, float* uBuffer);
}