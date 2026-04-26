#include "serverUtils.h"
#include "generate.h"

int main(){
    float currentVoltageValue;


    Generator generator = Generator();
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

    int nagleFlag = 1;
    setsockopt(client, IPPROTO_TCP, TCP_NODELAY, &nagleFlag, sizeof(nagleFlag));
    std::cout << "TCP_NODELAY enabled!\n";

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
            rp_acq_decimation_t dec;
            rp_pinState_t gain;
            
            if(!PitayaServerUtils::sendReady(client)){
                std::cout << "Error sending the ready status to client\n";
                break;
            } 

            if(!PitayaServerUtils::receiveSettings(client, freq, dec, gain)){
                std::cout << "Error recieving setup values\n";
                break;
            }
            if(!PitayaServerUtils::setGenSettings(freq)){
                std::cout << "Error setting generator settings\n";
                break;
            }
            if(!PitayaServerUtils::setAcqSettings(dec, gain)){
                std::cout << "Error setting acquisitor settings\n";
                break;
            }
            if(!PitayaServerUtils::changeVoltage(currentVoltageValue)){
                std::cout << "error setting starting voltage\n";
                break;
            }
            if(!PitayaServerUtils::sendReady(client)){
                std::cout << "Error sending the ready status to client\n";
                break;
            }              

        }

        else if(cmd == PitayaServerUtils::SETUP_C_GEN_COMMAND){
            if(!PitayaServerUtils::sendReady(client)){
                std::cout << "Error sending the ready status to client\n";
                break;
            } 
            GeneratorConstants::GenType genType;
            if(!PitayaServerUtils::receiveGenType(client, genType)){
                std::cout << "Error receiving GenType\n";
                break;
            }

            float startingValue;
            float hRange;
            float step;
            if(genType == GeneratorConstants::GenType::NORMAL){
                float lRange;
                GeneratorConstants::Direction direction;
                if(!PitayaServerUtils::receiveGenSettings(client, startingValue, hRange, lRange, step, direction)){
                    std::cout << "Error receiving Cgenerator settings\n";
                    break;
                }
                generator.setup(genType, startingValue, hRange, lRange, step, direction);
            }
            else if(genType == GeneratorConstants::GenType::STEPPING){
                int32_t numSteps;
                if(!PitayaServerUtils::receiveGenSettings(client, startingValue, hRange, step, numSteps)){
                    std::cout << "Error receiving Cgenerator settings\n";
                    break;
                }
                generator.setup(genType, startingValue, hRange, step, static_cast<int>(numSteps));
            }
            currentVoltageValue = startingValue;

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
            generator.reset();
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
            if(!PitayaServerUtils::stopGen()){
                std::cout << "Error stopping generator";
                break;
            }
            if(!PitayaServerUtils::sendReady(client)){
                std::cout << "Error sending the ready status to client\n";
                break;
            }            
        }

        else if(cmd == PitayaServerUtils::STOP_ACQ_COMMAND){
            if(!PitayaServerUtils::stopAcq()){
                std::cout << "Error stopping acquisition";
                break;
            }
            if(!PitayaServerUtils::sendReady(client)){
                std::cout << "Error sending the ready status to client\n";
                break;
            }            
        }

        else if(cmd == PitayaServerUtils::PAUSE_C_GEN_COMMAND){
            generator.setPause(true);
        }

        else if(cmd == PitayaServerUtils::UNPAUSE_C_GEN_COMMAND){
            generator.setPause(false);
        }

        else if(cmd == PitayaServerUtils::RESET_C_GEN_COMMAND){
            generator.reset();
        }

        else if (cmd == PitayaServerUtils::FLIP_C_GEN_COMMAND){
            generator.flip();
        }
        //possibly manual change volatge also
        else if(cmd == PitayaServerUtils::FULL_CYCLE_COMMAND){
            //Generate part
            float newVoltageValue = generator.workRoutine();
            if(!PitayaServerUtils::changeVoltage(newVoltageValue)){
                std::cout << "Error changing the voltage on redpitaya\n";
                break;
            }
            currentVoltageValue = newVoltageValue;
            //Acq part
            float ch1Val;
            float ch2Val;
            // wait for a small time
            PitayaServerUtils::wait(10000);
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

            float values[3] = {ch1Val, ch2Val, newVoltageValue};
            std::cout << "VOLTAGE VALUES ACQUIRED: " << ch1Val << " | " << ch2Val << " | " << newVoltageValue << "\n";
            if(!PitayaServerUtils::sendVoltageValue(client, values)){ 
                std::cout << "Error sending the voltage value back to python program\n";
                break;
            }
        }

        else if(cmd == PitayaServerUtils::NOGEN_FULL_CYCLE_COMMAND){
            float ch1Val;
            float ch2Val;

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

            float values[3] = {ch1Val, ch2Val, currentVoltageValue};
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