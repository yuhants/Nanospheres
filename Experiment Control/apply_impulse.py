import numpy as np
import src.Tektronix_control.AFG1022.AFG1022_control as tek

import ctypes
from picosdk.ps4000a import ps4000a as ps
from picosdk.functions import adc2mV, assert_pico_ok
import matplotlib.pyplot as plt
import time

#
# At the moment `Trigger Inteval` (burst period) that defines the interval between
# pulses has to be manually set on AFG1022
# The current value is set to 300 ms, i.e., the pulses are at least 300 ms apart
#
# Picoscope data collection routine is modified from picoscope SDK example
# https://github.com/yuhants/picosdk-python-wrappers/blob/master/ps4000aExamples/ps4000aStreamingExample.py
#

_VISA_ADDRESS_tektronix = "USB0::0x0699::0x0353::2238362::INSTR"

AMPLIFIED = False
collect_data = False

# Amplitude of impulse in V
AMP  = 2
OFFSET = 0
# ndata = 5

if AMPLIFIED:
    AMP = AMP / 20
    OFFSET1 = OFFSET / -20
else:
    OFFSET1 = OFFSET
OFFSET2 = OFFSET

# Create chandle and status used by picoscope
chandle = ctypes.c_int16()
status = {}
# This is a global variable used by picoscope DAQ
nextSample = 0

def main():
    global channels

    # Connect to function generator and transfer custom impulse
    # For some reason the transfer will fail at the first time - just run again
    tek.impulse(_VISA_ADDRESS_tektronix, amplitude=AMP, offset=OFFSET1-AMP/2, channel=1)
    tek.dc_offset(_VISA_ADDRESS_tektronix, offset=OFFSET2, channel=2)
    # tek.sine_wave(_VISA_ADDRESS_tektronix, amplitude=1, frequency=20000)

    if collect_data:
        # channels = ['A', 'B', 'F', 'H']
        channels = ['C', 'F']

        # Collect 500 ms of data
        # Total length of data = `samp_interval` * `buffer_size`
        nbuffer = 1  # Number of buffer to capture
        buffer_size = 10000000
        samp_interval = 500
        time_units = 'PS4000A_NS'

        # Channel range go through in the order listed in Picoscope software
        # Options:
        # 0, 1, 2   - +- 10, 20, 50 mV
        # 3, 4, 5   - +- 100, 200, 500 mV
        # 6, 7, 8   - +- 1, 2, 5 V
        # 9, 10, 11 - +- 10, 20, 50 V
        channel_range = 10

        # Initialize picoscope, then turn on the impulse signal
        initialize_pico(ps, status)
        tek.turn_on(_VISA_ADDRESS_tektronix)

        # Capture data and then turn off
        # Time in specificed units, signal in mV
        tt, data = stream_data(ps, status, channels, channel_range, buffer_size, nbuffer, samp_interval, time_units)
        tek.turn_off(_VISA_ADDRESS_tektronix, channel=1)
        tek.turn_off(_VISA_ADDRESS_tektronix, channel=2)
        
        # Plot the data
        plt.plot(tt/1e6, data[0])
        plt.plot(tt/1e6, data[1])
        # plt.plot(tt/1e6, data[2])
        # plt.plot(tt/1e6, data[3])
        plt.xlabel('Time (ms)')
        plt.ylabel('Signal (mV)')
        plt.show()

        # Time in ms, data in mV
        return tt/1e6, data

    else:
        # Turn it on and leave it on until interruption
        tek.turn_on(_VISA_ADDRESS_tektronix, channel=1)
        tek.turn_on(_VISA_ADDRESS_tektronix, channel=2)

        i = 0
        while i < 260:
            try:
                time.sleep(1)
                i+=1
            except KeyboardInterrupt:
                break

        tek.turn_off(_VISA_ADDRESS_tektronix, channel=1)
        tek.turn_off(_VISA_ADDRESS_tektronix, channel=2)

    print('Program ends')

def initialize_pico(ps, status):
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

