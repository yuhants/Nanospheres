import numpy as np
import matplotlib.pyplot as plt

from scan_cooling_phase import get_area_psd
from scipy.signal import welch
import scipy.io as sio

from numpy.polynomial.polynomial import Polynomial

def main():
    gain = [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    prefix = r"D:\cooling\20240802_zgain_scan_4_3e-8mbar"
    prefix2 = r"\20240802_zgain_"
    nfile = 1

    area_gain = np.empty(len(gain), dtype=np.float32)
    for i, g in enumerate(gain):
        area, std_area = get_area_psd(g, prefix, prefix2, nfile, 'D', (65e3, 100e3))
        area_gain[i] = area



    kb  = 1.38e-23
    rho = 2000 # kg/m^3
    r   = 167e-9 / 2
    m   = rho * (4 * np.pi / 3) * r**3
    hbar = 1.05457e-34
    omega0 = 5.01493521e+05

    c_cal_square = 160888032841252.19
    temp = (area_gain * 0.5 * m * omega0**2 / c_cal_square) / kb

    def mk2nphonons(x):
        return (x/1000) * kb / (hbar * omega0)
    
    def nphonons2mk(x):
        return x * (hbar * omega0) / (kb/1000)

    # Fit with a 2d polynomial
    poly = Polynomial.fit(np.asarray(gain), temp, deg=2)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(gain, poly(np.asarray(gain))*1000, '--', color='#b73779')
    ax.plot(gain, temp*1000, '.', color='#b73779', markersize=10)
    secax = ax.secondary_yaxis('right', functions=(mk2nphonons, nphonons2mk))
    secax.set_ylabel('Number of phonons', fontsize=14)

    plt.title(r'Pressure = $4.3 \times 10^{-8}$ mbar; SRS scaling amplifier gain=0.07', fontsize=14)
    plt.ylabel('Effective temperature (mK)', fontsize=14)
    plt.xlabel('Feedback gain in $z$ (a.u.)', fontsize=14)

if __name__ == '__main__':
    main()
    plt.show()