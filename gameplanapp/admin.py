from django.contrib import admin

# Register your models here.
from .models import Event, Genre, GameplanUser, Game, EventGallery, Friendship

admin.site.register(Event)
admin.site.register(Genre)
admin.site.register(GameplanUser)
admin.site.register(Game)
admin.site.register(EventGallery)
admin.site.register(Friendship)
