#   Prints out all available scpi commands

from constants import *
import redpitaya_scpi as scpi

RP_S = scpi.scpi(RED_PITAYA_IP)

RP_S.tx_txt('SYSTem:Help?')
text = RP_S.rx_txt()
print(text)