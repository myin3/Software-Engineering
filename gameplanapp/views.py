"""render html templates and return them as a response. URL's are mapped in url.py"""
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from gameplanapp.forms import SignUpForm, EventForm
from gameplanapp.models import Game, Event, GameplanUser

# Create your views here.


def index(request):
    """ view function for the home page """
    events_list = Event.objects.all()
    games_list = Game.objects.all()
    context = {'events_list': events_list,
               'games_list': games_list}
    return render(request, 'gameplanapp/index.html', context)

def signup(request):
    """create user and gameplanuser objects"""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.gameplanuser.user_dateofbirth = form.cleaned_data.get(
                'birth_date')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/gameplanapp/')
    else:
        form = SignUpForm()
    return render(request, 'gameplanapp/signup.html', {'form': form})

def logged_out(request):
    """log out splash page"""
    return render(request, 'gameplanapp/logged_out.html')

def logout_view(request):
    """log out and redirect"""
    logout(request)
    return redirect('/gameplanapp/logged_out/')

@login_required
def create_event(request):
    """create events, current user will be the event manager"""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.event_manager = request.user.gameplanuser
            event = form.save()
            return redirect('/gameplanapp/')
    else:
        form = EventForm()
    return render(request, 'gameplanapp/create_event.html', {'form': form})

class UserProfileView(generic.DetailView):
    """View for the user profile page"""
    model = GameplanUser

class EventListView(generic.ListView):
    """generic event list view"""
    model = Event

class EventDetailView(generic.DetailView):
    """generic event detail view"""
    model = Event
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['attending_list'] = self.request.user.gameplanuser.event_attending.all()
        return context

class EventUpdateView(generic.UpdateView):
    model = Event

class EventDelete(generic.DeleteView):
    model = Event
    success_url = reverse_lazy('events')
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)



def join_event(request, pk):
    request.user.gameplanuser.attend_event(pk)
    return redirect(reverse_lazy('events'))
