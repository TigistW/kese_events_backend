from django.contrib import admin
from django.urls import path, include
from django.urls import path

from events.views import EventDetailAPIView, EventListAPIView, EventListByTagsAPIView, TagListAPIView, UpcomingEventListAPIView

app_name = 'events'
urlpatterns = [
    path('events/', EventListAPIView.as_view(), name='event-list-api'),
    path('events/<int:pk>/', EventDetailAPIView.as_view(), name='event-detail-api'),
    path('upcoming-events/', UpcomingEventListAPIView.as_view(), name='upcoming-events'),
    path('tags/', TagListAPIView.as_view(), name='tags-list'),
    path('events-by-tags-list/', EventListByTagsAPIView.as_view(), name='events-by-tags-list'),
]

