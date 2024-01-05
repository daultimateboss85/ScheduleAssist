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

#work on trying to shift event one by one

"""
want ordered other_events 

iterate through other_events looking for an event where new event's start time is between its start and end time- preevent
    previous_queue = other_events[:preevent+1][::-1]


also looking for an event where new event's end time is between another's start and end time -endevent
    after_queue = other_events[postevent:]

if only one found continue with algorithm
if none found save with bypass = true
if two found
    if not same event 
        continue with algorithm
    else
        return false - means event is contained in another and we aint doin all at

copyset = copy other_events

if preevent:
    pre_shift_needed = preevent.end_time - new_event.start_time

    done = False
    while not done:
        
        preevent.start_time -= pre_shift_ needed
        preevent.end_time -= pre_shift_needed

        if preevent.start_time > time(0):
            preevent.save(bypass = True)

        
            next_in_line = prev_queue.dequeue
            if preevent.start_time between next_in_line start and end time:
                preevent = next_in_line
            else:
                done = True
        else:
            return False
            iterate through copy and restore db

if postevent:
    post_shift_needed = newevent.end_time - postevent.start_time

"""


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
