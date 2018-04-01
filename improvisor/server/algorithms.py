'''
Functions used in improvisor
'''
import numpy as np

def yinpitch(signal, fs, w_size=6000, tau_max=3000):
    '''
    This algorithm was developed by A. de Cheveigné and H. Kawahara and
    published in:

    de Cheveigné, A., Kawahara, H. (2002) "YIN, a fundamental frequency
    estimator for speech and music", J. Acoust. Soc. Am. 111, 1917-1930.

    see http://recherche.ircam.fr/equipes/pcm/pub/people/cheveign.html

    ARGS:
        signal:                 - Input signal
        fs                      - Sampling frequency
        w_size                  - Window size
        tau_max                 - Lag used to calculate autocorrelation
    '''

    # discrete fourier transform
    data = np.fft.fft(signal)

    # Calculate auto-correlation
    r = np.zeros(tau_max)
    for i in range(tau_max):
        s = 0.0
        for j in range(w_size):
            s += (data[j] - data[j+i]) * (data[j] - data[j+i])
        r[i] = s

    # Get the normalized difference function

    # Select peaks

    # Map pitches to the input signal

    pass
