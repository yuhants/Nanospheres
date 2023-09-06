import numpy as np
import pyvisa
import time
import src.RIGOL_control.DG822.DG822_control as rig
import src.Tektronix_control.AFG1022.AFG1022_control as tek

"""
Charge calibration by applying a sinuisoidal E field 
at a fixed frequency through an arbitrary function generator.
Can send control sigla to the HV amplifier to moidfy the 
charge state

!!!!!!!!!!

TODO: need to add the bit that collects and analyses the data. 

!!!!!!!!!!
"""

### Variables 
HV   = False  # Trigger HV supply

# FREQ = 48000  # Driving frequency in Hz
# AMP  = 1
FREQ = 41000
AMP  = 20    # Peak-to-peak amplitude of the driving E field @ 1 mbar

VOLT = 1      # Voltage for triggering HV supply for needle. Value in kV.
              # There will be a minimum below which it will not ionise the air. 
              # I think this probably also maxes out around 1 kV as it can't supply more current.

### Don't change unless error with these values (e.g. does not connect)
### Can find out what the value should be using the following lines. You will have to figure out which resource is which instrument
rm = pyvisa.ResourceManager()
rm.list_resources()

_VISA_ADDRESS_rigol = "USB0::0x1AB1::0x0643::DG8A204201834::INSTR"
_VISA_ADDRESS_tektronix = "USB0::0x0699::0x0353::2238362::INSTR"

# Connect to function generator and apply sine wave
tek.sine_wave(_VISA_ADDRESS_tektronix, amplitude=AMP, frequency=FREQ)
tek.turn_on(_VISA_ADDRESS_tektronix)

# Initialise the function generator outputs
if HV:
    # Apply a *negative* impulse every five seconds
    # the signal is sent to the HV amplifier with a negavie polarity
    DG822 = rig.FuncGen(_VISA_ADDRESS_rigol)
    DG822.pulse(amp=VOLT, duty=98, freq=0.2, off=-VOLT/2)

    # Ouput signals
    DG822.turn_on()

    # Hold in loop until cancel - have 10 minute timeout
    i = 0
    while i < 260:
        try:
            time.sleep(1)
            i+=1
        except KeyboardInterrupt:
            break
    DG822.turn_off()
    print('HV switched off')

# Have the E field on for a while
i = 0
while i < 260:
    try:
        time.sleep(1)
        i+=1
    except KeyboardInterrupt:
        break

tek.turn_off(_VISA_ADDRESS_tektronix)
print('Program ends')