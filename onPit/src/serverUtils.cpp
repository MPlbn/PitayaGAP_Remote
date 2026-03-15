#ifndef SERVERUTILS_H
#define SERVERUTILS_H

#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/tcp.h>
#include <cstring>
#include <iostream>
#include <typeinfo>
#include <string>
#include "rp.h"

/*
    Redpitaya API has super bad documentation, it isn't mentioned anywhere what the return values of functions are so it's hard to check for any errors 
    and handle them here. I leave the wrappers to return bool, if the documentation becomes more thorough somebody can write the error handling.
*/

namespace PitayaServerUtils{

    constexpr rp_channel_t outputChannel = RP_CH_1;
    constexpr rp_channel_t inputChannels[2] = {RP_CH_1, RP_CH_2};

    bool isNegative = false;

    bool processPitayaErrorcode(int errorcode, std::string functionName){
        std::string errorMsg;
        bool isNoError = false;
        switch (errorcode){
                case RP_OK:      errorMsg = "Success"; isNoError = true; break;
                case RP_EOED:    errorMsg = "Failed to Open EEPROM Device"; break;
                case RP_EOMD:    errorMsg = "Failed to Open Memory Device"; break;
                case RP_ECMD:    errorMsg = "Failed to Close Memory Device"; break;
                case RP_EMMD:    errorMsg = "Failed to Map Memory Device"; break;
                case RP_EUMD:    errorMsg = "Failed to Unmap Memory Device"; break;
                case RP_EOOR:    errorMsg = "Value Out Of Range"; break;
                case RP_ELID:    errorMsg = "LED Input Direction is not valid"; break;
                case RP_EMRO:    errorMsg = "Modifying Read Only field"; break;
                case RP_EWIP:    errorMsg = "Writing to Input Pin is not valid"; break;
                case RP_EPN:     errorMsg = "Invalid Pin number"; break;
                case RP_UIA:     errorMsg = "Uninitialized Input Argument"; break;
                case RP_FCA:     errorMsg = "Failed to Find Calibration Parameters"; break;
                case RP_RCA:     errorMsg = "Failed to Read Calibration Parameters"; break;
                case RP_BTS:     errorMsg = "Buffer too small"; break;
                case RP_EIPV:    errorMsg = "Invalid parameter value"; break;
                case RP_EUF:     errorMsg = "Unsupported Feature"; break;
                case RP_ENN:     errorMsg = "Data not normalized"; break;
                case RP_EFOB:    errorMsg = "Failed to open bus"; break;
                case RP_EFCB:    errorMsg = "Failed to close bus"; break;
                case RP_EABA:    errorMsg = "Failed to acquire bus access"; break;
                case RP_EFRB:    errorMsg = "Failed to read from the bus"; break;
                case RP_EFWB:    errorMsg = "Failed to write to the bus"; break;
                case RP_EMNC:    errorMsg = "Extension module not connected"; break;
                case RP_NOTS:    errorMsg = "Command not supported"; break;
                case RP_EAM:     errorMsg = "Error allocate memory"; break;
                case RP_EANI:    errorMsg = "API not initialized"; break;
                case RP_EOP:     errorMsg = "Execution error"; break;
                default:         errorMsg = "Unknown error code"; break;
        }
        std::cout << "Return Code for: <" << functionName << ">|" << errorcode << "|: " << errorMsg <<"\n";
        return isNoError;
    }

    bool initialize(){
        return processPitayaErrorcode(
            rp_Init(),
            "rp_Init()"
        );
    }

    bool close(){
        return processPitayaErrorcode(
            rp_Release(),
            "rp_Release()"
        );
    }

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

    bool receiveSettings(int uClient, float& hStartVolVal, int32_t& hFreq, rp_acq_decimation_t& hDec, rp_pinState_t& hGain){
        float volt;
        int32_t freq;
        int32_t dec;
        uint8_t gain;
        if(!recv_all(uClient, &volt, sizeof(volt))) return false;
        if(!recv_all(uClient, &freq, sizeof(freq))) return false;
        if(!recv_all(uClient, &dec, sizeof(dec))) return false;
        if(!recv_all(uClient, &gain, sizeof(gain))) return false;

        hStartVolVal = volt;
        hFreq = freq;
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
        hGain = gain ? RP_HIGH : RP_LOW;
        return true;
        }

    bool resetGen(){
        return processPitayaErrorcode(
            rp_GenReset(),
            "rp_GenReset()"
        );
    }

