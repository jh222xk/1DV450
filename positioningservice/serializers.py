from rest_framework.serializers import ModelSerializer, StringRelatedField, HyperlinkedRelatedField

from .models import Position, Event, Tag


class EventSerializer(ModelSerializer):

    """
    Serializing all the Events
    """
    class Meta:
        model = Event
        fields = ('name', 'user', 'position')


class PositionSerializer(ModelSerializer):
    events = EventSerializer(many=True, read_only=True)
    """
    Serializing all the Positions
    """
    class Meta:
        model = Position
        fields = ('name', 'address', 'longitude', 'latitude', 'events')


class TagSerializer(ModelSerializer):

    """
    Serializing all the Tags
    """
    class Meta:
        model = Tag
        fields = ['name']
