import midi


def extract_bar(start, pattern):
    pattern.make_ticks_abs()
    bar = pattern.resolution * 4
    track = pattern[0]

    new = midi.Pattern()
    track_new = midi.Track()

    for event in track:
        if(event.tick >= start and event.tick <= (start + bar) and isinstance(event, midi.NoteEvent)):
            tick_val = event.tick - start
            new_event = midi.Event.copy(event)
            new_event.tick = tick_val
            track_new.append(new_event)
        if(event.tick > (start + bar)):
            break
            
    if track_new:
        result = midi.Track()
        result.append(track_new[0])
        for x in xrange(len(track_new) - 1):
            ev = midi.Event.copy(track_new[x + 1])
            ev.tick = track_new[x + 1].tick - track_new[x].tick
            result.append(ev) 

        result.append(midi.EndOfTrackEvent())
        new.append(result)
    
        midi.write_midifile("temp.mid", new)

    return event.tick
