from constants import *
from commands import *
import CMDManager
import time
import socket
import struct

def transformToFloat(value:str) -> float:
    try:
        retVal = float(value)
        return retVal
    except ValueError:
        print(f'ERROR: {value} is not a valid number')
        return None



# cmdMan = CMDManager.CMDManager(RED_PITAYA_IP)
# cmdMan.connectToPitaya()
# cmdMan.executeCommand(CMD_LOAD_SCPI_FPGA)
# cmdMan.executeCommand(CMD_START_CUSTOM_SERVER)
# cmdMan.disconnectFromPitaya()
for _ in range(5):
    try:
        sock = socket.create_connection((RED_PITAYA_IP,5000))
        break
    except ConnectionRefusedError:
        time.sleep(0.5)

freq:int = 1000
amp:float = 0.0

dec:int = 1
gain = 0


sock.sendall(SETUP_COMMAND)
response = sock.recv(1)
if(response == RESPONSE_READY):
    print("READY!")

packet = struct.pack('<f i i B', amp, freq, dec, gain)

sock.sendall(packet)

response = sock.recv(1)
if(response == RESPONSE_READY):
    print("READY!")

# while(True):
#     userInput = input("Provide float value or write 'C' to finish the program").lower()

#     if(userInput == 'c'):
#         break
#     else:
#         value:float = transformToFloat(userInput)
#         if(value is None):
#             value = 0.10
        
#         sock.sendall(GEN_COMMAND)
#         response = sock.recv(1)
        
#         if(response == RESPONSE_READY):
#             print("READY!")
#             sock.sendall(struct.pack('f', value))
#         else:
#             print("ERROR: PITAYA NOT READY")
#             break
time.sleep(2)
sock.sendall(CLOSE_COMMAND)
sock.close()