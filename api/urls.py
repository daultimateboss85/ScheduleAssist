from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




urlpatterns = [
    path("", views.getRoutes),

    #get schedulecalendars, make new ones
    path("ScheduleCalendars/", views.ScheduleCalendarList.as_view(), name="schedulecalendar-list"),

    #get schedulecalendar, update, delete
    path("ScheduleCalendars/<str:pk>", views.ScheduleCalendarItem.as_view(), name="schedulecalendar-item"),

    #get schedules for a calendar, make new ones
    path("ScheduleCalendars/<str:cal_id>/Schedule", views.ScheduleList.as_view(), name="schedule-list"),

    #get schedule, update, delete
    path("Schedule/<str:pk>", views.ScheduleItem.as_view(), name="schedule-item"), 

    #get events in a schedule/ create a new event in schedule
    path("Schedule/<str:sched_id>/events", views.DailyEventList.as_view(), name="event-list"),

    #get event, update, delete
    path("events/<str:pk>", views.DailyEventItem.as_view(), name="event-item"),


    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


 
]
   
"""     

     """