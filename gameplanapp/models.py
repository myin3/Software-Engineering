"""models for our gameplan apps"""
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
# Used to generate URLs by reversing the URL patterns
from django.urls import reverse

User = get_user_model()
# Create your models here.


class Genre(models.Model):
    """Model representing a game genre."""
    name = models.CharField(
        max_length=200, help_text='Enter a game genre (e.g. Science Fiction)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Game(models.Model):
    """Model representing a game"""
    game_title = models.CharField(max_length=200)
    game_genre = models.ManyToManyField(Genre, blank=True)

    def __str__(self):
        """String for representing the Model object."""
        return self.game_title


class GameplanUser(models.Model):
    """Model representing a user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    event_attending = models.ManyToManyField(
        'Event', related_name='attending', blank=True)
    user_email = models.EmailField()
    user_dateofbirth = models.DateField(null=True, blank=True)
    user_bio = models.TextField(default="A simple bio")
    profile_picture = models.ImageField(null=True, blank=True, upload_to='profiles')
    def __str__(self):
        return self.user.__str__()

    def get_absolute_url(self):
        """Returns the url to access a particular GamePlanUser instance."""
        return reverse('GameplanUser_detail', args=[str(self.id)])

    def attend_event(self, event_id):
        """make a user attend an event"""
        event = Event.objects.get(id=event_id)
        self.event_attending.add(event)
        self.save()
        event.save()

    def leave_event(self, event_id):
        """make user unattend event"""
        event = Event.objects.get(id=event_id)
        self.event_attending.remove(event)
        self.save()
        event.save()

    def addfriend(self, second_user_id):
        """add a user as a friend"""
        second_user = User.objects.get(id=second_user_id)
        new_friendship = Friendship.objects.create(friend_user=self, friend=second_user.gameplanuser)
        new_friendship.save()
        
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    """every time we create a new user, create a gameplanuser as well"""
    if created:
        GameplanUser.objects.create(user=instance)
    instance.gameplanuser.save()


class Event(models.Model):
    """
    model representing an event
    """
    event_title = models.CharField(max_length=200, default="Event Title")
    event_location = models.CharField(max_length=200)
    event_details = models.TextField()
    event_date = models.DateField(null=True, blank=True)
    event_manager = models.ForeignKey('GamePlanUser', on_delete=models.CASCADE)
    event_game = models.ForeignKey(
        Game, blank=True, null=True, on_delete=models.SET_NULL)
    event_status = models.CharField(max_length=200, default='ACTIVE')

    def __str__(self):
        return self.event_title

    def get_absolute_url(self):
        """
        returns a url to access a particular event instance
        """
        return reverse('event_detail', args=[str(self.id)])

class EventGallery(models.Model):
    """
    list of pictures for each event
    """
    gallery_event = models.ForeignKey('Event', on_delete=models.CASCADE)
    gallery_picture = models.ImageField(upload_to='gallery', null=True, blank=True)

class Friendship(models.Model):
    """
    model for the friendship table
    """
    friend_user = models.ForeignKey('GameplanUser', on_delete=models.CASCADE, related_name="friend_one")
    friend = models.ForeignKey('GameplanUser', on_delete=models.CASCADE, related_name="friend_two")
    


class Message(models.Model):
    """
    model to send message from one user to the next
    """
    sender = models.ForeignKey(
        'GameplanUser', on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(
        'GameplanUser', on_delete=models.CASCADE, related_name="recipient")
    contents = models.TextField()
    

    def get_absolute_url(self):
        """
        returns a url to access a particular message instance
        """
        return reverse('message_detail', args=[str(self.id)])
