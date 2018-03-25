'''
Module contents:
  - SoundInterface (ABC)
  - Improvisor
'''

"""
    Algorithm

    Allow microphone input for a given interval of time
    While the user is inputting, calculate the fast fourier
    transform of the signal

    Use averaged and log distributed fft against a trained neural network
    to calculate the pitch
    post the pitch to the server
    Send the signal to the front end, that would play the desired
    animation
"""
import time

import numpy as np
import pyaudio as paud

from abc import ABCMeta, abstractmethod


class SoundInterface(ABCMeta):

    @abstractmethod
    def read_audio(self):
      '''
      Listen audio
      '''
      pass

    @abstractmethod
    def process(self):
      '''
      Process sound data
      '''
      pass

    @abstractmethod
    def write_audio(self):
      '''
      Write audio data to the file or audio output
      '''
      pass

class PitchDetector(SoundInterface):
  '''
  Detect pitch from Audio
  '''
  def read(self, src, *args, **kwargs):
    '''
    Read input data as numpy array
    from an audio source
    ARGS:
      src                - Audio source, could be a sound device or a file
    RETURNS:
      out              - A pandas series representation of input data
    '''
    if isinstance(src, paud.PyAudio):
      # Audio is from the recording device
      if kwargs:
        if 'sec' in kwargs:
          sec = kwargs['sec']
          aud_arry = self._listen(sec=10)
      else:
        audio_arr = []
        try:
          audo_arr = self.listen()
          time.sleep(1)
        except KeyboardInterrupt as err:
          print('Recording terminated')

    if isinstance(src, str):
      # Audio is from an audio file, proceed accordingly
      pass


  def process(self, algo, *args, **kwargs):
    '''
    Process audio data calculate pitch in an audion file
    ARGS:
      algo                  - Pitch detection algorithm in use
    RETURNS:
      processed_audio       - Returns a pandas series containing notes
                              corresponding to audio in the read audion file
    '''
    pass

  def write(self, player, *args, **kwargs):
    '''
    Write audion either to a file, or to audio output devices.
    The audio audio for the output data generated is written either to
    the disk as a wave file or to output
    ARGS:
      player                - Player ditermine the timbre and instrument
                              that plays the sound
    '''
    pass


  # Private methods
  def _listen(self, **kwargs):
    '''
    Listen to audio
    ARGS:
      kwargs(optional):
        sec               - Time in seconds to listen to audio input
    RETURNS:
      aud_arry            - An arry of audion signal in time domain
    '''





# import sys
# from audiolazy import (tostream, AudioIO, freq2str, sHz, chunks,
#                        lowpass, envelope, pi, thub, Stream, maverage)
# from numpy.fft import rfft

# def limiter(sig, threshold=.1, size=256, env=envelope.rms, cutoff=pi/2048):
#   sig = thub(sig, 2)
#   return sig * Stream( 1. if el <= threshold else threshold / el
#                        for el in maverage(size)(env(sig, cutoff=cutoff)) )


# @tostream
# def dft_pitch(sig, size=2048, hop=None):
#   for blk in Stream(sig).blocks(size=size, hop=hop):
#     dft_data = rfft(blk)
#     idx, vmax = max(enumerate(dft_data),
#                     key=lambda el: abs(el[1]) / (2 * el[0] / size + 1)
#                    )
#     yield 2 * pi * idx / size


# def pitch_from_mic(upd_time_in_ms):
#   rate = 44100
#   s, Hz = sHz(rate)

#   api = sys.argv[1] if sys.argv[1:] else None # Choose API via command-line
#   chunks.size = 1 if api == "jack" else 16

#   with AudioIO(api=api) as recorder:
#     snd = recorder.record(rate=rate)
#     sndlow = lowpass(400 * Hz)(limiter(snd, cutoff=20 * Hz))
#     hop = int(upd_time_in_ms * 1e-3 * s)
#     for pitch in freq2str(dft_pitch(sndlow, size=2*hop, hop=hop) / Hz):
#       yield pitch






    # rate = 44100 # Sampling rate, in samples/second
    # s, Hz = sHz(rate) # Seconds and hertz
    # ms = 1e-3 * s
    # note1 = karplus_strong(440 * Hz) # Pluck "digitar" synth
    # note2 = zeros(300 * ms).append(karplus_strong(880 * Hz))
    # notes = (note1 + note2) * .5
    # sound = notes.take(int(2 * s)) # 2 seconds of a Karplus-Strong note
    # with AudioIO(True) as player: # True means "wait for all sounds to stop"
    #     player.play(sound, rate=rate)

