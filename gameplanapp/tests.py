from datetime import date
from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.
from gameplanapp.models import Event, GameplanUser

User = get_user_model()


class GameplanUserModelTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        test_user = User.objects.create(
            username='test_user', password='1X<ISRUkw+tuK')
        test_user.save()
        test_user.gameplanuser.user_dateofbirth = date.today()
        test_user.gameplanuser.save()
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def testdateofbirth(self):
        user = User.objects.get(username='test_user')
        test_gameplanuser = GameplanUser.objects.get(user=user)
        self.assertEqual(test_gameplanuser.user_dateofbirth, date.today())


class EventModelTest(TestCase):
    """tests for the event model"""
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(
        username='test_user', password='1X<ISRUkw+tuK')
        test_user.save()
        test_user.gameplanuser.user_dateofbirth = date.today()
        test_user.gameplanuser.save()
        test_event = Event.objects.create(event_title="Test Event Title",
                                          event_location="Test Location", event_manager=User.objects.get(id=1).gameplanuser, event_date=date.today())
        test_event.save()

    def test_event_date(self):
        test_event = Event.objects.get(id=1)
        self.assertEqual(test_event.event_date, date.today())