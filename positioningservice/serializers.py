from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from rest_framework.fields import CharField
from rest_framework.reverse import reverse
from rest_framework.serializers import ModelSerializer
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from .models import Position, Tag, Coffee, Review


class UserSerializer(ModelSerializer):
    """
    Serializing all the Users
    """
    links = serializers.SerializerMethodField()
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = get_user_model()
        fields = (User.USERNAME_FIELD, 'email', 'date_joined', 'password', 'last_login', 'is_active', 'links',)
        write_only_fields = ('password',)

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('api-v1:user-detail',
                            kwargs={'pk': obj.pk}, request=request) + '?key={}'.format(request.query_params.get('key')),


        }

    def create(self, validated_data):
        """
        Hashes the password upon creation
        """
        user = User(email=validated_data['email'], username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class TagSerializer(ModelSerializer):
    """
    Serializing all the Tags
    """
    links = serializers.SerializerMethodField()
    user = UserSerializer(many=False, read_only=True)
    name = CharField(
        validators=[UniqueValidator(queryset=Tag.objects.all())]
    )

    class Meta:
        model = Tag
        fields = ('name', 'links', 'user')

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('api-v1:tag-detail',
                            kwargs={'pk': obj.pk}, request=request) + '?key={}'.format(request.query_params.get('key')),


        }

    def validate_user(self):
        return self.context['request'].user


class PositionSerializer(ModelSerializer):
    """
    Serializing all the Positions
    """

    links = serializers.SerializerMethodField()

    class Meta:
        model = Position
        fields = ('longitude', 'latitude', 'links', 'created_at',)

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('api-v1:position-detail',
                            kwargs={'pk': obj.pk}, request=request) + '?key={}'.format(request.query_params.get('key')),


        }


class ReviewSerializer(ModelSerializer):
    """
    Serializing all the Reviews
    """
    links = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('rating', 'description', 'coffee', 'links')
        write_only_fields = ('coffee',)

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('api-v1:review-detail',
                            kwargs={'pk': obj.pk}, request=request) + '?key={}'.format(request.query_params.get('key')),
            'user': reverse('api-v1:user-detail', kwargs={'pk': obj.user.pk},
                            request=request) + '?key={}'.format(request.query_params.get('key')),
            'coffeehouse': reverse('api-v1:coffeehouses-detail', kwargs={'pk': obj.coffee.pk},
                                   request=request) + '?key={}'.format(request.query_params.get('key')),


        }

    def validate_user(self):
        return self.context['request'].user


class ReviewCoffee(ModelSerializer):
    user = UserSerializer(many=False)

    class Meta:
        model = Review
        fields = ('rating', 'description', 'created_at', 'user',)


class CoffeeSerializer(ModelSerializer):
    """
    Serializing all the Coffeehouses
    """
    position = PositionSerializer(many=False, read_only=True)
    reviews = ReviewCoffee(many=True, read_only=True, source='review')
    links = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    image = serializers.ImageField(max_length=None, allow_empty_file=False, use_url=True)

    class Meta:
        model = Coffee
        fields = ('id', 'name', 'address', 'rating', 'links', 'description', 'position', 'image', 'tags', 'reviews',)

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('api-v1:coffeehouses-detail',
                            kwargs={'pk': obj.pk}, request=request) + '?key={}'.format(request.query_params.get('key')),


        }


class NestedReviewSerializer(ModelSerializer):
    """
    A nested review with just the URL and the coffeehouse, used when nesting
    """
    links = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ('rating', 'description', 'links',)

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('api-v1:review-detail',
                            kwargs={'pk': obj.pk}, request=request) + '?key={}'.format(request.query_params.get('key')),
            'coffeehouse': reverse('api-v1:coffeehouses-detail', kwargs={'pk': obj.coffee.pk},
                                   request=request) + '?key={}'.format(request.query_params.get('key')),


        }


