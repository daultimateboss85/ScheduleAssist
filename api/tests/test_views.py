from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from testing.models import User, ScheduleCalendar, Schedule, DailyEvent


class ViewTestCase(APITestCase):
    def setUp(self):
        #creating users
        dault = User.objects.create_user(
            username="daultimateboss", password="thechosenone"
        )
        batman = User.objects.create_user(username="batman", password="theshadows")

        #creating calendars
        daults_daily_calendar = ScheduleCalendar.objects.create(name="Daily Calendar", owner=dault)
        daults_school_calendar = ScheduleCalendar.objects.create(name="School calendar", owner=dault)

        batman_gotham_calendar = ScheduleCalendar.objects.create(name="Gotham", owner=batman)

        #creating schedules in calendars
        #daily



        #creating events in schedules

        self.factory = APIRequestFactory()

    def test_authentication(self):
        """Test user authentication"""
        user = User.objects.get(username="daultimateboss")
        response = self.client.post(
            "/api/token/", {"username": "daultimateboss", "password": "thechosenone"}
        )     

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "access")

    

    
        


""" daultimateboss_daily_cal = ScheduleCalendar.objects.create(name="Daily", owner=daultimateboss)
        batman_cal = ScheduleCalendar.objects.create(name="Daily", owner=batman)

        daultimateboss_school_cal = ScheduleCalendar.objects.create(name="School", owner=daultimateboss) """
