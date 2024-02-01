import numpy as np
import pyvisa
import src.Tektronix_control.AFG1022.AFG1022_control as tek

AMPLIFIED = True

FREQ = 103000
AMP  = 25    # Peak-to-peak amplitude of the driving E field
OFFSET = -10

if AMPLIFIED:
    OFFSET1 = OFFSET / -20
else:
    OFFSET1 = OFFSET
OFFSET2 = OFFSET

_VISA_ADDRESS_tektronix = "USB0::0x0699::0x0353::2238362::INSTR"

# Connect to function generator and apply sine wave
tek.dc_offset(_VISA_ADDRESS_tektronix, offset=OFFSET1, channel=1)
tek.dc_offset(_VISA_ADDRESS_tektronix, offset=OFFSET2, channel=2)
tek.turn_on(_VISA_ADDRESS_tektronix, channel=1)
tek.turn_on(_VISA_ADDRESS_tektronix, channel=2)

print('E field switched on\nNeed to manually turn off')