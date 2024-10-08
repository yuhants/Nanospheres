import numpy as np
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

AMPLIFIED = False

# Amplitude of impulse in V
AMP  = 9
OFFSET = 0.01

if AMPLIFIED:
    AMP = AMP / 20
    OFFSET1 = OFFSET / -20
else:
    OFFSET1 = OFFSET
OFFSET2 = OFFSET

def main():

    # Connect to function generator and transfer custom impulse
    # For some reason the transfer will fail at the first time - just run again
    tek.impulse(_VISA_ADDRESS_tektronix, amplitude=AMP, offset=OFFSET1-AMP/2, channel=1)
    # tek.impulse_afg1062(_VISA_ADDRESS_tektronix, amplitude=AMP, offset=OFFSET1-AMP/2, channel=1)
    tek.dc_offset(_VISA_ADDRESS_tektronix, offset=OFFSET2, channel=2)

    # Turn it on and leave it on until interruption
    tek.turn_on(_VISA_ADDRESS_tektronix, channel=1)
    if OFFSET2 != 0:
        tek.turn_on(_VISA_ADDRESS_tektronix, channel=2)

    i = 0
    while i < 1000:
        try:
            time.sleep(1)
            i+=1
        except KeyboardInterrupt:
            break

    tek.turn_off(_VISA_ADDRESS_tektronix, channel=1)
    if OFFSET2 != 0:
        tek.turn_off(_VISA_ADDRESS_tektronix, channel=2)

    print('Program ends')

if __name__=="__main__":
    main()
