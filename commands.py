from constants import *

CMD_LOAD_SCPI_FPGA = "echo STANDARD OVERLAY && /opt/redpitaya/sbin/overlay.sh v0.94"
CMD_STOP_NGINX = "echo STOPING NGINX && systemctl stop redpitaya_nginx"
CMD_START_SCPI_SERVER = "echo START SCPI SERVER && systemctl start redpitaya_scpi &"

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
    '-r', 'inf', #tochange
    '-v'
    ] #add .exe for windows
def CMD_START_STREAMING_DAC():
    return CCMD_START_STREAMING_DAC.copy()

CCMD_START_STREAMING_ADC = [
    './streaming_app/rpsa_client', 
    '-s', 
    '-h', f'{RED_PITAYA_IP}',
    '-f', 'csv', 
    '-d', './dataLogs', 
    '-l', '', 
    '-m', 'volt',
    'v'
    ]
def CMD_START_STREAMING_ADC():
    return CCMD_START_STREAMING_ADC.copy()

CMD_LIST_PROCESS = "pgrep -af streaming-server"
CMD_LIST_PROCESS_SCPI = "pgrep -af scpi-server"

# ==================== TEST GENERATE FUNCTIONS ====================
TEST_CMD_GENERATE = "/opt/redpitaya/bin/generate 1 "
