import numpy as np
import matplotlib.pyplot as plt

import src.Tektronix_control.AFG1022.AFG1022_control as tek
import time

_VISA_ADDRESS_tektronix = "USB0::0x0699::0x0353::2238362::INSTR"

AMPLIFIED = True
OFFSET = 0

# DO NOT change the `FREQ` parameter
AMP  = 60  # Intended peak-to-peak voltage *for each frequency applied*

FREQ = 100
collect_data = False

# The amplifier amplify the signal by -20
if AMPLIFIED:
    AMP = AMP / 20
    OFFSET1 = OFFSET / -20
else:
    OFFSET1 = OFFSET
OFFSET2 = OFFSET

drive_sig_file = r"C:\Users\yuhan\nanospheres\Experiment Control\drive_signal_charging_69khz1v_200khz5v.npz"

def norm_amp(amp, signal):
    """Normalized driving amplitude"""
    # AFG1022 automatically peak-normalized the input waveform
    return AMP * np.max(signal)

comb_data = np.load(drive_sig_file, allow_pickle=True)
signal = comb_data['sig']

AMP_NORM = norm_amp(AMP, signal)

# Connect to function generator and apply custom impulse
tek.freq_comb(_VISA_ADDRESS_tektronix, signal=signal, amplitude=AMP_NORM, frequency=FREQ, offset=OFFSET1, channel=1)
tek.dc_offset(_VISA_ADDRESS_tektronix, offset=OFFSET2, channel=2)
tek.turn_on(_VISA_ADDRESS_tektronix, channel=1)
tek.turn_on(_VISA_ADDRESS_tektronix, channel=2)
print('Drive signal switched on')

i = 0
while True:
    try:
        time.sleep(1)
        i+=1
    except KeyboardInterrupt:
        break

tek.turn_off(_VISA_ADDRESS_tektronix, channel=1)
tek.turn_off(_VISA_ADDRESS_tektronix, channel=2)
print('Drive signal switched off')
print('Program ends')
