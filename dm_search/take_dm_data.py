"""
This code performs impulse calibration by applying
impulses of various different ampitudes
"""

import sys, os
sys.path.append(os.path.dirname(r'C:\Users\yuhan\nanospheres\control'))
sys.path.append(os.path.dirname(r'C:\Users\yuhan\nanospheres\daq'))

import numpy as np
from control.apply_impulse import impulse_on, turn_off
from daq.take_data_pico_stream import *
import matplotlib.pyplot as plt

# Monitoring E field (TODO)
_VISA_ADDRESS_tektronix = "USB0::0x0699::0x0353::2238362::INSTR"
amp, freq = 2, 89000
offset_1, offset_2 = 0.01, 0.01

# Picoscope DAQ
serial_0 = ctypes.create_string_buffer(b'JO279/0118')  # Picoscope on cloud
serial_1 = ctypes.create_string_buffer(b'JY140/0294')

# Digitization range (0-11): 10, 20, 50, 100, 200, 500 (mV), 1, 2, 5, 10, 20, 50 (V)
channels = ['E']
channel_ranges = np.array([6])
channel_couplings = ['DC']

# channels = ['D', 'E', 'F']
# channel_ranges = np.array([6, 6, 0])
# channel_couplings = ['DC', 'DC', 'DC']
analog_offsets = None

# Need to sample fast enough to capture the pulses
# here 30 million samples is 6 seconds
n_buffer = 1  # Number of buffer to capture
buffer_size = int(1e6)

sample_interval = 2
sample_units = 'PS4000A_US'

global nextSample, wasCalledBack, autoStopOuter, one_buffer, total_buffer

file_directory = r"E:\dm_data\20241025_10e_long"
file_prefix = '20241025_def_10e'
n_file = 1

def main():
    if not os.path.isdir(file_directory):
        os.mkdir(file_directory)

    chandle, status = set_up_pico(serial_1, channels, channel_ranges, channel_couplings, analog_offsets,
                                  buffer_size, sample_interval, sample_units)

    # Data taking
    for i in range(n_file):
        file_name = rf'{file_prefix}_{i+1}.hdf5'
        timestamp, dt, adc2mvs, data = stream_data(chandle, status, sample_interval, sample_units, channel_ranges, buffer_size, n_buffer)

        with h5py.File(os.path.join(file_directory, file_name), 'w') as f:
            print(f'Writing file {file_name}')

            g = f.create_group('data')
            g.attrs['timestamp'] = timestamp
            g.attrs['delta_t'] = dt * time_dict[sample_units]
            for i, channel in enumerate(channels):
                dataset = g.create_dataset(f'channel_{channel.lower()}', data=data[i], dtype=np.int16)
                dataset.attrs['adc2mv'] = adc2mvs[i]
            f.close()

    stop_and_disconnect(chandle, status)

if __name__=="__main__":
    main()