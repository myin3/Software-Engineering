"""render html templates and return them as a response. URL's are mapped in url.py"""
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from gameplanapp.forms import SignUpForm, EventForm, UserProfilePageForm, EventGalleryForm, MessageForm, EventFeedbackForm
from gameplanapp.models import Game, Event, GameplanUser, Friendship, EventGallery, Message

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
                'date_of_birth')
            user.gameplanuser.user_email = form.cleaned_data.get('email')
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
        context['eventgallery_list'] = EventGallery.objects.filter(
            gallery_event=self.object)
        return context


class EventUpdateView(generic.UpdateView):
    model = Event
    form_class = EventForm


class EventDelete(generic.DeleteView):
    model = Event
    success_url = reverse_lazy('events')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


def join_event(request, pk):
    request.user.gameplanuser.attend_event(pk)
    return redirect(reverse_lazy('events'))

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['attending_list'] = self.request.user.gameplanuser.event_attending.all()
        return context


def leave_event(request, pk):
    request.user.gameplanuser.leave_event(pk)
    return redirect(reverse_lazy('events'))

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['attending_list'] = self.request.user.gameplanuser.event_attending.all()
        return context


class UserProfileView(generic.DetailView):
    """View for the user profile page"""
    model = GameplanUser

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['attending_list'] = self.request.user.gameplanuser.event_attending.all()
        context['friends_list'] = Friendship.objects.filter(
            friend_user=self.request.user.gameplanuser)
        return context


class UserProfileUpdateView(generic.UpdateView):
    model = GameplanUser
    form_class = UserProfilePageForm


@login_required
def friendsview(request):
    user_list = GameplanUser.objects.all()
    friends_list = Friendship.objects.filter(
        friend_user=request.user.gameplanuser)
    existing_friends = [friendship.friend for friendship in friends_list]
    excludefromuser_list = existing_friends + [request.user.gameplanuser]
    context = {'user_list': user_list,
               'friends_list': friends_list,
               'existing_friends': existing_friends,
               'excludefromuser_list': excludefromuser_list}
    return render(request, 'gameplanapp/friends.html', context)


def addfriendview(request, pk):
    request.user.gameplanuser.addfriend(pk)
    return(redirect(reverse_lazy('friends')))


def addGalleryPictureView(request, pk):
    if request.method == 'POST':
        form = EventGalleryForm(request.POST, request.FILES)
        if form.is_valid():
            eventgallery = form.save(commit=False)
            eventgallery.gallery_event = Event.objects.get(pk=pk)
            eventgallery = form.save()
            return redirect(eventgallery.gallery_event.get_absolute_url())
    else:
        form = EventGalleryForm()
    return render(request, 'gameplanapp/addgalleryphoto.html', {'form': form})


class CreateMessageView(generic.CreateView):
    model = Message
    form_class = MessageForm

    def get_initial(self):
        sender = self.request.user.gameplanuser
        return {
            'sender': sender,
        }


class EventFeedbackView(generic.CreateView):
    model = Message
    form_class = EventFeedbackForm
    def get_initial(self):
        sender = self.request.user.gameplanuser
        return {
            'sender': sender,
        }

class MessageListView(generic.ListView):
    context_object_name = "message_list"
    paginate_by = 10
    def get_queryset(self):
        return Message.objects.filter(recipient=self.request.user.gameplanuser)

class MessageDetailView(generic.DetailView):
    model = Message