# """
#     Plays the song back to the user. This module uses fast fourier transform.
#     A fast fourier transform converts an amplitude response to a frequency
#     response. The required frequency can then then be selected from the response
#     To know more, check out the wikipedia entries
# """
# import time
# import itertools
# import numpy as np
# import pyaudio

# from improvisor.config import DETECTION_CONFIG

# class SoundDetector(object):
#     """
#         Detection module reads sound data using python audio library(pyAudio)
#         configuration files are loaded from config module
#     """

#     def __init__(self):
#         self.sampling_rate = DETECTION_CONFIG['SAMPLING_RATE']
#         self.chunk_size = DETECTION_CONFIG['CHUNK_SIZE']
#         self.chunks_per_fft = DETECTION_CONFIG['CHUNK_PER_FFT']
#         self.note_min = DETECTION_CONFIG['NOTE_MIN']
#         self.note_max = DETECTION_CONFIG['NOTE_MAX']
#         self.time_period = DETECTION_CONFIG['TIME_INTERVAL']
#         self.samples_per_fft = self.chunk_size * self.chunks_per_fft
#         self.freq_step = self.sampling_rate / self.samples_per_fft

#     def listen(self):
#         """
#             Read audio
#         """
#         sampling_rate = self.sampling_rate
#         chunk_size = self.chunk_size
#         chunks_per_fft = self.chunks_per_fft
#         samples_per_fft = self.samples_per_fft
#         freq_step = self.freq_step

#         imin = max(0, int(np.floor(
#             self._midi_to_fftbin(
#                 self.note_min
#             )
#         )))
#         imax = max(0, int(np.floor(
#             self._midi_to_fftbin(
#                 self.note_max
#             )
#         )))
#         stream = pyaudio.PyAudio().open(
#             format=pyaudio.paInt16,
#             channels=1,
#             rate=sampling_rate,
#             input=True,
#             frames_per_buffer=chunk_size
#         )
#         hanning_window = 0.5 * (
#             1 - np.cos(
#                 np.linspace(0, 2 * np.pi, samples_per_fft, False)
#             )
#         )

#         recording_data = []
#         frames_processed = 0
#         stream_buffer = np.zeros(samples_per_fft, dtype=np.float)
#         stream.start_stream()

#         print('Sampling at {}hz with maximum resolution of {}'.format(sampling_rate, freq_step))

#         start_time = time.time() # Timer starts
#         time_since_silence = 0   # Initialize time since silence
#         while stream.is_active():
#             stream_buffer[:-chunk_size] = stream_buffer[chunk_size:]
#             stream_buffer[-chunk_size:] = np.fromstring(
#                 stream.read(chunk_size),
#                 np.int16
#             )
#             fft = np.fft.rfft(stream_buffer * hanning_window)
#             power = (20 * np.log10(np.abs(fft))).argmax()
#             freq = (np.abs(fft[imin:imax]).argmax() + imin) * freq_step

#             note = self._freq_to_midi(freq)
#             note_abs = int(round(note))
#             frames_processed += 1

#             if frames_processed >= chunks_per_fft:
#                 if np.average(power) > 300:
#                     time_since_silence = 0 # Reset silence
#                     note_timestamp = time.time() - start_time
#                     recording_data.append((note_abs, note_timestamp))
#                     print('time : {:.2f} midi_note: {}'.format(
#                         note_timestamp, note_abs
#                     ))
#                 else:
#                     time_since_silence += (time.time() - start_time)
#                     if time_since_silence > 5.0: # If silence for more than 5 sec
#                         return recording_data

#     def _freq_to_midi(self, freq):
#         """
#             Frequency to midi value
#         """
#         return 69 + 12 * np.log2(freq / 440)

#     def _midi_to_freq(self, midi):
#         """
#             midi to frequency
#         """
#         return 440 * 2.0 ** ((midi - 69) / 12)


#     def _midi_to_fftbin(self, note):
#         """
#             Pass
#         """
#         return self._midi_to_freq(note) / self.freq_step


# class SoundPlayer(object):
#     """
#         Play wave MIDI data
#     """

#     def __init__(self):
#         """
#             Detection module reads sound data using python audio library(pyAudio)
#             configuration files are loaded from config module
#         """
#         self.sampling_rate = DETECTION_CONFIG['SAMPLING_RATE']

