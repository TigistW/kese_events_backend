from rest_framework import serializers

from .models import Event, Organizer, Tag

class OrganizerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organizer
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'  # Include all fields you want to serialize for the Tag model

class EventSerializer(serializers.ModelSerializer):
    organizer = OrganizerSerializer()
    tags = TagSerializer(many=True)
    
    class Meta:
        model = Event
        fields = '__all__'
class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']