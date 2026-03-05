#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/tcp.h>
#include <cstring>
#include <iostream>

#include "rp.h"
#include "serverUtils.h"

/*
    Redpitaya API has super bad documentation, it isn't mentioned anywhere what the return values of functions are so it's hard to check for any errors 
    and handle them here. I leave the wrappers to return bool, if the documentation becomes more thorough somebody can write the error handling.
*/

namespace PitayaServerUtils{
    rp_channel_t outputChannel = RP_CH_1;
    rp_channel_t inputChannels[2] = {RP_CH_1, RP_CH_2};


    bool resetGen(){
        rp_GenReset();
        return true;
    }

    bool startGen(int uClient){
        rp_GenOutEnable(outputChannel);
        rp_GenResetTrigger(outputChannel);
        return true;
    }

    bool stopGen(int uClient){
        rp_GenOutDisable(outputChannel);
        return true;
    }

    bool setGenSettings(int uClient){
        float startingVoltageValue;
        int frequency;
        rp_waveform_t wfType;
        //TODO Get those from python

        rp_GenWaveform(outputChannel, wfType);
        rp_GenFreq(outputChannel, frequency);
        rp_GenAmp(outputChannel, startingVoltageValue);

        return true;
    }

    bool resetAcq(int uClient){
        rp_AcqReset();
        return true;
    }

    bool startAcq(int uClient){
        rp_AcqStart();      
        return true;
    }
    
    bool triggerAcq(int uClient){
        rp_acq_trig_src_t triggerSource = RP_TRIG_SRC_NOW; 
        rp_AcqSetTriggerSrc(triggerSource);
        return true;
    }

    bool stopAcq(int uClient){
        rp_AcqStop();
        return true;
    }

    bool setAcqSettings(int uClient){
        rp_acq_decimation_t decimation;
        rp_pinState_t gainState;
        
        rp_AcqSetArmKeep(true); // keeps the continuous acquisition
        rp_AcqSetAveraging(false); // averages all samples skipped due to decimation
        rp_AcqSetGain(inputChannels[0], gainState);
        rp_AcqSetGain(inputChannels[1], gainState);
        rp_AcqSetDecimation(decimation);


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

    bool recieveNewVoltage(int uClient, float& uValueHolder){
        float recBuffer;
     
        int recieved = recv(uClient, &recBuffer, sizeof(recBuffer), 0);
        if (recieved <= 0){
            return false;
        }
        uValueHolder = recBuffer;
        return true;
    }

    bool changeVoltage(float uNewVoltage){
        rp_GenAmp(outputChannel, uNewVoltage);
        return true;
    }

    bool acquireVoltage(int uChannel, float& uValueHolder){
        //to write with redpitaya api
        if(true){
            return false;
        }

        return true;
    }

    bool sendVoltageValue(int uClient, float* uBuffer){
        int sent = send(uClient, uBuffer, sizeof(uBuffer), 0);  
        
        if(sent <= 0){
            return false;
        }
    
        return true;
    }
}