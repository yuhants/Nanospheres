import numpy as np
import pyvisa
import src.Tektronix_control.AFG1022.AFG1022_control as tek

AMPLIFIED = True

FREQ = 103000
AMP  = 25    # Peak-to-peak amplitude of the driving E field

if AMPLIFIED:
    AMP = AMP / 20

_VISA_ADDRESS_tektronix = "USB0::0x0699::0x0353::2238362::INSTR"

# Connect to function generator and apply sine wave
tek.sine_wave(_VISA_ADDRESS_tektronix, amplitude=AMP, frequency=FREQ)
tek.turn_on(_VISA_ADDRESS_tektronix)
print('E field switched on\nNeed to manually turn off')