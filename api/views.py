from testing.models import ScheduleCalendar, Schedule, DailyEvent
from django.http import Http404
from .serializers import CalendarSerializer, ScheduleSerializer, EventSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .utils import get_calendar, get_schedule, get_event, check_time_clash


@api_view(["GET"])
def getRoutes(request):
    return Response("Under construction")


class ScheduleCalendarList(APIView):
    """
    List all schedulecalendars or create a new one.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # remove this point of failure
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
    



# implement update and delete
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

                return Response(new_serializer.data)

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
            
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


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
                if check_time_clash(
                    request,
                    sched_id,
                    None,
                    serializer._validated_data["start_time"],
                    serializer.validated_data["end_time"],
                ):
                    newly_created = serializer.save(schedule=schedule)
                    new_serializer = EventSerializer(newly_created)
                    return Response(new_serializer.data)
                
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            

        return Response(status=status.HTTP_400_BAD_REQUEST)


class DailyEventItem(APIView):
    """Retrieve, update and delete daily events"""

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
                print("hello")
                # making sure no clashes between events
                if check_time_clash(
                    event,
                    serializer.validated_data["start_time"],
                    serializer.validated_data["end_time"],
                ):
                    newly_created = serializer.save()
                    new_serializer = EventSerializer(newly_created)
                    return Response(new_serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = self.get_object(request, pk)

        if event:
            event.delete()
            return Response({"deleted": "true"})

        return Response(status=status.HTTP_400_BAD_REQUEST)
