from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Tasks(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    def __str__(self):
        return self.title

class ScheduleCalendar(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schedule_cal", blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.owner}'s {self.name} calendar"

class MiscellanousCalendar(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="misc_cal")
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.owner}'s {self.name} calendar"

class Schedule(models.Model):
    NAME_CHOICES = (
        ("0", "Master"),
        ("1", "Monday"),
        ("2", "Tuesday"),
        ("3", "Wednesday"),
        ("4", "Thursay"),
        ("5", "Friday"),
        ("6", "Saturday"),
        ("7", "Sunday")
    )

    VALUE_CHOICES = ((1,"Main"),(2,"Alt1"),(3,"Alt2"))

    calendar = models.ForeignKey(ScheduleCalendar,on_delete=models.CASCADE, related_name="day_schedule", blank=True)
    name = models.CharField(max_length=255, choices=NAME_CHOICES)
    value = models.IntegerField(choices=VALUE_CHOICES, default=1, blank=True)

    class Meta:
        ordering = ["name"]
        unique_together = [["calendar", "name", "value"]]

    def __str__(self):
        return f"{self.calendar}'s {self.get_name_display()} schedule"

class DailyEvent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class MiscEvent(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    calendar = models.ForeignKey(MiscellanousCalendar, on_delete=models.CASCADE)

    def __str__(self):
        return self.title