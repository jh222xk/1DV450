from django.views.generic.edit import CreateView, UpdateView, DeleteView

from rest_framework import generics
from oauth2_provider.models import Application

from .models import Position
from .serializers import PositionSerializer


class PositionView(generics.ListAPIView):

    """
    Returns a list of all authors.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class ClientCreate(CreateView):
    model = Application
    fields = ['name']


# class ClientUpdate(UpdateView):
#     model = Client
#     fields = ['name']
