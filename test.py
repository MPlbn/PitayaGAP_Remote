#!/usr/bin/env python3

import sys
import time
import redpitaya_scpi as scpi

#constants
IP = 'rp-f0ba38.local'
rp_s = scpi.scpi(IP)



#closing scpi connection
rp_s.close()
