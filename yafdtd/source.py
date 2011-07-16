# collect most of popular source function here
# include:
#   Gaussian and its derivative
#   Rayleigh                       (not yet)
#   chirp                          (not yet)
#   polynomial                     (not yet)

import math

def gaussian(t, center, width):
    return math.exp( -0.5 * math.pow((float(center) - t)/width, 2.0) )

def gaussian_p(t, sigma, mean):
    return ( (mean - t) / sqrt(2 * pi) * sigma**3 ) * exp( -1 * (t - mean)**2 / (2*sigma**2) )