    bool startGen(){
        if(!processPitayaErrorcode(
            rp_GenOutEnable(outputChannel),
            "rp_GenOutEnable()"
        )) return false;

        if(!processPitayaErrorcode(
            rp_GenResetTrigger(outputChannel),
            "rp_GenResetTrigger()"
        )) return false;

        return true;
    }

    bool stopGen(){
        return processPitayaErrorcode(
            rp_GenOutDisable(outputChannel),
            "rp_GenOutDisable()"
        );
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

        if(!processPitayaErrorcode(
            rp_GenWaveform(RP_CH_1, wfType),
            "rp_GenWaveform()"
        )) return false;

        if(!processPitayaErrorcode(
            rp_GenFreq(RP_CH_1, uFreq),
            "rp_GenFreq()"
        )) return false;

        if(!processPitayaErrorcode(
            rp_GenAmp(RP_CH_1, uStartVolVal),
            "rp_GenAmp()"
        )) return false;

        return true;
    }

    bool resetAcq(){
        return processPitayaErrorcode(
            rp_AcqReset(),
            "rp_AcqReset()"
        );
    }

    bool startAcq(){
        return processPitayaErrorcode(
            rp_AcqStart(),
            "rp_AcqStart()"    
        );
    }
    
    bool triggerAcq(){
        rp_acq_trig_src_t triggerSource = RP_TRIG_SRC_NOW; 
        return processPitayaErrorcode(
            rp_AcqSetTriggerSrc(triggerSource),
            "rp_AcqSetTriggerSrc()"
        );
    }

    bool isBufferFilled(){
        bool fillState = false;
        while(!fillState){
            if(!processPitayaErrorcode(
                rp_AcqGetBufferFillState(&fillState),
                "rp_AcqGetBufferFillState()"
            )) return false;
        }
        return true;
    }

    bool stopAcq(){
        return processPitayaErrorcode(
            rp_AcqStop(),
            "rp_AcqStop()"
        );
    }

    bool setAcqSettings(rp_acq_decimation_t uDec, rp_pinState_t uGain){
        if(!processPitayaErrorcode(
            rp_AcqSetArmKeep(true), // keeps the continuous acquisition
            "rp_AcqSetArmKeep()"
        )) return false;
        
        if(!processPitayaErrorcode(
            rp_AcqSetAveraging(false), // averages all samples skipped due to decimation
            "rp_AcqSetAveraging()"
        )) return false;

        if(!processPitayaErrorcode(
            rp_AcqSetGain(inputChannels[0], uGain),
            "rp_AcqSetGain()"
        )) return false;
        
        if(!processPitayaErrorcode(
            rp_AcqSetGain(inputChannels[1], uGain),
            "rp_AcqSetGain()"
        )) return false;
        
        if(!processPitayaErrorcode(
            rp_AcqSetDecimation(uDec),
            "rp_AcqSetDecimation()"
        )) return false;

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
        std::cout << "| NEW VOLTAGE VALUE: " << uNewVoltage << " |\n";
        if(isNegative){
            if(uNewVoltage >= 0){
                isNegative = false;
                if(!processPitayaErrorcode(
                    rp_GenWaveform(RP_CH_1, RP_WAVEFORM_DC),
                    "rp_GenWaveform(RP_CH_1, RP_WAVEFORM_DC)"
                )) return false;
            }
        }
        else{
            if(uNewVoltage < 0){
                isNegative = true;
                if(!processPitayaErrorcode(
                    rp_GenWaveform(RP_CH_1, RP_WAVEFORM_DC_NEG),
                    "rp_GenWaveform(RP_CH_1, RP_WAVEFORM_DC_NEG)"
                )) return false;
            }
        }

        if(!processPitayaErrorcode(
            rp_GenAmp(RP_CH_1, std::abs(uNewVoltage)), //change to absolute value + DC_NEG set for values lower than 0
            "rp_GenAmp()"
        )) return false;

        return true;
    }

    bool acquireVoltage(rp_channel_t uChannel, int16_t& hValue){
        int16_t buffer[1];
        uint32_t size = 1;



        if(!processPitayaErrorcode(
            rp_AcqGetLatestDataRaw(uChannel, &size, buffer),
            "rp_AcqGetLatestDataRaw()"
        )) return false;

        hValue = buffer[0];

        return true;
    }

    bool sendVoltageValue(int uClient, int16_t* uBuffer){
        int sent = send_all(uClient, uBuffer, sizeof(int16_t) * 2);  
        
        if(sent <= 0){
            return false;
        }
    
        return true;
    }
}

#endif