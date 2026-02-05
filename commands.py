from constants import *

CMD_LOAD_SCPI_FPGA = "echo SCPI OVERLAY && /opt/redpitaya/sbin/overlay.sh v0.94"
CMD_STOP_NGINX = "echo STOPING NGINX && systemctl stop redpitaya_nginx"
CMD_START_SCPI_SERVER = "echo START SCPI SERVER && systemctl start redpitaya_scpi &"

CMD_START_STREAMING_SERVER = "echo STREAMINGSERVER && /opt/redpitaya/bin/streaming-server -b"
CMD_STOP_PROCESS = "kill "
CMD_LOAD_STREAMING_FPGA = "echo OVERLAY && /opt/redpitaya/sbin/overlay.sh stream_app"
CMD_UPLOAD_CONFIG = [
    './streaming_app/rpsa_client.exe', 
    '-c', 
    '-s', 'F', 
    '-f', './streaming_app/GAPconfig.json'] #add .exe for windows
CMD_START_STREAMING_DAC = [
    './streaming_app/rpsa_client.exe', 
    '-o', 
    '-f', 'wav', 
    '-d', '', 
    '-r', 'inf'
    ] #add .exe for windows
CMD_START_STREAMING_ADC = [
    './streaming_app/rpsa_client.exe', 
    '-s', 
    '-f', 'csv', 
    '-d', './dataLogs', 
    '-l', '', 
    '-m', 'volt'
    ]

CMD_LIST_PROCESS = "pgrep -af streaming-server"
CMD_LIST_PROCESS_SCPI = "pgrep -af scpi-server"