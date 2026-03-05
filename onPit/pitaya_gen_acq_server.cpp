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

    // ========== main server loop ==========
    while(true){
        char cmd;
        int n = recv(client, &cmd, 1, 0);
        if(n <= 0){
            std::cout << "Client disconnected\n";
            break;
        }

        if(cmd == PitayaServerUtils::GEN_COMMAND){ //CMD FOR CHANGE VOLT
            if(!PitayaServerUtils::sendReady(client)){
                std::cout << "Error sending the ready status to client\n";
                break;
            }
            float newVoltageValue;
            if(!PitayaServerUtils::recieveNewVoltage(client ,newVoltageValue)){
                std::cout << "Error recieving new voltage\n";
                break;
            }
            if(!PitayaServerUtils::changeVoltage(newVoltageValue)){
                std::cout << "Error changing the voltage on redpitaya\n";
                break;
            }
        }

        if(cmd == PitayaServerUtils::ACQ_COMMAND){ //CMD FOR ACQUIRE
            float values[2];
            if(!PitayaServerUtils::acquireVoltage(PitayaServerUtils::CH_1, values[0])){
                std::cout << "Error acquiring the voltage from CH1 on redpitaya";
                break;
            }
            if(!PitayaServerUtils::acquireVoltage(PitayaServerUtils::CH_2, values[1])){
                std::cout << "Error acquiring the voltage from CH2 on redpitaya";
                break;
            }            
            if(!PitayaServerUtils::sendVoltageValue(client, values)){
                std::cout << "Error sending the voltage value back to python program";
                break;
            }
        }

        if(cmd == PitayaServerUtils::CLOSE_COMMAND){ //CMD FOR STOPPING THE SERVER
            std::cout << "Client disconnected\n";
            break;
        } 
    }
    close(client);
    close(server);
}