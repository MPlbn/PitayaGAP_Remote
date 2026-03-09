#ifndef SERVERUTILS_H
#define SERVERUTILS_H

#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/tcp.h>
#include <cstring>
#include <iostream>
#include "rp.h"

/*
    Redpitaya API has super bad documentation, it isn't mentioned anywhere what the return values of functions are so it's hard to check for any errors 
    and handle them here. I leave the wrappers to return bool, if the documentation becomes more thorough somebody can write the error handling.
*/

namespace PitayaServerUtils{

    constexpr rp_channel_t outputChannel = RP_CH_1;
    constexpr rp_channel_t inputChannels[2] = {RP_CH_1, RP_CH_2};

    bool isNegative = false;

    bool sendNextValue(int uClient){ //unused
        return false;
    }

    bool send_all(int sock, const void* buffer, size_t length){
        size_t total = 0;
        while(total < length){
            ssize_t n = send(sock, (const char*)buffer + total, length - total, 0);
            if(n <= 0){
                return false;
            }
            total += n;
        }
        return true;
    }

    bool recv_all(int sock, void* buffer, size_t length){
        size_t total = 0;
        while (total < length){
            ssize_t n = recv(sock, (char*)buffer + total, length - total, 0);
            if (n <= 0) return false;
            total += n;
        }
        return true;
    }
    bool resetGen(){
        rp_GenReset();
        return true;
    }

    bool startGen(){
        rp_GenOutEnable(outputChannel);
        rp_GenResetTrigger(outputChannel);
        return true;
    }

    bool stopGen(){
        rp_GenOutDisable(outputChannel);
        return true;
    }

    bool receiveGenSettings(int uClient, float& hStartVolVal, int& hFreq){
        
        if(!recv_all(uClient, &hStartVolVal, sizeof(hStartVolVal))){
            return false;
        }

        if(!recv_all(uClient, &hFreq, sizeof(hFreq))){
            return false;
        }
        return true;
    }

    bool setGenSettings(float uStartVolVal, int uFreq){
        rp_waveform_t wfType;
        if(uStartVolVal < 0){
            isNegative = true;
            wfType = RP_WAVEFORM_DC_NEG;
        }
        else{
            isNegative = false;
            wfType = RP_WAVEFORM_DC;
        }

        rp_GenWaveform(outputChannel, wfType);
        rp_GenFreq(outputChannel, uFreq);
        rp_GenAmp(outputChannel, uStartVolVal);

        return true;
    }

    bool resetAcq(){
        rp_AcqReset();
        return true;
    }

    bool startAcq(){
        rp_AcqStart();      
        return true;
    }
    
    bool triggerAcq(){
        rp_acq_trig_src_t triggerSource = RP_TRIG_SRC_NOW; 
        rp_AcqSetTriggerSrc(triggerSource);
        return true;
    }

    bool stopAcq(){
        rp_AcqStop();
        return true;
    }

    bool receiveAcqSettings(int uClient, rp_acq_decimation_t& hDec, rp_pinState_t& hGain){
        uint32_t dec;
        uint8_t gain;

        if(!recv_all(uClient, &dec, sizeof(dec))){
            return false;
        }

        if(!recv_all(uClient, &gain, sizeof(gain))){
            return false;
        }

        switch(dec){
            case 1: 
            case 2: 
            case 4: 
            case 8: 
            case 16:
            case 32: 
            case 64: 
            case 128: 
            case 256:
            case 512: 
            case 1024: 
            case 2048: 
            case 4096:
            case 8192: 
            case 16384: 
            case 32768: 
            case 65536:
                hDec = static_cast<rp_acq_decimation_t>(dec);
                break;
            default:
                return false;
        }
        rp_pinState_t convGain = gain ? RP_HIGH : RP_LOW;
        hGain = convGain;

        return true;
    }

    bool setAcqSettings(rp_acq_decimation_t uDec, rp_pinState_t uGain){
        
        rp_AcqSetArmKeep(true); // keeps the continuous acquisition
        rp_AcqSetAveraging(false); // averages all samples skipped due to decimation
        rp_AcqSetGain(inputChannels[0], uGain);
        rp_AcqSetGain(inputChannels[1], uGain);
        rp_AcqSetDecimation(uDec);


        return true;
    }
    
    // bool sendPleaseKindlyRepeatTheLastData(int uClient){

    //     char repeatCommand = 'E';
    //     int sent = send_all(uClient, &repeatCommand, 1);
    //     if(sent <= 0){
    //         return false;
    //     }
    //     return true;
    // }

    bool sendReady(int uClient){
        char readyCommand = 'R';
        int sent = send_all(uClient, &readyCommand, 1);
        if(sent <= 0){
            return false;
        }
        return true;
    }

    bool receiveNewVoltage(int uClient, float& hValue){
        float recBuffer;
     
        if(!recv_all(uClient, &recBuffer, sizeof(recBuffer))){
            return false;
        }
        hValue = recBuffer;
        return true;
    }

    bool changeVoltage(float uNewVoltage){
        if(isNegative){
            if(uNewVoltage >= 0){
                isNegative = false;
                rp_GenWaveform(outputChannel, RP_WAVEFORM_DC);
            }
        }
        else{
            if(uNewVoltage < 0){
                isNegative = true;
                rp_GenWaveform(outputChannel, RP_WAVEFORM_DC_NEG);
            }
        }
        rp_GenAmp(outputChannel, uNewVoltage);
        return true;
    }

    bool acquireVoltage(rp_channel_t uChannel, float& hValue){
        float buffer[1];
        uint32_t size = 1;

        rp_AcqGetLatestDataV(uChannel, &size, buffer);
        hValue = buffer[0];

        return true;
    }

    bool sendVoltageValue(int uClient, float* uBuffer){
        int sent = send_all(uClient, uBuffer, sizeof(float) * 2);  
        
        if(sent <= 0){
            return false;
        }
    
        return true;
    }
}

#endif