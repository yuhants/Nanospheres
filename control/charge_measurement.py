import numpy as np
import pyvisa
import time
import src.RIGOL_control.DG822.DG822_control as rig
import src.Tektronix_control.AFG1022.AFG1022_control as tek

# from PicoControl.take_data_pico import initialize_pico, stream_data

"""
Charge calibration by applying a sinuisoidal E field at a fixed
frequency through the arbitrary function generator.
Optionally send control signal to the HV amplifier to moidfy the 
charge state

!!!!!!!!!!

TODO: need to add the bit that collects and analyses the data. 

!!!!!!!!!!
"""

### Variables
AMPLIFIED = True
HV   = False
collect_data = False

# DC bias in V
# OFFSET1 = 0
# OFFSET2 = 0
# OFFSET1 = 60
# OFFSET2 = 60
OFFSET1 = -40
OFFSET2 = -40

AMP  = 100    # Peak-to-peak amplitude of the driving E field @ 1 mbar
FREQ = 81000 # Driving frequency in Hz

# ## Values at low pressure
# AMP  = 5
# FREQ = 97000


if AMPLIFIED:
    AMP = AMP / 20
    OFFSET1 = OFFSET1 / -20
    OFFSET2 = OFFSET2 / -20
else:
    OFFSET1 = OFFSET1
    OFFSET2 = OFFSET2


VOLT = 1.05      # Voltage for triggering HV supply for needle. Value in kV.
              # There will be a minimum below which it will not ionise the air. 
              # I think this probably also maxes out around 1 kV as it can't supply more current.
FREQ_PULSE = 0.2

### Don't change unless error with these values (e.g. does not connect)
### Can find out what the value should be using the following lines. You will have to figure out which resource is which instrument
# rm = pyvisa.ResourceManager()
# rm.list_resources()

_VISA_ADDRESS_rigol = "USB0::0x1AB1::0x0643::DG8A204201834::INSTR"
_VISA_ADDRESS_tektronix = "USB0::0x0699::0x0353::2238362::INSTR"

if collect_data:
    pass

# Connect to function generator and apply sine wave
tek.sine_wave(_VISA_ADDRESS_tektronix, amplitude=AMP, frequency=FREQ, offset=OFFSET1, channel=1)
tek.turn_on(_VISA_ADDRESS_tektronix, channel=1)
if OFFSET2 != 0:
    tek.dc_offset(_VISA_ADDRESS_tektronix, offset=OFFSET2, channel=2)
    tek.turn_on(_VISA_ADDRESS_tektronix, channel=2)
print('E field switched on')

## Tom likes to keep the E field on for a while
# i = 0
# while i < 10:
#     try:
#         time.sleep(1)
#         i+=1
#     except KeyboardInterrupt:
#         break

# Initialise the function generator outputs
if HV:
    # Apply a *negative* impulse every five seconds
    # the signal is sent to the HV amplifier with a negative polarity
    DG822 = rig.FuncGen(_VISA_ADDRESS_rigol)
    DG822.pulse(amp=VOLT, duty=95, freq=FREQ_PULSE, off=-VOLT/2)
    # DG822.pulse(amp=VOLT, duty=50, freq=FREQ_PULSE, off=-VOLT/2)

    # Hold off 10 second before turning on HV so the lock in 
    # could settle
    i = 0
    while i < 10:
        time.sleep(1)
        i+=1

    # Ouput signals
    DG822.turn_on()
    print('HV triggered')

    # Hold in loop until cancel - have 10 minute timeout
    i = 0
    while i < 200:
        try:
            time.sleep(1)
            i+=1
        except KeyboardInterrupt:
            break
    DG822.turn_off()
    print('HV switched off')

# Have the E field on for a while
i = 0
while True:
    try:
        time.sleep(1)
        i+=1
    except KeyboardInterrupt:
        break

tek.turn_off(_VISA_ADDRESS_tektronix, channel=1)
if OFFSET2 != 0:
    tek.turn_off(_VISA_ADDRESS_tektronix, channel=2)
print('E field switched off')
print('Program ends')