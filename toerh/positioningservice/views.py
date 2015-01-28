from django.views.generic.edit import CreateView, UpdateView, DeleteView

from rest_framework import generics

from .models import Position
from .serializers import PositionSerializer


class PositionListView(generics.ListAPIView):

    """
    Returns a list of all positions.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class PositionDetailView(generics.RetrieveUpdateDestroyAPIView):

    """
    Returns a single position.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer