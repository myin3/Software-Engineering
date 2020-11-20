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
    path('event/<int:pk>', views.EventDetailView.as_view(), name='event_detail'),
    path('event/<int:pk>/update/', login_required(views.EventUpdateView.as_view()), name='event_update'),
    path('event/<int:pk>/join/', views.join_event, name='join'),
    path('event/<int:pk>/delete', login_required(views.EventDelete.as_view()), name='event_delete'),
    path('user/<int:pk>', login_required(views.UserProfileView.as_view()), name='GameplanUser_detail'),
    path('user/<int:pk>/update/', login_required(views.UserProfileUpdateView.as_view()), name='GameplanUser_update'),
    path('friends/', views.friendsview, name='friends'),
    path('user/<int:pk>/addfriend/', views.addfriendview, name="addfriend"),
    path('event/<int:pk>/addgalleryphoto/',views.addGalleryPictureView, name="addgalleryphoto")
]