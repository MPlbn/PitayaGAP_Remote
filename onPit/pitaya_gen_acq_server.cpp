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
            float newVoltageValue;
            PitayaServerUtils::recieveNewVoltage(newVoltageValue);
            PitayaServerUtils::changeVoltage(newVoltageValue);
        }

        if(cmd == PitayaServerUtils::ACQ_COMMAND){ //CMD FOR ACQUIRE
            float values[2];
            PitayaServerUtils::acquireVoltage(PitayaServerUtils::CH_1, values[0]);
            PitayaServerUtils::acquireVoltage(PitayaServerUtils::CH_2, values[1]);
            PitayaServerUtils::sendVoltageValue(client, values);
        }

        if(cmd == PitayaServerUtils::CLOSE_COMMAND){ //CMD FOR STOPPING THE SERVER
            std::cout << "Client disconnected\n";
            break;
        } 
    }
    close(client);
    close(server);
}