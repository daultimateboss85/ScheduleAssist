from rest_framework import serializers
from testing.models import ScheduleCalendar, Schedule, User, DailyEvent


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance:
            try:
                for object in self.instance:
                    object.name = Schedule.NAME_CHOICES_VALUES[object.name]

            except:
                self.instance.name = Schedule.NAME_CHOICES_VALUES[self.instance.name] 

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = DailyEvent
        fields = "__all__"
        depth = 1
