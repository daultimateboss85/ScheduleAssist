from testing.models import ScheduleCalendar, Schedule, DailyEvent
from django.http import Http404
from .serializers import CalendarSerializer, ScheduleSerializer, EventSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser


import json

from .utils import get_calendar, get_schedule, get_event


@api_view(["GET"])
def getRoutes(request):
    return Response("Under construction")


class LastViewedCalendar(APIView):
    """
    Set and get persons last viewed calendar
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get user's last viewed calendar"""

        last_viewed_calendar = (
            request.user.last_viewed_cal
        )  # this should always return a calendar as calendars are created upon user creation

        if last_viewed_calendar:
            return Response({"id": last_viewed_calendar.id})

        return Response("No last viewed Calendar", status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """Set last viewed calendar"""
        id = request.data.get("id", None)

        if id:
            cal = get_calendar(request, int(id))

            if cal:
                request.user.last_viewed_cal = cal
                request.user.save()

                return Response("Last calendar set")

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ScheduleCalendarList(APIView):
    """
    List all schedulecalendars or create a new one.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        calendars = ScheduleCalendar.objects.filter(owner=request.user)

        if calendars:
            serializer = CalendarSerializer(calendars, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = CalendarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleCalendarItem(APIView):
    """
    Retrieve, Update or Delete a ScheduleCalendar instance.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return get_calendar(request, pk)

    def get(self, request, pk):
        calendar = self.get_object(request, pk)

        if calendar:
            serializer = CalendarSerializer(calendar, many=False)
            request.user.last_viewed_cal = calendar
            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        calendar = self.get_object(request, pk)

        if calendar:
            serializer = CalendarSerializer(instance=calendar, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        calendar = self.get_object(request, pk)

        if calendar:
            calendar.delete()

        return Response({"Deleted": "true"})


class ScheduleList(APIView):
    """
    List all Schedules in a given ScheduleCalendar
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, request, cal_id):
        return get_calendar(request, cal_id)

    def get(self, request, cal_id):
        """
        getting all schedules that belong to a calendar
        """
        calendar = self.get_object(request, cal_id)

        if calendar:
            schedules = Schedule.objects.filter(calendar=calendar)

            if schedules:
                serializer = ScheduleSerializer(schedules, many=True)
                return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    # test post
    def post(self, request, cal_id):
        """
        create schedule belonging to a calendar
        """
        calendar = self.get_object(request, cal_id)

        if calendar:
            serializer = ScheduleSerializer(data=request.data)

            if serializer.is_valid():
                value = serializer.validated_data.get("value", 1)
                newly_created = serializer.save(
                    calendar=calendar, value=value
                )  # setting the calendar and value of schedule

                # so that newly created object can be returned, might refactor
                new_serializer = ScheduleSerializer(newly_created)

                return Response(new_serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ScheduleItem(APIView):
    """
    Retrieve, Update or Delete a Schedule instance.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return get_schedule(request, pk)

    def get(self, request, pk):
        schedule = self.get_object(request, pk)

        if schedule:
            serializer = ScheduleSerializer(schedule, many=False)

            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        schedule = self.get_object(request, pk)

        if schedule:
            serializer = ScheduleSerializer(instance=schedule, data=request.data)

            if serializer.is_valid():
                new_schedule = serializer.save()
                new_serializer = ScheduleSerializer(new_schedule)

                return Response(new_serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        schedule = self.get_object(request, pk)

        if schedule:
            schedule.delete()

            return Response({"deleted": "true"})

        return Response(status=status.HTTP_400_BAD_REQUEST)


class DailyEventList(APIView):
    """
    List daily events / create daily event
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, request, sched_id):
        return get_schedule(request, sched_id)

    def get(self, request, sched_id):
        schedule = self.get_object(request, sched_id)

        if schedule:
            events = DailyEvent.objects.filter(schedule=schedule)
            serializer = EventSerializer(events, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, sched_id):
        schedule = self.get_object(request, sched_id)

        if schedule:
            serializer = EventSerializer(data=request.data)

            if serializer.is_valid():
                print("hey im valid")
                try:
                    newly_created = serializer.save(schedule=schedule)
                    new_serializer = EventSerializer(newly_created)
                    return Response(new_serializer.data, status=status.HTTP_200_OK)

                except ValueError:
                    return Response("INvalid times", status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class DailyEventItem(APIView):
    """Retrieve, update and delete daily events"""
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return get_event(request, pk)

    def get(self, request, pk):
        event = self.get_object(request, pk)

        if event:
            serializer = EventSerializer(event)
            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        event = self.get_object(request, pk)

        if event:
            serializer = EventSerializer(instance=event, data=request.data)

            if serializer.is_valid():
                # making sure no clashes between events
                try:
                    newly_created = serializer.save()
                    new_serializer = EventSerializer(newly_created)
                    return Response(new_serializer.data)

                except ValueError:
                    return Response("Invalid times", status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = self.get_object(request, pk)

        if event:
            event.delete()
            return Response({"deleted": "true"})

        return Response(status=status.HTTP_400_BAD_REQUEST)


class CopySchedule(APIView):
    """Copy a schedule into other schedule(s)"""
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    # copy from_id schedule into to_id schedule

    def get_object(self, request, sched_id):
        return get_schedule(request, sched_id)

    def put(self, request, from_id):
        from_schedule = self.get_object(request, from_id)

        if from_schedule:
            #get list of schedules to copy to from body of request
            #for each in list, copy from_schedule into each

            for to_id in request.data["schedules"]:
            
                to_schedule = self.get_object(request, to_id)
                if to_schedule:

                    for event in to_schedule.events_set:
                        event.delete()

                    for event in from_schedule.events_set:
                        DailyEvent.objects.create(
                            title=event.title,
                            start_time=event.start_time,
                            end_time=event.end_time,
                            description=event.description,
                            schedule=to_schedule,
                        )
                else:
                    return Response({"message":"Couldnt copy some schedules"}, status=status.HTTP_400_BAD_REQUEST)
                    
            return Response({"copied"})

        return Response(status=status.HTTP_400_BAD_REQUEST)
 

class ClearSchedule(APIView):
    """Clear a Schedule"""
    
    permission_classes = [IsAuthenticated]
    
    def get_object(self, request, sched_id):
        return get_schedule(request, sched_id)
    
    def put(self, request, sched_id):
        schedule = self.get_object(request, sched_id)

        if schedule:
            events = schedule.events_set
            for event in events:
                event.delete()

            return Response({"message":"Schedule Cleared"})

        return Response({"message":"Bad request"}, status.HTTP_400_BAD_REQUEST)
    