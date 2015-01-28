from rest_framework import serializers

from .models import Position


class PositionSerializer(serializers.ModelSerializer):

    """
    Serializing all the Positions
    """
    class Meta:
        model = Position
        fields = ('name', 'address', 'longitude', 'latitude')
