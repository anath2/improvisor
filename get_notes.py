import pitch_detection_file as pitch
import itertools 


def notes(filename, time):

    
    """
     Takes an input wav file and finds musical notes in it. We don't care about the octave here. 
     A C is represented by 0, D by 1 and so on. 
     We also use a threshold time which is the minimum time a note must last for it to be registered 
     A valid note. The threshold time is calculated using the Note times of the midi file for which
     the notes are to be compared
    """
    
    
    freqs = pitch.midi("%s" %(filename))

    # Store the dictionary extracted frequencies into a list 
    t = [(k, freqs[k]) for k in freqs]
    t.sort()

    # group by the Note values 
    midi_notes = []
    for key, igroup in itertools.groupby(t, lambda x: x[1]):
	    midi_notes.append(list(igroup)[0])

    temp = []

    for i in range(len(midi_notes) - 1):
        if((midi_notes[i + 1][0] - midi_notes[i][0]) > time):
    	    temp.append(midi_notes[i])

    midi_notes = temp[:]

    # Convert the midi numbers into notes. C = 0, D = 1 and so on 
    # Reset temp 
    temp = []

    for i in midi_notes:
        if(i[1] != -1):
             temp.append(i[1] % 12)    

    notes = temp[:]

    return notes
    
