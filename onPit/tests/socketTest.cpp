#include <iostream>
#include <unistd.h>
#include <arpa/inet.h>
#include <netinet/tcp.h>
#include <cstring>

bool recv_all(int sock, void* buffer, size_t length){
    size_t total = 0;
    while (total < length){
        int n = recv(sock, (char*)buffer + total, length - total, 0);
        if (n <= 0) return false;
        total += n;
    }
    return true;
}

int main(){
    int server = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in addr{};
    addr.sin_family = AF_INET;
    addr.sin_port = htons(5000);
    addr.sin_addr.s_addr = INADDR_ANY;

    bind(server, (sockaddr*)&addr, sizeof(addr));
    listen(server, 1);

    std::cout << "Listening... \n";

    int client = accept(server, nullptr, nullptr);
    int flag = 1;
    std::cout << "Client connected \n";

    while(true){
        char cmd;
        int n = recv(client, &cmd, 1, 0); // just 1 byte
        if (n <= 0){
            std::cout << "Client disconnected\n";
            break;
        }
        
        if (cmd == 'X'){
            std::cout << "Received: " << cmd << "\n";
        }
        else if (cmd == 'S'){
            char buffer = 'R';
            send(client, &buffer, 1, 0);

            float recievedVal;
            recv(client, &recievedVal, sizeof(recievedVal), 0);
            std::cout << "Recieved float: " << recievedVal << "\n";

            float sendList[2];
            sendList[0] = recievedVal + 1.5f;
            sendList[1] = recievedVal - 1.0f;
            send(client, &sendList, sizeof(sendList), 0);
            
        }
    }

    close(client);
    close(server);
}