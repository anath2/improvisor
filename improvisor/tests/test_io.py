"""
    Test sound io
"""
import unittest
from improvisor.sound_io import SoundPlayer

class TestOutput(unittest.TestCase):
    """
        Test output
    """

    def setUp(self):
        """
            Setup input for the player
        """
        # Creating fake recording data
        # The note progression being
        # C -> D -> E
        self.recording_data = [
            (60, 0.0),
            (60, 0.3),
            (60, 0.5),
            (60, 1.0),
            (60, 1.5),
            (62, 2.0),
            (62, 2.3),
            (62, 2.5),
            (62, 3.0),
            (62, 3.5),
            (64, 4.0),
            (64, 4.3),
            (64, 4.5),
            (64, 5.0),
            (64, 5.5),
        ]
        self.pl = SoundPlayer()

    def test_processing(self):
        """
            Test if the recorded fft data is processed properly
        """
        processed_sound = self.pl._process(self.recording_data)

        # Assert processed sound consists of only 3 notes
        self.assertTrue(len(processed_sound) == 3)


    def test_create_wave(self):
        """
            Write a wave
        """
        wave = self.pl.create_wave(self.recording_data)

        # Assert wave is not empty
        self.assertTrue(len(wave) > 0)
