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
    event_attending = models.ManyToManyField('Event', related_name='attending', blank=True)
    user_email = models.EmailField()
    user_dateofbirth = models.DateField(null=True, blank=True)
    user_bio = models.TextField(default="A simple bio")

    def __str__(self):
        return self.user.__str__()

    def get_absolute_url(self):
        """Returns the url to access a particular GamePlanUser instance."""
        return reverse('gameplanuser-detail', args=[str(self.user)])
    
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
    event_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    event_title = models.CharField(max_length=200, default="Event Title")
    event_location = models.CharField(max_length=200)
    event_details = models.TextField()
    event_date = models.DateField(null=True, blank=True)
    event_manager = models.OneToOneField(
        "GamePlanUser", on_delete=models.CASCADE, related_name='manager')
    event_game = models.OneToOneField(Game, on_delete=models.SET_NULL, null=True)
    event_status = models.CharField(max_length=200, default='ACTIVE')

    def get_absolute_url(self):
        """
        returns a url to access a particular event instance
        """
        return reverse('event-detail', args=[str(self.event_id)])
