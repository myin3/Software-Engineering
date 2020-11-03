"""Forms for data users can enter"""
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from gameplanapp.models import Event
User = get_user_model()


class SignUpForm(UserCreationForm):
    """extend the default django user creation form to add specific gameplan user stuff."""
    email = forms.EmailField(
        max_length=254, help_text='Required. Enter a valid email address.')
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    date_of_birth = forms.DateField(required=False, widget=forms.SelectDateWidget())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',
                  'date_of_birth', 'first_name', 'last_name')

class EventForm(ModelForm):
    """Form to allow users to create an event"""
    event_date = forms.DateField(widget=forms.SelectDateWidget())
    class Meta:
        model = Event
        fields = ('event_title', 'event_location', 'event_details', 'event_date', 'event_game')
        
class JoinEventForm(forms.Form):
    join_event = forms.BooleanField()