#     def play(self, recording_data):
#         """
#             Plays audio data using a MIDI library
#         """
#         stream = pyaudio.PyAudio().open(
#             format=pyaudio.paFloat32,
#             channels=1,
#             rate=self.sampling_rate,
#             output=True,
#         )
#         wave = self.create_wave(recording_data)
#         stream.write(wave)

#     def create_wave(self, recording_data):
#         """
#             Combine sound waves
#         """
#         sound_data = self._process(recording_data)
#         wave_series = []
#         for note, delay, duration in sound_data:
#             wave = self._create_note(note, duration)
#             wave_series += list(wave)
#             silence = self._create_silence(delay)
#             wave_series += list(silence)
#         return np.array(wave_series)

#     def _create_silence(self, silence_time):
#         """
#             Create series for the duration no note is being played
#             INPUT :
#                 silence_time
#             OUTPUT:
#                 numpy series of zeros

#         """
#         silence = (0 * np.arange(self.sampling_rate * silence_time).astype(np.float32))
#         return silence

#     def _create_note(self, note, pressed_time):
#         """
#             Write a wave using sine function. pressed_time indicates how long
#             the note is 'pressed'.

#             INPUT :
#                 note,  note duration
#             Output:
#                 numpy series
#         """
#         freq = self._midi_to_freq(note)
#         wave = (
#             np.sin(
#                 2 * np.pi * np.arange(
#                     self.sampling_rate * pressed_time
#                 ) * freq / self.sampling_rate
#             )
#         ).astype(np.float32)
#         return wave

#     def _midi_to_freq(self, midi):
#         """
#             midi to frequency
#         """
#         return 440 * 2.0 ** ((midi - 69) / 12)

#     def _process(self, recording_data):
#         """
#             Convert the frequency and time data
#             into wave
#             RETURNS:
#                 (note, delay, duration)
#             Where, note is midi note value, delay is the interval between current
#             and previous note and duration is the time interval, the note lasts
#         """
#         # Algorithm :
#             # For each note get pair with the note and
#             # list of times where note doesn't change

#             # Do another pass over the list and filter out notes
#             # with very short durations

#             # Calculate delays and durations for each note and return the result

#         note_times = [
#             (note, list(time for _, time in values)) for note, values in itertools.groupby(
#                 recording_data,
#                 lambda x: x[0]
#             )
#         ]
#         # Filter out all notes with duration less than .5 second
#         note_times_filtered = [
#             (note, times) for note, times in note_times
#             if (times[-1] - times[0]) > .5
#         ]

#         # Filter out notes that that are bunched together

#         processed = []
#         for index, note_data in enumerate(note_times_filtered):
#             current_note, current_times = note_data
#             # Use previous note to calculate delay
#             if index > 0:
#                 # Create a temporary index pointing to the previous note
#                 temp_index = index - 1
#                 _, prev_times = note_times_filtered[temp_index]
#                 delay = current_times[0] - prev_times[-1]
#             else:
#                 delay = current_times[0]
#             duration = current_times[-1] - current_times[0]
#             processed.append((current_note, delay, duration,))
#         return processed
# #! /usr/bin/env python
# import pyaudio
# import wave
# import numpy as np
# from aubio import pitch

# CHUNK = 1024
# FORMAT = pyaudio.paFloat32
# CHANNELS = 1
# RATE = 44100
# RECORD_SECONDS = 5
# WAVE_OUTPUT_FILENAME = "output.wav"

# p = pyaudio.PyAudio()

# stream = p.open(format=FORMAT,
#                 channels=CHANNELS,
#                 rate=RATE,
#                 input=True,
#                 frames_per_buffer=CHUNK)

# print("* recording")

# frames = []

# # Pitch
# tolerance = 0.8
# downsample = 1
# win_s = 4096 // downsample # fft size
# hop_s = 1024  // downsample # hop size
# pitch_o = pitch("yin", win_s, hop_s, RATE)
# pitch_o.set_unit("midi")
# pitch_o.set_tolerance(tolerance)


# for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
#     buffer = stream.read(CHUNK)
#     frames.append(buffer)

#     signal = np.fromstring(buffer, dtype=np.float32)

#     pitch = pitch_o(signal)[0]
#     confidence = pitch_o.get_confidence()

#     print("{} / {}".format(pitch,confidence))


# print("* done recording")

# stream.stop_stream()
# stream.close()
# p.terminate()

# wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# wf.setnchannels(CHANNELS)
# wf.setsampwidth(p.get_sample_size(FORMAT))
# wf.setframerate(RATE)
# wf.writeframes(b''.join(frames))
# wf.close()