import numpy as np
import matplotlib.pyplot as plt

import src.Tektronix_control.AFG1022.AFG1022_control as tek
import time

_VISA_ADDRESS_tektronix = "USB0::0x0699::0x0353::2238362::INSTR"

AMPLIFIED = True
OFFSET = 0

# DO NOT change the `FREQ` parameter
# the comb timestream is generated assuming 100 Hz repetition rate
# CAUTION: too large amplitude will knock the sphere out
AMP  = 25  # Intended peak-to-peak voltage *for each frequency applied*
# AMP = 10

FREQ = 100
collect_data = False

# The amplifier amplify the signal by -20
if AMPLIFIED:
    AMP = AMP / 20
    OFFSET1 = OFFSET / -20
else:
    OFFSET1 = OFFSET
OFFSET2 = OFFSET

# freq_comb_file = r"C:\Users\microspheres\Documents\Python Scripts\Experiment Control\freq_comb_20khz_70khz_deltaf5khz.npz"
freq_comb_file = r"C:\Users\yuhan\nanospheres\Experiment Control\freq_comb_10khz_60khz_deltaf2khz.npz"

def norm_amp(amp, signal):
    """Normalized driving amplitude"""
    # AFG1022 automatically peak-normalized the input waveform
    return AMP * np.max(signal)

comb_data = np.load(freq_comb_file, allow_pickle=True)
signal = comb_data['sig']

AMP_NORM = norm_amp(AMP, signal)

# Connect to function generator and apply custom impulse
tek.freq_comb(_VISA_ADDRESS_tektronix, signal=signal, amplitude=AMP_NORM, frequency=FREQ, offset=OFFSET1, channel=1)
#tek.dc_offset(_VISA_ADDRESS_tektronix, offset=OFFSET2, channel=2)
tek.turn_on(_VISA_ADDRESS_tektronix, channel=1)
#tek.turn_on(_VISA_ADDRESS_tektronix, channel=2)
print('Frequency comb switched on')

if collect_data:
    pass

i = 0
while i < 260:
    try:
        time.sleep(1)
        i+=1
    except KeyboardInterrupt:
        break

tek.turn_off(_VISA_ADDRESS_tektronix, channel=1)
tek.turn_off(_VISA_ADDRESS_tektronix, channel=2)
print('Frequency comb switched off')
print('Program ends')
