from django.db import models
from core.mixins import BaseMixin, NULL
from authentication.models import UserProfile

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
class Organizer(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    website = models.URLField(max_length=200)
    contact_email = models.EmailField()
    logo = models.ImageField(upload_to='organizer_logos/')
    
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='event_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="events")
    
    # Add other fields specific to the event model as needed

    def __str__(self):
        return self.title

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    purchased_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField()
    # Add other fields related to tickets, such as ticket type, description, etc.

    def __str__(self):
        return f"{self.event.title} - {self.price}"

