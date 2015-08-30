import alsaaudio
import struct
from aubio.task import *
from math import *
import time

# constants
CHANNELS = 1
INFORMAT = alsaaudio.PCM_FORMAT_FLOAT_LE
RATE = 44100
FRAMESIZE = 1024
PITCHALG = aubio_pitch_yin
PITCHOUT = aubio_pitchm_freq

# set up audio input
recorder = alsaaudio.PCM(type=alsaaudio.PCM_CAPTURE)
recorder.setchannels(CHANNELS)
recorder.setrate(RATE)
recorder.setformat(INFORMAT)
recorder.setperiodsize(FRAMESIZE)

# set up pitch detect
detect = new_aubio_pitchdetection(FRAMESIZE, FRAMESIZE / 2, CHANNELS,
                                  RATE, PITCHALG, PITCHOUT)
buf = new_fvec(FRAMESIZE, CHANNELS)


def pitches():

    # main loop
    runflag = 1
    notes = []
    start = time.time()
    # maximum idle time allowed
    TIMEOUT = 4 
    
    while runflag:
    
    	# read data from audio input
        [length, data] = recorder.read()

        # convert to an array of floats
        floats = struct.unpack('f' * FRAMESIZE,data)

        # copy floats into structure
        for i in range(len(floats)):
            fvec_write_sample(buf, floats[i], 0, i)

        # find pitch of audio frame
        freq = aubio_pitchdetection(detect, buf)
        
        if freq < 1083 and freq > 87:
        
            midi = int(round(log((freq / 440.0), 2) * 12 + 69))
        
            note = midi
            #note = midi % 12
            # Find enery of the audio frame

            energy = vec_local_energy(buf)
    
            # Only print values if energy is greater than 1        
        
            if(energy > 1):
                print "{:10.4f} {:10.4f}".format(note, energy)
                notes.append(note)
     	        start = time.time()
     	
     	    else : 
     	        if((time.time() - start) > TIMEOUT): 
     	    
     	            break
   
    return notes   

if __name__ == '__main__' :
	print pitches()
