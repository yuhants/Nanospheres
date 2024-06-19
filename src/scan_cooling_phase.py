import numpy as np
import matplotlib.pyplot as plt

from scipy.signal import welch
import scipy.io as sio

def get_area_psd(phi, prefix, prefix2, nfile, channel='C', passband=(60000, 80000)):
    """Calculate PSD then integrate over passband"""

    areas = np.empty(nfile, dtype=np.float32)
    
    for i in range(nfile):
        # fname = f"{prefix}{prefix2}{phi}{prefix2}{phi}_{i+1:02d}.mat"
        fname = f"{prefix}{prefix2}{phi}{prefix2}{phi}_{i+1:01d}.mat"
        data = sio.loadmat(fname)
        
        fs = int(np.floor(1 / data['Tinterval'][0, 0]))
        nperseg = fs / 10
        ff, pp = welch(data[channel][:,0], fs=fs, nperseg=nperseg)
        idx = np.logical_and(ff > passband[0], ff < passband[1])

        areas[i] = np.trapz(pp[idx], ff[idx]) / (2 * np.pi)

    area, std_area = np.mean(areas), np.std(areas)
    return area, std_area

def main():

    # prefix = r"D:\cooling\20240618_phase_scan_0_1mbar"

    # phiphi = [0, 60 ,120, 150, 180, 210, 240, 300]
    # prefix2 = r"\20240619_yscan_phase"
    # channel = 'A'
    # passband = (343000, 360000)

    phiphi = [270, 290, 310, 330, 350]
    prefix = r"D:\cooling\20240619_phase_scan_3e-4mbar"
    prefix2 = r"\20240619_xscan_phase"
    channel = 'B'
    passband = (255000, 274000)

    # prefix2 = r"\20240618_zscan_phase"
    # channel = 'C'
    # passband = (60000, 68000)
    nfile = 4

    area_phi = np.empty(len(phiphi), dtype=np.float32)
    std_area_phi = np.empty(len(phiphi), dtype=np.float32)
    for i, phi in enumerate(phiphi):
        area, std_area = get_area_psd(phi, prefix, prefix2, nfile, channel, passband)
        area_phi[i] = area
        std_area_phi[i] = std_area

    plt.errorbar(phiphi, area_phi, std_area_phi)
    plt.ylabel('Area under peak ($V^2$)')
    plt.xlabel('Phase (deg)')

if __name__ == '__main__':
    main()
    plt.show()