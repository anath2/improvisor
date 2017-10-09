"""
    Runner
"""
from improvisor.detector import Detector
def main():
    """
        Detector runner
    """
    det = Detector()
    sound_data = det.listen()
    det.play(sound_data)

if __name__ == '__main__':
    main()
