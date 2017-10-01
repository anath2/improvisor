import os
import unittest
import detector.from_file

class PitchFromFileTests(unittest.TestCase):
    
    def testIsEmpty(self):
        file_path = os.path.dirname(os.path.abspath(__file__)) + '/files/test.wav' 
        step = 512
        window_size = 4096 
        sample_rate = 44100
        tolerance = 0.8
        algorithm = 'yin'
        result = detector.from_file.get_pitch( 
                    file_path, 
                    algorithm,
                    sample_rate,
                    step,
                    window_size,
                    tolerance
                )

        self.assertTrue(len(result) != 0)
    

if __name__ == '__main__':
    unittest.main()
