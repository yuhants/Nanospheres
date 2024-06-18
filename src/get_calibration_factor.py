import numpy as np
import matplotlib.pyplot as plt

from utils import load_timestreams, get_psd
from get_sphere_charge import peak_func, fit_peak

from scipy.signal import welch
import scipy.io as sio

"""
Get calibration factor <x^2> = <V^2> / c_cal^2
from electric calibration with known charge
"""

def get_area_driven_peak(prefix, prefix2, nfile, channel='C', passband=(88900, 89100), plot=True):
    """Calculate PSD then integrate over passband"""

    v2_drive = np.empty(nfile, dtype=np.float32)
    
    if plot:
        fig, ax = plt.subplots(figsize=(6,4))

    for i in range(nfile):
        fname = f"{prefix}{prefix2}_{i+1:02d}.mat"
        data = sio.loadmat(fname)
        
        fs = int(np.floor(1 / data['Tinterval'][0, 0]))
        nperseg = fs / 10
        ffd, ppd = welch(data[channel][:,0], fs=fs, nperseg=nperseg)

        all_idx = np.logical_and(ffd > passband[0], ffd < passband[1])
        area_all = np.trapz(ppd[all_idx], ffd[all_idx]*2*np.pi)
        v2_drive[i] = area_all / (2 * np.pi)

        if plot:
            ax.plot(ffd[all_idx], ppd[all_idx])
            ax.set_title(f'Drive = {drive_amp} V Peak to Peak @ {int(drive_freq/1000)} kHz')
            ax.set_xlabel('Frequency (Hz)')
            ax.set_ylabel('Spectral density ($V^2 / Hz$)')
            ax.set_yscale('log')

    if plot:
        plt.show()

    return np.mean(v2_drive), np.std(v2_drive)


net_charge = 1  # +-e
drive_freq = 89000  # Hz
drive_amp  = 35     # V; peak to peak
efield_sim = 120    # Simulated E field at focus
                    # V/m when potential diff is 1 V

plot = True

prefix = r"D:\calibration\20240617_1e_50vp2p_89khz_5_4e-8mbar"
prefix2 = r"\20240617_1e_50vp2p_89khz_5_4e-8mbar"
nfile = 10

# Now calculate the area under the driven peak
f_lower, f_upper = 88920, 89080
area, std_area = get_area_driven_peak(prefix, prefix2, nfile, 'C', (f_lower, f_upper), plot)
print(area)