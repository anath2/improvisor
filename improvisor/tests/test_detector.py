"""
    Tests for detector module
"""
import unittest
import numpy as np

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
        sampling_rate = DETECTION_CONFIG['SAMPLING_RATE']
        interval = DETECTION_CONFIG['TIME_INTERVAL']
        self.test_detector = Detector()
        self.sound_data = round(127 * np.sin(np.linspace(0, 2*np.pi, sampling_rate * interval))) + 128
        # WIP

    def test_player(self):
        """
            Test sound player
        """
        detector = self.test_detector
        data = self.sound_data

        detector.play(data)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
