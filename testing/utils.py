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
    if delta_or_time == "delta":
        return difference

    else:
        return time(difference.hour, difference.minute, difference.second)

def add_times(first_time, second_time, delta_or_time):
    """return addition of two times
    - if delta_or_time="delta" return type is timedelta
    - else type time"""
    sum = datetime.combine(date.min, first_time) + datetime.combine(date.min, second_time)
    if delta_or_time == "delta":
        return sum

    else:
        return time(sum.hour, sum.minute, sum.second)

#what if no event after preevent
#what if first event is postevent
def new_save_with_overlap(event, other_events):
    #straight up copying events so can reset state if things go wrong
    new_copy = copy.deepcopy(other_events)
    #other_events should be ordered 
    print(other_events) 

    #some constants needed 
    zero_time = time(0)
    one_day = timedelta(days=1)
    
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
            post_queue.append(postevent)
            break       
        
        else:
            #means start of event is same as start of another event
            #its ambiguous the way to shift such an event
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
            preevent.start_time =  subtract_times(preevent.start_time, preshift)  
            preevent.end_time = subtract_times(preevent.end_time, preshift)

            #if it goes out of range raise value error
            if preevent.start_time <  zero_time:
                raise ValueError
            
            #else save
            else:
                preevent.save(bypass=True)
                new_prev = previous_queue.pop() #event prior to preevent
                if preevent.start_time < new_prev.end_time: #if it doesnt need to be shifted we are done else repeat
                    preevent = new_prev
                
                else:
                    done = True

    if postshift:
        pass 


    event.save(bypass=True)
   
    
    ######################################################
    
    for (i, other_event) in enumerate(other_events):
        if  other_event.start_time < event.start_time < other_event.end_time:
            preevent = other_event
            previous_queue = other_events[:i+1][::-1] #reverse list up to preevent


        if  other_event.start_time < event.end_time < other_event.end_time:
            postevent = other_event
            post_queue = other_events[i:] #all events after new event


    
# if only one found continue with algorithm
# if none found save with bypass = true
# if two found
#     if not same event 
#         continue with algorithm
#     else
#         return false - means event is contained in another and we aint doin all at

# copyset = copy other_events

# if preevent:
#     pre_shift_needed = preevent.end_time - new_event.start_time

#     done = False
#     while not done:
        
#         preevent.start_time -= pre_shift_ needed
#         preevent.end_time -= pre_shift_needed

#         if preevent.start_time > time(0):
#             preevent.save(bypass = True)

        
#             next_in_line = prev_queue.dequeue
#             if preevent.start_time between next_in_line start and end time:
#                 preevent = next_in_line
#             else:
#                 done = True
#         else:
#             return False
#             iterate through copy and restore db

# if postevent:
#     post_shift_needed = newevent.end_time - postevent.start_time




def save_with_overlap(event, other_events):
    # just a bad event
    if event.start_time > event.end_time:
        return False

    # finding event that overlaps with event to be saved
    for other_event in other_events:
        if other_event.start_time < event.start_time < other_event.end_time:
            # backward shift for events that come before one to be saved
            pre_shift_needed = other_event.end_time - event.start_time

        # forward shift for events that come after
        if other_event.start_time < event.end_time < other_event.end_time:
            post_shift_needed = event.end_time - other_event.start_time

    # changing shifts into datetimes for easy calculations
    pre_shift_needed, post_shift_needed = datetime.combine(
        date.min, pre_shift_needed
    ), datetime.combine(date.min, post_shift_needed)

    # copying other events in case things go awry we can revert
    event_set_copy = copy.deepcopy(other_events)

    zero_time = timedelta(0)
    one_day = timedelta(days=1)

    try:
        # for every other event
        for other_event in other_events:
            # shifting events before
            # if event before new event to be added
            if other_event.start_time < event.start_time:
                temp = datetime.combine(date.min, other_event.start_time)
                with_shift = temp - pre_shift_needed

                # check if subtracting necessary thing doesnt take it out of bounds of normal time
                # if so shift it back and save bypassing checking for conflicting times
                if with_shift > zero_time:
                    other_event.start_time = time(
                        with_shift.hour, with_shift.minute, with_shift.second
                    )

                    temp = (
                        datetime.combine(date.min, other_event.end_time)
                        - pre_shift_needed
                    )
                    other_event.end_time = time(temp.hours, temp.minute, temp.second)

                    other_event.save(bypass=True)
                    # timedelta(other_event.end_time.hours, other_event.end_time.minute, other_event.end_time.second)

                # else raise error
                else:
                    raise ValueError("Unsuccessful attempt to shift events")

            else:
                # if event comes after new event to be added
                temp = datetime.combine(date.min, other_event.start_time)
                with_shift = temp + post_shift_needed

                # if shifting event doesnt cause it to go out of bounds
                # shift event times and save bypassing checking for conflicting times
                if with_shift < one_day:
                    other_event.start_time = time(
                        with_shift.hour, with_shift.minute, with_shift.second
                    )

                    temp = (
                        datetime.combine(date.min, other_event.end_time)
                        - pre_shift_needed
                    )
                    other_event.end_time = time(temp.hours, temp.minute, temp.second)

                    other_event.save(bypass=True)

                else:
                    raise ValueError("Unsuccessful attempt at shifting events")
        
        event.save()
        
    except ValueError:
        # reverting to original state
        for original_event in event_set_copy:
            original_event.save(bypass=True)

        return False
