import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import butter, sosfilt, stft, welch
from scipy.optimize import curve_fit

def plot_tod(data, title):
    fig, ax = plt.subplots(figsize = (20, 6))

    ax.plot(data[0], data[1], label="Y detection")
    ax.plot(data[0], data[2], label="X detection")
    ax.plot(data[0], data[3], label="Applied voltage signal")
    try:
        ax.plot(data[0], data[4], label="Feedback signal")
    except:
        pass

    ax.legend(frameon=False, fontsize=18)
    ax.set_xlabel('Time (ms)', fontsize=18)
    ax.set_ylabel('Signal (V)', fontsize=18)
    ax.set_title(title, fontsize=18)
    
    return fig, ax

def get_psd(data, channel=1, time_unit_prefix=None):
    if time_unit_prefix is None:
        time_unit_prefix = 1
    fs = int(np.ceil(1 / ((data[0, 1] - data[0, 0]) * time_unit_prefix)))
    nperseg = fs / 10
    
    ff, pp = welch(data[channel], fs=fs, nperseg=nperseg)
    return ff, pp

def peak_amplitude_stft(tod, fs, nperseg, driving_freq):
    
    ff, tt, Zxx = stft(tod, fs=fs, nperseg=nperseg)
    sig = np.abs(Zxx)
    f = np.where(ff==driving_freq)[0][0]

    # time, peak amplitude^2, sample frequency, sftp
    return tt, sig[f], ff, Zxx[f]

def plot_peak_amp(data, drive_freq, title=None):
    fs = int(np.ceil(1 / (data[0, 1] - data[0, 0])))
    nperseg = fs / 10

    tt, sig, ff, Zxx = peak_amplitude_stft(data[1], fs, nperseg, drive_freq)
    
    fig, ax = plt.subplots(figsize = (20, 6))
    ax.grid()
    ax.plot(tt, sig, '-')

    ax.set_xlabel('Time (s)', fontsize=18)
    ax.set_ylabel(f'Peak amplitude@{int(drive_freq/1000)} kHz (V)', fontsize=18)
    ax.set_title('1 mbar, driving field = 20 V peak to peak', fontsize=20)
    if title is not None:
        ax.set_title(title, fontsize=20)

    return fig, ax

def get_filtered_signal(data, f_hp=20000, f_lp=100000):
    # This assumed that data is recorded in ms
    fs = int(np.ceil(1 / (data[0, 1] - data[0, 0]))) * 1000 # Sampling rate in Hz
    sos = butter(8, [f_hp, f_lp], 'bandpass', output='sos', fs=fs)
    filtered = sosfilt(sos, data[1])

    return filtered

def peak_func(x, amp, omega_0, gamma):
    """A Lorentzian line shape"""
    return amp * gamma / ( ( omega_0**2 - x**2)**2 + gamma**2 * x**2 )

def fit_peak(x, y, peak_func, p0=None):
    popt, pcov = curve_fit(peak_func, x, y, p0=p0)
    
    # Return central frequency and gamma
    return popt, x, peak_func(x, *popt)

def get_peak_area(data=None, channel=1, fdrive=20000, ff=None, pp=None):
    """Integrate to get the area under a driven peak"""
    if data is not None:
        ff, pp = get_psd(data, channel=channel)
    
    peak_idx = int(fdrive / 10)
    lb, ub = peak_idx-10, peak_idx+10
    
    all_idx = np.arange(lb, ub, 1)
    excluding_peak = np.logical_or(all_idx < (peak_idx-3), all_idx > (peak_idx+3))

    area_all = np.trapz(pp[all_idx], ff[all_idx]*2*np.pi)
    area_excluding_peak = np.trapz( pp[all_idx[excluding_peak]], ff[all_idx[excluding_peak]]*2*np.pi )

    # Excluding background contribution (which is very small anyway)
    # Take care of 2 pi normalization after numerical integration
    # because we integrated over omega here
    v2_drive = (area_all - area_excluding_peak) / (2 * np.pi)
    
    return v2_drive

def plot_and_fit_peak(ff, pp, lb, ub, p0=None):
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(ff[lb:ub], pp[lb:ub])

    # Fit with a Lorentzian and plot
    popt, omega_fit, p_fit = fit_peak(ff[lb:ub]*2*np.pi, pp[lb:ub], peak_func, p0=p0)
    ax.plot(omega_fit/(2*np.pi), p_fit)

    amp, omega0, gamma = popt[0], popt[1], popt[2]
    print(f'Amplitude: {amp}, central frequency: {omega0/(2*np.pi)} Hz, gamma: {gamma/(2*np.pi)} Hz')

    ax.set_xlabel('Frequency $\omega / 2 \pi$ (Hz)')
    ax.set_ylabel('Spectral density ($V^2 / Hz$)')

    ax.set_yscale('log')
    return fig, ax, popt

def get_chisquare(ff, pp, p2p_drive_amp, freq_comb_file, charge, efield, c_cal_square):
    comb_data = np.load(freq_comb_file, allow_pickle=True)
    ff_drive = comb_data['ff']

    amp = p2p_drive_amp / 2  # Amplitude from zero in V

    chisquare = np.zeros_like(ff_drive, dtype=np.float64)
    f0 = charge * amp * efield

    for i, f in enumerate(ff_drive):
        v2_drive = get_peak_area(None, 1, f, ff, pp)
        x2_drive = v2_drive / c_cal_square
        
        chisquare_drive = 2 * x2_drive / (f0**2)
        chisquare[i] = chisquare_drive
    
    return ff_drive, chisquare