"""
    Plays the song back to the user. This module uses fast fourier transform.
    A fast fourier transform converts an amplitude response to a frequency
    response. The required frequency can then then be selected from the response
    To know more, check out the wikipedia entries
"""
import time
import numpy as np
import pyaudio

from .config import DETECTION_CONFIG

class Detector(object):
    """
        Detection module reads sound data using python audio library(pyAudio)
        configuration files are loaded from config module
    """

    def __init__(self):
        self.sampling_rate = DETECTION_CONFIG['SAMPLING_RATE']
        self.chunk_size = DETECTION_CONFIG['FRAME_SIZE']
        self.chunks_per_fft = DETECTION_CONFIG['FRAMES_PER_FFT']
        self.note_min = DETECTION_CONFIG['NOTE_MIN']
        self.note_max = DETECTION_CONFIG['NOTE_MAX']

        self.samples_per_fft = self.chunk_size * self.chunks_per_fft
        self.freq_step = self.sampling_rate / self.samples_per_fft
        # The variable samples per fft is the unit in frequency domain

    def listen(self):
        """
            Read audio
        """
        sampling_rate = self.sampling_rate
        chunk_size = self.chunk_size
        chunks_per_fft = self.chunks_per_fft
        samples_per_fft = self.samples_per_fft
        freq_step = self.freq_step

        imin = max(0, int(np.floor(
            self._midi_to_fftbin(
                self.note_min
            )
        )))
        imax = max(0, int(np.floor(
            self._midi_to_fftbin(
                self.note_max
            )
        )))
        stream = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sampling_rate,
            input=True,
            frames_per_buffer=chunk_size
        )
        hanning_window = 0.5 * (
            1 - np.cos(
                np.linspace(0, 2 * np.pi, samples_per_fft, False)
            )
        )

        recording_data = []
        frames_processed = 0
        recording_time = 5.0 # Record for 5 seconds
        stream_buffer = np.zeros(samples_per_fft, dtype=np.float)
        stream.start_stream()

        print('Sampling at {}hz with maximum resolution of {}'.format(sampling_rate, freq_step))

        start_time = time.time()
        while stream.is_active():
            stream_buffer[:-chunk_size] = stream_buffer[chunk_size:]
            stream_buffer[-chunk_size:] = np.fromstring(
                stream.read(chunk_size),
                np.int16
            )
            fft = np.fft.rfft(stream_buffer * hanning_window)
            power = (20 * np.log10(np.abs(fft))).argmax()
            freq = (np.abs(fft[imin:imax]).argmax() + imin) * freq_step

            note = _freq_to_midi(freq)
            note_abs = int(round(note))
            frames_processed += 1
            if frames_processed >= chunks_per_fft:
                if np.average(power) > 60:
                    print('freq: {:7.2f} power: {} Hz note: {} {:+.2f}'.format(
                        freq, power, note_abs, note - note_abs
                    ))
                    recording_data.append((time.time() - start_time, note_abs,))
            if time.time() - start_time > recording_time:
                return recording_data

    def record_processing(self, recording_data):
        """
            Convert the frequency and time data
            into wave
        """
        pass

    def play(self, sound_data):
        """
            Plays audio data using a MIDI library
        """
        sampling_rate = self.sampling_rate
        stream = pyaudio.PyAudio().open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sampling_rate,
            output=True,
        )
        stream.write(sound_data)

    def _midi_to_fftbin(self, note):
        """
            Pass
        """
        return _midi_to_freq(note) / self.freq_step

# Internals

def _freq_to_midi(freq):
    """
        Frequency to midi value
    """
    return 69 + 12 * np.log2(freq / 440)

def _midi_to_freq(midi):
    """
        midi to frequency
    """
    return 440 * 2.0 ** ((midi - 69) / 12)
