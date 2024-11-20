import numpy as np
import sys, os
sys.path.append(os.path.dirname(r'C:\Users\yuhan\nanospheres\control\src'))
import src.Tektronix_control.AFG1022.AFG1022_control as tek

import matplotlib.pyplot as plt
import time

#
# Last update
#
# At the moment `Trigger Inteval` (burst period) that defines the interval between
# pulses has to be manually set on AFG1022
# The current value is set to 300 ms, i.e., the pulses are at least 300 ms apart
#

_VISA_ADDRESS_tektronix = "USB0::0x0699::0x0353::2238362::INSTR"
# _VISA_ADDRESS_tektronix = 'USB0::0x0699::0x0353::2328304::INSTR'

AMPLIFIED = True

# Amplitude of impulse in V
AMP  = 50
OFFSET = 0.01

if AMPLIFIED:
    AMP = AMP / 20
    OFFSET1 = OFFSET / -20
    OFFSET2 = OFFSET / -20

else:
    OFFSET1 = OFFSET
    OFFSET2 = OFFSET

def impulse_on(visa_address, amp, offset_1, offset_2):
    tek.impulse(visa_address, amplitude=amp, offset=offset_1-amp/2, channel=1)
    tek.dc_offset(visa_address, offset=offset_2, channel=2)

    tek.turn_on(visa_address, channel=1)
    tek.turn_on(visa_address, channel=2)
    print(f'Impulse turned on, amplitude={amp:.1f} V')

def turn_off(visa_address):
    tek.turn_off(visa_address, channel=1)
    tek.turn_off(visa_address, channel=2)
    print('Output turned off')

def main():
    # Connect to function generator and transfer custom impulse
    # For some reason the transfer might fail at the first time - just run again
    impulse_on(_VISA_ADDRESS_tektronix, AMP, OFFSET1, OFFSET2)

    i = 0
    while i < 1000:
        try:
            time.sleep(1)
            i+=1
        except KeyboardInterrupt:
            break

    turn_off(_VISA_ADDRESS_tektronix)

if __name__=="__main__":
    main()
