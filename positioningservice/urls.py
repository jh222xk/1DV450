from django.conf.urls import patterns, url
from .views import PositionListView, PositionDetailView, EventListView, EventDetailView, TagListView, TagDetailView

urlpatterns = patterns('positioningservice.views',
                       # Positions API
                       url(r'^positions/$', PositionListView.as_view(),
                           name='positions_list'),
                       url(r'^positions/(?P<pk>[-_\w]+)$',
                           PositionDetailView.as_view(), name='positions_detail'),

                       # Events API
                       url(r'^events/$', EventListView.as_view(),
                           name='events_list'),
                       url(r'^events/(?P<pk>[-_\w]+)$',
                           EventDetailView.as_view(), name='events_detail'),

                       # Tags API
                       url(r'^tags/$', TagListView.as_view(),
                           name='tags_list'),
                       url(r'^tags/(?P<pk>[-_\w]+)$',
                           TagDetailView.as_view(), name='tags_detail'),
                       )
