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
    d = np.zeros(tau_max)
    s = r[0]
    for i in range(1, tau_max):
        s += r[i]
        d[i] = r[i] / ((1 / i) * s)

    # Select frequencies
    freqs = []
    for i in range(tau_max):
        if d[i] > 0.5:
            continue
        if d[i-1] > d[i] < d[i+1]:
            freq = fs / i
            freqs.append(freq)

    # Map pitches to the input signal
    to_pad = 0 if len(signal) % tau_max == 0 else tau_max - (len(signal) % tau_max)
    extended_signal = np.resize(signal, len(signal) + to_pad)
    signal_2d = extended_signal.reshape(len(extended_signal) // tau_max, tau_max)
    mapped = zip(freqs, signal_2d)
    return mapped
