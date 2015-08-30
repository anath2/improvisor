import itertools
import midi
import random


def genetic(comp_notes, user_notes):
    
    comp_unique = map(list, zip(* comp_notes))[0]
    comp_times = map(list, zip(* comp_notes))[1]
    
           
    user_new = [ x if x in dict(user_notes) else None for x in comp_unique]
    
    user_notes = dict(user_notes)
    
    # We define a function for random weighted choice.
    
    def weighted_random_choice(choices):
        max = sum(choices.values())
        pick = random.uniform(0, max)
        current = 0
        for key, value in choices.items():
            current += value
            if current > pick:
                return key
    
    user_new = [x if(x != None) else weighted_random_choice(user_notes) for x in user_new]
    
    # Do the genetic crossover operation and replace half of the wrong notes. 
    pack = map(list, zip(comp_unique, user_new))
    
    indices = []
    
    for a in pack:
        if a[0] != a[1]:
            indices.append(pack.index(a))
     
    # Replace half of the bad notes        
    indices = random.sample(set(indices), len(indices) / 2)
    
    if indices != []:
        # Swapping values 
        for i in indices:
            pack[i][0], pack[i][1] = pack[i][1], pack[i][0]
        
        # Return the modified user notes 
        
        user_new = map(list, zip(*pack))[1]
        user_new = map(list, zip(user_new, comp_times))
        notes = [[x[0]]*x[1] for x in user_new]
        
        notes =  list(itertools.chain(*notes))
 
        return notes 
     
    else:    
        notes = [[x[0]]*x[1] for x in comp_notes]
        notes =  list(itertools.chain(*notes))
        
        return notes

                
     
     
