import numpy as np
import matplotlib.pyplot as plt

import ctypes
from picosdk.ps4000a import ps4000a as ps
from picosdk.functions import adc2mV, assert_pico_ok
import time

import h5py

# Data collection settings
channels = ['D', 'E']
# Digitization range (0-11): 10, 20, 50, 100, 200, 500 (mV), 1, 2, 5, 10, 20, 50 (V)
channel_ranges = [6, 7]
analog_offsets = None

# Total length of data = `sample_interval`*`buffer_size`*`n_buffer`
n_buffer = 1  # Number of buffer to capture
buffer_size = int(1e7)

sample_interval = 400
sample_units = 'PS4000A_NS'

# Variables
enabled = 1
disabled = 0
channel_dict = {'A':0, 'B':1, 'C':2, 'D':3, 'E':4, 'F':5, 'G':6, 'H':7}
time_dict = {'PS4000A_NS':1e-9, 'PS4000A_US':1e-6, 'PS4000A_MS':1e-3}

# Other global variables used for streaming
nextSample = 0
wasCalledBack = False
autoStopOuter = False
one_buffer = None
total_buffer = None

def main():
    # Create chandle and status
    chandle = ctypes.c_int16()
    status = {}

    # Initialize picoscope
    initialize_pico(chandle, status)
    set_channels_pico(chandle, status, channels, channel_ranges, analog_offsets)

    # Create buffer that stores the data
    set_data_buffers(chandle, status, channels, buffer_size)

    # Start streaming
    for i in range(3):
        dt, data = stream_data(chandle, status, sample_interval, sample_units, channel_ranges, buffer_size, n_buffer)

        file_name = rf'D:\h5test_{i}.hdf5'
        with h5py.File(file_name, 'w') as f:
            print(f'Saving file {file_name}')

            dd = f.create_dataset('channel_d', data=data[0], dtype='f')
            ee = f.create_dataset('channel_e', data=data[1], dtype='f')

            for dataset in [dd, ee]:
                dataset.attrs['delta_t'] = dt*time_dict[sample_units]

            f.close()

        # tt = np.arange(start=0, stop=dt*data.shape[1], step=dt*time_dict[sample_units])
        # plt.plot(tt, data[0])
        # plt.plot(tt, data[1])
        # plt.xlabel('Time (us)')
        # plt.ylabel('Signal (mV)')
        # plt.show()

    # # Time in ms, data in mV
    # return tt/1e6, data
    stop_and_disconnect(chandle, status)

# Functions
def initialize_pico(chandle, status):
    # Returns handle to chandle for use in future API functions
    status["openunit"] = ps.ps4000aOpenUnit(ctypes.byref(chandle), None)
    try:
        assert_pico_ok(status["openunit"])
    except:
        powerStatus = status["openunit"]
        if powerStatus == 286:
            status["changePowerSource"] = ps.ps4000aChangePowerSource(chandle, powerStatus)
        else:
            raise
        assert_pico_ok(status["changePowerSource"])

def set_channels_pico(chandle, status, channels, channel_ranges, analog_offsets):
    if analog_offsets is None:
        analog_offsets = [0.0] * len(channels)
    for i, channel in enumerate(channels):
        set_channel(chandle, status, channel, channel_ranges[i], analog_offsets[i])

def set_channel(chandle, status, channel, channel_range, analog_offset):
    status_prefix = 'setCh' + channel
    # There is a but for Channel E in picoscope sdk so manually find the number
    channel_num = channel_dict[channel]

    status[status_prefix] = ps.ps4000aSetChannel(chandle,
                                                #  ps.PS4000A_CHANNEL[channel_prefix],
                                                 channel_num,
                                                 enabled,
                                                 ps.PS4000A_COUPLING['PS4000A_DC'],
                                                 channel_range,
                                                 analog_offset)
    assert_pico_ok(status[status_prefix])

