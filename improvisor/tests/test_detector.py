"""
    Tests for detector module
"""
import unittest
import numpy as np
import pyaudio
import time

from improvisor.detector import Detector
from improvisor.config import DETECTION_CONFIG

class TestDetector(unittest.TestCase):
    """
        The detector module includes the following methods
            - Listen to audio data and output an array of tuples (timestamp, note)
            - process the heard data back into wave format
            - play the output
    """
    def setUp(self):
        """
            Test setup
        """
        self.sampling_rate = DETECTION_CONFIG['SAMPLING_RATE']
        self.interval = DETECTION_CONFIG['TIME_INTERVAL']
        self.sound_data = []
        self.player = pyaudio.PyAudio()
        self.volume = 0.1

        note1 = (
            np.sin(
                2 * np.pi * np.arange(
                    self.sampling_rate * self.interval
                ) * 440.0 / self.sampling_rate
            )
        ).astype(np.float32)
        self.sound_data.append((note1, 1.0,))

        note2 = (
            np.sin(
                2 * np.pi * np.arange(
                    self.sampling_rate * self.interval
                ) * 493.88 / self.sampling_rate
            )
        ).astype(np.float32)
        self.sound_data.append((note2, 5.0,))
        # p = self.player.open(
        #     format=pyaudio.paFloat32,
        #     channels=1,
        #     rate=self.sampling_rate,
        #     output=True,
        # )
        # p.write(note2 * 1)


    def test_player(self):
        """
            Test sound player
        """
        # player = self.player
        # p = player.open(
        #     format=pyaudio.paInt32,
        #     channels=1,
        #     rate=self.sampling_rate,
        #     output=True,
        # )
        # temp_arr = [(0, 0)] + self.sound_data
        # for curr, next_elem in zip(temp_arr, temp_arr[1:]):
        #     print("sleeping for:", next_elem[1] - curr[1])
        #     time.sleep(next_elem[1] - curr[1])
        #     p.write(next_elem[0] * self.volume)
        # Loop through the array
            # Make the element sleep in the array
            # Call the function

        # detector = self.test_detector
        # data = self.sound_data
        # detector.play(data)
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
