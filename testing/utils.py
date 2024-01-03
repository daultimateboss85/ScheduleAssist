from datetime import datetime,timedelta, time
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


def save_With_overlap(event, other_events):
    #just a bad event
    if event.start_time > event.end_time:
        return False

    #finding event that overlaps with event to be saved
    for other_event in other_events:
        if other_event.start_time < event.start_time < other_event.end_time:
            #backward shift for events that come before one to be saved
            pre_shift_needed = other_event.end_time - event.start_time
        
        #forward shift for events that come after
        if other_event.start_time < event.end_time < other_event.end_time:
            post_shift_needed = event.end_time - other_event.start_time
    
    #changing shifts into datetimes for easy calculations
    pre_shift_needed, post_shift_needed = datetime.combine(pre_shift_needed), datetime.combine(post_shift_needed)
    #copying other events in case things go awry we can revert
    event_set_copy = copy.deepcopy(other_events)

    try:
        for other_event in other_events:
            #shifting events before
            if other_event.start_time < event.start_time:
                temp = other_event.start_time

    except:
        return False