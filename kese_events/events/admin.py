from cloudinary.uploader import upload
from django.contrib import admin
from .models import Event, Organizer, Tag

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('title','ticket_price', 'start_date', 'image_url') 
    # Include 'image_url' in the list display if desired
    def save_model(self, request, obj, form, change):
        # Handle image upload to Cloudinary when saving an event through Django admin
        print(request.POST.get('image'))
        image_file = request.FILES.get('image')
        print(image_file)
        if image_file:
            result = upload(image_file)
            print(result)
            if 'url' in result:
                obj.image_url = result['url']
        print(request)
        super().save_model(request, obj, form, change)

class OrganizerAdmin(admin.ModelAdmin):
    list_display = ('name','contact_email', 'logo_url') 
    # Include 'image_url' in the list display if desired
    def save_model(self, request, obj, form, change):
        # Handle image upload to Cloudinary when saving an event through Django admin
        print(request.POST.get('logo'))
        image_file = request.FILES.get('logo')
        print(image_file)
        if image_file:
            result = upload(image_file)
            print(result)
            if 'url' in result:
                obj.logo_url = result['url']
        print(request)
        super().save_model(request, obj, form, change)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Include 'image_url' in the list display if desired

    # def save_model(self, request, obj, form, change):
    #     # Handle image upload to Cloudinary when saving an event through Django admin
    #     print(request.POST.get('image'))
    #     image_file = request.FILES.get('image')
    #     print(image_file)
    #     if image_file:
    #         result = upload(image_file)
    #         print(result)
    #         if 'url' in result:
    #             obj.image_url = result['url']
    #     print(request)
    #     super().save_model(request, obj, form, change)

admin.site.register(Event, EventAdmin)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Tag, TagAdmin)