def set_data_buffers(chandle, status, channels, buffer_size):
    global one_buffer

    sizeOfOneBuffer = buffer_size
    memory_segment = 0

    # Create buffers ready for assigning pointers for data collection
    one_buffer = np.zeros(shape=(len(channels), buffer_size), dtype=np.int16)

    for i, channel in enumerate(channels):
        status_prefix_buff = f'setDataBuffers{channel}'
        channel_num = channel_dict[channel]

        status[status_prefix_buff] = ps.ps4000aSetDataBuffers(chandle,
                                                              channel_num,
                                                              one_buffer[i].ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
                                                              None,
                                                              sizeOfOneBuffer,
                                                              memory_segment,
                                                              ps.PS4000A_RATIO_MODE['PS4000A_RATIO_MODE_NONE'])
        assert_pico_ok(status[status_prefix_buff])
    return one_buffer

def stream_data(chandle, status, sample_interval, sample_units, channel_ranges, buffer_size, n_buffer):
    global nextSample, wasCalledBack, autoStopOuter, total_buffer

    sizeOfOneBuffer = buffer_size
    numBuffersToCapture = n_buffer
    totalSamples = sizeOfOneBuffer * numBuffersToCapture
    total_buffer = np.zeros(shape=(len(channel_ranges), totalSamples), dtype=np.int16)

    sampleInterval = ctypes.c_int32(sample_interval)
    sampleUnits = ps.PS4000A_TIME_UNITS[sample_units]

    # We are not triggering:
    maxPreTriggerSamples = 0
    autoStopOn = 1
    # No downsampling:
    downsampleRatio = 1

    nextSample = 0
    status["runStreaming"] = ps.ps4000aRunStreaming(chandle,
                                                    ctypes.byref(sampleInterval),
                                                    sampleUnits,
                                                    maxPreTriggerSamples,
                                                    totalSamples,
                                                    autoStopOn,
                                                    downsampleRatio,
                                                    ps.PS4000A_RATIO_MODE['PS4000A_RATIO_MODE_NONE'],
                                                    sizeOfOneBuffer)
    
    assert_pico_ok(status["runStreaming"])

    actualSampleInterval = sampleInterval.value
    print(f"Capturing at sample interval {actualSampleInterval} {sample_units}")

    autoStopOuter = False
    wasCalledBack = False

    # Convert the python function into a C function pointer.
    cFuncPtr = ps.StreamingReadyType(streaming_callback)

    # Fetch data from the driver in a loop, copying it out of the registered buffers and into our complete one.
    while nextSample < totalSamples and not autoStopOuter:
        wasCalledBack = False
        status["getStreamingLastestValues"] = ps.ps4000aGetStreamingLatestValues(chandle, cFuncPtr, None)
        if not wasCalledBack:
            # If we weren't called back by the driver, this means no data is ready. Sleep for a short while before trying
            # again.
            time.sleep(0.01)
    print("Done grabbing values.")

    # Find maximum ADC count value
    maxADC = ctypes.c_int16()
    status["maximumValue"] = ps.ps4000aMaximumValue(chandle, ctypes.byref(maxADC))
    assert_pico_ok(status["maximumValue"])

    # Convert ADC counts data to physical values
    data = np.empty_like(total_buffer)
    for i in range(len(channels)):
        data[i] = adc2mV(total_buffer[i], channel_ranges[i], maxADC)

    return actualSampleInterval, data

def streaming_callback(handle, noOfSamples, startIndex, overflow, triggerAt, triggered, autoStop, param):
    global nextSample, autoStopOuter, wasCalledBack, total_buffer, one_buffer

    # print(f'nextSample: {nextSample}')
    # print(f'noOfSamples: {noOfSamples}')

    wasCalledBack = True
    destEnd = nextSample + noOfSamples
    sourceEnd = startIndex + noOfSamples

    for i, channel in enumerate(channels):
        total_buffer[i][nextSample:destEnd] = one_buffer[i][startIndex:sourceEnd]

    nextSample += noOfSamples
    if autoStop:
        autoStopOuter = True

def stop_and_disconnect(chandle, status):
    # Stop the scope
    # handle = chandle
    status["stop"] = ps.ps4000aStop(chandle)
    assert_pico_ok(status["stop"])

    # Disconnect the scope
    # handle = chandle
    status["close"] = ps.ps4000aCloseUnit(chandle)
    assert_pico_ok(status["close"])

if __name__=="__main__":
    main()
