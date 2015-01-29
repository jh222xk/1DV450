from django.views.generic.edit import CreateView, UpdateView, DeleteView

from rest_framework import generics

from .models import Position, Event, Tag
from .serializers import PositionSerializer, EventSerializer, TagSerializer


class PositionListView(generics.ListAPIView):

    """
    Returns a list of all positions.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionDetailView(generics.RetrieveUpdateDestroyAPIView):

    """
    Returns a single position.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class EventListView(generics.ListAPIView):

    """
    Returns a list of all positions.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):

    """
    Returns a single position.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
