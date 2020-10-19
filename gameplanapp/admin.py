from django.contrib import admin

# Register your models here.
from .models import Event, Genre, GameplanUser, Game

admin.site.register(Event)
admin.site.register(Genre)
admin.site.register(GameplanUser)
admin.site.register(Game)