def set_up_channels_pico(ps, status, channels, channel_range=10, buffer_size=20000, nbuffer=1):
    enabled = 1
    disabled = 0
    analogue_offset = 0.0

    bufferMax = []
    for i, channel in enumerate(channels):
        bufferMax.append(set_channel(ps, status, channel, enabled, channel_range, analogue_offset, buffer_size, nbuffer))

    return bufferMax

def set_channel(ps, status, channel, enabled, channel_range, analogue_offset, buffer_size, nbuffer):
    status_prefix = 'setCh' + channel
    status_prefix_buff = 'setDataBuffers' + channel
    channel_prefix = 'PS4000A_CHANNEL_' + channel

    status[status_prefix] = ps.ps4000aSetChannel(chandle,
                                                 ps.PS4000A_CHANNEL[channel_prefix],
                                                 enabled,
                                                 ps.PS4000A_COUPLING['PS4000A_DC'],
                                                 channel_range,
                                                 analogue_offset)
    assert_pico_ok(status[status_prefix])

    # Size of capture 
    sizeOfOneBuffer = buffer_size
    numBuffersToCapture = nbuffer
    totalSamples = sizeOfOneBuffer * numBuffersToCapture
    
    # Create buffers ready for assigning pointers for data collection
    bufferMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)
    memory_segment = 0

    # Set data buffer location for data collection from channel
    status[status_prefix_buff] = ps.ps4000aSetDataBuffers(chandle,
                                                        ps.PS4000A_CHANNEL[channel_prefix],
                                                        bufferMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
                                                        None,
                                                        sizeOfOneBuffer,
                                                        memory_segment,
                                                        ps.PS4000A_RATIO_MODE['PS4000A_RATIO_MODE_NONE'])
    assert_pico_ok(status[status_prefix_buff])

    return bufferMax

def stream_data(ps, status, channels, channel_range, buffer_size, nbuffer, samp_interval, time_units):
    global nextSample

    bufferMax = set_up_channels_pico(ps, status, channels, channel_range, buffer_size, nbuffer)

    # Begin streaming mode:
    sampleInterval = ctypes.c_int32(samp_interval)
    sampleUnits = ps.PS4000A_TIME_UNITS[time_units]

    # Size of capture 
    sizeOfOneBuffer = buffer_size
    numBuffersToCapture = nbuffer
    totalSamples = sizeOfOneBuffer * numBuffersToCapture

    # We are not triggering:
    maxPreTriggerSamples = 0
    autoStopOn = 1

    # No downsampling:
    downsampleRatio = 1
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
    print("Capturing at sample interval %s ns" % actualSampleInterval)

    # Size of capture 
    sizeOfOneBuffer = buffer_size
    numBuffersToCapture = nbuffer
    totalSamples = sizeOfOneBuffer * numBuffersToCapture

    # Create a big buffer
    bufferComplete = np.zeros(shape=(len(channels), totalSamples), dtype=np.int16)
    autoStopOuter = False
    wasCalledBack = False

    def streaming_callback(handle, noOfSamples, startIndex, overflow, triggerAt, triggered, autoStop, param):
        global nextSample, autoStopOuter, wasCalledBack, channels

        wasCalledBack = True
        destEnd = nextSample + noOfSamples
        sourceEnd = startIndex + noOfSamples

        for i, channel in enumerate(channels):
            bufferComplete[i][nextSample:destEnd] = bufferMax[i][startIndex:sourceEnd]

        nextSample += noOfSamples
        if autoStop:
            autoStopOuter = True

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

    # Convert ADC counts data to mV
    data = np.empty_like(bufferComplete)
    for i in range(len(channels)):
        data[i] = adc2mV(bufferComplete[i], channel_range, maxADC)

    # Create time data
    tt = np.linspace(0, (totalSamples - 1) * actualSampleInterval, totalSamples)

    # Stop the scope
    # handle = chandle
    status["stop"] = ps.ps4000aStop(chandle)
    assert_pico_ok(status["stop"])

    # Disconnect the scope
    # handle = chandle
    status["close"] = ps.ps4000aCloseUnit(chandle)
    assert_pico_ok(status["close"])

    # Display status returns
    print(status)

    return tt, data

if __name__=="__main__":
    main()
