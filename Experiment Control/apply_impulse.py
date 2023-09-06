import numpy as np
import src.Tektronix_control.AFG1022.AFG1022_control as tek

import ctypes
from picosdk.ps4000a import ps4000a as ps
from picosdk.functions import adc2mV, assert_pico_ok
import matplotlib.pyplot as plt
import time

_VISA_ADDRESS_tektronix = "USB0::0x0699::0x0353::2238362::INSTR"

AMP  = 1
FREQ = 20
collect_data = False

# Connect to function generator and apply custom impulse
tek.impulse(_VISA_ADDRESS_tektronix, amplitude=AMP, frequency=FREQ, offset=AMP/2, channel=1)
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

def take_data_pico():
    pass
        # buffer_size = 400
    # nbuffer = 1
    # samp_interval = 1  # Sampling interval in us

    # ## Ask the picoscope to collect 20 ms of data
    # ##
    # # Below modified from picoscope SDK example
    # # https://github.com/yuhants/picosdk-python-wrappers/blob/master/ps4000aExamples/ps4000aStreamingExample.py

    # # Create chandle and status ready for use
    # chandle = ctypes.c_int16()
    # status = {}

    # # Returns handle to chandle for use in future API functions
    # status["openunit"] = ps.ps4000aOpenUnit(ctypes.byref(chandle), None)

    # try:
    #     assert_pico_ok(status["openunit"])
    # except:
    #     powerStatus = status["openunit"]

    #     if powerStatus == 286:
    #         status["changePowerSource"] = ps.ps4000aChangePowerSource(chandle, powerStatus)
    #     else:
    #         raise

    #     assert_pico_ok(status["changePowerSource"])

    # # Set up channel A, B, F, H
    # enabled = 1
    # disabled = 0
    # analogue_offset = 0.0
    # channel_range = 10

    # status["setChA"] = ps.ps4000aSetChannel(chandle,
    #                                         ps.PS4000A_CHANNEL['PS4000A_CHANNEL_A'],
    #                                         enabled,
    #                                         ps.PS4000A_COUPLING['PS4000A_DC'],
    #                                         channel_range,
    #                                         analogue_offset)
    # assert_pico_ok(status["setChA"])

    # status["setChB"] = ps.ps4000aSetChannel(chandle,
    #                                         ps.PS4000A_CHANNEL['PS4000A_CHANNEL_B'],
    #                                         enabled,
    #                                         ps.PS4000A_COUPLING['PS4000A_DC'],
    #                                         channel_range,
    #                                         analogue_offset)
    # assert_pico_ok(status["setChB"])

    # status["setChF"] = ps.ps4000aSetChannel(chandle,
    #                                         ps.PS4000A_CHANNEL['PS4000A_CHANNEL_F'],
    #                                         enabled,
    #                                         ps.PS4000A_COUPLING['PS4000A_DC'],
    #                                         channel_range,
    #                                         analogue_offset)
    # assert_pico_ok(status["setChF"])

    # status["setChG"] = ps.ps4000aSetChannel(chandle,
    #                                         ps.PS4000A_CHANNEL['PS4000A_CHANNEL_G'],
    #                                         enabled,
    #                                         ps.PS4000A_COUPLING['PS4000A_DC'],
    #                                         channel_range,
    #                                         analogue_offset)
    # assert_pico_ok(status["setChG"])

    # # Size of capture 
    # sizeOfOneBuffer = buffer_size
    # numBuffersToCapture = nbuffer

    # totalSamples = sizeOfOneBuffer * numBuffersToCapture

    # # Create buffers ready for assigning pointers for data collection
    # # Create buffers ready for assigning pointers for data collection
    # bufferAMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)
    # bufferBMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)
    # bufferFMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)
    # bufferGMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)

    # memory_segment = 0

    # # Set data buffer location for data collection from channel A, B, F, G
    # status["setDataBuffersA"] = ps.ps4000aSetDataBuffers(chandle,
    #                                                      ps.PS4000A_CHANNEL['PS4000A_CHANNEL_A'],
    #                                                      bufferAMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
    #                                                      None,
    #                                                      sizeOfOneBuffer,
    #                                                      memory_segment,
    #                                                      ps.PS4000A_RATIO_MODE['PS4000A_RATIO_MODE_NONE'])
    # assert_pico_ok(status["setDataBuffersA"])

    # status["setDataBuffersB"] = ps.ps4000aSetDataBuffers(chandle,
    #                                                      ps.PS4000A_CHANNEL['PS4000A_CHANNEL_B'],
    #                                                      bufferBMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
    #                                                      None,
    #                                                      sizeOfOneBuffer,
    #                                                      memory_segment,
    #                                                      ps.PS4000A_RATIO_MODE['PS4000A_RATIO_MODE_NONE'])
    # assert_pico_ok(status["setDataBuffersB"])

    # status["setDataBuffersF"] = ps.ps4000aSetDataBuffers(chandle,
    #                                                      ps.PS4000A_CHANNEL['PS4000A_CHANNEL_F'],
    #                                                      bufferAMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
    #                                                      None,
    #                                                      sizeOfOneBuffer,
    #                                                      memory_segment,
    #                                                      ps.PS4000A_RATIO_MODE['PS4000A_RATIO_MODE_NONE'])
    # assert_pico_ok(status["setDataBuffersF"])

    # status["setDataBuffersG"] = ps.ps4000aSetDataBuffers(chandle,
    #                                                      ps.PS4000A_CHANNEL['PS4000A_CHANNEL_G'],
    #                                                      bufferBMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
    #                                                      None,
    #                                                      sizeOfOneBuffer,
    #                                                      memory_segment,
    #                                                      ps.PS4000A_RATIO_MODE['PS4000A_RATIO_MODE_NONE'])
    # assert_pico_ok(status["setDataBuffersG"])

    # # Begin streaming mode:
    # sampleInterval = ctypes.c_int32(samp_interval)
    # sampleUnits = ps.PS4000A_TIME_UNITS['PS4000A_US']

    # # We are not triggering:
    # maxPreTriggerSamples = 0
    # autoStopOn = 1
    # # No downsampling:
    # downsampleRatio = 1
    # status["runStreaming"] = ps.ps4000aRunStreaming(chandle,
    #                                                 ctypes.byref(sampleInterval),
    #                                                 sampleUnits,
    #                                                 maxPreTriggerSamples,
    #                                                 totalSamples,
    #                                                 autoStopOn,
    #                                                 downsampleRatio,
    #                                                 ps.PS4000A_RATIO_MODE['PS4000A_RATIO_MODE_NONE'],
    #                                                 sizeOfOneBuffer)
    # assert_pico_ok(status["runStreaming"])

    # actualSampleInterval = sampleInterval.value
    # print("Capturing at sample interval %s us" % actualSampleInterval)

    # # We need a big buffer, not registered with the driver, to keep our complete capture in.
    # bufferCompleteA = np.zeros(shape=totalSamples, dtype=np.int16)
    # bufferCompleteB = np.zeros(shape=totalSamples, dtype=np.int16)
    # bufferCompleteF = np.zeros(shape=totalSamples, dtype=np.int16)
    # bufferCompleteG = np.zeros(shape=totalSamples, dtype=np.int16)
    # nextSample = 0
    # autoStopOuter = False
    # wasCalledBack = False

    # def streaming_callback(handle, noOfSamples, startIndex, overflow, triggerAt, triggered, autoStop, param):
    #     global nextSample, autoStopOuter, wasCalledBack
    #     wasCalledBack = True
    #     destEnd = nextSample + noOfSamples
    #     sourceEnd = startIndex + noOfSamples
    #     bufferCompleteA[nextSample:destEnd] = bufferAMax[startIndex:sourceEnd]
    #     bufferCompleteB[nextSample:destEnd] = bufferBMax[startIndex:sourceEnd]
    #     bufferCompleteF[nextSample:destEnd] = bufferFMax[startIndex:sourceEnd]
    #     bufferCompleteG[nextSample:destEnd] = bufferGMax[startIndex:sourceEnd]
    #     nextSample += noOfSamples
    #     if autoStop:
    #         autoStopOuter = True

    # # Convert the python function into a C function pointer.
    # cFuncPtr = ps.StreamingReadyType(streaming_callback)

    # # Fetch data from the driver in a loop, copying it out of the registered buffers and into our complete one.
    # while nextSample < totalSamples and not autoStopOuter:
    #     wasCalledBack = False
    #     status["getStreamingLastestValues"] = ps.ps4000aGetStreamingLatestValues(chandle, cFuncPtr, None)
    #     if not wasCalledBack:
    #         # If we weren't called back by the driver, this means no data is ready. Sleep for a short while before trying
    #         # again.
    #         time.sleep(0.01)
    # print("Done grabbing values.")

    # # Find maximum ADC count value
    # maxADC = ctypes.c_int16()
    # status["maximumValue"] = ps.ps4000aMaximumValue(chandle, ctypes.byref(maxADC))
    # assert_pico_ok(status["maximumValue"])

    # # Convert ADC counts data to mV
    # adc2mVChAMax = adc2mV(bufferCompleteA, channel_range, maxADC)
    # adc2mVChBMax = adc2mV(bufferCompleteB, channel_range, maxADC)
    # adc2mVChFMax = adc2mV(bufferCompleteF, channel_range, maxADC)
    # adc2mVChGMax = adc2mV(bufferCompleteG, channel_range, maxADC)

    # # Create time data
    # time = np.linspace(0, (totalSamples - 1) * actualSampleInterval, totalSamples) / 1000

    # # Plot data from channel A and B
    # plt.plot(time, adc2mVChAMax[:])
    # plt.plot(time, adc2mVChBMax[:])
    # # plt.plot(time, adc2mVChFMax[:])
    # # plt.plot(time, adc2mVChGMax[:])
    # plt.xlabel('Time (ms)')
    # plt.ylabel('Voltage (mV)')
    # plt.show()

    # # Stop the scope
    # # handle = chandle
    # status["stop"] = ps.ps4000aStop(chandle)
    # assert_pico_ok(status["stop"])

    # # Disconnect the scope
    # # handle = chandle
    # status["close"] = ps.ps4000aCloseUnit(chandle)
    # assert_pico_ok(status["close"])

    # # Display status returns
    # print(status)