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

    bool sendNextValue(int uClient){ //unused
        return false;
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
            wfType = RP_DC_NEG;
        }
        else{
            wfType = RP_DC;
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
        int dec;
        bool gain;

        if(!recv_all(uClient, &dec, sizeof(dec))){
            return false;
        }

        if(!recv_all(uClient, &gain, sizeof(gain))){
            return false;
        }

        //perform the transformation and assign the values

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
    
    bool sendPleaseKindlyRepeatTheLastData(int uClient){

        char repeatCommand = 'E';
        int sent = send(uClient, &repeatCommand, 1, 0);
        if(sent <= 0){
            return false;
        }
        return true;
    }

    bool sendReady(int uClient){
        char readyCommand = 'R';
        int sent = send(uClient, &readyCommand, 1, 0);
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
        rp_GenAmp(outputChannel, uNewVoltage);
        return true;
    }

    bool acquireVoltage(rp_channel_t uChannel, float& hValue){
        float value[1];
        uint32_t size = 1;

        rp_AcqGetLatestDataV(uChannel, &size, value);
        hValue = value[0];

        return true;
    }

    bool sendVoltageValue(int uClient, float* uBuffer){
        int sent = send(uClient, uBuffer, sizeof(float) * 2 , 0);  
        
        if(sent <= 0){
            return false;
        }
    
        return true;
    }
}