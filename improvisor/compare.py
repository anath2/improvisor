import midi
from get_notes import notes


def compare(comp, user):
	
	"""
	Compares the midi file with the user input returns true if they match
	
	"""
	pattern = midi.read_midifile("%s" %(comp))
	# take the average of tick values of all offtimes 
	offtimes = [x.tick for x in pattern[0] if(isinstance(x, midi.NoteOffEvent))]
	avg_tick = sum(offtimes) / len(offtimes)
	# convert it into seconds. Here we are assuming the resolution to be 220 and tempo 120  
	time = (avg_tick * 60.0) / (120 * 220) 
	user_notes = notes("%s" %(user), time)
	# calculate the notes in midi file
	comp_notes = []
	for event in pattern[0]:
	    if(isinstance(event, midi.NoteOnEvent)):
	        comp_notes.append(event.pitch % 12)
	
	# We are just checking if all the notes in user input are also present in midi in the same sequence 
	print "User Notes", user_notes
	print "Computer Notes", comp_notes
	x = [i for i, j in zip(comp_notes, user_notes) if i == j] 
	return set(x) == set(user_notes)
	
