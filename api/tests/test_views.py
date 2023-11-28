from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from testing.models import User, ScheduleCalendar, Schedule, DailyEvent


class AuthenticationViewTestCase(APITestCase):
    def setUp(self):
        # creating users
        dault = User.objects.create_user(
            username="daultimateboss", password="thechosenone"
        )
        batman = User.objects.create_user(username="batman", password="theshadows")

    def test_correct_credentials_token(self):
        """Test correct credentials results in a 200"""
        
        response = self.client.post(
            "/api/token/", {"username": "daultimateboss", "password": "thechosenone"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "access")

    def test_incorrect_credentials(self):
        """Test incorrect credentials results in a 404"""

        response = self.client.post(
            "/api/token/", {"username": "daultimateboss", "password": "thechosene"}
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class ScheduleCalendarViewTestCase(APITestCase):
    def setUp(self):

        # creating users
        dault = User.objects.create_user(
            username="daultimateboss", password="thechosenone"
        )
        batman = User.objects.create_user(username="batman", password="theshadows")

        # creating calendars
        daults_daily_calendar = ScheduleCalendar.objects.create(
            name="Daily Calendar", owner=dault
        )
        daults_school_calendar = ScheduleCalendar.objects.create(
            name="School calendar", owner=dault
        )

        batman_gotham_calendar = ScheduleCalendar.objects.create(
            name="Gotham", owner=batman
        )

        # creating schedules in calendars
        dault_daily_master_schedule = Schedule.objects.create(name="0", calendar=daults_daily_calendar)
        dault_daily_monday_schedule = Schedule.objects.create(name="1", calendar=daults_daily_calendar)
        
        batman_gotham_master_schedule = Schedule.objects.create(name="0", calendar=batman_gotham_calendar)

        # creating events in schedules
        dault_pray = DailyEvent(schedule=dault_daily_master_schedule, title="Pray/Read Bible" ,start_time="7:00", end_time="7:30")

