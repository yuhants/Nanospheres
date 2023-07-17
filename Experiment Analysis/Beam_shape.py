import numpy as np 
import matplotlib.pyplot as plt
import scipy.optimize as opt

def erfc(w, w0, sigma, amp, offset):
    tot = [0]
    for i in range(1,len(w)):
        gauss = amp*np.exp(-(np.array(w[:i])-w0)**2/2/sigma**2)
        integral = np.trapz(gauss, w[:i])
        tot.append(integral)
    return np.array(tot[::-1]) + offset

amp = [98, 98, 97, 95, 92, 87, 81, 74, 65, 55, 46, 35, 26, 18, 11, 7, 4, 2, 1, 1, 0, 0]
pos = np.linspace(0, 5*10**(-4)*len(amp), len(amp))

fit, cov = opt.curve_fit(erfc, pos, amp, p0 = [30e-4, 1e-3, 100, 0])
print(fit)

fitted_pos = np.linspace(-5*10**(-4), 5*10**(-4)*len(amp), 100)
fitted_amp = erfc(fitted_pos, *fit)

plt.plot(pos, amp, 'o')
plt.plot(fitted_pos, fitted_amp)
plt.show()