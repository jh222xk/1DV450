from django.views.generic.edit import CreateView, UpdateView, DeleteView

from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView

from .models import Position, Event, Tag
from .serializers import PositionSerializer, EventSerializer, TagSerializer


class PositionListView(ListAPIView):

    """
    Returns a list of all positions.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionDetailView(RetrieveAPIView):

    """
    Returns a single position.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class EventListView(ListAPIView):

    """
    Returns a list of all events.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetailView(RetrieveUpdateDestroyAPIView):

    """
    Returns a single event.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class TagListView(ListAPIView):

    """
    Returns a list of all tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetailView(RetrieveUpdateDestroyAPIView):

    """
    Returns a single tag.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
