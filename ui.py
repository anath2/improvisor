import pygtk
pygtk.require('2.0')
import gtk, gobject
import signal
import pango
import subprocess
import os
import midi
import extract_bar as bar
import time
import threading
import compare
import pitch_detection_realtime as pitch
import itertools
import pickle
import genetic


gtk.gdk.threads_init()

class MyThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()





class Teacher:

    def __init__(self):
        # Process for the file being played
        self.proc = False
        # File Being Used
        self.filename = ""
        # Position in the file
        self.position = 0
        # The Console Window
        self.textview = gtk.TextView()
        # Thread for the practice button
        self.practicethread = MyThread()

        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_size_request(700, 350)
        window.set_title("The Improvisor")
        window.connect("delete_event",
                       lambda w,e: gtk.main_quit())


        table = gtk.Table(4, 4, True)
        window.add(table)

        button1 = gtk.Button("Open")
        button1.connect("clicked", self.clicked_open_file)
        button1.show()

        button2 = gtk.Button("Play")
        button2.connect("clicked", self.clicked_play)
        button2.show()

        button3 = gtk.Button("Stop")
        button3.connect("clicked", self.clicked_stop)
        button3.show()

        button4 = gtk.Button("Practice!")
        button4.connect("clicked", self.clicked_practice)
        button4.show()

        button5 = gtk.Button("Open Practice File")
        button5.connect("clicked", self.clicked_practicefile)
        button5.show()
        
        fontdesc = pango.FontDescription('monospace')
        self.textview.modify_font(fontdesc)
        scroll = gtk.ScrolledWindow()
        scroll.add(self.textview)
        self.textview.show()


        table.attach(button1, 0, 1, 0, 1)
        table.attach(button2, 0, 1, 1, 2)
        table.attach(button3, 0, 1, 2, 3)
        table.attach(button4, 1, 4, 3, 4)
        table.attach(button5, 0, 1, 3, 4)
        table.attach(scroll, 1, 4, 0, 3)


        window.show_all()





    def clicked_play(self, widget):
        if not self.practicethread.isAlive():
            filename = self.filename

            if filename == "":
                parent = None
                alert = gtk.MessageDialog(parent, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                  gtk.BUTTONS_CLOSE, "Please Select a File")
                alert.run()
                alert.destroy()


            else :

                self.proc = subprocess.Popen(["timidity", filename])


    def clicked_open_file(self, widget):
        
        if not self.practicethread.isAlive():
        
            chooser = gtk.FileChooserDialog(title="Open a file",action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                  buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        
            # create filter
            f = gtk.FileFilter()
            f.set_name("Midi Files")
            f.add_pattern("*.mid")
            chooser.add_filter(f)
        
            response = chooser.run()
            if response == gtk.RESPONSE_OK :
                # Flush the screen
                self.flush_text()
                res = chooser.get_filename()
                self.filename = res
                self.insert_text("File Selected : " + os.path.basename(res).rstrip(".mid"))

            chooser.destroy()

    def clicked_stop(self, widget=None):

        if self.practicethread.isAlive():
            self.practicethread.stop()
           
            
            confirm = gtk.MessageDialog(None, gtk.DIALOG_MODAL,
                                   gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO,
                                   "Do you want to save your progress?")
            
            response = confirm.run()
            confirm.destroy()
            if response == gtk.RESPONSE_YES :
            
                dialog = gtk.FileChooserDialog("Please choose a file", action=gtk.FILE_CHOOSER_ACTION_SAVE,
                         buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
                # Chose a default directory for the file
                dialog.set_current_folder("/home/ajit/Study/project/Improvisor/saved/")         
                dialog.set_current_name(os.path.basename(self.filename).rstrip(".mid"))
            
                dialog.run()
                save_file = dialog.get_filename()
                dialog.destroy()
                if not save_file.endswith('.im'):
                    save_file += '.im'  

                    
                temp = [self.filename, self.position]
                pickle.dump(temp, open(save_file, 'w'))
            
            
        if self.proc :
            self.proc.terminate()
            self.proc.wait()
            self.proc = False

        else :
            return


    def clicked_practicefile(self, widget):
        
        if not self.practicethread.isAlive():
        
            chooser = gtk.FileChooserDialog(title="Open a file",action=gtk.FILE_CHOOSER_ACTION_OPEN,
                                  buttons=(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        
            chooser.set_current_folder("/home/ajit/Study/project/Improvisor/saved/")
            # create filter
            f = gtk.FileFilter()
            f.set_name("Practice Files")
            f.add_pattern("*.im")
            chooser.add_filter(f)
        
            response = chooser.run()
            if response == gtk.RESPONSE_OK:
                self.filename = False
                res = chooser.get_filename()
        
                pkl_file = open(res, 'rb')
                data = pickle.load(pkl_file)
                self.filename = data[0]
                self.position = data[1] 
        
                self.flush_text()
            
                self.insert_text("File Selected : " + os.path.basename(res).rstrip(".mid"))
            chooser.destroy()
        


    def insert_text(self, text):
        self.textview.get_buffer().insert_at_cursor(text+"\n")

    def flush_text(self):
        start, end = self.textview.get_buffer().get_bounds()
        self.textview.get_buffer().delete(start, end)


    def clicked_practice(self, widget):
        # Start the method practice in a new thread
        #threading.Thread(target=self.practice) .start()
        self.practicethread = MyThread(target=self.practice)
        self.practicethread.start()


    # The Practice Script Goes here
    def practice(self):
        if not self.filename:
            parent = None
            alert = gtk.MessageDialog(parent, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO,
                  gtk.BUTTONS_CLOSE, "Please Select a File")
            alert.run()
            alert.destroy()

        else:
            pattern = midi.read_midifile("%s" %(self.filename))
            pattern.make_ticks_abs()
            track = pattern[0]
            

            
            # While loop checks if thread is stopped
            while not self.practicethread.stopped():
                self.position = bar.extract_bar(self.position, pattern)

                
                
                
                # Getting the unique notes in midifile 
                midi_values = []
                
                temp_pattern = midi.read_midifile("temp.mid")
                for event in temp_pattern[0]:
                    if(isinstance(event, midi.NoteOnEvent)):
                        midi_values.append(event.pitch)
                        
                  
                # Initialize the stack 
                stack = []
                # We append the ticks of the user to the stack variable
                stack.append(midi_values)
                
                while stack:
                    # Compute Unique notes and also the number of times they occur
                    comp_notes = []
                    
                    for key, iter in itertools.groupby(midi_values):
                        comp_notes.append([key, len(list(iter))])
                
                
                    # Return the result of insert_text to the main thread
                    gobject.idle_add(self.insert_text, "\nPlaying a new section of the song\nListen Carefully!\n----------------------")
                
                    play = subprocess.Popen(["timidity", "temp.mid"])
                    play.communicate()
                   
                
                    # real time pitch detection
                
                    gobject.idle_add(self.insert_text, "\n Try to Play what You've just heard\n------------------------")
                   
                    user_play = pitch.pitches()
                
                    
                   
                    # Getting the unique notes in user_play. We give a score to each note depending upon its prominence or length of sequence
                    user_notes = []
                    for key, iter in itertools.groupby(user_play):
                        user_notes.append([key, len(list(iter))])
                
                     
                    
                    """
                    Now we could eliminate singular detected pitches from user_play. 
                    It would require user to play the phrase very slowly so that only useful pitches
                    appear multiple times in continum. But the results would be more accurate
                    I'll leave it to user to decide if he wants to implement this
                
                    """
                    for note in user_notes:
                        if note[1] == 1:
                            user_notes.remove(note)          
                    
                     
                    print "user_notes", user_notes   
                
                    # We are just checking if all the notes in midi are also present in user recording in the same order 
                    absolute_user = map(list, zip(* user_notes))[0]
                    absolute_comp = map(list, zip(* comp_notes))[0] 
                    print "absolute user notes", absolute_user
                    print "absolute computer notes", absolute_comp
                
                    x = [i for i, j in zip(absolute_comp, absolute_user) if i == j] 
                    boolean_value = (set(x) == set(absolute_comp))
                 
               
                
                
                
                    if boolean_value:
                    
                        midi_values = stack.pop()
                    
                   
                    
                
                    else :
                        
                       
                        new_temp = genetic.genetic(comp_notes, user_notes)
                        stack.append(new_temp)
                        
                        
                    
                        # Code to write new temp to a midi file. 
                    
                        onevents = [x  for x in temp_pattern[0] if isinstance(x, midi.NoteOnEvent)]
                        offevents = [x for x in temp_pattern[0] if isinstance(x, midi.NoteOffEvent)]
                    
                        for i, j in zip(onevents, new_temp):
                            i.set_pitch(j)
                        for i, j in zip(offevents, new_temp):
                            i.set_pitch(j)

                        track = map(list, zip(onevents, offevents))
                        track = list(itertools.chain(*track))
                    
                        track.append(midi.EndOfTrackEvent())
                        new_pattern = midi.Pattern()
                        new_pattern.append(track)
                    
                        midi.write_midifile("temp.mid", new_pattern)
                        
                        midi_values = new_temp

                    
                # We've moved out of the loop
                gobject.idle_add(self.insert_text, "\n Well Done. We'll Move to the next section\n")
                
                # Check If we've reached the end of track
                
                if(track[-1].tick == self.position):
                    break
          
            
            
            
            
            
            # Flush the screen
            gobject.idle_add(self.flush_text)
            self.filename = False


    def main(self):
        signal.signal(signal.SIGTERM, self.clicked_stop)
        gtk.main()
        return 0




Teacher().main()
