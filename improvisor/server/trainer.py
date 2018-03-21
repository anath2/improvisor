"""
    Module for training the pitch detection algorithm
"""
import numpy as np
import pandas as pd
import keras
from audiolazy import (
    Stream, AudioIO, sHz, chunks, lowpass, limiter
)

class Trainer(object):
    """
        Trainer class for training the neural network
    """
    def __init__(self, upd_time_in_ms):
        self.upd_time_in_ms = upd_time_in_ms

    def record_snd(self, note):
        """
            Record sound training data from system
            microphone
        """
        rate = 44100
        sec, Hz = sHz(rate)
        dft_data = []
        chunks.size = 1
        with AudioIO(api=None) as recorder:
            snd = recorder.record(rate=rate)
            sndlow = lowpass(400 * Hz)(limiter(snd, cutoff=20 * Hz))
            hop = int(self.upd_time_in_ms * 1e-3 * sec)
            for dft in Trainer.pitch_to_dft(sndlow, size=2*hop, hop=hop):
                dft_data.append(dft)

        return Trainer.dft_to_df(dft_data, note)

    def load_data(self, data_path):
        """
            Load the data.csv file that contains
            training dft data for each note
        """
        sound_df = pd.read_csv(data_path)
        return sound_df

    def save_data(self, data_path, training_data):
        """
            Save / Append training data to data file
        """
        training_data.to_csv(data_path)

    @staticmethod
    def dft_to_df(dft, note):
        df = pd.DataFrame(dft, index=(len(dft) * [note]))
        return df

    @staticmethod
    def train_nn(self, train_data):
        """
            Train the neural network with given signal
        """
        pass

    @staticmethod
    def pitch_to_dft(signal, size, hop):
        """
            Convert pitches to dft
        """
        dft_list = []
        for blk in Stream(signal).blocks(size=size, hop=hop):
            dft = np.fft.rfft(blk)
            dft_list.append(dft)
        return dft_list

    @staticmethod
    def normalize_data(dft_df):
        """
            Normalize and clean up dimensions
        """
        pass

# def gen_traindata(note, signal, block_size=2048, hop=None):
#     """
#         Creates a training dataframe containing fast fourier
#         transform corresponding to the note.
#         ARGS:
#             note: Name of the note in the range E2 to E5 (Till 12th fret)
#             signal: Signal recorded from your system's microphone
#             block_size: Size of block in bytes
#             hop: how many bytes to skip before the next recording
#     """
#     dft_list = []
#     for blk in Stream(signal).blocks(size=block_size, hop=hop):
#         dft = np.fft.rfft(blk)
#         dft_list.append(dft)

#     dft_data = np.vstack(dft_list)
#     return dft_data

# def filter_dims(dft_df):
#     """
#         Filter the dataframe removing unncessessary blocks,
#         dimensionality reduction and normalize the data
#     """
#     pass

# def train_data():
#     """
#         Train the neural network on the dft_data
#     """
#     pass

# def save_dft(out_file, dft_df):
#     """
#         Save/Append data to the data csv file
#     """
#     pass



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
