from django.shortcuts import render
from rest_framework import generics
from datetime import datetime
from .models import Event, Tag
from . import serializers, models
from rest_framework import filters
from django.db.models import Q

class EventListAPIView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer
    permission_classes = []
    
    
class EventDetailAPIView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    permission_classes = []
    serializer_class = serializers.EventSerializer
    
class UpcomingEventListAPIView(generics.ListAPIView):
    # queryset = models.Event.objects.all().order_by('start_date') [:3] # Order by start_date in descending order
    current_time = datetime.now()
    queryset = models.Event.objects.filter(Q(end_date__gte=current_time) | Q(end_date=None)).order_by('-start_date')[:10]
    serializer_class = serializers.EventSerializer
    permission_classes = []
    
class EventListByTagsAPIView(generics.ListAPIView):
    serializer_class = serializers.EventSerializer
    permission_classes = []
    def get_queryset(self):
        tag_ids = self.request.query_params.getlist('tags')
        queryset = Event.objects.filter(tags__in=tag_ids).distinct()
        return queryset
    
     
class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = []
    