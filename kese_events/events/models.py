from django.utils import timezone
from django.db import models
from core.mixins import BaseModelMixin, NULL
from authentication.models import UserProfile
import datetime
from cloudinary.models import CloudinaryField
from cloudinary.uploader import upload
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
    logo_url = models.URLField(blank = True)
    
    def post(self, request):
    # ... other code ...
        if request.method == 'POST':
            logo_file = request.FILES.get('logo')
            if logo_file:
                result = upload(logo_file)
                if 'url' in result:
                    new_event = Event(
                        name = request['name'],
                        description = request['description'],
                        website = request['website'],
                        contact_email = request['contact_email'],
                        logo = request['logo'],
                        logo_url=result['url']
                    )
                    new_event.save()
                    return new_event
    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    end_date = models.DateTimeField(default = timezone.localtime)
    start_date = models.DateTimeField(default=timezone.localtime, editable=False)
    
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField()
    image = models.ImageField(upload_to='event_images/')  # To temporarily store the uploaded image
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organizer = models.ForeignKey(Organizer, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(Tag, related_name="events")
    
    # Add other fields specific to the event model as needed
    def post(self, request):
    # ... other code ...
        if request.method == 'POST':
            image_file = request.FILES.get('image')
            if image_file:
                result = upload(image_file)
                if 'url' in result:
                    new_event = Event(
                        title = request['title'],
                        description = request['title'],
                        location = request['location'],
                        end_date = request['end_date'],
                        start_date = request['start_date'],
                        ticket_price = request['ticket_price'],
                        capacity = request['capacity'],
                        image = request['image'],
                        created_at = request['created_at'],
                        updated_at = request['updated_at'],
                        organizer = request['organizer'],
                        tags = request['tags'],
                        image_url=result['url']
                    )
                    new_event.save()
                    return new_event
                    # return HttpResponse('Event created successfully.')
    def __str__(self):
        return self.title

# class Ticket(models.Model):
#     event = models.ForeignKey(Event, on_delete=models.DO_NOTHING)
#     ticket_type = models.CharField(max_length=50)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.PositiveIntegerField()
#     purchased_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     purchase_date = models.DateTimeField()
#     # Add other fields related to tickets, such as ticket type, description, etc.

#     def __str__(self):
#         return f"{self.event.title} - {self.price}"

