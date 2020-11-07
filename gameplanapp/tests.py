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
    def setUpTestData(self):
        test_user = User.objects.create(
            username='test_user', password='1X<ISRUkw+tuK')
        test_gameplanuser = GameplanUser.objects.create(
            user=test_user, user_dateofbirth=date.today(), user_email="test@gmail.com")
        test_event = Event.objects.create(event_title="Test Event Title",
                                          event_location="Test Location", event_manager=test_user, event_date=date.today())
        test_user.save()
        test_gameplanuser.save()
        test_event.save()
