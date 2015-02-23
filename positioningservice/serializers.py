from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField

from .models import Position, Event, Tag, Coffee, Review


class TagSerializer(ModelSerializer):

    """
    Serializing all the Tags
    """

    url = HyperlinkedIdentityField(view_name='api-v1:tag-detail')

    class Meta:
        model = Tag
        fields = ('name', 'url')


class EventSerializer(ModelSerializer):

    """
    Serializing all the Events
    """

    tags = TagSerializer(many=True, read_only=True)
    url = HyperlinkedIdentityField(view_name='api-v1:event-detail')

    class Meta:
        model = Event
        fields = ('name', 'url', 'tags')


class PositionSerializer(ModelSerializer):

    """
    Serializing all the Positions
    """

    events = EventSerializer(many=True, read_only=True)
    url = HyperlinkedIdentityField(
        view_name='api-v1:position-detail')

    class Meta:
        model = Position
        fields = ('name', 'address', 'longitude', 'latitude', 'url', 'events')


class ReviewSerializer(ModelSerializer):

    class Meta:
        model = Review
        fields = ('rating', 'description')


class CoffeeSerializer(ModelSerializer):
    position = PositionSerializer(many=False, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Coffee
        fields = ('name', 'position', 'reviews', 'rating')