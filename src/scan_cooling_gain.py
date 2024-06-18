import numpy as np
import matplotlib.pyplot as plt

from scan_cooling_phase import get_area_psd
from scipy.signal import welch
import scipy.io as sio

from numpy.polynomial.polynomial import Polynomial

def main():
    gain = [10, 20, 30, 40, 50, 60, 70, 80]

    prefix = r"D:\cooling\20240617_zgain_scan_5_4e-8mbar"
    prefix2 = r"\20240617_zgain"
    nfile = 10

    area_gain = np.empty(len(gain), dtype=np.float32)
    std_area_gain = np.empty(len(gain), dtype=np.float32)
    for i, g in enumerate(gain):
        area, std_area = get_area_psd(g, prefix, prefix2, nfile, 'C', (62e3, 68e3))
        area_gain[i] = area
        std_area_gain[i] = std_area

    # Fit with a 2d polynomial
    poly = Polynomial.fit(np.asarray(gain), area_gain, deg=2)

    plt.plot(gain, poly(np.asarray(gain)), '--', color='#b73779')
    plt.errorbar(gain, area_gain, std_area_gain, linestyle='', marker='.', color='#b73779')
    plt.title(r'Pressure = $5.4 \times 10^{-8}$ mbar', fontsize=14)
    plt.ylabel('Area under peak ($V^2$)', fontsize=14)
    plt.xlabel('Feedback gain in $z$', fontsize=14)

if __name__ == '__main__':
    main()
    plt.show()