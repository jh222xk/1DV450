from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

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
