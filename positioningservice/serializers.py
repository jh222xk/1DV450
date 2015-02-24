from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField, HyperlinkedModelSerializer

from .models import Position, Event, Tag, Coffee, Review


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'date_joined', 'last_login', 'is_active')


class TagSerializer(ModelSerializer):

    """
    Serializing all the Tags
    """

    url = HyperlinkedIdentityField(view_name='api-v1:tag-detail')
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Tag
        fields = ('name', 'url', 'user')


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
        fields = ('address', 'longitude', 'latitude', 'url', 'created_at', 'events')


class ReviewSerializer(ModelSerializer):
    #coffee_id = serializers.PrimaryKeyRelatedField(read_only=True)
    #user = serializers.Field(source='user.username')
    #review = serializers.PrimaryKeyRelatedField()
    url = HyperlinkedIdentityField(view_name='api-v1:review-detail')
    user_url = HyperlinkedIdentityField(view_name='api-v1:user-detail')
    coffee_url = HyperlinkedIdentityField(view_name='api-v1:coffeehouses-detail')


    #owner = serializers.HiddenField(
     #   default=CurrentUserDefault()
    #)

    class Meta:
        model = Review
        fields = ('rating', 'description', 'url','coffee', 'coffee_url', 'user_url')

    def validate_user(self):
        return self.context['request'].user




class CoffeeSerializer(ModelSerializer):
    position = PositionSerializer(many=False, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    url = HyperlinkedIdentityField(view_name='api-v1:coffeehouses-detail')

    class Meta:
        model = Coffee
        fields = ('name', 'reviews', 'rating', 'url', 'position',)


class NestedReviewSerializer(ModelSerializer):
    coffee = CoffeeSerializer()
    url = HyperlinkedIdentityField(view_name='api-v1:review-detail')

    class Meta:
        model = Review
        fields = ('rating', 'description', 'url', 'coffee', )


