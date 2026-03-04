#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/tcp.h>
#include <cstring>
#include <iostream>

namespace PitayaServerUtils{
    constexpr int PORT = 5000;
    constexpr char ACQ_COMMAND = 'A';
    constexpr char GEN_COMMAND = 'G';
    constexpr char CLOSE_COMMAND = 'C';
    constexpr int CH_1 = 1;
    constexpr int CH_2 = 2;

    bool recieveNewVoltage(int uClient, float& uValueHolder);
    bool changeVoltage(float uNewVoltage);
    bool acquireVoltage(int uChannel, float& uValueHolder);
    bool sendVoltageValue(int uClient, float* uBuffer);
}