from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.testHome, name="home"),
    path("adddailyevent", views.addDailyevent, name="add-daily-event"),
    path("addSchedule", views.addSchedule, name="add-schedule")
]
