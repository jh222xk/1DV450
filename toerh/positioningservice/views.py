from rest_framework import generics

from .models import Position
from .serializers import PositionSerializer


class PositionView(generics.ListAPIView):

    """
    Returns a list of all authors.
    """
    model = Position
    serializer_class = PositionSerializer
