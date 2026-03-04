#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/tcp.h>
#include <cstring>
#include <iostream>

namespace PitayaServerUtils{

    bool recieveNewVoltage(int uClient, float& uValueHolder){
        float recBuffer;
     
        int error = recv(uClient, &recBuffer, sizeof(recBuffer), 0);
        if (error <= 0){
            std::cout << "Client disconnected or error\n";
            return false;
        }
        uValueHolder = recBuffer;
        return true;
    }

    bool changeVoltage(float uNewVoltage){
        //to write with redpitaya api
        if(true){
            std::cout << "Error changing the output voltage on redpitaya\n";
            return false;
        }
  
        return true;
    }

    bool acquireVoltage(int uChannel, float& uValueHolder){
        //to write with redpitaya api
        if(true){
            std::cout << "Error acquiring the voltage from redpitaya\n";
            return false;
        }

        return true;
    }

    bool sendVoltageValue(int uClient, float* uBuffer){
        int error = send(uClient, uBuffer, sizeof(uBuffer), 0);  
        
        if(error <= 0){
            std::cout << "Error sending voltage to client\n";
            return false;
        }
    
        return true;
    }
}