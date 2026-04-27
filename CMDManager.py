import paramiko
import numpy as np
import threading
import select
import subprocess
import time
import socket
import struct
import threading

from commands import *

#TODO possible cleanup
class CMDManager:
    def __init__(self, uIP, uUsername='root', uPassword='root'):
        self.ip = uIP
        self.username = uUsername
        self.password = uPassword
        self.currentOutputContent = ""
        self.client = None

    def connectToPitaya(self, use_key=False):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.ip, username=self.username, password=self.password)
        print("Connected")
        return self.client
    
    def disconnectFromPitaya(self):
        if(self.client):
            self.client.close()
            print("Disconnected")

    def executeCommand(self, uCommand):
        self.stdin, self.stdout, self.stderr = self.client.exec_command(uCommand)
        self.startListening()
        self.stdout.channel.recv_exit_status()
        return self.stdout, self.stderr, True
    
    def executeLocalCommand(self, uCommand):
        subprocess.run(uCommand)

    def startListening(self):
        self.outputContent = ""
        self.errorContent = ""
        self.listenerThread = threading.Thread(target=self.listener)
        self.listenerThread.start()

    def getOutput(self):
        return self.currentOutputContent

    def listener(self):
        while True:
            isReadyToRead, _, _ = select.select([self.stdout.channel, self.stderr.channel], [], [], 0.1)
            if (not isReadyToRead):
                continue
            for stream in isReadyToRead:
                if stream == self.stdout.channel and stream.recv_ready():
                    outputContent = stream.recv(1024).decode('utf-8')
                    print("STDOUT LISTENER:", outputContent, end='', flush=True)
                    self.currentOutputContent = outputContent
                elif (stream == self.stderr.channel and stream.recv_stderr_ready()):
                    errorContent = stream.recv_stderr(1024).decode('utf-8')
                    print("STDERR LISTENER:", errorContent, end='', flush=True)
            if (self.stdout.channel.exit_status_ready()):
                break

#================== TCP =================#

def recv_all(uSocket, uSize):
    data = bytearray()
    while len(data) < uSize:
        packet = uSocket.recv(uSize - len(data), socket.MSG_WAITALL)
        if not packet:
            raise ConnectionError("Socket closed early")
        data.extend(packet)
    return bytes(data)

# def connectTCP(uIP):
#     for _ in range(5):
#         try:
#             sock = socket.create_connection((uIP, 5000))
#             break
#         except ConnectionRefusedError:
#             time.sleep(0.5)
#     return sock

# def disconnectTCP(uSocket):
#     uSocket.sendall(CLOSE_COMMAND)
#     time.sleep(0.2)
#     uSocket.close()

def executeTCPCommand(uSocket, uCommand):
    uSocket.sendall(uCommand)

def sendTCPNewVoltage(uSocket, uValue):
    packet = struct.pack('<f', uValue)
    uSocket.sendall(packet)

def sendTCPGenMode(uSocket, uGenMode:GenModeGUI):
    genMode = int(uGenMode)
    packet = struct.pack('<i', genMode)
    uSocket.sendall(packet)

def sendTCPSetupValues(uSocket, uFrequency, uDecimation, uGain):
    packet = struct.pack('<i i B', uFrequency, uDecimation, uGain)
    uSocket.sendall(packet)

def sendTCPCGenSetupValues(uSocket, uStartingValue:float, uHRange:float, uLRange:float, uStep:float, uDirection:int):
    packet = struct.pack('<f f f f i', uStartingValue, uHRange, uLRange, uStep, uDirection)
    uSocket.sendall(packet)

def sendTCPCGenStepSetupValues(uSocket, uBase:float, uLimit:float, uStep:float, uNumSteps:int):
    packet = struct.pack('<f f f i', uBase, uLimit, uStep, uNumSteps)   
    uSocket.sendall(packet)

def readTCPReadyState(uSocket) -> bool:
    response = recv_all(uSocket, 1)
    if(response == RESPONSE_READY):
        return True
    return False

def readTCPAcqValues(uSocket): 
    buffer = recv_all(uSocket, 12) 
    values = struct.unpack('<f f f', buffer)
    #print(values)
    return values
