"""
    Plays the song back to the user. This module uses fast fourier transform.
    A fast fourier transform converts an amplitude response to a frequency
    response. The required frequency can then then be selected from the response
    To know more, check out the wikipedia entries
"""
import time
import itertools
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
        self.chunk_size = DETECTION_CONFIG['CHUNK_SIZE']
        self.chunks_per_fft = DETECTION_CONFIG['CHUNK_PER_FFT']
        self.note_min = DETECTION_CONFIG['NOTE_MIN']
        self.note_max = DETECTION_CONFIG['NOTE_MAX']
        self.time_period = DETECTION_CONFIG['TIME_INTERVAL']
        self.samples_per_fft = self.chunk_size * self.chunks_per_fft
        self.freq_step = self.sampling_rate / self.samples_per_fft

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

            if frames_processed >= chunks_per_fft and np.average(power) > 300:
                print(
                    'freq: {:7.2f} power: {} note: {} {:+.2f} timestamp: {}'.format(
                        freq,
                        np.average(power),
                        note_abs,
                        note - note_abs,
                        time.time() - start_time
                    )
                )
                recording_data.append((time.time() - start_time, note_abs,))

            if time.time() - start_time > recording_time:
                return _process(recording_data)

    def play(self, sound_data):
        """
            Plays audio data using a MIDI library
        """
        sampling_rate = self.sampling_rate
        stream = pyaudio.PyAudio().open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=sampling_rate,
            output=True,
        )
        for interval, note in sound_data:
            # Add a delay here
                # Calculate the time period the note stays the same
                # And add it to the pressed time
                # Calculate the time between next note and time of last note
                # Create a delay
            time.sleep(interval)
            freq = _midi_to_freq(note)
            wave = _create_wave(freq, sampling_rate, 1)
            stream.write(wave)

    def _midi_to_fftbin(self, note):
        """
            Pass
        """
        return _midi_to_freq(note) / self.freq_step

# Internals

def _process(recording_data):
    """
        Convert the frequency and time data
        into wave
    """
    # Get the time interval the note stays the same
    # The start point of the note to the end point of the note
    processed = []
    for time, note in recording_data:
        start = time
        interval = 0
        # calculate the interval note stays the same

        while True:
            current_time, current_note = elem
            if index > 0:
                prev_time, prev_note = recording_data[index - 1]
                if prev_note != current_note:
                    processed.append((current_time - prev_time, current_note,))
            else:
                processed.append((current_time, current_note,))
    return processed

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

def _create_wave(freq, sampling_rate, pressed_time):
    """
        Write a wave using sine function. pressed_time indicates how long
        the note is 'pressed'.
    """
    wave = (
        np.sin(
            2 * np.pi * np.arange(
                sampling_rate * pressed_time
            ) * freq / sampling_rate
        )
    ).astype(np.float32)
    return wave

