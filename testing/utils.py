from datetime import datetime, date, timedelta, time
import copy


def is_good_event(event, other_events):
    for other_event in other_events:
        if (
            event.start_time == other_event.start_time
            or event.end_time == other_event.end_time
            or other_event.start_time < event.start_time < other_event.end_time
            or other_event.start_time < event.end_time < other_event.end_time
        ):
            raise ValueError("Bad times")  # describe this

    # if the end_time is less than the start_time ie start something today and end tomorrow return false
    if event.start_time >= event.end_time:
        raise ValueError("Bad times")  # describe this

    return True

def subtract_times(first_time, second_time, delta_or_time):
    """return subtraction of two times
    - if delta_or_time="delta" return type is timedelta
    - else type time"""
    difference = datetime.combine(date.min, first_time) - datetime.combine(date.min, second_time)
    
    if difference < timedelta(0):
        raise ValueError
    
    if delta_or_time == "delta":
        return difference

    else:
        return time(difference.hour, difference.minute, difference.second)

def add_times(first_time, second_time):
    """return addition of two times"""
    #no intrinsic solution for this

    addition = (timedelta(hours=first_time.hour, minutes=first_time.minute, seconds=first_time.second) + timedelta(hours=second_time.hour, minutes=second_time.minute,  seconds=second_time.second))

    seconds = addition.seconds

    if addition.days:
        raise ValueError
    
    hour = seconds // 3600
    minute = (seconds % 3600) // 60
    seconds = (seconds % 3600) % 60

    return time(hour, minute, seconds)

#what if no event after preevent
#what if first event is postevent
def new_save_with_overlap(event, other_events):
    #straight up copying events so can reset state if things go wrong
    other_events = list(other_events)
    new_copy = copy.deepcopy(other_events)
    #other_events should be ordered 
    print(other_events) 

    try:
        #some constants needed 
        zero_time = time(0)
        
        preevent = None
        postevent = None
        preshift = None
        postshift = None    

        previous_queue = [] 
        post_queue = [] 

        #logic here is bcuz times are ordered, when difference switches from positive to negative we have found event before and after
        for i, other_event in enumerate(other_events):
            difference = subtract_times(event.start_time, other_event.start_time)

            if difference > zero_time:
                preevent = other_event
                previous_queue.append(preevent)

            elif difference < zero_time:
                postevent = other_event
                post_queue = other_events[i+1:]
                break       
            
            else:
                #means start of event is same as start of another event
                #its ambiguous the way to shift such an event
                #no event has been touched yet so just return false
                return False

        #now check if new event overlaps preevent or postevent
        #we already know their start time's relation to new event
        if event.start_time < preevent.end_time:
            preshift = subtract_times(preevent.end_time, event.start_time)

        if event.end_time > postevent.start_time:
            postshift = subtract_times(event.end_time, postevent.start_time)

        if preshift:
            #shifting events prior to new event to make space for it
            done = False
            previous_queue.pop() #removing preevent from previous queue

            while not done:
                #shift preevent backwards
                try:
                    preevent.start_time =  subtract_times(preevent.start_time, preshift)  
                    preevent.end_time = subtract_times(preevent.end_time, preshift)
                except ValueError: #if shifted out of range value error is raised
                    raise ValueError
                       
                preevent.save(bypass=True)
                new_prev = previous_queue.pop() #event prior to preevent
                if preevent.start_time < new_prev.end_time: #if it doesnt need to be shifted we are done else repeat
                    preevent = new_prev
                
                else:
                    done = True

        if postshift:
            done = False
            post_queue.reverse() #i think reversing the popping from the end might be more efficient overall

            while not done:
                #shift postevent backwards
                try:
                    postevent.start_time =  add_times(postevent.start_time, postshift)  
                    postevent.end_time = add_times(postevent.end_time, postshift)
                #if it goes out of range raise value error add_times raises valueerror
                except ValueError: 
                    raise ValueError

                #if it doesnt go out of range
                
                postevent.save(bypass=True)
                new_prev = post_queue.pop() #event prior to postevent
                if postevent.end_time > new_prev.start_time_time: #if it no need to be shifted we are done else repeat
                    postevent = new_prev
                    
                else:
                    done = True


        event.save(bypass=True)
    
        return True
    
    except ValueError:
        #returning to prior state
        for other_event in new_copy:
            event.save(bypass=True)
        return False
    
