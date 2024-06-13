import numpy as np
import scipy.io as sio

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

    return tt, aa, pp