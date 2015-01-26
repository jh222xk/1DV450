from django.conf.urls import patterns, url
from .views import PositionView

urlpatterns = patterns('positioningservice.views',
                       url(r'^$', PositionView.as_view(), name='position-list'),
                       url(r'^(?P<pk>[-_\w]+)$', PositionView.as_view(), name='position-detail'),
                       )
