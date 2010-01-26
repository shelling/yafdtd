# collect most of popular source function here
# include:
#   Gaussian and its derivative
#   Rayleigh                       (not yet)
#   chirp                          (not yet)
#   polynomial                     (not yet)

from mpmath import *
mp.dps = 50

# polynomial source and its 1-order and 2-order derivative
def polynomial_pulse(t):
    if abs(t)<1:
        return mpf(mpf(1)-mpf(t)**2)**4
    else:
        return 0

def polynomial_pulse_p(t):
    if abs(t)<1:
        return -8 * mpf(t) * (1-mpf(t)**2)**3
    else:
        return 0

def polynomial_pulse_pp(t):
    if abs(t)<1:
        return 48 * mpf(t)**2 * (1-mpf(t)**2)**2 - 8 * (1-mpf(t)**2)**3
    else:
        return 0

# guassian source and its 1-order derivative
def gaussian(t, sigma, mean):
    return exp(-1 * (t - mean)**2 / (2 * sigma**2)) / (sqrt(2 * pi) * sigma)

def gaussian_p(t, sigma, mean):
    return ( (mean - t) / sqrt(2 * pi) * sigma**3 ) * exp( -1 * (t - mean)**2 / (2*sigma**2) )
