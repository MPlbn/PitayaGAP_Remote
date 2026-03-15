#include "serverUtils.h"

int main(){
    // ========== starting server ===========
    int server = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(5000);
    addr.sin_addr.s_addr = INADDR_ANY;
    bind(server, (sockaddr*)&addr, sizeof(addr));
    listen(server, 1);

    std::cout << "Listening...\n";

    int client = accept(server, nullptr, nullptr);
    std::cout << "Client connected!\n";

    PitayaServerUtils::initialize();
    std::cout << "Redpitaya API initialized!\n";

    // ========== main server loop ==========
    while(true){
        char cmd;
        int n = recv(client, &cmd, 1, 0);
        if(n <= 0){
            std::cout << "Client disconnected\n";
            break;
        }

        if(cmd == PitayaServerUtils::SETUP_COMMAND){
            int32_t freq;
            float voltageValue;
            rp_acq_decimation_t dec;
            rp_pinState_t gain;
            
            if(!PitayaServerUtils::sendReady(client)){
                std::cout << "Error sending the ready status to client\n";
                break;
            } 

            if(!PitayaServerUtils::receiveSettings(client, voltageValue, freq, dec, gain)){
                std::cout << "Error recieving setup values\n";
                break;
            }
            if(!PitayaServerUtils::setGenSettings(voltageValue, freq)){
                std::cout << "Error setting generator settings\n";
                break;
            }
            if(!PitayaServerUtils::setAcqSettings(dec, gain)){
                std::cout << "Error setting acquisitor settings\n";
                break;
            }
            if(!PitayaServerUtils::sendReady(client)){
                std::cout << "Error sending the ready status to client\n";
                break;
            }              
        }

        else if(cmd == PitayaServerUtils::START_GEN_COMMAND){
            if(!PitayaServerUtils::startGen()){ 
                std::cout << "Error starting the generator";
                break;
            }
            if(!PitayaServerUtils::sendReady(client)){
                std::cout << "Error sending the ready status to client\n";
                break;
            }            
        }

        else if(cmd == PitayaServerUtils::START_ACQ_COMMAND){
            if(!PitayaServerUtils::startAcq()){
                std::cout << "Error starting the acquisition";
                break;
            }
            if(!PitayaServerUtils::sendReady(client)){
                std::cout << "Error sending the ready status to client\n";
                break;
            }            
        }

        else if(cmd == PitayaServerUtils::RESET_GEN_COMMAND){
            if(!PitayaServerUtils::resetGen()){
                std::cout << "Error reseting generator";
                break;
            }
            if(!PitayaServerUtils::sendReady(client)){
                std::cout << "Error sending the ready status to client\n";
                break;
            }            
        }

        else if(cmd == PitayaServerUtils::RESET_ACQ_COMMAND){
            if(!PitayaServerUtils::resetAcq()){
                std::cout << "Error reseting acquisition";
                break;
            }
            if(!PitayaServerUtils::sendReady(client)){
                std::cout << "Error sending the ready status to client\n";
                break;
            }            
        }

        else if(cmd == PitayaServerUtils::STOP_GEN_COMMAND){
            if(PitayaServerUtils::stopGen()){
                std::cout << "Error stopping generator";
                break;
            }
            if(!PitayaServerUtils::sendReady(client)){
                std::cout << "Error sending the ready status to client\n";
                break;
            }            
        }

        else if(cmd == PitayaServerUtils::STOP_ACQ_COMMAND){
            if(PitayaServerUtils::stopAcq()){
                std::cout << "Error stopping acquisition";
                break;
            }
            if(!PitayaServerUtils::sendReady(client)){
                std::cout << "Error sending the ready status to client\n";
                break;
            }            
        }

        else if(cmd == PitayaServerUtils::GEN_COMMAND){ //CMD FOR CHANGE VOLT
            if(!PitayaServerUtils::sendReady(client)){
                std::cout << "Error sending the ready status to client\n";
                break;
            }
            float newVoltageValue;
            if(!PitayaServerUtils::receiveNewVoltage(client, newVoltageValue)){
                std::cout << "Error recieving new voltage\n";
                break;
            }
            if(!PitayaServerUtils::changeVoltage(newVoltageValue)){
                std::cout << "Error changing the voltage on redpitaya\n";
                break;
            }
        }

        else if(cmd == PitayaServerUtils::ACQ_COMMAND){ //CMD FOR ACQUIRE
            int16_t ch1Val;
            int16_t ch2Val;

            if(!PitayaServerUtils::triggerAcq()){
                std::cout << "Error setting the ACQ trigger to CH1\n";
                break;
            }

            if(!PitayaServerUtils::isBufferFilled()){
                std::cout << "Error on filling the buffer\n";
                break;
            }

            if(!PitayaServerUtils::acquireVoltage(PitayaServerUtils::CH_1, ch1Val)){
                std::cout << "Error acquiring the voltage from CH1 on redpitaya\n";
                break;
            }

            if(!PitayaServerUtils::acquireVoltage(PitayaServerUtils::CH_2, ch2Val)){
                std::cout << "Error acquiring the voltage from CH2 on redpitaya\n";
                break;
            }       

            int16_t values[2] = {ch1Val, ch2Val};
            if(!PitayaServerUtils::sendVoltageValue(client, values)){ 
                std::cout << "Error sending the voltage value back to python program\n";
                break;
            }
        }

        else if(cmd == PitayaServerUtils::CLOSE_COMMAND){ //CMD FOR STOPPING THE SERVER
            std::cout << "Client disconnected\n";
            break;
        } 
    }
    close(client);
    close(server);
}