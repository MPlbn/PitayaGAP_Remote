from constants import *

CMD_START_SCPI_SERVER = ""
CMD_STOP_SCPI_SERVER = ""

CMD_START_STREAMING_SERVER = "echo STREAMINGSERVER && /opt/redpitaya/bin/streaming-server -b"
CMD_STOP_STREAMING_SERVER = "kill "
CMD_LOAD_STREAMING_FPGA = "echo OVERLAY && /opt/redpitaya/sbin/overlay.sh stream_app"
CMD_UPLOAD_CONFIG = [
    './streaming_app/rpsa_client', 
    '-c', 
    '-s', 'F', 
    '-f', './streaming_app/GAPconfig.json'] #add .exe for windows
CMD_START_STREAMING_DAC = [
    './streaming_app/rpsa_client', 
    '-o', 
    '-f', 'wav', 
    '-d', '', 
    '-r', 'inf'
    ] #add .exe for windows
CMD_START_STREAMING_ADC = [
    './streaming_app/rpsa_client', 
    '-s', 
    '-f', 'csv', 
    '-d', './dataLogs', 
    '-l', '', 
    '-m', 'volt'
    ]

CMD_LIST_PROCESS = "pgrep -af streaming-server"