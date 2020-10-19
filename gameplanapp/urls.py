"""contains the url paths, their names, and their associated views"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('logged_out/', views.logged_out, name='logged_out'),
    path('logout/', views.logout_view, name='logout'),
    path('create_event/', views.create_event, name='create_event')

]
