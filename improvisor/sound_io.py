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

class SoundDetector(object):
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
        stream_buffer = np.zeros(samples_per_fft, dtype=np.float)
        stream.start_stream()

        print('Sampling at {}hz with maximum resolution of {}'.format(sampling_rate, freq_step))

        start_time = time.time() # Timer starts
        time_since_silence = 0   # Initialize time since silence
        while stream.is_active():
            stream_buffer[:-chunk_size] = stream_buffer[chunk_size:]
            stream_buffer[-chunk_size:] = np.fromstring(
                stream.read(chunk_size),
                np.int16
            )
            fft = np.fft.rfft(stream_buffer * hanning_window)
            power = (20 * np.log10(np.abs(fft))).argmax()
            freq = (np.abs(fft[imin:imax]).argmax() + imin) * freq_step

            note = self._freq_to_midi(freq)
            note_abs = int(round(note))
            frames_processed += 1

            if frames_processed >= chunks_per_fft:
                if np.average(power) > 300:
                    time_since_silence = 0 # Reset silence
                    note_timestamp = time.time() - start_time
                    recording_data.append((note_abs, note_timestamp))
                    print('time : {:.2f} midi_note: {}'.format(
                        note_timestamp, note_abs
                    ))
                else:
                    time_since_silence += (time.time() - start_time)
                    if time_since_silence > 5.0: # If silence for more than 5 sec
                        return recording_data

    def _freq_to_midi(self, freq):
        """
            Frequency to midi value
        """
        return 69 + 12 * np.log2(freq / 440)

    def _midi_to_freq(self, midi):
        """
            midi to frequency
        """
        return 440 * 2.0 ** ((midi - 69) / 12)


    def _midi_to_fftbin(self, note):
        """
            Pass
        """
        return self._midi_to_freq(note) / self.freq_step


class SoundPlayer(object):
    """
        Play wave MIDI data
    """

    def __init__(self):
        """
            Detection module reads sound data using python audio library(pyAudio)
            configuration files are loaded from config module
        """
        self.sampling_rate = DETECTION_CONFIG['SAMPLING_RATE']

    def play(self, recording_data):
        """
            Plays audio data using a MIDI library
        """
        stream = pyaudio.PyAudio().open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=self.sampling_rate,
            output=True,
        )
        wave = self.create_wave(recording_data)
        stream.write(wave)

    def create_wave(self, recording_data):
        """
            Combine sound waves
        """
        sound_data = self._process(recording_data)
        wave_series = np.array([]).astype(np.float32)
        for note, delay, duration in sound_data:
            silence = self._create_silence(delay)
            freq = self._midi_to_freq(note)
            wave = self._create_note(freq, duration)
            np.append(
                wave_series,
                np.concatenate([silence, wave])
            )
        return wave_series

    def _create_silence(self, silence_time):
        """
            Create series for the duration no note is being played
            INPUT :
                silence_time
            OUTPUT:
                numpy series of zeros

        """
        silence = (0 * np.arange(self.sampling_rate * silence_time).astype(np.float32))
        return silence

    def _create_note(self, freq, pressed_time):
        """
            Write a wave using sine function. pressed_time indicates how long
            the note is 'pressed'.

            INPUT :
                freq,  note duration
            Output:
                numpy series
        """
        wave = (
            np.sin(
                2 * np.pi * np.arange(
                    self.sampling_rate * pressed_time
                ) * freq / self.sampling_rate
            )
        ).astype(np.float32)
        return wave

    def _midi_to_freq(self, midi):
        """
            midi to frequency
        """
        return 440 * 2.0 ** ((midi - 69) / 12)

    def _process(self, recording_data):
        """
            Convert the frequency and time data
            into wave
            RETURNS:
                (note, delay, duration)
            Where, note is midi note value, delay is the interval between current
            and previous note and duration is the time interval, the note lasts
        """
        # Algorithm :
            # For each note get pair with the note and
            # list of times where note doesn't change

            # Do another pass over the list and filter out notes
            # with very short durations

            # Calculate delays and durations for each note and return the result

        note_times = [
            (note, list(time for _, time in values)) for note, values in itertools.groupby(
                recording_data,
                lambda x: x[0]
            )
        ]
        # Filter out all notes with duration less than .5 second
        note_times_filtered = [
            (note, times) for note, times in note_times
            if (times[-1] - times[0]) > .5
        ]

        # Filter out notes that that are bunched together

        processed = []
        for index, note_data in enumerate(note_times_filtered):
            current_note, current_times = note_data
            # Use previous note to calculate delay
            if index > 0:
                # Create a temporary index pointing to the previous note
                temp_index = index - 1
                _, prev_times = note_times_filtered[temp_index]
                delay = current_times[0] - prev_times[-1]
            else:
                delay = current_times[0] - 0
            duration = current_times[-1] - current_times[0]
            processed.append((current_note, delay, duration,))
        return processed
