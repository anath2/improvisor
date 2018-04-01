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
import logging
import pyaudio

import numpy as np

logger = logging.getLogger(__name__)

class PitchDetector(object):
  '''
  Detect pitch from Audio
  '''
  def __init__(self, algo):
    self.algo = algo
    self.signal = None

  def read(self, src=None, time=None):
    '''
    Read input data as numpy array
    from an audio source
    ARGS:
      src                - Audio source, could be a sound device or a file
    RETURNS:
      out              - A pandas series representation of input data
    '''
    if src:
      logger.info('Reading audio file...')
      aud_arry = _read(src)
    else:
        if time:
          logger.info('Recording for {} seconds'.format(time))
          aud_arry = _listen(time=time)
        else:
          logger.info('Recording audio, press CTRL-C to stop')
          aud_arry = _listen()
    self.signal = aud_arry

  def process(self):
    '''
    Process audio data calculate pitch in an audion file
    '''
    self.signal = self.algo(self.signal)

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
def _listen(chunk=1024, frmt=pyaudio.paInt16, ch=2, rate=44100, time=None):
  '''
  Listen to audio
  ARGS:
    chunk               - Size of audio buffer in frames (1024 by default)
    format              - Format for audio data (16 bit Int by default)
    ch                  - Number of channels (2 by default)
    rate                - Sampling Rate in frames per sec (44100 by default)
    time                - Recording time (None by default,
                          stop on keyboard interrupt)

  RETURNS:
    aud_arry            - Data representation of audio data in time
                          domain. The size of the list is equal to the number of
                          audio buffers in the time period
  '''
  p = pyaudio.PyAudio()
  stream = p.open(format=frmt, channels=ch, rate=rate, input=True,
                    frames_per_buffer=chunk)
  logger.info('Recording...')
  frames = []
  if time:
    for i in range(0, int(rate / chunk) * time):
      data = stream.read(chunk)
      frames.append(data)
  else:
    logger.info('Press CTRL-C on terminal window to stop recording')
    while True:
      try:
        data = stream.read(chunk)
        frames.append(data)
      except KeyboardInterrupt:
        logger.info('Stopping recording...')
        break
  frames = np.array(frames)
  return frames


def _read(path):
  '''
  ARGS:
    path                - Path to audio file
  '''
  with open(path, 'rb') as f:
    data = f.read()
  return data


