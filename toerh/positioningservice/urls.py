from django.conf.urls import patterns, url
from .views import PositionListView, PositionDetailView

urlpatterns = patterns('positioningservice.views',
                       url(r'^$', PositionListView.as_view(), name='list'),
                       url(r'^(?P<pk>[-_\w]+)$', PositionDetailView.as_view(), name='position-detail'),
                       )
