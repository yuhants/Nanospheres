# -*- coding: utf-8 -*-
"""
Created on Fri May  5 16:18:52 2023

@author: microspheres
"""

  #
# Copyright (C) 2018-2019 Pico Technology Ltd. See LICENSE file for terms.
#

import ctypes
import numpy as np
from picosdk.ps4000a import ps4000a as ps
import matplotlib.pyplot as plt
from picosdk.functions import assert_pico_ok 
import time
from datetime import datetime
import scipy
#import scipy.io as sio
from scipy.signal import butter, lfilter
from PIL import Image, ImageTk
import tkinter as tk 
import cv2
'''
###############################################################################

num = 10    #this sets the number of iterations (in time intervals) we want to run the program

buff_size = 10**6     #this * num_buffs sets the number of samples to capture

num_buffs = 1         #this sets the number of buffers to capture

sample_int  = 1       #this sets the time interval (in seconds)

#to work out samples/second take buff_size*num_buffs/sample_int
'''

def butter_lowpass(highcut, fs, order=5):

    nyq = 0.5 * fs
    high = highcut / nyq
    b, a = butter(order, high, btype='lowpass')
    return b, a

def butter_lowpass_filter(data, highcut, fs, order=5):

    b, a = butter_lowpass(highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def butter_highpass(lowcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    b, a = butter(order, low, btype='highpass')
    return b, a

def butter_highpass_filter(data, lowcut, fs, order=5):
    b, a = butter_highpass(lowcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def charge_from_tt2(signal, drive, centre_freq):
    filt = butter_lowpass_filter(signal, centre_freq+3000, fs = 10**6, order=5)
    filtfilt = butter_highpass_filter(filt, centre_freq-3000, fs = 10**6, order=5)
    fftsig = scipy.fft.rfft(filtfilt)
    fftdrive = scipy.fft.rfft(drive)
    corr = fftsig*np.conjugate(fftdrive)
    charge = abs(max(corr, key = abs))
    return charge

def TT2Plot():
    
    window = tk.Tk
    file_name = 'D:\Python\\' + str(datetime.now().strftime('%d-%m-%y'))+'.jpeg'
    img = ImageTk.PhotoImage(Image.open(file_name))
    lbl = tk.Label(window, image=img).pack()
    
    window.mainloop()

def get_charge(num_tt2, buff_size_tt2, num_buffs_tt2, sample_int_tt2):
    #user-defined functions that allow us to observe the offset between two signal amplitudes
    

    ###############################################################################

    # Create chandle and status ready for use
    chandle = ctypes.c_int16()
    status = {}

    # Open PicoScope 2000 Series device
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


    enabled = 1
    disabled = 0
    analogue_offset = 0.0

    # Set up channel A
    # handle = chandle
    # channel = PS4000A_CHANNEL_A = 0
    # enabled = 1
    # coupling type = PS4000A_DC = 1
    # range = PS4000A_2V = 7
    # analogue offset = 0 V
    channel_range = 7
    status["setChA"] = ps.ps4000aSetChannel(chandle,
                                        ps.PS4000A_CHANNEL['PS4000A_CHANNEL_A'],
                                        enabled,
                                        ps.PS4000A_COUPLING['PS4000A_DC'],
                                        channel_range,
                                        analogue_offset)
    assert_pico_ok(status["setChA"])

    # Set up channel B
    # handle = chandle
    # channel = PS4000A_CHANNEL_B = 1
    # enabled = 1
    # coupling type = PS4000A_DC = 1
    # range = PS4000A_2V = 7
    # analogue offset = 0 V
    status["setChB"] = ps.ps4000aSetChannel(chandle,
                                        ps.PS4000A_CHANNEL['PS4000A_CHANNEL_B'],
                                        enabled,
                                        ps.PS4000A_COUPLING['PS4000A_DC'],
                                        channel_range,
                                        analogue_offset)
    assert_pico_ok(status["setChB"])
    timing = datetime.now() #gives timestamp in seconds to the readouts

    ###############################################################################
    #Collects 1 second worth of data from 2 channels, plots the output of the chargett2 function, 
    #and then starts over for the specified number of iterations
    start_time = time.time()
    while num_tt2 > 0: #sets up the while loop
    
    ###############################################################################        
    # Size of capture
        sizeOfOneBuffer = buff_size_tt2    #increasing buffer size is more efficient than increasing number of buffers
        numBuffersToCapture = num_buffs_tt2

        totalSamples = sizeOfOneBuffer * numBuffersToCapture   #we want 10**6 samples/sample interval

    # Create buffers ready for assigning pointers for data collection
        bufferAMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)
        bufferBMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)

        memory_segment = 0

    # Set data buffer location for data collection from channel A
    # handle = chandle
    # source = PS4000A_CHANNEL_A = 0
    # pointer to buffer max = ctypes.byref(bufferAMax)
    # pointer to buffer min = ctypes.byref(bufferAMin)
    # buffer length = maxSamples
    # segment index = 0
    # ratio mode = PS4000A_RATIO_MODE_NONE = 0
        status["setDataBuffersA"] = ps.ps4000aSetDataBuffers(chandle,
                                                     ps.PS4000A_CHANNEL['PS4000A_CHANNEL_A'],
                                                     bufferAMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
                                                     None,
                                                     sizeOfOneBuffer,
                                                     memory_segment,
                                                     ps.PS4000A_RATIO_MODE['PS4000A_RATIO_MODE_NONE'])
        assert_pico_ok(status["setDataBuffersA"])

    # Set data buffer location for data collection from channel B
    # handle = chandle
    # source = PS4000A_CHANNEL_B = 1
    # pointer to buffer max = ctypes.byref(bufferBMax)
    # pointer to buffer min = ctypes.byref(bufferBMin)
    # buffer length = maxSamples
    # segment index = 0
    # ratio mode = PS4000A_RATIO_MODE_NONE = 0
        status["setDataBuffersB"] = ps.ps4000aSetDataBuffers(chandle,
                                                     ps.PS4000A_CHANNEL['PS4000A_CHANNEL_B'],
                                                     bufferBMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
                                                     None,
                                                     sizeOfOneBuffer,
                                                     memory_segment,
                                                     ps.PS4000A_RATIO_MODE['PS4000A_RATIO_MODE_NONE'])
        assert_pico_ok(status["setDataBuffersB"])

    # Begin streaming mode:
        sampleInterval = ctypes.c_int32(sample_int_tt2) 
        sampleUnits = ps.PS4000A_TIME_UNITS['PS4000A_US']
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
        actualSampleIntervalNs = actualSampleInterval * 1000 #So we can see the sample interval in nanoseconds

        print("Capturing at sample interval %s ns" % actualSampleIntervalNs)

    # We need a big buffer, not registered with the driver, to keep our complete capture in.
    #Create arrays of zeros to read our data into
        bufferCompleteA = np.zeros(shape=totalSamples, dtype=np.int16)
        bufferCompleteB = np.zeros(shape=totalSamples, dtype=np.int16)
        global nextSample, autoStopOuter, wasCalledBack
        nextSample = 0
        autoStopOuter = False
        wasCalledBack = False

        def streaming_callback(handle, noOfSamples, startIndex, overflow, triggerAt, triggered, autoStop, param):
            global nextSample, autoStopOuter, wasCalledBack
            wasCalledBack = True
            destEnd = nextSample + noOfSamples
            sourceEnd = startIndex + noOfSamples
            bufferCompleteA[nextSample:destEnd] = bufferAMax[startIndex:sourceEnd]
            bufferCompleteB[nextSample:destEnd] = bufferBMax[startIndex:sourceEnd]
            nextSample += noOfSamples
            if autoStop:
                autoStopOuter = True


    # Convert the python function into a C function pointer.
        cFuncPtr = ps.StreamingReadyType(streaming_callback)

        #start =time.time() #checking how long this takes

    # Fetch data from the driver in a loop, copying it out of the registered buffers and into our complete one.
        while nextSample < totalSamples and not autoStopOuter:
            wasCalledBack = False
            status["getStreamingLastestValues"] = ps.ps4000aGetStreamingLatestValues(chandle, cFuncPtr, None)
            if not wasCalledBack:
                # If we weren't called back by the driver, this means no data is ready. Sleep for a short while before trying
                # again.
                time.sleep(0.01)

        #end = time.time() #checking how long data collection takes
        #print(end-start)

        #print("Done grabbing values.") #so you know that the data collection has finished. Is this line necessary

    ###############################################################################

    #taking our buffer data arrays, inputting them to the charge_from_tt2 function and plotting the result
       
        TT2 = charge_from_tt2(bufferCompleteA, bufferCompleteB, 20000)
        
        timstmp = time.time() - start_time
        plt.scatter(timstmp, TT2, s=8)
        
    
        plt.xlabel('Time from Start [s]')
        plt.ylabel('Charge from TT2') 
        
        #we need to save the image in order to call it. We'll use this format so that the image constantly overwrites itself and doesn't save individual files within the loop
        file_name = 'D:\Python\\chargefromtt2.' + str(datetime.now().strftime('%d-%m-%y'))+'.jpeg'

        plt.savefig(file_name)
        image = cv2.imread(file_name)
        
        #this opens the image
        cv2.imshow('Charge from TT2', image)
        
        #this keeps the image open for a specified duration (in milliseconds)
        cv2.waitKey(1000)
        
        #this closes the window and resumes the loop
        cv2.destroyAllWindows()
    
    ###############################################################################
        num_tt2 -=1    #this counts down to zero so we only iterate the desired # of times
        
    #  ##############################################################################
    # Stop the scope
    # handle = chandle
    status["stop"] = ps.ps4000aStop(chandle)
    assert_pico_ok(status["stop"])

    # Disconnect the scope
    # handle = chandle
    status["close"] = ps.ps4000aCloseUnit(chandle)
    assert_pico_ok(status["close"])

    # Display status returns

    #print(status)

#get_charge(12, 10**6, 1, 1)