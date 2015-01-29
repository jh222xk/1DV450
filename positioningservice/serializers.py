from rest_framework.serializers import ModelSerializer, StringRelatedField, HyperlinkedRelatedField

from .models import Position, Event, Tag


class TagSerializer(ModelSerializer):

    """
    Serializing all the Tags
    """
    class Meta:
        model = Tag
        fields = ['name']


class EventSerializer(ModelSerializer):
    """
    Serializing all the Events
    """

    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Event
        fields = ('name', 'tags')


class PositionSerializer(ModelSerializer):
    """
    Serializing all the Positions
    """

    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = Position
        fields = ('name', 'address', 'longitude', 'latitude', 'events')
