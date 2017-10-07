"""
    Improvisor configurations
    VALUES:
        NOTE_MIN : MINIMUM MIDI VALUE
        NOTE_MAX : MAXIMUM MIDI VALUE
        SAMPLING_RATE : SAMPLE RATE FOR RECORDING.(https://en.wikipedia.org/wiki/Sampling_(signal_processing))
        CHUNK_SIZE : SAMPLES PER FRAME. (Chunk size is the number of samples that can be read at once)
        CHUNKS_PER_FFT : NUMBER OF CHUNKS INSIDE ONE FFT (https://en.wikipedia.org/wiki/Fast_Fourier_transform)
        TIME_INTERVAL : NUMBER OF SECOND PER RECORDING
"""
DETECTION_CONFIG = {
    'NOTE_MIN': 60,
    'NOTE_MAX': 69,
    'SAMPLING_RATE': 22050,
    'CHUNK_SIZE': 2048,
    'CHUNK_PER_FFT': 16,
    'TIME_INTERVAL': 5
}
