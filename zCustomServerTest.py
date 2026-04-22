from constants import *
from commands import *
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

sock.sendall(RESET_GEN_COMMAND)
response = sock.recv(1)
if(response == RESPONSE_READY):
    print("Reset Ready")

sock.sendall(RESET_ACQ_COMMAND)
response = sock.recv(1)
if(response == RESPONSE_READY):
    print("acq reset!")

sock.sendall(SETUP_COMMAND)
response = sock.recv(1)
if(response == RESPONSE_READY):
    print("ready to send setup values!")

packet = struct.pack('<f i i B', amp, freq, dec, gain)

sock.sendall(packet)

response = sock.recv(1)
if(response == RESPONSE_READY):
    print("setup done!")

sock.sendall(START_GEN_COMMAND)
response = sock.recv(1)
if(response == RESPONSE_READY):
    print("gen started!")


sock.sendall(START_ACQ_COMMAND)
response = sock.recv(1)
if(response == RESPONSE_READY):
    print("acq started!")

voltageValue = GEN_DEFAULT_VOLTAGE
step = GEN_DEFAULT_STEP
highRange = GEN_MAX_RANGE
lowRange = GEN_MIN_RANGE

testValueX = []
testValueY = []

timeValues = []

for _ in range(50):
    startTime = time.time()
    if(voltageValue + step > highRange):
        if(step > 0):
            step *= -1.0
    if(voltageValue + step < lowRange):
        if(step < 0):
            step *= -1.0 
    voltageValue += step
    
    sock.sendall(GEN_COMMAND)
    response = sock.recv(1)
    if(response == RESPONSE_READY):
        print("value change initiated")

    sendValue = voltageValue/1000
    packet = struct.pack('<f', sendValue)
    sock.sendall(packet)

    sock.sendall(ACQ_COMMAND)
    buffer = sock.recv(8)
    values = struct.unpack("<f f", buffer)
    testValueX.append(values[0])
    endTime = time.time()
    timeValues.append(endTime-startTime)


print(timeValues)

sock.sendall(STOP_GEN_COMMAND)
response = sock.recv(1)
if(response == RESPONSE_READY):
    print("gen stopped!")
sock.sendall(STOP_ACQ_COMMAND)
response = sock.recv(1)
if(response == RESPONSE_READY):
    print("acq stopped!")

sock.sendall(CLOSE_COMMAND)

sock.close()