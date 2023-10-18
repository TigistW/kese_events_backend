from django.contrib import admin
from .models import Event, Organizer, Tag

# Register your models here.
admin.site.register(Event)
admin.site.register(Organizer)
admin.site.register(Tag)