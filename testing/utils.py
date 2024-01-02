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

def find_overlap(event, other_events):
     for other_event in other_events:
            if (
                event.end_time == other_event.end_time
                or other_event.start_time < event.start_time < other_event.end_time
                or other_event.start_time < event.end_time < other_event.end_time
            ):
                raise ValueError("Bad times")  # describe this
     