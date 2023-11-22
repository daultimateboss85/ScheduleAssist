from rest_framework import serializers
from testing.models import ScheduleCalendar, Schedule, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]

class CalendarSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ScheduleCalendar
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["owner"].required = False
       


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"
        depth = 1