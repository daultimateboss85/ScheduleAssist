from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    last_viewed_cal = models.OneToOneField(
        "ScheduleCalendar", on_delete=models.SET_NULL, null=True, blank=True
    )

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not update_fields:
            default_calendar = ScheduleCalendar.objects.create(
                name="Default Calendar", owner=self
            )
            self.last_viewed_cal = default_calendar
            super().save(
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=update_fields,
            )

        else:
            super().save(
                force_insert=force_insert,
                force_update=force_update,
                using=using,
                update_fields=update_fields,
            )


class Tasks(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return self.title


class MiscellanousCalendar(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="misc_cal", blank=True
    )
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.owner}'s {self.name} calendar"


class Schedule(models.Model):
    NAME_CHOICES_VALUES = {
        "0": "Master",
        "1": "Monday",
        "2": "Tuesday",
        "3": "Wednesday",
        "4": "Thursay",
        "5": "Friday",
        "6": "Saturday",
        "7": "Sunday",
    }

    VALUE_CHOICES_VALUES = {"1": "Main", "2": "Alt1", "3": "Alt2"}

    NAME_CHOICES = (
        ("0", "Master"),
        ("1", "Monday"),
        ("2", "Tuesday"),
        ("3", "Wednesday"),
        ("4", "Thursay"),
        ("5", "Friday"),
        ("6", "Saturday"),
        ("7", "Sunday"),
    )

    VALUE_CHOICES = ((1, "Main"), (2, "Alt1"), (3, "Alt2"))

    calendar = models.ForeignKey(
        "ScheduleCalendar",
        on_delete=models.CASCADE,
        blank=True,
    )
    name = models.CharField(max_length=255, choices=NAME_CHOICES, blank=True)
    value = models.IntegerField(choices=VALUE_CHOICES, default=1, blank=True)

    class Meta:
        ordering = ["name", "value"]
        unique_together = [["calendar", "name", "value"]]

    def __str__(self):
        return f"{self.calendar}'s {self.get_name_display()} schedule"

    @property
    def events_set(self):
        return self.events.all()


class ScheduleCalendar(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="schedule_cals", blank=True
    )
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.owner}'s {self.name} calendar"

    @property
    def schedules_set(self):
        return self.schedule_set.values("id", "name", "value")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        for i in range(8):
            schedule = Schedule.objects.create(calendar=self, name=str(i))


class DailyEvent(models.Model):
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True, null=True)
    start_time = models.TimeField(blank=True)
    end_time = models.TimeField(blank=True)
    schedule = models.ForeignKey(
        Schedule, on_delete=models.CASCADE, blank=True, related_name="events"
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["start_time"]

    def save(self,*args, **kwargs):

        unsaved = self.id is None
        
        if unsaved:
            other_events = self.schedule.events_set
        else:
            other_events = self.schedule.events_set.exclude(id=self.id)

        for other_event in other_events:
            if (
                self.start_time == other_event.start_time or 
                self.end_time  == other_event.end_time or
                other_event.start_time < self.start_time < other_event.end_time
                or other_event.start_time < self.end_time < other_event.end_time
            ):
                raise ValueError("Bad times") #describe this
            
         # if the end_time is less than the start_time ie start something today and end tomorrow return false
        if self.start_time >= self.end_time:
            raise ValueError("Bad times") #describe this

        else:
            super().save(*args, **kwargs)

        
            


class MiscEvent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    calendar = models.ForeignKey(MiscellanousCalendar, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
