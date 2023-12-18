from django.test import TestCase
from django.urls import reverse
from django.db.models import Max

from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from testing.models import User, ScheduleCalendar, Schedule, DailyEvent


class AuthenticationViewTestCase(APITestCase):
    """Testing authentication works"""

    @classmethod
    def setUpTestData(cls):
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


class ScheduleCalendarListViewTestCase(APITestCase):
    """Testing schedule calendar list / creating new schedule calendar"""

    @classmethod
    def setUpTestData(cls):
        # creating users

        # dont forget a default calendar is auto created
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

        # calendars are auto populated with empty schedules

    def test_schedule_calendar_list_anonymoususer(self):
        """Should return an error as view needs a logged in user"""
        response = self.client.get(reverse("schedulecalendar-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_schedule_calendar_list_loggedin(self):
        """Test appropriate calendars are returned for logged in user"""
        user = User.objects.get(username="daultimateboss")
        self.client.force_authenticate(user=user)

        response = self.client.get(
            reverse("schedulecalendar-list"),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_create_calendar(self):
        """Test calendars are created"""
        user = User.objects.get(username="daultimateboss")
        self.client.force_authenticate(user=user)

        response = self.client.post(
            reverse("schedulecalendar-list"), {"name": "Gym Calendar"}
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Gym Calendar")
        self.assertEqual(user.schedule_cals.all().count(), 4)

    def test_invalid_data(self):
        """Test appropriate response message is sent"""
        user = User.objects.get(username="daultimateboss")
        self.client.force_authenticate(user=user)

        response = self.client.post(
            reverse("schedulecalendar-list"), {"nae": "Gym Calendar"}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GenTest(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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
            name="School Calendar", owner=dault
        )

        batman_gotham_calendar = ScheduleCalendar.objects.create(
            name="Gotham", owner=batman
        )

    def setUp(self):
        batman = User.objects.get(username="batman")
        dault = User.objects.get(username="daultimateboss")
        self.client.force_authenticate(user=dault)
        self.owner = dault
        self.other_owner = batman


class ScheduleCalendarItemViewTestCase(GenTest):
    def test_get_rightowner_calendarexists(self):
        """Test proper calendar is returned"""
        calendar = ScheduleCalendar.objects.get(owner=self.owner, name="Daily Calendar")
        response = self.client.get(reverse("schedulecalendar-item", args=[calendar.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Daily Calendar")

    def test_get_wrongowner_calendarexists(self):
        """Test appropriate response is returned"""
        calendar = ScheduleCalendar.objects.get(owner=self.other_owner, name="Gotham")

        response = self.client.get(reverse("schedulecalendar-item", args=[calendar.id]))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_rightowner_calendarnotexists(self):
        """Test appropriate response is returned when calendar doenst exist"""
        bad_calendar_id = ScheduleCalendar.objects.all().aggregate(Max("id"))["id__max"] + 1
        
        response = self.client.get(reverse("schedulecalendar-item", args=[bad_calendar_id]))
       
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_changing_name_validdata(self):
        """Test put endpoint"""
        cal_id = ScheduleCalendar.objects.get(owner=self.owner, name="School Calendar").id

        response = self.client.put(reverse("schedulecalendar-item", args=[cal_id]),
                                   data={"name": "Gym Calendar"})
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Gym Calendar")

    def test_put_changing_name_invaliddata(self):
        """Ensure appropriate response is returned"""

        cal_id = ScheduleCalendar.objects.get(owner=self.owner, name="School Calendar").id

        response = self.client.put(reverse("schedulecalendar-item", args=[cal_id]),
                                   data={"nam": "Gym Calendar"})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_validid(self):
        """Ensure ability to delete calendars"""

        cal_id = ScheduleCalendar.objects.get(owner=self.owner, name="School Calendar").id 


"""
T#o test
#
t#est crud  of calendars
c#rud of schedules
c#rud of events
#
creation of schedules when calendar is created
all apis"""
