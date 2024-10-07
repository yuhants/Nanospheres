import numpy as np
import scipy.io as sio
from scipy.signal import welch

####
#### Loading matlab files
####
def load_timestreams(file, channels=['C']):
    data = sio.loadmat(file)
    length = data['Length'][0,0]
    delta_t = data['Tinterval'][0,0]

    tt = np.arange(length*delta_t, step=delta_t)
    timestreams = []
    for c in channels:
        timestreams.append(data[c][:,0])

    return delta_t, tt, timestreams
    

def load_charging_files(file_list):
    length = 0
    delta_t = 0
    amp, phase = [], []
    
    for file in file_list:
        data = sio.loadmat(file)
        length += data['Length'][0,0]
        delta_t = data['Tinterval'][0,0]
        amp.append(data['E'][:,0])
        phase.append(data['F'][:,0])
    
    tt = np.arange(length*delta_t, step=delta_t)
    aa = np.concatenate(amp)
    pp = np.concatenate(phase)

    return tt, aa, pp

def load_impulse_cal_files(file_list):
    length = 0
    delta_t = 0
    _xx, _yy, _zz, _vv = [], [], [], []
    
    for file in file_list:
        data = sio.loadmat(file)
        length += data['Length'][0,0]
        delta_t = data['Tinterval'][0,0]
        _xx.append(data['B'][:,0])
        _yy.append(data['A'][:,0])
        _zz.append(data['C'][:,0])
        _vv.append(data['G'][:,0])
    
    tt = np.arange(length*delta_t, step=delta_t)
    xx = np.concatenate(_xx)
    yy = np.concatenate(_yy)
    zz = np.concatenate(_zz)
    vv = np.concatenate(_vv)

    return tt, xx, yy, zz, vv

#####
def get_psd(dt=None, tt=None, zz=None, nperseg=None):
    if dt is not None:
        fs = int(np.round(1 / dt))
    elif tt is not None:
        fs = int(np.ceil(1 / (tt[1] - tt[0])))
    else:
        raise SyntaxError('Need to supply either `dt` or `tt`.')
    
    if nperseg is None:
        nperseg = fs / 10
    ff, pp = welch(zz, fs=fs, nperseg=nperseg)
    return ff, pp