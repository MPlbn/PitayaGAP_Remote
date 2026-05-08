# Installation Guide
Please follow the guide to correctly setup redpitaya generator + acquisitor program.
## Versions that the program was developed on
- Pitaya OS: 2.07-3afd5c148
- Python: 3.12.3
## 1. Preparing the client side
1. Clone the repository from the main branch.
2. Create additional folders if missing to keep the structure. Make sure that the newly created folders are named correctly. If the streaming_app folder is missing or empty please follow this guide to get all the needed elements: [Redpitaya remote streaming command line tool](https://redpitaya.readthedocs.io/en/latest/appsFeatures/applications/streaming/usage/stream_command_line.html).
```
PitayaGAP_Remote/
├── dataLogs
├── onPit/
│   └── src
├── saved_csv_datalogs
├── streaming_app/
│   ├── configs
│   ├── python_lib
│   └── streaming_api
└── styles
```
3. All needed python packages are located in requirements.txt
## 2. Preparing Redpitaya
1. Connect to redpitaya via ssh.
2. `cd Redpitaya/`
3. `mkdir gen-acq-server`
4. Now transfer the insides of `PitayaGAP_Remote/onPit/` folder into the `~/Redpitaya/gen-acq-server`. 
Example: `scp -r ./PitayaGAP_Remote/onPit/. root@xxx.xxx.xx.xxx:~/RedPitaya/gen-acq-server/`
Structure of the `gen-acq-server` folder should look like that:
```
gen-acq-server/
├── Makefile
└── src/
    ├── generate.cpp
    ├── generate.h
    ├── pitaya_gen_acq_server.cpp
    ├── serverUtils.cpp
    └── serverUtils.h
```
5. On Redpitaya go inside `Redpitaya/gen-acq-server` 
Then: `make`
6. Wait till the compilation finishes
## 3. Running the program
To start the program simply run the `run.py` file. When opening the program please make sure that the redpitaya IP is correctly set - if it's different than the default one, change it then press the SET button.
# Problems
### Rarely there could be an issue connecting to pitaya through Continuous Generator mode due to some redpitaya connection problems or if the program was closed abruptly mid-operation. If it happens please try the following steps.
1. Check if the IP that You provide is a correct one - You can easily verify it by trying to connect via ssh.
2. If the IP is correct and it still doesn't connect try waiting a little bit then pressing the Continuous Generator button again. Sometimes connectivity issues appear when the program is closed, then quickly reopened and redpitaya doesn't close the server quickly enough. This can end in TCP socket being blocked.
3. If both of those options don't fix the problem, please connect to the pitaya via ssh, then `pgrep -af custom_server`. If anything shows up, then redpitaya had trouble closing the custom_server process - most likely caused by abrupt closing of the program. Kill all the processes that are shown.
4. If the problem is still there, then there must be some issue with redpitaya itself. Try restarting the device.

### In case the Continuous Generator mode is laggy or unresponsive after start.
1. Try changing the loop time value to bigger one. If it's set too low it may cause unresposiveness if the client hardware cannot handle the computation quickly enough.
