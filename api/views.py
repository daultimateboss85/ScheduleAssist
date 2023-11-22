from testing.models import ScheduleCalendar, Schedule
from django.http import Http404
from .serializers import CalendarSerializer, ScheduleSerializer
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


    def get_calendar(self, request,  cal_id):
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

    def post(self, request, cal_id):
        """
        create schedule belonging to a calendar
        """
        calendar = self.get_calendar(request, cal_id)
        serializer = ScheduleSerializer(request.data)

        if serializer.is_valid():
            value = serializer.validated_data.get("value", 1)
            serializer.save(
                calendar=calendar, value=value
            )  # setting the calendar and value of schedule

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
