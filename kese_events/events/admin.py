from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Event, Organizer, Ticket, Tag

# Register your models here.
admin.site.register(Event)
admin.site.register(Organizer)
admin.site.register(Ticket)
admin.site.register(Tag)