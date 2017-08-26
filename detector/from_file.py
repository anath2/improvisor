"""
    THIS PITCH DETECTION ALORITHM IS BASED IS USING THE OPEN SOURCE AUBIO LIBRARY
    PLEASE LOOK AT AUBIO SOURCE FOR MORE INFORMATION AT
    http://github.com/aubio/aubio
"""
import aubio

def get_pitch(filename, algorithm, sample_rate, step, window_size, tolerance):
    """
         CALCULATES PITCH FROM FILE
         OUTPUT : { PITCH (IN HERTZ) : CONFIDENCE }
    """
    aubio_source = aubio.source(filename, sample_rate, step)
    samplerate = aubio_source.samplerate #TODO : SEE THIS
    pitch_obj = aubio.pitch(algorithm, window_size, step, samplerate)
    pitch_obj.set_unit('midi')
    pitch_obj.set_tolerance(tolerance) # TODO : SEE THIS

    pitch_list = []
    confidence_list = []
    total_frames = 0
    while True: 
        sample, read = aubio_source() # TODO: explore the insides of this
        pitch = pitch_obj(sample)[0] 
        pitch_list.append(pitch)
        confidence = pitch_obj.get_confidence()
        confidence_list.append(confidence)
        total_frames += read
        if read < step:
            break;
        
    skip = 1
    pitch_list = pitch_list[skip:]
    confidence_list = confidence_list[skip:]
    time_list = [time * step for time in range(len(pitch_list))]
    return list(zip(time_list, pitch_list, confidence_list))