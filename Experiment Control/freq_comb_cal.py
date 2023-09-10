import numpy as np
import matplotlib.pyplot as plt

import src.Tektronix_control.AFG1022.AFG1022_control as tek
import time

_VISA_ADDRESS_tektronix = "USB0::0x0699::0x0353::2238362::INSTR"

# DO NOT change the `FREQ` parameter
# the comb timestream is generated assuming 100 Hz
# repetition rate

# CAUTION: too large amplitude will knock the sphere out
# 2V peak to peak knocks a sphere out at 1e-6 mbar
AMP  = 1
FREQ = 100
collect_data = False

freq_comb_file = r"C:\Users\microspheres\Documents\Python Scripts\Experiment Control\freq_comb_20khz_70khz.npz"

# Connect to function generator and apply custom impulse
tek.freq_comb(_VISA_ADDRESS_tektronix, file=freq_comb_file, amplitude=AMP, frequency=FREQ, offset=0, channel=1)
tek.turn_on(_VISA_ADDRESS_tektronix)

if collect_data:
    pass

i = 0
while i < 260:
    try:
        time.sleep(1)
        i+=1
    except KeyboardInterrupt:
        break

tek.turn_off(_VISA_ADDRESS_tektronix)
print('Program ends')