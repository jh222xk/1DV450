from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Position, Event, Tag
from .serializers import PositionSerializer, EventSerializer, TagSerializer


class PositionViewSet(ReadOnlyModelViewSet):

    """
    Returns a list of all positions
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class EventViewSet(ModelViewSet):

    """
    Returns a list of all events
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class TagViewSet(ModelViewSet):

    """
    Returns a list of all tags
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
