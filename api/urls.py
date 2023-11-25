from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)




urlpatterns = [
    path("", views.getRoutes),

    #get schedulecalendars, make new ones
    path("ScheduleCalendars/", views.ScheduleCalendarList.as_view()),

    #get schedulecalendar, update, delete
    path("ScheduleCalendars/<str:pk>", views.ScheduleCalendarItem.as_view()),

    #get schedules for a calendar, make new ones
    path("ScheduleCalendars/<str:cal_id>/Schedule", views.ScheduleList.as_view()),

    #get schedule, update, delete
    path("Schedule/<str:pk>", views.ScheduleItem.as_view()), 

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


 
]
   
"""     

     """