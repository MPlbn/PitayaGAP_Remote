from constants import *

CMD_LOAD_STANDARD_FPGA = "echo STANDARD OVERLAY && /opt/redpitaya/sbin/overlay.sh v0.94"
CMD_STOP_NGINX = "echo STOPING NGINX && systemctl stop redpitaya_nginx"
CMD_START_NGINX = "echo STOPING NGINX && systemctl start redpitaya_nginx" 
CMD_START_SCPI_SERVER = "echo START SCPI SERVER && systemctl start redpitaya_scpi &" #TODO delete

CMD_START_CUSTOM_SERVER = "echo START CUSTOM SERVER && nohup /root/RedPitaya/gen-acq-server/custom_server > /tmp/server.log 2>&1 < /dev/null &"

CMD_START_STREAMING_SERVER = "echo STREAMINGSERVER && /opt/redpitaya/bin/streaming-server -b"
CMD_STOP_PROCESS = "kill "
CMD_LOAD_STREAMING_FPGA = "echo OVERLAY && /opt/redpitaya/sbin/overlay.sh stream_app"
CCMD_UPLOAD_CONFIG = [
    './streaming_app/rpsa_client', 
    '-c', 
    '-h', f'{RED_PITAYA_IP}',
    '-s', 'F', 
    '-f', './streaming_app/GAPconfig.json'] #add .exe for windows
def CMD_UPLOAD_CONFIG():
    return CCMD_UPLOAD_CONFIG.copy()

CCMD_START_STREAMING_DAC = [
    './streaming_app/rpsa_client', 
    '-o',
    '-h', f'{RED_PITAYA_IP}',
    '-f', 'wav', 
    '-d', '', 
    '-r', 'inf'
    #'-v'
    ] 
def CMD_START_STREAMING_DAC():
    return CCMD_START_STREAMING_DAC.copy()

CCMD_START_STREAMING_ADC = [
    './streaming_app/rpsa_client', 
    '-s', 
    '-h', f'{RED_PITAYA_IP}',
    '-f', 'bin', 
    '-d', './dataLogs', 
    '-l', '', 
    '-m', 'raw'
    #'-v'
    ]
def CMD_START_STREAMING_ADC():
    return CCMD_START_STREAMING_ADC.copy()

CMD_LIST_PROCESS = "pgrep -af streaming-server"
CMD_LIST_PROCESS_SCPI = "pgrep -af scpi-server"


SETUP_COMMAND = b'A'
SETUP_C_GEN_COMMAND = b'B'
START_ACQ_COMMAND = b'C'
START_GEN_COMMAND = b'D'
RESET_GEN_COMMAND = b'E'
RESET_ACQ_COMMAND = b'F'
STOP_GEN_COMMAND = b'G'
STOP_ACQ_COMMAND = b'H'
PAUSE_C_GEN_COMMAND = b'I'
UNPAUSE_C_GEN_COMMAND = b'J'
RESET_C_GEN_COMMAND = b'K'
FLIP_C_GEN_COMMAND = b'L'
GEN_COMMAND = b'M'
ACQ_COMMAND = b'N'
CLOSE_COMMAND = b'Z'

RESPONSE_READY = b'R'
