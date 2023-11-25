from testing.models import ScheduleCalendar, Schedule, DailyEvent
from django.http import Http404
from .serializers import CalendarSerializer, ScheduleSerializer, EventSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
def getRoutes(request):
    return Response("Under construction")


class ScheduleCalendarList(APIView):
    """
    List all schedulecalendars or create a new one.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        calendars = ScheduleCalendar.objects.filter(owner=request.user)
        serializer = CalendarSerializer(calendars, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = CalendarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# implement update and delete
class ScheduleCalendarItem(APIView):
    """
    Retrieve, Update or Delete a ScheduleCalendar instance.
    """

    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        try:
            return ScheduleCalendar.objects.filter(owner=request.user).get(pk=pk)
        except ScheduleCalendar.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        calendar = self.get_object(request, pk)
        serializer = CalendarSerializer(calendar, many=False)
        return Response(serializer.data)

    def put(self, request, pk):
        calendar = self.get_object(request, pk)
        serializer = CalendarSerializer(instance=calendar, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        calendar = self.get_object(request, pk)
        calendar.delete()

        return Response({"Deleted": "true"})


class ScheduleList(APIView):
    """
    List all Schedules in a given ScheduleCalendar
    """

    permission_classes = [IsAuthenticated]

    def get_calendar(self, request, cal_id):
        try:
            return ScheduleCalendar.objects.filter(owner=request.user).get(pk=cal_id)
        except Schedule.DoesNotExist:
            raise Http404

    def get(self, request, cal_id):
        """
        getting all schedules that belong to a calendar
        """
        schedules = Schedule.objects.filter(calendar=self.get_calendar(request, cal_id))
        serializer = ScheduleSerializer(schedules, many=True)

        return Response(serializer.data)

    #test post
    def post(self, request, cal_id):
        """
        create schedule belonging to a calendar
        """
        calendar = self.get_calendar(request, cal_id)
        serializer = ScheduleSerializer(data=request.data)

        if serializer.is_valid():
            value = serializer.validated_data.get("value", 1)
            serializer.save(
                calendar=calendar, value=value
            )  # setting the calendar and value of schedule

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScheduleItem(APIView):
    """
    Retrieve, Update or Delete a Schedule instance.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        #also makes sure user is owner of schedule to be modified
        """
        i could also add an owner attribute to schedule model and query that way... however
        right now i feel i could sacrifice speed for space... to be fair my app is small 
        and extra space or speed should be inconsequential, but i could also easily refactor to
        add owner attribute later on rather than the other way round
        """
        try:
            schedule = Schedule.objects.get(pk=pk)
        
        except Schedule.DoesNotExist:
            raise Http404
        


        if schedule.calendar.owner == request.user:
            return schedule
        
        else:
            return Response({"Denied": "bad request"})
            

    def get(self, request, pk):
    
        schedule = self.get_object(request, pk)
        serializer = ScheduleSerializer(schedule, many=False)

        return Response(serializer.data)


    def put(self, request, pk):

        schedule = self.get_object(request, pk)
        serializer = ScheduleSerializer(instance=schedule, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):

        schedule = self.get_object(request, pk)
        schedule.delete()

        return Response({"deleted":"true"})


class DailyEventList(APIView):
    """
    List daily events / create daily event
    """
    permission_classes = [IsAuthenticated]

    def get_schedule(self, request, sched_id):
        #make sure you own schedule
        try:
            schedule = Schedule.objects.get(pk=sched_id)
            
        except Schedule.DoesNotExist:
            return Response({"bad request"})
        
        if schedule.calendar.owner == request.user:
                return schedule
            
        else:
            return Response({"unauthorized"})
    
    def get(self, request, sched_id):
        schedule = self.get_schedule(request, sched_id)

        events = DailyEvent.objects.filter(schedule=schedule)

        serializer = EventSerializer(events, many=True)
        
        return Response(serializer.data)

    def post(self, request, sched_id):

        schedule = self.get_schedule(request, sched_id)

        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            new =   serializer.save(schedule=schedule)
            new_serializer = EventSerializer(new)
            return Response(new_serializer.data)

