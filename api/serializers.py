from rest_framework import serializers
from testing.models import ScheduleCalendar, Schedule


class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleCalendar
        fields = "__all__"

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"

    