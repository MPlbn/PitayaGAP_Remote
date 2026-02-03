import paramiko
import numpy as np
import threading
import select

class CMDManager:
    def __init__(self, uIP, uUsername='root', uPassword='root'):
        self.ip = uIP
        self.username = uUsername
        self.password = uPassword
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
        return self.stdout, self.stderr
    
    def startListening(self):
        self.outputContent = ""
        self.errorContent = ""
        self.listenerThread = threading.Thread(target=self.listener)
        self.listenerThread.start()

    def listener(self):
        while True:
            isReadyToRead, _, _ = select.select([self.stdout.channel, self.stderr.channel], [], [], 0.1)
            if (not isReadyToRead):
                continue
            for stream in isReadyToRead:
                if stream == self.stdout.channel and stream.recv_ready():
                    outputContent = stream.recv(1024).decode('utf-8')
                    print("STDOUT LISTENER:", outputContent, end='', flush=True)
                elif (stream == self.stderr.channel and stream.recv_stderr_ready()):
                    errorContent = stream.recv_stderr(1024).decode('utf-8')
                    print("STDERR LISTENER:", errorContent, end='', flush=True)
            if (self.stdout.channel.exit_status_ready()):
                break