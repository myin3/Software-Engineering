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
        gameplan_user = test_user.gameplanuser
        gameplan_user.user_dateofbirth = date.today()
        gameplan_user.user_bio = "Sample user bio"
        gameplan_user.user_email = "test@test.com"
        test_user.gameplanuser.save()
        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def testuserdateofbirth(self):
        user = User.objects.get(username='test_user')
        test_gameplanuser = GameplanUser.objects.get(user=user)
        self.assertEqual(test_gameplanuser.user_dateofbirth, date.today())

    def testProfile(self):
        test_user=User.objects.get(username='test_user')
        test_gameplanuser=GameplanUser.objects.get(user=user)
        self.assertEqual(test_gameplanuser.user_bio, "Sample user bio")




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
                                          event_location="Test Location", event_manager=User.objects.get(id=1).gameplanuser, event_date=date.today(),event_status="Active",event_details="sample details")
        test_event.save()

    def test_event_date(self):
        test_event = Event.objects.get(id=1)
        test_user = User.objects.get(id=1)
        User.username
        self.assertEqual(test_event.event_date, date.today())

    def test_event_manager(self):
        test_event = Event.objects.get(id=1)
        test_user = User.objects.get(id=1)
        self.assertEqual(test_event.event_manager.user.username, test_user.username)


class JoinEventTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        test_user1 = User.objects.create(
            username='test_user1', password='1X<ISRUkw+tuK')
        test_user1.save()
        test_user2 = User.objects.create(
            username='test_user2', password='1X<ISRUkw+tuK')
        test_user2.save()
        test_event = Event.objects.create(event_title="Test Event Title", event_location="Test Location",
                                          event_manager=User.objects.get(username="test_user1").gameplanuser, event_date=date.today())
        test_event.save()

        pass

    def tearDown(self):
        # Clean up run after every test method.
        pass

    def testJoinEvent(self):
        user = User.objects.get(username='test_user2')
        test_event = Event.objects.get(event_title="Test Event Title")
        user.gameplanuser.attend_event(event_id=test_event.pk)
        containsevent = test_event in user.gameplanuser.event_attending.all()
        self.assertTrue(containsevent)

    def testCancelEvent(self):
        test_event = Event.objects.get(event_title="Test Event Title")
        user = User.objects.get(username='test_user2')
        test_event.delete()
        user.event_attending.remove(test_event)
        containsevent = test_event in user.gameplanuser.event_attending.all()
        self.assertFalse(containsevent)

        class FriendTest(TestCase):
    def setUp(self):
        # Setup run before every test method.
        test_user1 = User.objects.create(
            username='test_user1', password='1X<ISRUkw+tuK')
        test_user1.save()
        test_user2 = User.objects.create(
            username='test_user2', password='1X<ISRUkw+tuK')
        test_user2.save()
        test_event = Event.objects.create(event_title="Test Event Title", event_location="Test Location",
                                          event_manager=User.objects.get(username="test_user1").gameplanuser, event_date=date.today())
        test_event.save()

        pass

    def testaddFriend(self):
        user1 = User.objects.get(username='test_user1')
        user2 = User.objects.get(username='test_user2')
        user1.gameplanuser.addfriend(second_user_id=user2.id)
        test_Friend = Friendship.objects.get(friend_user=user1.gameplanuser, friend=user2.gameplanuser)
        if(test_Friend.friend_user.user.username == 'test_user1'):
            if(test_Friend.friend.user.username == 'test_user2'):
                self.assertTrue(True)
            else:
                self.assertTrue(False)
        else:
            self.assertFalse(True)