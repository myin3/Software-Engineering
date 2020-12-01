"""contains the url paths, their names, and their associated views"""
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('logged_out/', views.logged_out, name='logged_out'),
    path('logout/', views.logout_view, name='logout'),
    path('create_event/', views.create_event, name='create_event'),
    path('events/', login_required(views.EventListView.as_view()), name='events'),
    path('events/joined', login_required(views.JoinedEventListView.as_view()), name='joined_events'),
    path('events/managing', login_required(views.ManagingEventListView.as_view()), name="managing_events"),
    path('event/<int:pk>', views.EventDetailView.as_view(), name='event_detail'),
    path('event/<int:pk>/update/', login_required(views.EventUpdateView.as_view()), name='event_update'),
    path('event/<int:pk>/join/', views.join_event, name='join'),
    path('event/<int:pk>/leave/', views.leave_event, name='leave'),
    path('event/<int:pk>/delete', login_required(views.EventDelete.as_view()), name='event_delete'),
    path('event/<int:pk>/feedback', views.eventFeedBackView, name="event_feedback"),
    path('event/<int:pk>/send_reminder', views.sendReminderView, name='send_reminder'),
    path('user/<int:pk>', login_required(views.UserProfileView.as_view()), name='GameplanUser_detail'),
    path('user/<int:pk>/update/', login_required(views.UserProfileUpdateView.as_view()), name='GameplanUser_update'),
    path('friends/', views.friendsview, name='friends'),
    path('messages/', login_required(views.MessageListView.as_view()), name="messages"),
    path('create_message/', login_required(views.CreateMessageView.as_view()), name='create_message'),
    path('message/<int:pk>', login_required(views.MessageDetailView.as_view()), name="message_detail"),
    path('user/<int:pk>/addfriend/', views.addfriendview, name="addfriend"),
    path('event/<int:pk>/addgalleryphoto/', views.addGalleryPictureView, name="addgalleryphoto"),
    path('contactus', views.contactus, name="contactus")
]