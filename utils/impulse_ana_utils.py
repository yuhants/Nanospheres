import numpy as np
from scipy.signal import butter, sosfilt

def bandpass_filtered(data, fs, f_low=10000, f_high=100000, order=4): 
    sos_bp = butter(order, [f_low, f_high], 'bandpass', fs=fs, output='sos')
    filtered = sosfilt(sos_bp, data)
    
    return filtered

def lowpass_filtered(tod, fs, f_lp=50000, order=4):
    sos_lp = butter(order, f_lp, 'lp', fs=fs, output='sos')
    filtered = sosfilt(sos_lp, tod)
    
    return filtered

def highpass_filtered(tod, fs, f_hp=50000, order=4):
    sos_hp = butter(order, f_hp, 'hp', fs=fs, output='sos')
    filtered = sosfilt(sos_hp, tod)
    
    return filtered