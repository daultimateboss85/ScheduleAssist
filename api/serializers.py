from rest_framework import serializers
from testing.models import ScheduleCalendar, Schedule, User, DailyEvent


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class CalendarSerializer(serializers.ModelSerializer):
    schedules = serializers.SerializerMethodField()

    class Meta:
        model = ScheduleCalendar
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_schedules(self, obj):
        return obj.schedules_set


class ScheduleSerializer(serializers.ModelSerializer):
    events = serializers.SerializerMethodField()

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

    def get_events(self, obj):
        return EventSerializer(obj.events_set, many=True).data


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyEvent
        fields = "__all__"
        depth = 1

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance:
            try:
                for object in self.instance:
                    object.start_time = object.start_time.strftime("%H:%M")
                    object.end_time = object.end_time.strftime("%H:%M")

            except:
                self.instance.start_time = self.instance.start_time.strftime("%H:%M")
                self.instance.end_time = self.instance.end_time.strftime("%H:%M")
