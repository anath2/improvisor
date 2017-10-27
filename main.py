"""
    Runner
"""
from improvisor.sound_io import SoundDetector, SoundPlayer
def main():
    """
        Detector runner
    """
    # Record
    detector = SoundDetector()
    recorded_data = detector.listen()

    # Playback
    player = SoundPlayer()
    player.play(recorded_data)

if __name__ == '__main__':
    main()
