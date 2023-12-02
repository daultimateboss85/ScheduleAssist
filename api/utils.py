from datetime import datetime, timedelta
from .views import ScheduleCalendar, Schedule, DailyEvent

# helper functions for retrieving stuff from database
# if error in retrieving or unauthorized access they all return None


def get_calendar(request, cal_id):
    try:
        calendar = ScheduleCalendar.objects.get(pk=cal_id)
    except ScheduleCalendar.DoesNotExist:
        return None

    if request.user == calendar.owner:
        return calendar


def get_schedule(request, sched_id):
    # also makes sure user is owner of schedule to be modified
    """
    i could also add an owner attribute to schedule model and query that way... however
    right now i feel i could sacrifice speed for space... to be fair my app is small
    and extra space or speed should be inconsequential, but i could also easily refactor to
    add owner attribute later on rather than the other way round
    """
    try:
        schedule = Schedule.objects.get(pk=sched_id)
    except Schedule.DoesNotExist:
        return None

    if request.user == schedule.calendar.owner:
        return schedule

    return None


def get_event(request, event_id):
    try:
        event = DailyEvent.objects.get(pk=event_id)
    except DailyEvent.DoesNotExist:
        return None

    if request.user == event.schedule.calendar.owner:
        return event

    return None


def check_time_clash(event, start_time, end_time):
    """makes sure event to be created doesnt clash with any other event in schedule it's to be added"""
    schedule = event.schedule

    if schedule:
        events = schedule.events.all().exclude(event)
        
        # if there is a clash with any other events return False
        for other_event in events:
            if (
                other_event.start_time < start_time < other_event.end_time
                or other_event.start_time < end_time < other_event.end_time
            ):
                return False

        # if the end_time is less than the start_time ie start something today and end tomorrow return false
        if start_time >= end_time:
            return False

        else:
            return True

    return False
