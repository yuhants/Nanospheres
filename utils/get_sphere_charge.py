import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
from utils import load_timestreams, get_psd

"""
Derive charge (assume mass) based on thermal calibration
at 1 mbar and the sphere's response to an AC driving
field.
Can use this to check if we're trapping a single sphere
or a cluster. In the latter case derived charge will not 
match expectation.

Applied to data taken with picoscope setting 100 ms/div, 1 MS
"""

drive_freq = 64000  # Hz
lb_d, ub_d = 6390, 6410

drive_amp  = 80      # V; peak to peak
efield_sim = 120    # Simulated E field at focus
                    # V/m when potential diff is 1 V
nsphere    = 2

file_1mbar  = r"D:\calibration\20241014_noefield_1mbar.mat"
file_driven = r"D:\calibration\20241014_3e_80vp2p_64khz_1mbar.mat"

plot = True

def peak_func(x, amp, omega_0, gamma):
    """A Lorentzian line shape"""
    return amp * gamma / ( ( omega_0**2 - x**2)**2 + gamma**2 * x**2 )

def fit_peak(x, y, peak_func, p0=None):
    popt, pcov = curve_fit(peak_func, x, y, p0=p0)
    
    # Return central frequency and gamma
    return popt, x, peak_func(x, *popt)

def main():
    # Load timestreams from the matlab files
    dt0, tt0, zz0 = load_timestreams(file_1mbar)
    dtd, ttd, zzd = load_timestreams(file_driven)

    print(zzd)
    ff0, pp0 = get_psd(dt=dt0, zz=zz0[0])
    ffd, ppd = get_psd(dt=dtd, zz=zzd[0])

    # Fit thermally driven peak to a Lorentzian
    lb, ub = 5000, 8000
    popt, omega_fit, p_fit = fit_peak(ff0[lb:ub]*2*np.pi, pp0[lb:ub], peak_func, p0=[5e9, 64000*2*np.pi, 8000])
    amp, omega0, gamma = popt[0], popt[1], popt[2]
    print(f'Amplitude: {amp}, central frequency: {omega0/(2*np.pi)} Hz, gamma: {gamma/(2*np.pi)} Hz')

    if plot:
        fig, ax = plt.subplots(figsize=(6,4))
        ax.plot(ff0[lb:ub], pp0[lb:ub])
        ax.plot(omega_fit/(2*np.pi), p_fit)
        ax.set_title('No driving field')
        ax.set_xlabel('Frequency $\omega / 2 \pi$ (Hz)')
        ax.set_ylabel('Spectral density ($V^2 / Hz$)')
        ax.set_yscale('log')

    # Derive the calibration factor assumed mass and
    # thermal equilibrium at 300 K
    T   = 300  # K
    kb  = 1.38e-23

    # Use this value after ethanol is gone
    rho = 2000 # kg/m^3
    r   = 167e-9 / 2
    m   = rho * (4 * np.pi / 3) * r**3 * nsphere

    # Again need to take care of 2 pi normalization
    # because the formula assume integrating over `omega`, not `f`
    v2 = 0.5 * np.pi/(gamma * omega0**2) * amp * gamma / (2 * np.pi)

    # Calibration factor converting <V^2> to (x^2)
    c_cal_square = (v2 * m * omega0**2) / (kb * T)
    print(fr'Calibration factor square $c^2$: {c_cal_square}')

    # Now calculate the area under the driven peak

    if plot:
        fig2, ax2 = plt.subplots(figsize=(6,4))
        ax2.plot(ffd[lb_d:ub_d], ppd[lb_d:ub_d])
        ax2.set_title(f'Drive = {drive_amp} V Peak to Peak @ {int(drive_freq/1000)} kHz')
        ax2.set_xlabel('Frequency (Hz)')
        ax2.set_ylabel('Spectral density ($V^2 / Hz$)')
        ax2.set_yscale('log')

    all_idx = np.arange(lb_d, ub_d, 1)
    excluding_peak = np.logical_or(all_idx < (lb_d+7), all_idx > (ub_d-7))

    area_all = np.trapz(ppd[all_idx], ffd[all_idx]*2*np.pi)
    area_excluding_peak = np.trapz( ppd[all_idx[excluding_peak]], ffd[all_idx[excluding_peak]]*2*np.pi )

    # Excluding background contribution (which is very small)
    # Take care of 2 pi normalization after numerical integration
    # because we integrated over omega here
    v2_drive = (area_all - area_excluding_peak) / (2 * np.pi)

    vp2p = drive_amp
    omega_drive = drive_freq * 2 * np.pi

    x2_drive = v2_drive / c_cal_square
    f_amp_squared = x2_drive * 2 * m**2 * ( (omega0**2 - omega_drive**2)**2 + gamma**2 * omega_drive**2)

    charge = np.sqrt(f_amp_squared) / (1.6e-19 * efield_sim * (vp2p / 2))
    print(f'Assume {int(nsphere)} spheres, derived charge = +/- {charge:.2f} e')

if __name__=="__main__":
    main()
    plt.show()