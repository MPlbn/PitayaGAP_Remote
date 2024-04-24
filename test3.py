#!/usr/bin/env python3
import redpitaya_scpi as scpi

rp_s = scpi.scpi('rp-f0ba38.local')

rp_s.tx_txt('OUTPUT1:STATE OFF')